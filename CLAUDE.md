# Claude Marketplace

Hub marketplace for all personal Claude Code plugins and curated obra/superpowers forks.

## Structure

```
├── index.json              # Marketplace registry (all plugins via URL sources)
├── README.md               # Plugin directory with install instructions
└── docs/                   # Historical design docs
```

## Plugins

### Personal (cameronsjo repos)

| Plugin | Repo |
|---|---|
| essentials | cameronsjo/essentials |
| dev-toolkit | cameronsjo/dev-toolkit |
| session-continuity | cameronsjo/session-continuity |
| mcp-toolkit | cameronsjo/mcp-toolkit |
| obsidian-dev | cameronsjo/obsidian-dev |
| homebridge-dev | cameronsjo/homebridge-dev |
| image-gen-toolkit | cameronsjo/image-gen-toolkit |
| homelab | cameronsjo/homelab |

### Superpowers (obra forks)

| Plugin | Repo |
|---|---|
| superpowers | cameronsjo/superpowers |
| superpowers-chrome | cameronsjo/superpowers-chrome |
| superpowers-lab | cameronsjo/superpowers-lab |
| superpowers-developing-for-claude-code | cameronsjo/superpowers-developing-for-claude-code |
| episodic-memory | cameronsjo/episodic-memory |
| double-shot-latte | cameronsjo/double-shot-latte |
| elements-of-style | cameronsjo/the-elements-of-style |

## Plugin Repo Structure

Each plugin repo follows:

```
repo-root/
├── .claude-plugin/
│   ├── marketplace.json    # Declares repo as a standalone marketplace
│   └── plugin.json         # Plugin metadata
├── commands/               # Slash commands (.md)
├── agents/                 # Subagents (.md)
├── skills/                 # Skills with SKILL.md
├── README.md
├── LICENSE
└── .gitignore
```
