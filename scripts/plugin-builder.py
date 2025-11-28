#!/usr/bin/env python3
"""
Plugin Builder CLI

Interactive tool for managing Claude Code marketplace plugins.
Manages a central registry of commands, agents, and skills,
and creates plugins by symlinking from the registry.

Usage:
    python scripts/plugin-builder.py [command]

Commands:
    dashboard       Show overview dashboard with stats and health
    list            List all assets in registry
    list-plugins    List all plugins and their assets
    usage           Show asset usage across plugins
    search          Search assets by name or description
    orphans         Find unused assets in registry
    duplicates      Find assets used in multiple plugins
    add             Add a new asset to registry
    create          Create a new plugin
    edit            Edit a plugin (add/remove assets)
    rename          Rename an asset in registry
    delete          Delete an asset from registry
    build           Build/rebuild plugin symlinks
    validate        Validate all plugins and symlinks
    export          Export plugin/registry as JSON
    sync            Sync assets from external directory
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


# ANSI color codes for terminal output
class Colors:
    """Terminal colors."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @classmethod
    def disable(cls) -> None:
        """Disable colors."""
        cls.HEADER = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.RED = ""
        cls.BOLD = ""
        cls.DIM = ""
        cls.RESET = ""


class AssetType(Enum):
    """Types of assets in the registry."""
    COMMAND = "commands"
    AGENT = "agents"
    SKILL = "skills"


@dataclass
class Asset:
    """Represents an asset in the registry."""
    name: str
    asset_type: AssetType
    path: Path
    description: str = ""
    size_bytes: int = 0
    modified: Optional[datetime] = None

    @property
    def registry_path(self) -> Path:
        """Path within registry."""
        return Path("registry") / self.asset_type.value / self.name


@dataclass
class Plugin:
    """Represents a plugin definition."""
    name: str
    description: str = ""
    version: str = "1.0.0"
    commands: list[str] = field(default_factory=list)
    agents: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    category: str = "productivity"

    @property
    def total_assets(self) -> int:
        """Total number of assets in plugin."""
        return len(self.commands) + len(self.agents) + len(self.skills)


@dataclass
class UsageInfo:
    """Tracks which plugins use an asset."""
    asset_name: str
    asset_type: AssetType
    plugins: list[str] = field(default_factory=list)

    @property
    def usage_count(self) -> int:
        """Number of plugins using this asset."""
        return len(self.plugins)

    @property
    def is_orphan(self) -> bool:
        """True if not used by any plugin."""
        return self.usage_count == 0

    @property
    def is_shared(self) -> bool:
        """True if used by multiple plugins."""
        return self.usage_count > 1


