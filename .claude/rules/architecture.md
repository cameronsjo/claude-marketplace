# Architecture

This marketplace uses a **flat file architecture** - plugins contain real files, not symlinks.

## Why Flat Files?

Claude Code doesn't follow symlinks when scanning for commands, agents, and skills. When users install plugins via `/plugin install`, symlinks would be preserved but unresolvable.

See @docs/adr/0001-flat-file-architecture.md for the full decision record.

## Duplication is Intentional

Some assets appear in multiple plugins. This is by design:

- Keeps plugins self-contained and portable
- Avoids symlink resolution issues
- Simplifies mental model (what you see is what you get)

**Trade-off:** When updating a shared asset, check if other plugins need the same update.

## Plugin Structure

```
plugins/{plugin-name}/
├── .claude-plugin/plugin.json  # Required: Plugin metadata
├── agents/                     # Agent prompts (.md files)
├── commands/                   # Slash command prompts (.md files)
├── skills/                     # Skill directories (SKILL.md + resources/)
└── hooks/                      # Event handlers (optional)
```

## Marketplace Configuration

`.claude-plugin/marketplace.json` defines available plugins:

- Plugin name, description, version
- Source path pointing to `./plugins/{name}`
- Keywords for discovery
