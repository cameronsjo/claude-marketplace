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

```bash
# 1. Create plugin structure
mkdir -p plugins/my-plugin/.claude-plugin
mkdir -p plugins/my-plugin/{agents,commands,skills}

# 2. Create plugin.json
cat > plugins/my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does"
}
EOF

# 3. Add assets (agents, commands, skills)

# 4. Register in marketplace
# Edit .claude-plugin/marketplace.json to add entry
```

**Note**: Assets are copied, not symlinked. If sharing an asset across plugins, copy the file to each plugin that needs it.

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
