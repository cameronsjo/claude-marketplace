# Claude Code Marketplace

Personal Claude Code plugin marketplace - a curated collection of agents, commands, and skills for software development.

[![Support me on Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20Me-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/cameronsjo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Quick Start

```bash
# Add marketplace
/plugin marketplace add cameronsjo/claude-marketplace

# Browse available plugins
/plugin

# Install a plugin
/plugin install core-productivity@cameron-tools
```

## Available Plugins

| Plugin | Description | Docs |
|--------|-------------|------|
| [**core-productivity**](docs/core-productivity.md) | Git workflows, code review, project checks | [View](docs/core-productivity.md) |
| [**python-toolkit**](docs/python-toolkit.md) | Python development with uv, async, testing | [View](docs/python-toolkit.md) |
| [**typescript-toolkit**](docs/typescript-toolkit.md) | TypeScript/React/Next.js patterns | [View](docs/typescript-toolkit.md) |
| [**api-development**](docs/api-development.md) | REST API design, OpenAPI, architecture | [View](docs/api-development.md) |
| [**security-suite**](docs/security-suite.md) | OWASP, vulnerability scanning, auth | [View](docs/security-suite.md) |
| [**pr-workflow**](docs/pr-workflow.md) | Multi-perspective PR reviews, labels | [View](docs/pr-workflow.md) |
| [**research-tools**](docs/research-tools.md) | Comprehensive research, academic sources | [View](docs/research-tools.md) |
| [**obsidian-pkm**](docs/obsidian-pkm.md) | Obsidian markdown, MOCs, tags, linking | [View](docs/obsidian-pkm.md) |
| [**mcp-development**](docs/mcp-development.md) | MCP server architecture, testing, security | [View](docs/mcp-development.md) |
| [**dx-tools**](docs/dx-tools.md) | Debugging, optimization, prompts | [View](docs/dx-tools.md) |
| [**cloud-ops**](docs/cloud-ops.md) | AWS/Azure/GCP, Kubernetes, Terraform | [View](docs/cloud-ops.md) |
| [**data-science**](docs/data-science.md) | SQL, ML pipelines, data engineering | [View](docs/data-science.md) |

## Installation

### Add the Marketplace

```bash
/plugin marketplace add cameronsjo/claude-marketplace
```

### Install by Composition

Use pre-configured [compositions](docs/compositions.md) for common workflows:

| Composition | Best For | Plugins |
|-------------|----------|---------|
| **essentials** | Every project | core-productivity, pr-workflow |
| **fullstack-ts** | TypeScript/React | essentials + typescript-toolkit, api-development |
| **python-backend** | Python services | essentials + python-toolkit, api-development |
| **code-quality** | Security focus | essentials + security-suite |
| **writing** | Docs & PKM | core-productivity, obsidian-pkm, research-tools |
| **cloud-native** | DevOps/Infra | essentials + cloud-ops, security-suite |
| **data-platform** | Data/ML | essentials + python-toolkit, data-science |
| **mcp-builder** | MCP servers | essentials + mcp-development, typescript-toolkit |

See [compositions.md](docs/compositions.md) for copy-paste configs.

### Install Individual Plugins

```bash
# Essential for every project
/plugin install core-productivity@cameron-tools

# For Python projects
/plugin install python-toolkit@cameron-tools

# For TypeScript/React projects
/plugin install typescript-toolkit@cameron-tools

# For API development
/plugin install api-development@cameron-tools
```

### Project Configuration

Configure auto-installation in your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "cameron-tools": {
      "source": {
        "source": "github",
        "repo": "cameronsjo/claude-marketplace"
      }
    }
  },
  "enabledPlugins": [
    "core-productivity@cameron-tools",
    "python-toolkit@cameron-tools"
  ]
}
```

## Documentation

See the [docs/](docs/) folder for detailed documentation on each plugin:

- [Getting Started](docs/getting-started.md) - Installation and basic usage
- [Plugin Guide](docs/plugin-guide.md) - How plugins work together
- [Compositions](docs/compositions.md) - Pre-configured plugin bundles
- Individual plugin docs linked in the table above

## Acknowledgments

Many of the original agent prompts in this collection were inspired by or derived from [davepoon/claude-code-subagents-collection](https://github.com/davepoon/claude-code-subagents-collection). Huge thanks to [@davepoon](https://github.com/davepoon) for the foundational work on Claude Code subagents!

## Support

If you find this marketplace useful, consider supporting the project:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cameronsjo)

## Contributing

1. Fork this repository
2. Add or modify plugins in `plugins/`
3. Update `marketplace.json`
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.
