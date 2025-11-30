#!/usr/bin/env python3
"""
Plugin Builder CLI

Interactive tool for managing Claude Code marketplace plugins.
Manages a central registry of commands, agents, and skills,
and creates plugins by symlinking from the registry.

Usage:
    python scripts/plugin-builder.py [command]

Commands:
    (no command)    Launch interactive TUI
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
    repair          Fix or remove broken symlinks
    export          Export plugin/registry as JSON
    sync            Sync assets from external directory
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

# Import from TUI package
sys.path.insert(0, str(Path(__file__).parent))
from plugin_builder_tui.builder import (
    Asset,
    AssetType,
    Plugin,
    PluginBuilder,
    UsageInfo,
)


# ANSI color codes for terminal output (CLI mode only)
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

    print(
        f"\n{c.BOLD}{c.CYAN}╔══════════════════════════════════════════════════════════════╗{c.RESET}"
    )
    print(
        f"{c.BOLD}{c.CYAN}║          CLAUDE CODE MARKETPLACE - DASHBOARD                 ║{c.RESET}"
    )
    print(
        f"{c.BOLD}{c.CYAN}╚══════════════════════════════════════════════════════════════╝{c.RESET}"
    )

    # Stats
    print(f"\n{c.BOLD}REGISTRY STATS{c.RESET}")
    print(f"   Commands: {c.GREEN}{stats['commands']}{c.RESET}")
    print(f"   Agents:   {c.GREEN}{stats['agents']}{c.RESET}")
    print(f"   Skills:   {c.GREEN}{stats['skills']}{c.RESET}")
    print(
        f"   Total:    {c.BOLD}{stats['total_assets']}{c.RESET} ({stats['total_size_kb']} KB)"
    )

    # Plugins
    print(f"\n{c.BOLD}PLUGINS ({len(plugins)}){c.RESET}")
    for p in plugins:
        asset_count = p.total_assets
        print(
            f"   {p.name}: {asset_count} assets (C:{len(p.commands)} A:{len(p.agents)} S:{len(p.skills)})"
        )

    # Health
    print(f"\n{c.BOLD}HEALTH{c.RESET}")

    if orphans:
        print(f"   Orphaned assets: {c.YELLOW}{len(orphans)}{c.RESET}")
        for o in orphans[:3]:
            print(f"      {o.asset_type.value}/{o.name}")
        if len(orphans) > 3:
            print(f"      ... and {len(orphans) - 3} more")
    else:
        print(f"   Orphaned assets: {c.GREEN}0{c.RESET}")

    if shared:
        print(f"   Shared assets: {c.BLUE}{len(shared)}{c.RESET}")
        for s in shared[:3]:
            print(f"      {s.asset_type.value}/{s.asset_name} ({len(s.plugins)} plugins)")
        if len(shared) > 3:
            print(f"      ... and {len(shared) - 3} more")
    else:
        print(f"   Shared assets: {c.DIM}0{c.RESET}")

    # Validation
    valid, issues = builder.validate()
    status = f"{c.GREEN}HEALTHY{c.RESET}" if valid else f"{c.RED}ISSUES FOUND{c.RESET}"
    print(f"   Symlinks: {status}")

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
            print(
                f"  {u.asset_name:30} {status:20} {Colors.DIM}{plugins_str}{Colors.RESET}"
            )


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

    print(
        f"\n{Colors.BOLD}{Colors.YELLOW}Orphaned assets (not used by any plugin):{Colors.RESET}\n"
    )

    for asset in orphans:
        print(f"  [{asset.asset_type.value}] {asset.name}")


def cmd_duplicates(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Find assets used in multiple plugins."""
    shared = builder.get_shared_assets()

    if not shared:
        print(f"{Colors.DIM}No shared assets found{Colors.RESET}")
        return

    print(
        f"\n{Colors.BOLD}{Colors.BLUE}Shared assets (used by multiple plugins):{Colors.RESET}\n"
    )

    for u in sorted(shared, key=lambda x: -x.usage_count):
        print(f"  [{u.asset_type.value}] {Colors.CYAN}{u.asset_name}{Colors.RESET}")
        print(f"    Used by: {', '.join(u.plugins)}")


