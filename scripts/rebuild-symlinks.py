#!/usr/bin/env python3
"""
Rebuild symlinks from registry to plugins.

This script uses plugin manifests to recreate symlinks from registry to plugins.
"""

from __future__ import annotations

import os
from pathlib import Path

# Plugin definitions: which assets belong to which plugin
PLUGIN_MANIFESTS = {
    "core-productivity": {
        "commands": ["catchup", "check", "clean", "commit", "context-prime",
                     "explore", "hype", "ready", "roast", "sass", "turbo"],
        "agents": ["code-reviewer"],
        "skills": ["prompt-engineering", "roadmap", "skill-builder"]
    },
    "python-toolkit": {
        "commands": ["test-gen"],
        "agents": ["python-expert"],
        "skills": ["python-development"]
    },
    "typescript-toolkit": {
        "commands": [],
        "agents": ["frontend-developer", "javascript-expert", "nextjs-app-router-developer",
                   "react-performance-optimization", "typescript-expert"],
        "skills": []
    },
    "api-development": {
        "commands": ["review.api", "review.architecture"],
        "agents": ["api-documenter", "backend-architect", "graphql-architect"],
        "skills": ["api-design"]
    },
    "security-suite": {
        "commands": ["review.security"],
        "agents": ["api-security-audit", "security-auditor"],
        "skills": ["security-principles", "security-review"]
    },
    "pr-workflow": {
        "commands": ["review.pr", "review.pr-fix", "setup-labels"],
        "agents": [],
        "skills": []
    },
    "research-tools": {
        "commands": [],
        "agents": ["academic-research-synthesizer", "academic-researcher",
                   "comprehensive-researcher", "research-coordinator",
                   "research-synthesizer", "search-specialist"],
        "skills": ["remembering-conversations"]
    },
    "obsidian-pkm": {
        "commands": [],
        "agents": ["connection-agent", "moc-agent", "tag-agent"],
        "skills": ["obsidian-markdown"]
    },
    "mcp-development": {
        "commands": [],
        "agents": ["mcp-deployment-orchestrator", "mcp-expert", "mcp-registry-navigator",
                   "mcp-security-auditor", "mcp-server-architect", "mcp-testing-engineer"],
        "skills": ["chrome-devtools-mcp", "mcp-development"]
    },
    "dx-tools": {
        "commands": ["code_analysis", "optimize"],
        "agents": ["debugger", "dx-optimizer", "error-detective", "prompt-engineer"],
        "skills": ["cli-development", "developer-experience", "feature-flags",
                   "performance-optimization", "prompt-engineering"]
    },
    "cloud-ops": {
        "commands": [],
        "agents": ["cloud-architect", "deployment-engineer", "devops-troubleshooter",
                   "network-engineer", "terraform-specialist"],
        "skills": []
    },
    "data-science": {
        "commands": [],
        "agents": ["data-analyst", "data-engineer", "data-scientist",
                   "database-optimizer", "ml-engineer", "mlops-engineer", "sql-expert"],
        "skills": ["ai-integration"]
    }
}


def create_symlink(source: Path, target: Path) -> None:
    """Create a relative symlink."""
    if target.exists() or target.is_symlink():
        target.unlink()

    rel_path = os.path.relpath(source, target.parent)
    os.symlink(rel_path, target)


def main() -> None:
    """Main function."""
    script_dir = Path(__file__).parent
    marketplace_root = script_dir.parent
    plugins_dir = marketplace_root / "plugins"
    registry_dir = marketplace_root / "registry"

    for plugin_name, manifest in PLUGIN_MANIFESTS.items():
        plugin_dir = plugins_dir / plugin_name
        print(f"\nRebuilding symlinks for: {plugin_name}")

        for asset_type in ["commands", "agents", "skills"]:
            assets = manifest.get(asset_type, [])
            if not assets:
                continue

            target_dir = plugin_dir / asset_type
            target_dir.mkdir(exist_ok=True)

            for asset_name in assets:
                # Find in registry (could be .md file or directory)
                source = registry_dir / asset_type / f"{asset_name}.md"
                if not source.exists():
                    source = registry_dir / asset_type / asset_name

                if not source.exists():
                    print(f"  WARNING: Asset not found in registry: {asset_type}/{asset_name}")
                    continue

                # Create symlink
                if source.is_file():
                    target = target_dir / source.name
                else:
                    target = target_dir / asset_name

                create_symlink(source, target)
                print(f"  Linked: {asset_type}/{asset_name}")

    print("\n\nSymlinks rebuilt successfully!")


if __name__ == "__main__":
    main()
