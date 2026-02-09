# Cameron's Plugin Directory

A directory of Claude Code plugins. Each plugin lives in its own repo for independent installation.

## Plugins

| Plugin | Repo | Description |
|---|---|---|
| essentials | [cameronsjo/essentials](https://github.com/cameronsjo/essentials) | Personality commands - hype, sass, roast, turbo, catchup |
| dev-toolkit | [cameronsjo/dev-toolkit](https://github.com/cameronsjo/dev-toolkit) | Development workflow tools - logging, checks, release pipelines |
| session-continuity | [cameronsjo/session-continuity](https://github.com/cameronsjo/session-continuity) | Cross-session context with timeline logging and inbox capture |
| mcp-toolkit | [cameronsjo/mcp-toolkit](https://github.com/cameronsjo/mcp-toolkit) | MCP server development toolkit - architecture patterns, tools-as-code |
| obsidian-dev | [cameronsjo/obsidian-dev](https://github.com/cameronsjo/obsidian-dev) | Obsidian plugin development - scaffolding, TypeScript, GitHub Actions |
| homebridge-dev | [cameronsjo/homebridge-dev](https://github.com/cameronsjo/homebridge-dev) | Homebridge plugin development - HAP mappings, accessory patterns |
| image-gen-toolkit | [cameronsjo/image-gen-toolkit](https://github.com/cameronsjo/image-gen-toolkit) | Image generation toolkit for Gemini 3 Pro Image |
| homelab | [cameronsjo/homelab](https://github.com/cameronsjo/homelab) | Homelab infrastructure context - Unraid, media stack, Docker |

## Installation

Each plugin repo is its own marketplace. Add and install individually:

```bash
# Add the marketplace
/plugin marketplace add cameronsjo/essentials

# Install the plugin
/plugin install essentials@essentials
```

Or use the automated setup in `~/.claude/setup-marketplaces.sh` which handles all registrations.

## Why Individual Repos?

Previously this was a monorepo containing all plugins. Splitting them means:

- **Install only what you use** — other machines download just the plugins they need
- **Independent versioning** — each plugin has its own release cycle
- **Dev machine uses local paths** — no duplication, edits take effect immediately

## License

MIT
