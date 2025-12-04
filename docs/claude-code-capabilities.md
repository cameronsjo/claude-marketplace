# Claude Code Capabilities Guide

A comprehensive reference for Claude Code's extensibility features: hooks, agents, skills, commands, plugins, and the Agent SDK.

## Table of Contents

1. [Overview](#overview)
2. [Hooks](#hooks)
3. [Subagents](#subagents)
4. [Skills](#skills)
5. [Slash Commands](#slash-commands)
6. [Plugins & Marketplaces](#plugins--marketplaces)
7. [Claude Agent SDK](#claude-agent-sdk)
8. [Feature Comparison](#feature-comparison)

---

## Overview

Claude Code provides multiple extensibility mechanisms:

| Feature | Purpose | Invocation | Location |
|---------|---------|------------|----------|
| **Hooks** | Automate actions at lifecycle events | Automatic | `settings.json` |
| **Subagents** | Specialized AI assistants | Claude-delegated | `.claude/agents/` |
| **Skills** | Domain expertise modules | Auto-detected | `.claude/skills/` |
| **Commands** | User-triggered shortcuts | `/command` | `.claude/commands/` |
| **Plugins** | Bundled extensions | `/plugin install` | Marketplace |
| **SDK** | Programmatic API | Code | npm/pip |

---

## Hooks

Hooks execute shell commands at specific lifecycle events, enabling workflow automation without manual intervention.

### Hook Events

| Event | Trigger | Use Cases |
|-------|---------|-----------|
| `SessionStart` | Claude Code starts | Install dependencies, set env vars |
| `SessionEnd` | Session terminates | Cleanup, save state |
| `UserPromptSubmit` | User submits prompt | Validate input, pre-process |
| `PreToolUse` | Before tool execution | Validate, set up logging |
| `PostToolUse` | After tool completes | Process results, update state |
| `Stop` | Claude finishes responding | Save session, archive changes |
| `PreCompact` | Before context compaction | Preserve important context |
| `SubagentStop` | Subagent finishes | Coordinate results |

### Configuration

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "./scripts/setup.sh",
        "timeout": 120,
        "statusMessage": "Setting up environment..."
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./scripts/validate-bash.sh"
      }]
    }]
  }
}
```

### Hook Options

| Field | Type | Description |
|-------|------|-------------|
| `matcher` | string | Pattern to match (for PreToolUse/PostToolUse) |
| `type` | string | `"command"` or `"prompt"` |
| `command` | string | Shell command or script path |
| `timeout` | number | Max execution time in seconds (default: 60) |
| `statusMessage` | string | Display message during execution |
| `continue` | boolean | Whether to continue after hook (default: true) |
| `stopReason` | string | Message when `continue` is false |

### Exit Codes

- **0**: Success
- **2**: Blocking error (stderr fed to Claude)
- **Other**: Non-blocking error (shown to user)

### Environment Variables

| Variable | Description |
|----------|-------------|
| `$CLAUDE_PROJECT_DIR` | Project root directory |
| `$CLAUDE_PLUGIN_ROOT` | Plugin installation directory |
| `$CLAUDE_ENV_FILE` | Path to session env file |
| `$CLAUDE_CODE_REMOTE` | `"true"` if running in cloud |

---

## Subagents

Subagents are specialized AI assistants that Claude delegates tasks to based on the task type and complexity.

### File Structure

```markdown
---
name: code-reviewer
description: Specialized agent for thorough code reviews
tools: Read, Grep, Bash
model: sonnet
permissionMode: default
skills: security-review
---

You are an expert code reviewer specializing in:
- Security vulnerabilities
- Performance optimization
- Code maintainability

When reviewing code:
1. Check for security issues first
2. Analyze performance implications
3. Suggest specific improvements
```

### Configuration Options

| Field | Description |
|-------|-------------|
| `name` | Unique identifier |
| `description` | When to invoke this agent |
| `tools` | Comma-separated tool list |
| `model` | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `skills` | Skills to auto-load |

### Locations

- **User agents**: `~/.claude/agents/` (all projects)
- **Project agents**: `.claude/agents/` (team-shared)
- **Plugin agents**: `plugins/{name}/agents/`

---

## Skills

Skills are modular directories containing instructions and resources that Claude loads dynamically for specialized tasks.

### Directory Structure

```
skills/my-skill/
├── SKILL.md              # Required: Core definition
├── README.md             # Optional: Documentation
├── reference.md          # Optional: Detailed specs
├── resources/            # Optional: Reference files
│   ├── config.json
│   └── templates/
└── scripts/              # Optional: Helper scripts
    └── validate.py
```

### SKILL.md Format

```markdown
---
name: api-design
description: REST API design and review based on best practices
---

# API Design Skill

## When to Use This Skill
- Designing new REST APIs
- Reviewing API specifications
- Validating OpenAPI documents

## Core Principles
- Resource-oriented design
- Standard HTTP methods
- Consistent naming conventions

## Resources
- [Error codes reference](./resources/error-codes.json)
- [OpenAPI template](./resources/openapi-template.yaml)
```

### Progressive Loading

1. **Level 1 (Always)**: Name and description for discovery
2. **Level 2 (On relevance)**: Main SKILL.md body
3. **Level 3+ (On demand)**: Additional files and resources

### Locations

- **User skills**: `~/.claude/skills/`
- **Project skills**: `.claude/skills/`
- **Plugin skills**: `plugins/{name}/skills/`

---

## Slash Commands

Slash commands are user-triggered shortcuts for frequently-used operations.

### File Format

```markdown
---
description: Comprehensive code quality review
category: review
argument-hint: <file or directory>
allowed-tools: Read, Grep, Bash
disable-model-invocation: true
model: claude-sonnet-4-5-20250929
---

# Code Review Command

Perform a thorough code review of the specified target.

## Instructions
1. Analyze code structure
2. Check for code smells
3. Review security implications
4. Suggest improvements

## Arguments
$ARGUMENTS - The file or directory to review
```

### Frontmatter Options

| Field | Description |
|-------|-------------|
| `description` | Shown in `/help` |
| `category` | Logical grouping |
| `argument-hint` | Shows expected arguments |
| `allowed-tools` | Restricts available tools |
| `disable-model-invocation` | Prevents auto-invocation |
| `model` | Specific model to use |

### Built-in Commands

- `/help` - Show available commands
- `/context` - Display context info
- `/usage` - Show token usage
- `/model` - View/change model
- `/compact` - Compact conversation
- `/plugin` - Manage plugins
- `/permissions` - Manage permissions
- `/hooks` - Review hook changes

### Locations

- **User commands**: `~/.claude/commands/`
- **Project commands**: `.claude/commands/`
- **Plugin commands**: `plugins/{name}/commands/`

---

## Plugins & Marketplaces

Plugins bundle commands, agents, skills, hooks, and MCP servers for easy distribution.

### Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: Manifest
├── commands/                # Slash commands
├── agents/                  # Subagents
├── skills/                  # Skills
├── hooks/
│   ├── hooks.json           # Hook configuration
│   └── scripts/
└── .mcp.json                # MCP servers
```

### plugin.json

```json
{
  "name": "my-plugin",
  "displayName": "My Plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": "Your Name",
  "commands": "./commands",
  "agents": "./agents",
  "skills": "./skills",
  "hooks": "./hooks/hooks.json",
  "mcp": "./.mcp.json"
}
```

### Marketplace Configuration

```json
{
  "name": "my-marketplace",
  "metadata": {
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "plugin-name",
      "source": "./plugins/plugin-name",
      "description": "Plugin description",
      "category": "productivity",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

### Installing Plugins

```bash
# Add marketplace
/plugin marketplace add https://github.com/org/marketplace

# Install plugin
/plugin install plugin-name@marketplace-name

# List installed
/plugin list
```

### Settings Configuration

```json
{
  "enabledPlugins": {
    "plugin@marketplace": true
  },
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": { "source": "github", "repo": "org/plugins" }
    }
  }
}
```

---

## Claude Agent SDK

The Claude Agent SDK provides programmatic access to Claude Code's capabilities.

### Installation

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### Python Example

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
        cwd="/path/to/project"
    )

    async for message in query(prompt="Create a hello world script", options=options):
        if message.type == "assistant":
            for block in message.content:
                if block.type == "text":
                    print(block.text)

anyio.run(main)
```

