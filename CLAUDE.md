# Claude Marketplace

Plugin directory for Claude Code. Plugins have been split into individual repos.

## Structure

```
├── index.json              # Discovery document (lists all plugin repos)
├── README.md               # Plugin directory with install instructions
└── docs/                   # Historical design docs
```

## Where Plugins Live Now

Each plugin is its own repo and marketplace:

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

## Plugin Repo Structure

Each plugin repo follows:

```
repo-root/
├── .claude-plugin/
│   ├── marketplace.json    # Declares repo as a marketplace
│   └── plugin.json         # Plugin metadata
├── commands/               # Slash commands (.md)
├── agents/                 # Subagents (.md)
├── skills/                 # Skills with SKILL.md
├── README.md
├── LICENSE
└── .gitignore
```
