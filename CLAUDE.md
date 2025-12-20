# Claude Code Plugin Marketplace

A collection of agents, commands, and skills that extend Claude Code's capabilities.

## Quick Start

```bash
# Add this marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Browse available plugins
/plugin discover

# Install a plugin
/plugin install core@cameronsjo
```

## Documentation

Project instructions have moved to modular rule files:

| Location | Content |
|----------|---------|
| `.claude/CLAUDE.md` | Development quick reference |
| `.claude/rules/architecture.md` | Flat file philosophy, plugin structure |
| `.claude/rules/versioning.md` | Conventional commits, releases |
| `.claude/rules/commands.md` | Command format (path-targeted) |
| `.claude/rules/agents.md` | Agent format (path-targeted) |
| `.claude/rules/skills.md` | Skill format (path-targeted) |

Path-targeted rules load automatically when editing relevant files.

## Key Files

| File | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Plugin registry |
| `.github/workflows/release.yml` | Auto-versioning |
| `docs/adr/0001-flat-file-architecture.md` | Architecture decision |
| `docs/compositions.md` | Plugin bundles |
