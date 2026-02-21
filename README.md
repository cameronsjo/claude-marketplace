# Workbench

Hub registry for all personal Claude Code plugins and curated obra/superpowers forks.

## Installation

```bash
# Register the marketplace
/plugin marketplace add cameronsjo/workbench

# Install what you need
/plugin install essentials@cameronsjo
/plugin install superpowers@cameronsjo
```

Or use the automated setup in `~/.claude/setup-marketplaces.sh`.

## Plugins (17)

### Personal

| Plugin | Description |
|---|---|
| essentials | Core workflow: brainstorming, worktrees, enforcement hooks, session management |
| vibes | Communication styles: hype, sass, roast, unhinged |
| rules | 10 languages, security, quality, git, CI/CD, Docker, MCP, documentation |
| dev-toolkit | Logging agents, project checks, release pipelines |
| mcp-toolkit | MCP server development patterns |
| obsidian | Vault management, markdown reference, Bases, plugin development |
| homebridge-dev | Homebridge plugin development: HAP mappings, accessory patterns |
| image-gen-toolkit | Image generation toolkit for Gemini |
| homelab | Homelab infrastructure: Unraid, media stack, Docker services |
| git-guardrails | Push/gh write guards, branch warnings, commit nudges |
| project-onboard | Onboarding skills for project portfolio |

### Superpowers (obra forks)

| Plugin | Description |
|---|---|
| superpowers | Core skills: TDD, debugging, collaboration patterns |
| superpowers-chrome | Chrome DevTools Protocol: skill mode + MCP mode |
| superpowers-lab | Experimental: tmux, MCP discovery, duplicate detection |
| superpowers-developing-for-claude-code | Plugin/skill/MCP development docs |
| double-shot-latte | Auto-continues work instead of stopping to ask |
| the-elements-of-style | Strunk's writing guidance (1918) |

## Architecture

Each plugin lives in its own GitHub repo. This registry's `marketplace.json` references them via URL sources. On the dev machine, local path overrides in `setup-marketplaces.sh` provide instant edit propagation.

## License

MIT
