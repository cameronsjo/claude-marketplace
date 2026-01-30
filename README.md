# Claude Code Marketplace

Lean Claude Code toolkit - actual tools and workflows, not prompt wrappers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Philosophy

This marketplace contains **actual tools and automation**, not "expert prompts" that duplicate Claude's built-in capabilities.

**What's here:**
- CLI tool wrappers (`/ready`)
- Behavior mode commands (`/turbo`, `/roast`)
- MCP servers with real code
- Scripts and templates with actual functionality

**What's NOT here:**
- "Be a Python expert" prompts (use built-in `python-expert` agent)
- "Be a security expert" prompts (use built-in `security-auditor` agent)
- Prompt wrappers that duplicate built-in agents

## Quick Start

```bash
# Add marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Install core workflow commands
/plugin install core@cameronsjo

# Install user memory MCP + PR workflows
/plugin install essentials@cameronsjo
```

## Plugins

| Plugin | What It Actually Does |
|--------|----------------------|
| **core** | Workflow modes (`/turbo`, `/roast`, `/hype`), `/ready` CLI wrapper, `/check`, `/clean` |
| **essentials** | User memory MCP server (actual code), PR review commands, roadmap tracking |
| **research** | Conversation indexing tool - semantic search over past sessions |
| **security** | Python scripts: OWASP checklist, secret scanning, security audit |
| **api** | OpenAPI templates, validation scripts, naming checkers |
| **dx** | Feature flags TypeScript toolkit with generators and stale detection |
| **cc-web** | Session start hook templates for cloud Claude Code |

## Installation

```bash
# Minimal - just workflow modes
/plugin install core@cameronsjo

# Recommended - core + memory + PR workflows
/plugin install core@cameronsjo
/plugin install essentials@cameronsjo
```

Or configure in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cameronsjo": {
      "source": { "source": "github", "repo": "cameronsjo/claude-marketplace" }
    }
  },
  "enabledPlugins": ["core@cameronsjo", "essentials@cameronsjo"]
}
```

## Why So Few Plugins?

Claude Code v2.0+ has excellent built-in agents:
- `python-expert`, `typescript-expert` for language expertise
- `security-auditor`, `api-security-audit` for security
- `mcp-expert`, `mcp-server-architect` for MCP development
- `Explore` agent for codebase investigation

**Use those.** This marketplace only contains things that provide value beyond prompts.

## License

MIT
