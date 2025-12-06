# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugin marketplace - a collection of agents, commands, and skills that extend Claude Code's capabilities. Plugins are distributed via GitHub and installed using `/plugin` commands.

## Architecture

### Flat File Structure

Plugins contain real files (not symlinks) because Claude Code's plugin system doesn't follow symlinks when scanning for commands/agents/skills. The registry serves as the canonical source, and files are copied into plugins.

```
registry/               # Source of truth for all assets
├── agents/            # Agent prompts (.md files)
├── commands/          # Slash command prompts (.md files)
└── skills/            # Skill directories (SKILL.md + resources/)

plugins/               # Installable plugin packages (real files, not symlinks)
├── {plugin-name}/
│   ├── .claude-plugin/plugin.json  # Plugin metadata
│   ├── agents/        # Copied from registry/agents/
│   ├── commands/      # Copied from registry/commands/
│   └── skills/        # Copied from registry/skills/
```

**Important:** When updating assets, edit the file in `registry/` then copy to all plugins that use it. The plugin-builder CLI can help manage this.

### Plugin Builder CLI

`scripts/plugin-builder.py` manages the marketplace:

```bash
# Show dashboard with stats and health
python scripts/plugin-builder.py dashboard

# List all assets in registry
python scripts/plugin-builder.py list

# Show which plugins use each asset
python scripts/plugin-builder.py usage

# Find orphaned (unused) assets
python scripts/plugin-builder.py orphans

# Add asset to a plugin (copies from registry)
python scripts/plugin-builder.py edit add {plugin} {asset} -t {commands|agents|skills}

# Interactive mode
python scripts/plugin-builder.py
```

### Marketplace Configuration

`.claude-plugin/marketplace.json` defines available plugins:

- Plugin name, description, version
- Source path pointing to `./plugins/{name}`
- Keywords for discovery

## Asset Formats

### Commands (registry/commands/*.md)

YAML frontmatter with description, category, and allowed-tools. Body contains the prompt template.

### Agents (registry/agents/*.md)

YAML frontmatter defining the agent persona. Body contains system prompt and behavioral guidelines.

### Skills (registry/skills/{name}/)

Directory structure:

- `SKILL.md` - Main skill definition with frontmatter
- `README.md` - Optional documentation
- `resources/` - Additional reference files

## Development Workflow

When adding new assets:

1. Create the asset in `registry/{type}/`
2. Use plugin-builder to add it to plugins: `python scripts/plugin-builder.py edit add {plugin} {asset} -t {type}`

When creating a new plugin:

1. `python scripts/plugin-builder.py create {name} -d "description"`
2. Add assets using `edit add` commands
3. Add entry to `.claude-plugin/marketplace.json`

When updating existing assets:

1. Edit the file in `registry/{type}/`
2. The change needs to be propagated to all plugins using that asset (plugin-builder can help identify which plugins)

## Versioning

Auto-versioning on push to main via conventional commits:

| Commit Prefix | Bump | Example |
|--------------|------|---------|
| `feat!:` or `BREAKING CHANGE` | MAJOR | 1.0.0 -> 2.0.0 |
| `feat:` | MINOR | 1.0.0 -> 1.1.0 |
| `fix:` | PATCH | 1.0.0 -> 1.0.1 |
| `chore:`, `docs:`, `refactor:` | none | no release |

The workflow updates `marketplace.json`, creates a git tag, and publishes a GitHub release.

## Key Files

- `.claude-plugin/marketplace.json` - Plugin registry for Claude Code
- `.github/workflows/release.yml` - Auto-versioning workflow
- `scripts/plugin-builder.py` - CLI for managing assets and plugins
- `docs/compositions.md` - Pre-configured plugin bundles for common workflows
