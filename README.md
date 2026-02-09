# Cameron's Plugin Marketplace

A single Claude Code marketplace with personal plugins and curated obra/superpowers forks.

## Installation

```bash
# Register the marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Install what you need
/plugin install essentials@cameronsjo
/plugin install superpowers@cameronsjo
```

Or use the automated setup in `~/.claude/setup-marketplaces.sh`.

## Plugins

### Personal

| Plugin | Description |
|---|---|
| essentials | Personality commands - hype, sass, roast, turbo, catchup |
| dev-toolkit | Development workflow tools - logging, checks, release pipelines |
| session-continuity | Cross-session context with timeline logging and inbox capture |
| mcp-toolkit | MCP server development - architecture patterns, tools-as-code |
| obsidian-dev | Obsidian plugin development - scaffolding, TypeScript, GitHub Actions |
| homebridge-dev | Homebridge plugin development - HAP mappings, accessory patterns |
| image-gen-toolkit | Image generation toolkit for Gemini 3 Pro Image |
| homelab | Homelab infrastructure - Unraid, media stack, Docker services |

### Superpowers (obra forks)

| Plugin | Description |
|---|---|
| superpowers | Core skills: TDD, debugging, collaboration patterns |
| superpowers-chrome | Chrome DevTools Protocol - skill mode + MCP mode |
| superpowers-lab | Experimental: tmux, MCP discovery, duplicate detection |
| superpowers-developing-for-claude-code | Plugin/skill/MCP development docs |
| episodic-memory | Semantic search for conversations across sessions |
| double-shot-latte | Auto-continues work instead of stopping to ask |
| elements-of-style | Strunk's writing guidance (1918) |

## Architecture

Each plugin lives in its own GitHub repo. This marketplace's `index.json` references them via URL sources. On the dev machine, local path overrides provide instant edit propagation.

## License

MIT
