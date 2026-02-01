# Claude Marketplace

Personal Claude Code plugin marketplace by [@cameronsjo](https://github.com/cameronsjo).

## Installation

```bash
# Add marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Install plugins
/plugin install essentials@cameronsjo
/plugin install development@cameronsjo
```

## Plugins

### essentials

Personality commands for celebration, wit, and productivity.

| Command | Description |
|---------|-------------|
| `/hype` | Encouragement mode - Ted Lasso energy, specific wins |
| `/sass` | Witty responses with 4 intensity levels 🌶️ |
| `/roast` | Maximum scrutiny - thorough analysis |
| `/turbo` | Parallel execution, zero hesitation |
| `/catchup` | Reload uncommitted changes after `/clear` |

### development

Development workflow tools and agents.

| Command | Description |
|---------|-------------|
| `/check` | Run project validation, fix errors |
| `/clean` | Fix all linting and formatting |
| `/context-prime` | Load project context |

| Agent | Description |
|-------|-------------|
| `add-logging` | Storytelling-style structured logging |

### release-pipelines

Three-stage release pipeline (Beta → RC → Stable) for Node/TypeScript.

| Command | Description |
|---------|-------------|
| `/setup-release-pipeline` | Generate GitHub Actions workflows |

### obsidian-dev

Complete toolkit for Obsidian plugin development.

| Command | Description |
|---------|-------------|
| `/obsidian.init` | Scaffold new Obsidian plugin |
| `/obsidian.release` | Trigger beta/RC/stable releases |

| Agent | Description |
|-------|-------------|
| `obsidian-plugin-expert` | TypeScript, Obsidian API, BRAT |

## License

MIT