def cmd_add(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Add asset to registry."""
    source_path = Path(args.source)
    asset_type = AssetType(args.type)

    asset = builder.add_to_registry(source_path, asset_type, args.name)
    print(f"{Colors.GREEN}Added to registry: {asset_type.value}/{asset.name}{Colors.RESET}")


def cmd_create(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Create a new plugin."""
    plugin = builder.create_plugin(args.name, args.description or "")
    print(f"{Colors.GREEN}Created plugin: {plugin.name}{Colors.RESET}")


def cmd_edit(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Edit a plugin (add/remove assets)."""
    action = args.action
    plugin_name = args.plugin
    asset_name = args.asset
    asset_type = AssetType(args.type)

    if action == "add":
        success = builder.add_asset_to_plugin(plugin_name, asset_name, asset_type)
        if success:
            print(
                f"{Colors.GREEN}Added {asset_type.value[:-1]} '{asset_name}' to plugin '{plugin_name}'{Colors.RESET}"
            )
        else:
            print(f"{Colors.YELLOW}Asset already exists in plugin{Colors.RESET}")
    elif action == "remove":
        success = builder.remove_asset_from_plugin(plugin_name, asset_name, asset_type)
        if success:
            print(
                f"{Colors.GREEN}Removed {asset_type.value[:-1]} '{asset_name}' from plugin '{plugin_name}'{Colors.RESET}"
            )
        else:
            print(f"{Colors.YELLOW}Asset not found in plugin{Colors.RESET}")


def cmd_rename(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Rename an asset."""
    asset_type = AssetType(args.type)

    # Need to re-implement rename since we moved the class
    type_dir = builder.registry_dir / asset_type.value

    old_path = type_dir / args.old_name
    if not old_path.exists():
        old_path = type_dir / f"{args.old_name}.md"

    if not old_path.exists():
        raise ValueError(
            f"Asset '{args.old_name}' not found in registry/{asset_type.value}"
        )

    if old_path.is_file():
        new_path = type_dir / f"{args.new_name}.md"
    else:
        new_path = type_dir / args.new_name

    if new_path.exists():
        raise ValueError(f"Asset '{args.new_name}' already exists")

    import os

    # Rename in registry
    old_path.rename(new_path)

    # Update symlinks in all plugins
    for plugin in builder.get_plugins():
        plugin_dir = builder.plugins_dir / plugin.name
        assets_dir = plugin_dir / asset_type.value
        if not assets_dir.exists():
            continue

        for item in assets_dir.iterdir():
            if item.is_symlink():
                try:
                    target = item.resolve()
                    if target == old_path.resolve():
                        item.unlink()
                        rel_path = os.path.relpath(new_path, item.parent)
                        new_link = assets_dir / (
                            f"{args.new_name}.md"
                            if new_path.suffix == ".md"
                            else args.new_name
                        )
                        os.symlink(rel_path, new_link)
                        print(f"  Updated symlink in {plugin.name}")
                except Exception:
                    pass

    print(f"{Colors.GREEN}Renamed '{args.old_name}' to '{args.new_name}'{Colors.RESET}")


def cmd_delete(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Delete an asset."""
    asset_type = AssetType(args.type)
    builder.delete_asset(args.name, asset_type, args.force)
    print(f"{Colors.GREEN}Deleted '{args.name}' from registry{Colors.RESET}")


def cmd_validate(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Validate plugins."""
    valid, issues = builder.validate()

    if issues:
        print("\nIssues found:")
        for issue in issues:
            color = Colors.RED if issue.issue_type == "broken" else Colors.YELLOW
            print(f"  {color}{issue.issue_type.upper()}{Colors.RESET}: {issue.path}")
            print(f"    {issue.message}")
    else:
        print(f"{Colors.GREEN}All plugins validated successfully{Colors.RESET}")

    sys.exit(0 if valid else 1)


def cmd_repair(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Repair broken symlinks."""
    import os

    valid, issues = builder.validate()

    if not issues:
        print(f"{Colors.GREEN}No issues to repair{Colors.RESET}")
        return

    broken_count = 0
    fixed_count = 0
    removed_count = 0

    for issue in issues:
        if issue.issue_type != "broken":
            continue

        broken_count += 1
        path = Path(issue.path)

        if not path.is_symlink():
            continue

        # Try to determine what the symlink was pointing to
        try:
            target = os.readlink(path)
            target_name = Path(target).name

            # Extract asset type from path
            asset_type_name = path.parent.name  # e.g., "skills", "commands", "agents"

            # Look for matching asset in registry
            registry_path = builder.registry_dir / asset_type_name

            # Try to find matching asset
            matched_asset = None
            if registry_path.exists():
                # Check for exact match
                potential_paths = [
                    registry_path / target_name,
                    registry_path / f"{target_name}.md" if not target_name.endswith(".md") else None,
                    registry_path / target_name.replace(".md", "") if target_name.endswith(".md") else None,
                ]
                for p in potential_paths:
                    if p and p.exists():
                        matched_asset = p
                        break

            if matched_asset and not args.remove_only:
                # Re-create the symlink
                if args.dry_run:
                    print(f"  Would fix: {path}")
                    print(f"    -> {matched_asset}")
                else:
                    path.unlink()
                    rel_path = os.path.relpath(matched_asset, path.parent)
                    os.symlink(rel_path, path)
                    print(f"{Colors.GREEN}Fixed{Colors.RESET}: {path}")
                    print(f"    -> {matched_asset}")
                fixed_count += 1
            else:
                # Remove broken symlink
                if args.dry_run:
                    print(f"  Would remove: {path}")
                else:
                    path.unlink()
                    print(f"{Colors.YELLOW}Removed{Colors.RESET}: {path}")
                removed_count += 1

        except Exception as e:
            print(f"{Colors.RED}Error processing {path}: {e}{Colors.RESET}")

    print()
    if args.dry_run:
        print(f"{Colors.CYAN}Dry run complete{Colors.RESET}")
        print(f"  Would fix: {fixed_count}")
        print(f"  Would remove: {removed_count}")
    else:
        print(f"{Colors.GREEN}Repair complete{Colors.RESET}")
        print(f"  Broken: {broken_count}")
        print(f"  Fixed: {fixed_count}")
        print(f"  Removed: {removed_count}")


def cmd_rebuild(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Rebuild symlinks."""
    import os

    plugins = builder.get_plugins()
    if args.plugin:
        plugins = [p for p in plugins if p.name == args.plugin]
        if not plugins:
            raise ValueError(f"Plugin '{args.plugin}' not found")

    for plugin in plugins:
        plugin_dir = builder.plugins_dir / plugin.name
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


def cmd_export(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Export to JSON."""
    output = Path(args.output) if args.output else None
    data = builder.export_json(output)

    if output:
        print(f"{Colors.GREEN}Exported to: {output}{Colors.RESET}")
    else:
        print(json.dumps(data, indent=2))


def cmd_sync(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Sync from directory."""
    source = Path(args.source)
    asset_type = AssetType(args.type)

    if not source.exists():
        raise ValueError(f"Source directory does not exist: {source}")

    existing = {a.name for a in builder.get_registry_assets(asset_type)}
    added = 0
    skipped = 0

    for item in source.iterdir():
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

        if args.dry_run:
            print(f"  Would add: {name}")
        else:
            builder.add_to_registry(item, asset_type, name)

        added += 1

    print(f"\n{Colors.GREEN}Added: {added}, Skipped (existing): {skipped}{Colors.RESET}")


def cmd_tui(args: argparse.Namespace, builder: PluginBuilder) -> None:
    """Launch interactive TUI."""
    try:
        from plugin_builder_tui.app import PluginBuilderApp

        app = PluginBuilderApp(marketplace_root=builder.root)
        app.run()
    except ImportError as e:
        print(f"{Colors.RED}Error: TUI dependencies not installed.{Colors.RESET}")
        print(f"Install with: pip install textual")
        print(f"\nDetails: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Plugin Builder CLI for Claude Code marketplace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                            # Launch interactive TUI
  %(prog)s dashboard                  # Show overview dashboard
  %(prog)s list                       # List all assets
  %(prog)s usage                      # Show usage report
  %(prog)s search "python"            # Search for assets
  %(prog)s orphans                    # Find unused assets
  %(prog)s edit add core-prod commit -t commands  # Add asset to plugin
        """,
    )
    parser.add_argument("--root", type=Path, help="Marketplace root directory")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")
    parser.add_argument(
        "--no-tui", action="store_true", help="Disable TUI, use simple CLI"
    )

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
    add_parser.add_argument(
        "--type", "-t", required=True, choices=["commands", "agents", "skills"]
    )
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
    edit_parser.add_argument(
        "--type", "-t", required=True, choices=["commands", "agents", "skills"]
    )

    # rename
    rename_parser = subparsers.add_parser("rename", help="Rename asset")
    rename_parser.add_argument("old_name", help="Current name")
    rename_parser.add_argument("new_name", help="New name")
    rename_parser.add_argument(
        "--type", "-t", required=True, choices=["commands", "agents", "skills"]
    )

    # delete
    delete_parser = subparsers.add_parser("delete", aliases=["rm"], help="Delete asset")
    delete_parser.add_argument("name", help="Asset name")
    delete_parser.add_argument(
        "--type", "-t", required=True, choices=["commands", "agents", "skills"]
    )
    delete_parser.add_argument(
        "--force", "-f", action="store_true", help="Force delete even if used"
    )

    # validate
    subparsers.add_parser("validate", help="Validate all plugins")

    # repair
    repair_parser = subparsers.add_parser("repair", help="Repair broken symlinks")
    repair_parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without applying"
    )
    repair_parser.add_argument(
        "--remove-only", action="store_true", help="Only remove broken symlinks, don't try to fix"
    )

    # rebuild
    rebuild_parser = subparsers.add_parser("rebuild", help="Rebuild symlinks")
    rebuild_parser.add_argument("--plugin", "-p", help="Specific plugin")

    # export
    export_parser = subparsers.add_parser("export", help="Export to JSON")
    export_parser.add_argument("--output", "-o", help="Output file")

    # sync
    sync_parser = subparsers.add_parser("sync", help="Sync from directory")
    sync_parser.add_argument("source", help="Source directory")
    sync_parser.add_argument(
        "--type", "-t", required=True, choices=["commands", "agents", "skills"]
    )
    sync_parser.add_argument("--dry-run", action="store_true", help="Preview only")

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    builder = PluginBuilder(args.root)

    commands = {
        "dashboard": cmd_dashboard,
        "dash": cmd_dashboard,
        "d": cmd_dashboard,
        "list": cmd_list,
        "ls": cmd_list,
        "list-plugins": cmd_list_plugins,
        "lp": cmd_list_plugins,
        "usage": cmd_usage,
        "u": cmd_usage,
        "search": cmd_search,
        "s": cmd_search,
        "orphans": cmd_orphans,
        "duplicates": cmd_duplicates,
        "shared": cmd_duplicates,
        "add": cmd_add,
        "create": cmd_create,
        "edit": cmd_edit,
        "rename": cmd_rename,
        "delete": cmd_delete,
        "rm": cmd_delete,
        "validate": cmd_validate,
        "repair": cmd_repair,
        "rebuild": cmd_rebuild,
        "export": cmd_export,
        "sync": cmd_sync,
    }

    if args.command in commands:
        try:
            commands[args.command](args, builder)
        except Exception as e:
            print(f"{Colors.RED}Error: {e}{Colors.RESET}")
            sys.exit(1)
    else:
        # No command specified - launch TUI (or show help with --no-tui)
        if args.no_tui:
            parser.print_help()
        else:
            cmd_tui(args, builder)


if __name__ == "__main__":
    main()