class PluginBuilder:
    """Main plugin builder class."""

    def __init__(self, marketplace_root: Optional[Path] = None, no_color: bool = False):
        """Initialize the plugin builder."""
        if marketplace_root is None:
            script_dir = Path(__file__).parent
            marketplace_root = script_dir.parent

        self.root = marketplace_root
        self.registry_dir = self.root / "registry"
        self.plugins_dir = self.root / "plugins"

        if no_color:
            Colors.disable()

    def get_registry_assets(self, asset_type: Optional[AssetType] = None) -> list[Asset]:
        """Get all assets from the registry."""
        assets = []
        types_to_check = [asset_type] if asset_type else list(AssetType)

        for atype in types_to_check:
            type_dir = self.registry_dir / atype.value
            if not type_dir.exists():
                continue

            for item in type_dir.iterdir():
                if item.name.startswith("."):
                    continue

                if item.is_file() and item.suffix == ".md":
                    name = item.stem
                    size = item.stat().st_size
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                elif item.is_dir():
                    name = item.name
                    size = sum(f.stat().st_size for f in item.rglob("*") if f.is_file())
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                else:
                    continue

                assets.append(Asset(
                    name=name,
                    asset_type=atype,
                    path=item,
                    description=self._get_asset_description(item),
                    size_bytes=size,
                    modified=mtime
                ))

        return sorted(assets, key=lambda a: (a.asset_type.value, a.name))

    def _get_asset_description(self, path: Path) -> str:
        """Extract description from asset file."""
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8")
            elif path.is_dir():
                for name in ["SKILL.md", "README.md"]:
                    desc_file = path / name
                    if desc_file.exists():
                        content = desc_file.read_text(encoding="utf-8")
                        break
                else:
                    return ""

            lines = content.strip().split("\n")
            if lines and lines[0] == "---":
                for i, line in enumerate(lines[1:], 1):
                    if line == "---":
                        break
                    if line.startswith("description:"):
                        return line.split(":", 1)[1].strip().strip("\"'")

            for line in lines:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("---"):
                    return line[:100]

            return ""
        except Exception:
            return ""

    def get_plugins(self) -> list[Plugin]:
        """Get all plugin definitions."""
        plugins = []

        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
                continue

            plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
            if plugin_json.exists():
                try:
                    data = json.loads(plugin_json.read_text(encoding="utf-8"))
                    plugin = Plugin(
                        name=data.get("name", plugin_dir.name),
                        description=data.get("description", ""),
                        version=data.get("version", "1.0.0"),
                        keywords=data.get("keywords", []),
                        category=data.get("category", "productivity")
                    )

                    plugin.commands = self._list_plugin_assets(plugin_dir, "commands")
                    plugin.agents = self._list_plugin_assets(plugin_dir, "agents")
                    plugin.skills = self._list_plugin_assets(plugin_dir, "skills")

                    plugins.append(plugin)
                except Exception as e:
                    print(f"Warning: Could not load plugin {plugin_dir.name}: {e}")

        return sorted(plugins, key=lambda p: p.name)

    def _list_plugin_assets(self, plugin_dir: Path, asset_type: str) -> list[str]:
        """List asset names in a plugin directory."""
        assets_dir = plugin_dir / asset_type
        if not assets_dir.exists():
            return []

        names = []
        for item in assets_dir.iterdir():
            if item.name.startswith("."):
                continue
            if item.is_file() and item.suffix == ".md":
                names.append(item.stem)
            elif item.is_dir() or item.is_symlink():
                names.append(item.name.replace(".md", "") if item.name.endswith(".md") else item.name)

        return sorted(set(names))

    def get_usage_info(self) -> dict[str, UsageInfo]:
        """Get usage information for all assets."""
        usage: dict[str, UsageInfo] = {}

        # Initialize with all registry assets
        for asset in self.get_registry_assets():
            key = f"{asset.asset_type.value}:{asset.name}"
            usage[key] = UsageInfo(
                asset_name=asset.name,
                asset_type=asset.asset_type,
                plugins=[]
            )

        # Track which plugins use each asset
        for plugin in self.get_plugins():
            for cmd in plugin.commands:
                key = f"commands:{cmd}"
                if key in usage:
                    usage[key].plugins.append(plugin.name)

            for agent in plugin.agents:
                key = f"agents:{agent}"
                if key in usage:
                    usage[key].plugins.append(plugin.name)

            for skill in plugin.skills:
                key = f"skills:{skill}"
                if key in usage:
                    usage[key].plugins.append(plugin.name)

        return usage

    def get_orphans(self) -> list[Asset]:
        """Get assets not used by any plugin."""
        usage = self.get_usage_info()
        orphans = []

        for asset in self.get_registry_assets():
            key = f"{asset.asset_type.value}:{asset.name}"
            if key in usage and usage[key].is_orphan:
                orphans.append(asset)

        return orphans

    def get_shared_assets(self) -> list[UsageInfo]:
        """Get assets used by multiple plugins."""
        usage = self.get_usage_info()
        return [u for u in usage.values() if u.is_shared]

    def search_assets(self, query: str) -> list[Asset]:
        """Search assets by name or description."""
        query = query.lower()
        results = []

        for asset in self.get_registry_assets():
            if query in asset.name.lower() or query in asset.description.lower():
                results.append(asset)

        return results

    def get_stats(self) -> dict:
        """Get marketplace statistics."""
        assets = self.get_registry_assets()
        plugins = self.get_plugins()
        usage = self.get_usage_info()

        commands = [a for a in assets if a.asset_type == AssetType.COMMAND]
        agents = [a for a in assets if a.asset_type == AssetType.AGENT]
        skills = [a for a in assets if a.asset_type == AssetType.SKILL]

        orphans = [u for u in usage.values() if u.is_orphan]
        shared = [u for u in usage.values() if u.is_shared]

        total_size = sum(a.size_bytes for a in assets)

        return {
            "total_assets": len(assets),
            "commands": len(commands),
            "agents": len(agents),
            "skills": len(skills),
            "plugins": len(plugins),
            "orphans": len(orphans),
            "shared": len(shared),
            "total_size_kb": total_size // 1024,
            "avg_assets_per_plugin": sum(p.total_assets for p in plugins) / len(plugins) if plugins else 0,
        }

    def create_plugin(self, name: str, description: str = "") -> Plugin:
        """Create a new empty plugin."""
        plugin_dir = self.plugins_dir / name

        if plugin_dir.exists():
            raise ValueError(f"Plugin '{name}' already exists")

        plugin_dir.mkdir(parents=True)
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / "commands").mkdir()
        (plugin_dir / "agents").mkdir()
        (plugin_dir / "skills").mkdir()

        plugin = Plugin(name=name, description=description)
        plugin_json = {
            "name": name,
            "description": description,
            "version": "1.0.0",
            "author": {"name": "Cameron Sjo"},
            "keywords": [],
            "category": "productivity"
        }

        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(plugin_json, indent=2),
            encoding="utf-8"
        )

        print(f"{Colors.GREEN}Created plugin: {name}{Colors.RESET}")
        return plugin

    def add_asset_to_plugin(
        self,
        plugin_name: str,
        asset_name: str,
        asset_type: AssetType
    ) -> None:
        """Add an asset from registry to a plugin via symlink."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        registry_path = self.registry_dir / asset_type.value / asset_name

        if not registry_path.exists():
            registry_path = self.registry_dir / asset_type.value / f"{asset_name}.md"

        if not registry_path.exists():
            raise ValueError(f"Asset '{asset_name}' not found in registry/{asset_type.value}")

        target_dir = plugin_dir / asset_type.value
        target_dir.mkdir(exist_ok=True)

        if registry_path.is_file():
            target_path = target_dir / registry_path.name
        else:
            target_path = target_dir / asset_name

        if target_path.exists():
            print(f"{Colors.YELLOW}Asset already exists in plugin: {target_path}{Colors.RESET}")
            return

        rel_path = os.path.relpath(registry_path, target_path.parent)
        os.symlink(rel_path, target_path)

        print(f"{Colors.GREEN}Added {asset_type.value[:-1]} '{asset_name}' to plugin '{plugin_name}'{Colors.RESET}")

    def remove_asset_from_plugin(
        self,
        plugin_name: str,
        asset_name: str,
        asset_type: AssetType
    ) -> None:
        """Remove an asset from a plugin."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        target_dir = plugin_dir / asset_type.value

        target_path = target_dir / asset_name
        if not target_path.exists():
            target_path = target_dir / f"{asset_name}.md"

        if not target_path.exists():
            raise ValueError(f"Asset '{asset_name}' not found in plugin")

        if target_path.is_symlink():
            target_path.unlink()
        elif target_path.is_file():
            target_path.unlink()
        elif target_path.is_dir():
            shutil.rmtree(target_path)

        print(f"{Colors.GREEN}Removed {asset_type.value[:-1]} '{asset_name}' from plugin '{plugin_name}'{Colors.RESET}")

    def add_to_registry(
        self,
        source_path: Path,
        asset_type: AssetType,
        name: Optional[str] = None
    ) -> Asset:
        """Add a new asset to the registry."""
        if not source_path.exists():
            raise ValueError(f"Source path does not exist: {source_path}")

        if name is None:
            name = source_path.stem if source_path.is_file() else source_path.name

        target_dir = self.registry_dir / asset_type.value
        target_dir.mkdir(parents=True, exist_ok=True)

        if source_path.is_file():
            target_path = target_dir / source_path.name
        else:
            target_path = target_dir / name

        if target_path.exists():
            raise ValueError(f"Asset already exists in registry: {target_path}")

        if source_path.is_file():
            shutil.copy2(source_path, target_path)
        else:
            shutil.copytree(source_path, target_path)

        print(f"{Colors.GREEN}Added to registry: {asset_type.value}/{name}{Colors.RESET}")

        return Asset(
            name=name,
            asset_type=asset_type,
            path=target_path,
            description=self._get_asset_description(target_path)
        )

    def rename_asset(self, old_name: str, new_name: str, asset_type: AssetType) -> None:
        """Rename an asset in the registry and update all symlinks."""
        type_dir = self.registry_dir / asset_type.value

        old_path = type_dir / old_name
        if not old_path.exists():
            old_path = type_dir / f"{old_name}.md"

        if not old_path.exists():
            raise ValueError(f"Asset '{old_name}' not found in registry/{asset_type.value}")

        if old_path.is_file():
            new_path = type_dir / f"{new_name}.md"
        else:
            new_path = type_dir / new_name

        if new_path.exists():
            raise ValueError(f"Asset '{new_name}' already exists")

        # Rename in registry
        old_path.rename(new_path)

        # Update symlinks in all plugins
        for plugin in self.get_plugins():
            plugin_dir = self.plugins_dir / plugin.name
            assets_dir = plugin_dir / asset_type.value

            for item in assets_dir.iterdir():
                if item.is_symlink():
                    target = item.resolve()
                    if target == old_path.resolve():
                        item.unlink()
                        rel_path = os.path.relpath(new_path, item.parent)
                        new_link = assets_dir / (f"{new_name}.md" if new_path.suffix == ".md" else new_name)
                        os.symlink(rel_path, new_link)
                        print(f"  Updated symlink in {plugin.name}")

        print(f"{Colors.GREEN}Renamed '{old_name}' to '{new_name}'{Colors.RESET}")

    def delete_asset(self, asset_name: str, asset_type: AssetType, force: bool = False) -> None:
        """Delete an asset from the registry."""
        usage = self.get_usage_info()
        key = f"{asset_type.value}:{asset_name}"

        if key in usage and usage[key].plugins and not force:
            plugins = ", ".join(usage[key].plugins)
            raise ValueError(f"Asset is used by plugins: {plugins}. Use --force to delete anyway.")

        type_dir = self.registry_dir / asset_type.value
        asset_path = type_dir / asset_name
        if not asset_path.exists():
            asset_path = type_dir / f"{asset_name}.md"

        if not asset_path.exists():
            raise ValueError(f"Asset '{asset_name}' not found")

        # Remove symlinks from plugins first
        for plugin in self.get_plugins():
            plugin_dir = self.plugins_dir / plugin.name
            assets_dir = plugin_dir / asset_type.value

            for item in assets_dir.iterdir():
                if item.is_symlink() and item.resolve() == asset_path.resolve():
                    item.unlink()
                    print(f"  Removed symlink from {plugin.name}")

        # Delete from registry
        if asset_path.is_file():
            asset_path.unlink()
        else:
            shutil.rmtree(asset_path)

        print(f"{Colors.GREEN}Deleted '{asset_name}' from registry{Colors.RESET}")

    def validate(self) -> bool:
        """Validate all plugins and symlinks."""
        valid = True
        issues = []

        for plugin in self.get_plugins():
            plugin_dir = self.plugins_dir / plugin.name

            for asset_type in AssetType:
                assets_dir = plugin_dir / asset_type.value
                if not assets_dir.exists():
                    continue

                for item in assets_dir.iterdir():
                    if item.is_symlink():
                        target = item.resolve()
                        if not target.exists():
                            issues.append(f"{Colors.RED}BROKEN{Colors.RESET}: {item}")
                            valid = False
                        else:
                            try:
                                target.relative_to(self.registry_dir)
                            except ValueError:
                                issues.append(f"{Colors.YELLOW}WARNING{Colors.RESET}: Not pointing to registry: {item}")

        if issues:
            print("\nIssues found:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print(f"{Colors.GREEN}All plugins validated successfully{Colors.RESET}")

        return valid

    def rebuild_symlinks(self, plugin_name: Optional[str] = None) -> None:
        """Rebuild all symlinks for a plugin or all plugins."""
        plugins = self.get_plugins()
        if plugin_name:
            plugins = [p for p in plugins if p.name == plugin_name]
            if not plugins:
                raise ValueError(f"Plugin '{plugin_name}' not found")

        for plugin in plugins:
            plugin_dir = self.plugins_dir / plugin.name
            print(f"Rebuilding symlinks for: {plugin.name}")

            for asset_type in AssetType:
                assets_dir = plugin_dir / asset_type.value
                if not assets_dir.exists():
                    continue

                for item in assets_dir.iterdir():
                    if item.is_symlink():
                        target = item.resolve()
                        if target.exists():
                            item.unlink()
                            rel_path = os.path.relpath(target, item.parent)
                            os.symlink(rel_path, item)

    def export_json(self, output_path: Optional[Path] = None) -> dict:
        """Export marketplace as JSON."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "registry": {
                "commands": [],
                "agents": [],
                "skills": []
            },
            "plugins": []
        }

        for asset in self.get_registry_assets():
            data["registry"][asset.asset_type.value].append({
                "name": asset.name,
                "description": asset.description,
                "size_bytes": asset.size_bytes
            })

        for plugin in self.get_plugins():
            data["plugins"].append({
                "name": plugin.name,
                "description": plugin.description,
                "version": plugin.version,
                "commands": plugin.commands,
                "agents": plugin.agents,
                "skills": plugin.skills
            })

        if output_path:
            output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"{Colors.GREEN}Exported to: {output_path}{Colors.RESET}")

        return data

    def sync_from_directory(self, source_dir: Path, asset_type: AssetType, dry_run: bool = False) -> None:
        """Sync assets from an external directory to registry."""
        if not source_dir.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")

        existing = {a.name for a in self.get_registry_assets(asset_type)}
        added = 0
        skipped = 0

        for item in source_dir.iterdir():
            if item.name.startswith("."):
                continue

            if item.is_file() and item.suffix == ".md":
                name = item.stem
            elif item.is_dir():
                name = item.name
            else:
                continue

            if name in existing:
                skipped += 1
                continue

            if dry_run:
                print(f"  Would add: {name}")
            else:
                self.add_to_registry(item, asset_type, name)

            added += 1

        print(f"\n{Colors.GREEN}Added: {added}, Skipped (existing): {skipped}{Colors.RESET}")


# ============================================================================
# CLI Commands
# ============================================================================

def cmd_dashboard(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Show dashboard with stats and health."""
    stats = builder.get_stats()
    orphans = builder.get_orphans()
    shared = builder.get_shared_assets()
    plugins = builder.get_plugins()

    c = Colors

    print(f"\n{c.BOLD}{c.CYAN}╔══════════════════════════════════════════════════════════════╗{c.RESET}")
    print(f"{c.BOLD}{c.CYAN}║          CLAUDE CODE MARKETPLACE - DASHBOARD                 ║{c.RESET}")
    print(f"{c.BOLD}{c.CYAN}╚══════════════════════════════════════════════════════════════╝{c.RESET}")

    # Stats
    print(f"\n{c.BOLD}📊 REGISTRY STATS{c.RESET}")
    print(f"   ├─ Commands: {c.GREEN}{stats['commands']}{c.RESET}")
    print(f"   ├─ Agents:   {c.GREEN}{stats['agents']}{c.RESET}")
    print(f"   ├─ Skills:   {c.GREEN}{stats['skills']}{c.RESET}")
    print(f"   └─ Total:    {c.BOLD}{stats['total_assets']}{c.RESET} ({stats['total_size_kb']} KB)")

    # Plugins
    print(f"\n{c.BOLD}📦 PLUGINS ({len(plugins)}){c.RESET}")
    for p in plugins:
        asset_count = p.total_assets
        print(f"   ├─ {p.name}: {asset_count} assets (C:{len(p.commands)} A:{len(p.agents)} S:{len(p.skills)})")

    # Health
    print(f"\n{c.BOLD}🏥 HEALTH{c.RESET}")

    if orphans:
        print(f"   ├─ Orphaned assets: {c.YELLOW}{len(orphans)}{c.RESET}")
        for o in orphans[:3]:
            print(f"   │  └─ {o.asset_type.value}/{o.name}")
        if len(orphans) > 3:
            print(f"   │  └─ ... and {len(orphans) - 3} more")
    else:
        print(f"   ├─ Orphaned assets: {c.GREEN}0{c.RESET}")

    if shared:
        print(f"   ├─ Shared assets: {c.BLUE}{len(shared)}{c.RESET}")
        for s in shared[:3]:
            print(f"   │  └─ {s.asset_type.value}/{s.asset_name} ({len(s.plugins)} plugins)")
        if len(shared) > 3:
            print(f"   │  └─ ... and {len(shared) - 3} more")
    else:
        print(f"   ├─ Shared assets: {c.DIM}0{c.RESET}")

    # Validation
    valid = builder.validate()
    status = f"{c.GREEN}HEALTHY{c.RESET}" if valid else f"{c.RED}ISSUES FOUND{c.RESET}"
    print(f"   └─ Symlinks: {status}")

    print()


def cmd_list(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """List assets in registry."""
    asset_type = None
    if args.type:
        asset_type = AssetType(args.type)

    assets = builder.get_registry_assets(asset_type)

    if not assets:
        print("No assets in registry")
        return

    current_type = None
    for asset in assets:
        if asset.asset_type != current_type:
            current_type = asset.asset_type
            print(f"\n{Colors.BOLD}{current_type.value.upper()}:{Colors.RESET}")
            print("-" * 50)

        desc = f" - {asset.description[:50]}..." if asset.description else ""
        print(f"  {Colors.CYAN}{asset.name}{Colors.RESET}{desc}")


def cmd_list_plugins(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """List all plugins."""
    plugins = builder.get_plugins()

    if not plugins:
        print("No plugins found")
        return

    for plugin in plugins:
        print(f"\n{Colors.BOLD}{plugin.name}{Colors.RESET}")
        print("=" * len(plugin.name))
        if plugin.description:
            print(f"  {Colors.DIM}{plugin.description}{Colors.RESET}")
        print(f"  Version: {plugin.version}")

        if plugin.commands:
            print(f"  Commands: {Colors.CYAN}{', '.join(plugin.commands)}{Colors.RESET}")
        if plugin.agents:
            print(f"  Agents: {Colors.GREEN}{', '.join(plugin.agents)}{Colors.RESET}")
        if plugin.skills:
            print(f"  Skills: {Colors.YELLOW}{', '.join(plugin.skills)}{Colors.RESET}")


def cmd_usage(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Show asset usage across plugins."""
    usage = builder.get_usage_info()

    # Group by type
    by_type: dict[AssetType, list[UsageInfo]] = defaultdict(list)
    for u in usage.values():
        by_type[u.asset_type].append(u)

    for asset_type in AssetType:
        items = sorted(by_type[asset_type], key=lambda x: (-x.usage_count, x.asset_name))

        print(f"\n{Colors.BOLD}{asset_type.value.upper()}:{Colors.RESET}")
        print("-" * 60)

        for u in items:
            if u.is_orphan:
                status = f"{Colors.RED}UNUSED{Colors.RESET}"
            elif u.is_shared:
                status = f"{Colors.BLUE}SHARED ({u.usage_count}){Colors.RESET}"
            else:
                status = f"{Colors.GREEN}1 plugin{Colors.RESET}"

            plugins_str = ", ".join(u.plugins) if u.plugins else "-"
            print(f"  {u.asset_name:30} {status:20} {Colors.DIM}{plugins_str}{Colors.RESET}")


def cmd_search(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Search assets."""
    results = builder.search_assets(args.query)

    if not results:
        print(f"No assets found matching '{args.query}'")
        return

    print(f"\n{Colors.BOLD}Search results for '{args.query}':{Colors.RESET}\n")

    for asset in results:
        print(f"  [{asset.asset_type.value}] {Colors.CYAN}{asset.name}{Colors.RESET}")
        if asset.description:
            print(f"    {Colors.DIM}{asset.description}{Colors.RESET}")


def cmd_orphans(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Find unused assets."""
    orphans = builder.get_orphans()

    if not orphans:
        print(f"{Colors.GREEN}No orphaned assets found{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}{Colors.YELLOW}Orphaned assets (not used by any plugin):{Colors.RESET}\n")

    for asset in orphans:
        print(f"  [{asset.asset_type.value}] {asset.name}")


def cmd_duplicates(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Find assets used in multiple plugins."""
    shared = builder.get_shared_assets()

    if not shared:
        print(f"{Colors.DIM}No shared assets found{Colors.RESET}")
        return

    print(f"\n{Colors.BOLD}{Colors.BLUE}Shared assets (used by multiple plugins):{Colors.RESET}\n")

    for u in sorted(shared, key=lambda x: -x.usage_count):
        print(f"  [{u.asset_type.value}] {Colors.CYAN}{u.asset_name}{Colors.RESET}")
        print(f"    Used by: {', '.join(u.plugins)}")


def cmd_add(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Add asset to registry."""
    source_path = Path(args.source)
    asset_type = AssetType(args.type)

    builder.add_to_registry(source_path, asset_type, args.name)


def cmd_create(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Create a new plugin."""
    builder.create_plugin(args.name, args.description or "")


def cmd_edit(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Edit a plugin (add/remove assets)."""
    action = args.action
    plugin_name = args.plugin
    asset_name = args.asset
    asset_type = AssetType(args.type)

    if action == "add":
        builder.add_asset_to_plugin(plugin_name, asset_name, asset_type)
    elif action == "remove":
        builder.remove_asset_from_plugin(plugin_name, asset_name, asset_type)


def cmd_rename(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Rename an asset."""
    asset_type = AssetType(args.type)
    builder.rename_asset(args.old_name, args.new_name, asset_type)


def cmd_delete(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Delete an asset."""
    asset_type = AssetType(args.type)
    builder.delete_asset(args.name, asset_type, args.force)


def cmd_validate(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Validate plugins."""
    valid = builder.validate()
    sys.exit(0 if valid else 1)


def cmd_rebuild(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Rebuild symlinks."""
    builder.rebuild_symlinks(args.plugin)


def cmd_export(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Export to JSON."""
    output = Path(args.output) if args.output else None
    data = builder.export_json(output)

    if not output:
        print(json.dumps(data, indent=2))


def cmd_sync(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Sync from directory."""
    source = Path(args.source)
    asset_type = AssetType(args.type)
    builder.sync_from_directory(source, asset_type, args.dry_run)


def cmd_interactive(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Interactive mode."""
    print(f"{Colors.BOLD}Plugin Builder - Interactive Mode{Colors.RESET}")
    print("=" * 40)

    while True:
        print(f"\n{Colors.BOLD}Options:{Colors.RESET}")
        print("  1. Dashboard")
        print("  2. List registry assets")
        print("  3. List plugins")
        print("  4. Usage report")
        print("  5. Search assets")
        print("  6. Find orphans")
        print("  7. Find shared assets")
        print("  8. Create new plugin")
        print("  9. Add asset to plugin")
        print(" 10. Remove asset from plugin")
        print(" 11. Add asset to registry")
        print(" 12. Validate all plugins")
        print(" 13. Export to JSON")
        print("  0. Exit")

        choice = input(f"\n{Colors.CYAN}Choice:{Colors.RESET} ").strip()

        try:
            if choice == "1":
                cmd_dashboard(argparse.Namespace(), builder)

            elif choice == "2":
                cmd_list(argparse.Namespace(type=None), builder)

            elif choice == "3":
                cmd_list_plugins(argparse.Namespace(), builder)

            elif choice == "4":
                cmd_usage(argparse.Namespace(), builder)

            elif choice == "5":
                query = input("Search query: ").strip()
                cmd_search(argparse.Namespace(query=query), builder)

            elif choice == "6":
                cmd_orphans(argparse.Namespace(), builder)

            elif choice == "7":
                cmd_duplicates(argparse.Namespace(), builder)

            elif choice == "8":
                name = input("Plugin name: ").strip()
                desc = input("Description: ").strip()
                builder.create_plugin(name, desc)

            elif choice == "9":
                plugins = builder.get_plugins()
                print(f"\nPlugins: {', '.join(p.name for p in plugins)}")
                plugin = input("Plugin name: ").strip()

                print("\nAsset types: commands, agents, skills")
                atype = input("Asset type: ").strip()

                assets = builder.get_registry_assets(AssetType(atype))
                print(f"\nAvailable {atype}: {', '.join(a.name for a in assets)}")
                asset = input("Asset name: ").strip()

                builder.add_asset_to_plugin(plugin, asset, AssetType(atype))

            elif choice == "10":
                plugin = input("Plugin name: ").strip()
                atype = input("Asset type (commands/agents/skills): ").strip()
                asset = input("Asset name: ").strip()
                builder.remove_asset_from_plugin(plugin, asset, AssetType(atype))

            elif choice == "11":
                source = input("Source path: ").strip()
                atype = input("Asset type (commands/agents/skills): ").strip()
                name = input("Name (or enter for auto): ").strip() or None
                builder.add_to_registry(Path(source), AssetType(atype), name)

            elif choice == "12":
                builder.validate()

            elif choice == "13":
                output = input("Output file (or enter for stdout): ").strip()
                output_path = Path(output) if output else None
                data = builder.export_json(output_path)
                if not output_path:
                    print(json.dumps(data, indent=2))

            elif choice == "0":
                break

            else:
                print(f"{Colors.RED}Invalid choice{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Plugin Builder CLI for Claude Code marketplace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s dashboard                    # Show overview dashboard
  %(prog)s list                         # List all assets
  %(prog)s usage                        # Show usage report
  %(prog)s search "python"              # Search for assets
  %(prog)s orphans                      # Find unused assets
  %(prog)s edit add core-prod commit -t commands  # Add asset to plugin
        """
    )
    parser.add_argument("--root", type=Path, help="Marketplace root directory")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")

    subparsers = parser.add_subparsers(dest="command")

    # dashboard
    subparsers.add_parser("dashboard", aliases=["dash", "d"], help="Show dashboard")

    # list
    list_parser = subparsers.add_parser("list", aliases=["ls"], help="List registry assets")
    list_parser.add_argument("--type", "-t", choices=["commands", "agents", "skills"])

    # list-plugins
    subparsers.add_parser("list-plugins", aliases=["lp"], help="List all plugins")

    # usage
    subparsers.add_parser("usage", aliases=["u"], help="Show asset usage")

    # search
    search_parser = subparsers.add_parser("search", aliases=["s"], help="Search assets")
    search_parser.add_argument("query", help="Search query")

    # orphans
    subparsers.add_parser("orphans", help="Find unused assets")

    # duplicates/shared
    subparsers.add_parser("duplicates", aliases=["shared"], help="Find shared assets")

    # add
    add_parser = subparsers.add_parser("add", help="Add asset to registry")
    add_parser.add_argument("source", help="Source file or directory")
    add_parser.add_argument("--type", "-t", required=True, choices=["commands", "agents", "skills"])
    add_parser.add_argument("--name", "-n", help="Asset name")

    # create
    create_parser = subparsers.add_parser("create", help="Create new plugin")
    create_parser.add_argument("name", help="Plugin name")
    create_parser.add_argument("--description", "-d", help="Plugin description")

    # edit
    edit_parser = subparsers.add_parser("edit", help="Edit plugin")
    edit_parser.add_argument("action", choices=["add", "remove"])
    edit_parser.add_argument("plugin", help="Plugin name")
    edit_parser.add_argument("asset", help="Asset name")
    edit_parser.add_argument("--type", "-t", required=True, choices=["commands", "agents", "skills"])

    # rename
    rename_parser = subparsers.add_parser("rename", help="Rename asset")
    rename_parser.add_argument("old_name", help="Current name")
    rename_parser.add_argument("new_name", help="New name")
    rename_parser.add_argument("--type", "-t", required=True, choices=["commands", "agents", "skills"])

    # delete
    delete_parser = subparsers.add_parser("delete", aliases=["rm"], help="Delete asset")
    delete_parser.add_argument("name", help="Asset name")
    delete_parser.add_argument("--type", "-t", required=True, choices=["commands", "agents", "skills"])
    delete_parser.add_argument("--force", "-f", action="store_true", help="Force delete even if used")

    # validate
    subparsers.add_parser("validate", help="Validate all plugins")

    # rebuild
    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild symlinks")
    rebuild_parser.add_argument("--plugin", "-p", help="Specific plugin")

    # export
    export_parser = subparsers.add_parser("export", help="Export to JSON")
    export_parser.add_argument("--output", "-o", help="Output file")

    # sync
    sync_parser = subparsers.add_parser("sync", help="Sync from directory")
    sync_parser.add_argument("source", help="Source directory")
    sync_parser.add_argument("--type", "-t", required=True, choices=["commands", "agents", "skills"])
    sync_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    # interactive
    subparsers.add_parser("interactive", aliases=["i"], help="Interactive mode")

    args = parser.parse_args()

    builder = PluginBuilder(args.root, args.no_color)

    commands = {
        "dashboard": cmd_dashboard, "dash": cmd_dashboard, "d": cmd_dashboard,
        "list": cmd_list, "ls": cmd_list,
        "list-plugins": cmd_list_plugins, "lp": cmd_list_plugins,
        "usage": cmd_usage, "u": cmd_usage,
        "search": cmd_search, "s": cmd_search,
        "orphans": cmd_orphans,
        "duplicates": cmd_duplicates, "shared": cmd_duplicates,
        "add": cmd_add,
        "create": cmd_create,
        "edit": cmd_edit,
        "rename": cmd_rename,
        "delete": cmd_delete, "rm": cmd_delete,
        "validate": cmd_validate,
        "rebuild": cmd_rebuild,
        "export": cmd_export,
        "sync": cmd_sync,
        "interactive": cmd_interactive, "i": cmd_interactive,
    }

    if args.command in commands:
        commands[args.command](args, builder)
    else:
        cmd_interactive(args, builder)


if __name__ == "__main__":
    main()