### TypeScript Example

```typescript
import { query, type ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

async function main() {
    const options: ClaudeAgentOptions = {
        systemPrompt: "You are a helpful assistant",
        allowedTools: ["Read", "Write", "Bash"],
        permissionMode: "acceptEdits",
        cwd: "/path/to/project"
    };

    for await (const message of query({ prompt: "Create a hello world script", options })) {
        if (message.type === "assistant") {
            for (const block of message.message.content) {
                if (block.type === "text") {
                    console.log(block.text);
                }
            }
        }
    }
}
```

### Key Options

| Option | Description |
|--------|-------------|
| `system_prompt` | Custom system instructions |
| `allowed_tools` | Tool whitelist |
| `permission_mode` | `"acceptEdits"` or `"manual"` |
| `cwd` | Working directory |
| `max_turns` | Conversation limit |
| `mcp_servers` | Custom MCP servers |
| `setting_sources` | Load project config |

### Custom Tools

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_weather", "Get weather for a location", {"location": str})
async def get_weather(args):
    return {"content": [{"type": "text", "text": f"Sunny in {args['location']}"}]}

server = create_sdk_mcp_server(name="my-tools", tools=[get_weather])
```

---

## Feature Comparison

### Invocation Methods

| Feature | User-Invoked | Auto-Invoked | Claude-Delegated |
|---------|--------------|--------------|------------------|
| Hooks | - | ✓ | - |
| Skills | - | ✓ | - |
| Commands | ✓ | Optional | - |
| Subagents | - | - | ✓ |
| Plugins | ✓ (install) | - | - |

### Configuration Locations

| Feature | User Level | Project Level | Plugin |
|---------|------------|---------------|--------|
| Hooks | `~/.claude/settings.json` | `.claude/settings.json` | `hooks.json` |
| Skills | `~/.claude/skills/` | `.claude/skills/` | `skills/` |
| Commands | `~/.claude/commands/` | `.claude/commands/` | `commands/` |
| Agents | `~/.claude/agents/` | `.claude/agents/` | `agents/` |

### Claude Code CLI vs SDK

| Feature | CLI | SDK |
|---------|-----|-----|
| Interactive REPL | ✓ | - |
| IDE Integration | ✓ | - |
| Plugins | ✓ | - |
| Sandbox Mode | ✓ | - |
| In-Process MCP | - | ✓ |
| Session Forking | - | ✓ |
| Runtime Tool Filtering | - | ✓ |
| Multi-Agent Orchestration | Limited | Full |

---

## Quick Reference

### File Locations

```
~/.claude/                    # User-level config
├── settings.json             # User settings
├── agents/                   # User agents
├── commands/                 # User commands
└── skills/                   # User skills

.claude/                      # Project-level config
├── settings.json             # Shared settings
├── settings.local.json       # Local overrides
├── agents/                   # Project agents
├── commands/                 # Project commands
└── skills/                   # Project skills

CLAUDE.md                     # Project context
.mcp.json                     # MCP servers
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API authentication |
| `ANTHROPIC_MODEL` | Model selection |
| `CLAUDE_CODE_USE_BEDROCK` | Enable Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Enable Vertex AI |
| `MAX_THINKING_TOKENS` | Extended thinking budget |

---

## Resources

### Official Documentation
- [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Skills Guide](https://www.anthropic.com/news/skills)
- [Plugins Guide](https://www.anthropic.com/news/claude-code-plugins)
- [Agent SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)

### GitHub Repositories
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)
