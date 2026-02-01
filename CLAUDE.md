# Claude Marketplace Development

Plugin marketplace for Claude Code.

## Structure

```
├── index.json              # Marketplace registry
├── essentials/             # Personality commands
├── development/            # Dev workflow tools
├── release-pipelines/      # CI/CD automation
└── obsidian-dev/           # Obsidian plugin toolkit
```

## Plugin Format

Each plugin follows:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json         # name, description, version, keywords
├── README.md
├── commands/               # Slash commands (.md)
└── agents/                 # Subagents (.md)
```

## Adding Plugins

1. Create plugin directory with structure above
2. Add entry to `index.json`
3. Commit and push

## Command Frontmatter

```yaml
---
description: Brief description shown in /help
category: workflow|code-analysis|context-loading
allowed-tools: Bash, Edit, Read
disable-model-invocation: true  # For personality commands
---
```

## Agent Frontmatter

```yaml
---
name: agent-id
description: |
  When to use this agent with examples.
model: inherit
tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
---
```

## Versioning

Use conventional commits. Version bumps via commit message:

- `feat:` → minor
- `fix:` → patch
- `feat!:` or `BREAKING CHANGE:` → major
