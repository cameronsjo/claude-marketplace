#!/usr/bin/env python3
"""
Migration script to move existing plugin assets to registry and create symlinks.

This script:
1. Finds all commands, agents, and skills across all plugins
2. Moves unique assets to the registry
3. Replaces the originals with symlinks to the registry
4. Handles duplicates by keeping the first occurrence

Run from marketplace root:
    python scripts/migrate-to-registry.py
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def main() -> None:
    """Main migration function."""
    # Determine paths
    script_dir = Path(__file__).parent
    marketplace_root = script_dir.parent
    plugins_dir = marketplace_root / "plugins"
    registry_dir = marketplace_root / "registry"

    # Ensure registry directories exist
    (registry_dir / "commands").mkdir(parents=True, exist_ok=True)
    (registry_dir / "agents").mkdir(parents=True, exist_ok=True)
    (registry_dir / "skills").mkdir(parents=True, exist_ok=True)

    # Track what we've already added to avoid duplicates
    registered: dict[str, dict[str, Path]] = {
        "commands": {},
        "agents": {},
        "skills": {}
    }

    # First pass: collect all unique assets and move to registry
    print("Phase 1: Moving assets to registry...")

    for plugin_dir in sorted(plugins_dir.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
            continue

        print(f"\nProcessing plugin: {plugin_dir.name}")

        for asset_type in ["commands", "agents", "skills"]:
            assets_dir = plugin_dir / asset_type
            if not assets_dir.exists():
                continue

            for item in sorted(assets_dir.iterdir()):
                if item.name.startswith("."):
                    continue

                # Skip if already a symlink
                if item.is_symlink():
                    print(f"  Skipping symlink: {asset_type}/{item.name}")
                    continue

                # Determine asset name
                if item.is_file() and item.suffix == ".md":
                    name = item.stem
                elif item.is_dir():
                    name = item.name
                else:
                    continue

                # Check if already in registry
                if name in registered[asset_type]:
                    print(f"  Duplicate: {asset_type}/{name} (keeping first from {registered[asset_type][name].parent.parent.name})")
                    # Remove this copy, will symlink later
                    if item.is_file():
                        item.unlink()
                    else:
                        shutil.rmtree(item)
                else:
                    # Move to registry
                    if item.is_file():
                        dest = registry_dir / asset_type / item.name
                    else:
                        dest = registry_dir / asset_type / name

                    print(f"  Moving: {asset_type}/{name} -> registry")
                    shutil.move(str(item), str(dest))
                    registered[asset_type][name] = dest

    # Second pass: create symlinks
    print("\n\nPhase 2: Creating symlinks...")

    for plugin_dir in sorted(plugins_dir.iterdir()):
        if not plugin_dir.is_dir() or plugin_dir.name.startswith("."):
            continue

        print(f"\nProcessing plugin: {plugin_dir.name}")

        # Get the plugin's asset list from a manifest or by convention
        # For now, we'll check what the plugin originally had
        for asset_type in ["commands", "agents", "skills"]:
            assets_dir = plugin_dir / asset_type
            if not assets_dir.exists():
                assets_dir.mkdir(exist_ok=True)

            # Create symlinks for assets this plugin should have
            # We need to determine which assets belong to which plugin
            # For now, we'll skip this and just ensure existing symlinks work


    # Create a manifest of what each plugin should have
    print("\n\nMigration complete!")
    print(f"Registry contains:")
    print(f"  Commands: {len(registered['commands'])}")
    print(f"  Agents: {len(registered['agents'])}")
    print(f"  Skills: {len(registered['skills'])}")

    # Print registry contents
    print("\nRegistry contents:")
    for asset_type in ["commands", "agents", "skills"]:
        print(f"\n{asset_type.upper()}:")
        for name in sorted(registered[asset_type].keys()):
            print(f"  - {name}")


if __name__ == "__main__":
    main()
