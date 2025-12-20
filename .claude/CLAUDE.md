# Claude Code Plugin Marketplace

A collection of agents, commands, and skills that extend Claude Code's capabilities.

## Quick Reference

- **Install plugins**: `/plugin marketplace add cameronsjo/claude-marketplace`
- **Browse plugins**: `/plugin discover`
- **Plugin registry**: `.claude-plugin/marketplace.json`

## Development

### Adding Assets

1. Create the asset in `plugins/{plugin-name}/{type}/`
2. If shared across plugins, copy to other relevant plugins

### Creating Plugins

1. Create directory: `plugins/{name}/`
2. Add `.claude-plugin/plugin.json` with metadata
3. Add agents, commands, and/or skills
4. Add entry to `.claude-plugin/marketplace.json`

### Key Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Plugin registry |
| `.github/workflows/release.yml` | Auto-versioning |
| `docs/adr/` | Architecture decisions |
| `docs/compositions.md` | Plugin bundles |

## Context

Path-specific rules load automatically:

- Editing `plugins/*/commands/*.md` -> command development rules
- Editing `plugins/*/agents/*.md` -> agent development rules
- Editing `plugins/*/skills/*/SKILL.md` -> skill development rules

See `.claude/rules/` for all development guidelines.
