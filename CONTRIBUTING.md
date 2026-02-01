# Contributing

Guide for adding plugins to the Claude Marketplace.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/cameronsjo/claude-marketplace.git
cd claude-marketplace

# 2. Create plugin
mkdir -p src/my-plugin/{.claude-plugin,commands}

# 3. Add plugin.json, commands, README
# 4. Register in index.json
# 5. Submit PR
```

## Plugin Structure

```
src/my-plugin/
├── .claude-plugin/
│   └── plugin.json      # Required: metadata
├── README.md            # Required: documentation
├── commands/            # Slash commands
│   └── my-command.md
└── agents/              # Subagents (optional)
    └── my-agent.md
```

## plugin.json

```json
{
  "name": "my-plugin",
  "description": "Brief description for /plugin discover",
  "version": "1.0.0",
  "author": {
    "name": "your-github-username"
  },
  "keywords": ["relevant", "search", "terms"]
}
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier (kebab-case) |
| `description` | Yes | One-line description |
| `version` | Yes | Semver (auto-updated on release) |
| `author.name` | Yes | GitHub username or name |
| `keywords` | No | Search/discovery terms |

## Command Format

`src/my-plugin/commands/my-command.md`:

```yaml
---
description: Brief description shown in /help
category: workflow|code-analysis|context-loading
allowed-tools: Bash, Edit, Read, Glob, Grep
---

# Command Title

Instructions for Claude when this command is invoked.

## Steps

1. First, do this
2. Then do that

$ARGUMENTS
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | Shown in `/help` |
| `category` | No | Grouping for organization |
| `allowed-tools` | No | Restrict available tools |
| `disable-model-invocation` | No | Set `true` for personality commands |

**Tips:**

- End with `$ARGUMENTS` to receive user input
- Use `allowed-tools` to limit scope (security)
- Use `disable-model-invocation: true` for commands that modify Claude's behavior rather than spawning agents

## Agent Format

`src/my-plugin/agents/my-agent.md`:

```yaml
---
name: my-agent
description: |
  When to use this agent.

  <example>
  user: "Help me with X"
  assistant: "I'll use my-agent to handle this."
  </example>

model: inherit
color: cyan
tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash"]
---

# Agent Instructions

What this agent does and how.

## Principles

- Key behavior 1
- Key behavior 2
```

**Frontmatter fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier |
| `description` | Yes | When/why to invoke (with examples) |
| `model` | No | `inherit` (default), `sonnet`, `opus`, `haiku` |
| `color` | No | Terminal color for output |
| `tools` | No | Available tools (defaults to all) |

## Registering in index.json

Add your plugin to the `plugins` array:

```json
{
  "plugins": [
    {
      "name": "my-plugin",
      "version": "1.0.0",
      "path": "./src/my-plugin",
      "description": "Same as plugin.json description"
    }
  ]
}
```

## PR Checklist

- [ ] Plugin directory in `src/`
- [ ] Valid `plugin.json` with name, description, version
- [ ] README.md documenting commands/agents
- [ ] All commands have `description` frontmatter
- [ ] All agents have `name` and `description` frontmatter
- [ ] Entry added to `index.json`
- [ ] CI passes (validates structure automatically)

## Versioning

Don't manually update versions. On merge to main:

1. Conventional commit determines bump type
2. All plugin versions sync automatically
3. Git tag + GitHub release created

**Commit prefixes:**

| Prefix | Version Bump |
|--------|--------------|
| `feat:` | Minor (0.1.0 → 0.2.0) |
| `fix:` | Patch (0.1.0 → 0.1.1) |
| `feat!:` | Major (0.1.0 → 1.0.0) |
| `chore:`, `docs:`, `refactor:` | No bump |

## Testing Locally

```bash
# Install from local path
/plugin install /path/to/claude-marketplace/src/my-plugin

# Or symlink for development
ln -s /path/to/claude-marketplace/src/my-plugin ~/.claude/plugins/my-plugin
```

## Questions?

Open an issue or check existing plugins for examples.
