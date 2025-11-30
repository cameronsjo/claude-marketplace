"""
Core plugin builder logic.

This module contains the PluginBuilder class and related data structures
for managing Claude Code marketplace plugins.
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


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


@dataclass
class ValidationIssue:
    """Represents a validation issue."""

    path: Path
    issue_type: str  # "broken", "warning"
    message: str


class PluginBuilder:
    """Main plugin builder class."""

    def __init__(self, marketplace_root: Optional[Path] = None):
        """Initialize the plugin builder."""
        if marketplace_root is None:
            script_dir = Path(__file__).parent
            marketplace_root = script_dir.parent.parent

        self.root = marketplace_root
        self.registry_dir = self.root / "registry"
        self.plugins_dir = self.root / "plugins"

    def get_registry_assets(
        self, asset_type: Optional[AssetType] = None
    ) -> list[Asset]:
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
                    size = sum(
                        f.stat().st_size for f in item.rglob("*") if f.is_file()
                    )
                    mtime = datetime.fromtimestamp(item.stat().st_mtime)
                else:
                    continue

                assets.append(
                    Asset(
                        name=name,
                        asset_type=atype,
                        path=item,
                        description=self._get_asset_description(item),
                        size_bytes=size,
                        modified=mtime,
                    )
                )

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
            else:
                return ""

            lines = content.strip().split("\n")
            if lines and lines[0] == "---":
                for line in lines[1:]:
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
                        category=data.get("category", "productivity"),
                    )

                    plugin.commands = self._list_plugin_assets(plugin_dir, "commands")
                    plugin.agents = self._list_plugin_assets(plugin_dir, "agents")
                    plugin.skills = self._list_plugin_assets(plugin_dir, "skills")

                    plugins.append(plugin)
                except Exception:
                    pass  # Skip invalid plugins silently in TUI

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
                name = item.name
                if name.endswith(".md"):
                    name = name[:-3]
                names.append(name)

        return sorted(set(names))

    def get_usage_info(self) -> dict[str, UsageInfo]:
        """Get usage information for all assets."""
        usage: dict[str, UsageInfo] = {}

        for asset in self.get_registry_assets():
            key = f"{asset.asset_type.value}:{asset.name}"
            usage[key] = UsageInfo(
                asset_name=asset.name,
                asset_type=asset.asset_type,
                plugins=[],
            )

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
            "avg_assets_per_plugin": (
                sum(p.total_assets for p in plugins) / len(plugins) if plugins else 0
            ),
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
            "category": "productivity",
        }

        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(plugin_json, indent=2), encoding="utf-8"
        )

        return plugin

    def add_asset_to_plugin(
        self, plugin_name: str, asset_name: str, asset_type: AssetType
    ) -> bool:
        """Add an asset from registry to a plugin via symlink. Returns True on success."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        registry_path = self.registry_dir / asset_type.value / asset_name

        if not registry_path.exists():
            registry_path = self.registry_dir / asset_type.value / f"{asset_name}.md"

        if not registry_path.exists():
            raise ValueError(
                f"Asset '{asset_name}' not found in registry/{asset_type.value}"
            )

        target_dir = plugin_dir / asset_type.value
        target_dir.mkdir(exist_ok=True)

        if registry_path.is_file():
            target_path = target_dir / registry_path.name
        else:
            target_path = target_dir / asset_name

        if target_path.exists():
            return False  # Already exists

        rel_path = os.path.relpath(registry_path, target_path.parent)
        os.symlink(rel_path, target_path)

        return True

    def remove_asset_from_plugin(
        self, plugin_name: str, asset_name: str, asset_type: AssetType
    ) -> bool:
        """Remove an asset from a plugin. Returns True on success."""
        plugin_dir = self.plugins_dir / plugin_name
        if not plugin_dir.exists():
            raise ValueError(f"Plugin '{plugin_name}' does not exist")

        target_dir = plugin_dir / asset_type.value

        target_path = target_dir / asset_name
        if not target_path.exists():
            target_path = target_dir / f"{asset_name}.md"

        if not target_path.exists():
            return False

        if target_path.is_symlink():
            target_path.unlink()
        elif target_path.is_file():
            target_path.unlink()
        elif target_path.is_dir():
            shutil.rmtree(target_path)

        return True

    def add_to_registry(
        self, source_path: Path, asset_type: AssetType, name: Optional[str] = None
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

        return Asset(
            name=name,
            asset_type=asset_type,
            path=target_path,
            description=self._get_asset_description(target_path),
        )

    def delete_asset(
        self, asset_name: str, asset_type: AssetType, force: bool = False
    ) -> None:
        """Delete an asset from the registry."""
        usage = self.get_usage_info()
        key = f"{asset_type.value}:{asset_name}"

        if key in usage and usage[key].plugins and not force:
            plugins = ", ".join(usage[key].plugins)
            raise ValueError(
                f"Asset is used by plugins: {plugins}. Use force=True to delete anyway."
            )

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
            if not assets_dir.exists():
                continue

            for item in assets_dir.iterdir():
                if item.is_symlink():
                    try:
                        if item.resolve() == asset_path.resolve():
                            item.unlink()
                    except Exception:
                        pass

        # Delete from registry
        if asset_path.is_file():
            asset_path.unlink()
        else:
            shutil.rmtree(asset_path)

    def validate(self) -> tuple[bool, list[ValidationIssue]]:
        """Validate all plugins and symlinks. Returns (is_valid, issues)."""
        issues: list[ValidationIssue] = []

        for plugin in self.get_plugins():
            plugin_dir = self.plugins_dir / plugin.name

            for asset_type in AssetType:
                assets_dir = plugin_dir / asset_type.value
                if not assets_dir.exists():
                    continue

                for item in assets_dir.iterdir():
                    if item.is_symlink():
                        try:
                            target = item.resolve()
                            if not target.exists():
                                issues.append(
                                    ValidationIssue(
                                        path=item,
                                        issue_type="broken",
                                        message="Broken symlink",
                                    )
                                )
                            else:
                                try:
                                    target.relative_to(self.registry_dir)
                                except ValueError:
                                    issues.append(
                                        ValidationIssue(
                                            path=item,
                                            issue_type="warning",
                                            message="Not pointing to registry",
                                        )
                                    )
                        except Exception as e:
                            issues.append(
                                ValidationIssue(
                                    path=item,
                                    issue_type="broken",
                                    message=str(e),
                                )
                            )

        is_valid = not any(i.issue_type == "broken" for i in issues)
        return is_valid, issues

    def export_json(self, output_path: Optional[Path] = None) -> dict:
        """Export marketplace as JSON."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "registry": {"commands": [], "agents": [], "skills": []},
            "plugins": [],
        }

        for asset in self.get_registry_assets():
            data["registry"][asset.asset_type.value].append(
                {
                    "name": asset.name,
                    "description": asset.description,
                    "size_bytes": asset.size_bytes,
                }
            )

        for plugin in self.get_plugins():
            data["plugins"].append(
                {
                    "name": plugin.name,
                    "description": plugin.description,
                    "version": plugin.version,
                    "commands": plugin.commands,
                    "agents": plugin.agents,
                    "skills": plugin.skills,
                }
            )

        if output_path:
            output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        return data
