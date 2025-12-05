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
9. [CLI Reference](#cli-reference)
10. [Interactive Mode](#interactive-mode)

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

## CLI Reference

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `claude` | Start interactive REPL | `claude` |
| `claude "query"` | Start REPL with initial prompt | `claude "explain this project"` |
| `claude -p "query"` | Query via SDK, then exit | `claude -p "explain this function"` |
| `cat file \| claude -p "query"` | Process piped content | `cat logs.txt \| claude -p "explain"` |
| `claude -c` | Continue most recent conversation | `claude -c` |
| `claude -r "<id>" "query"` | Resume session by ID | `claude -r "abc123" "Finish PR"` |
| `claude update` | Update to latest version | `claude update` |
| `claude mcp` | Configure MCP servers | `claude mcp` |

### CLI Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--add-dir` | Add additional working directories | `claude --add-dir ../apps ../lib` |
| `--agents` | Define custom subagents via JSON | See below |
| `--allowedTools` | Tools allowed without permission | `"Bash(git log:*)" "Read"` |
| `--disallowedTools` | Tools to block | `"Bash(rm:*)" "Edit"` |
| `--print`, `-p` | Print mode (non-interactive) | `claude -p "query"` |
| `--system-prompt` | Replace entire system prompt | `claude --system-prompt "..."` |
| `--append-system-prompt` | Append to default prompt | `claude --append-system-prompt "..."` |
| `--output-format` | Output format: `text`, `json`, `stream-json` | `claude -p --output-format json` |
| `--verbose` | Enable verbose logging | `claude --verbose` |
| `--max-turns` | Limit agentic turns | `claude -p --max-turns 3` |
| `--model` | Set model (`sonnet`, `opus`, or full name) | `claude --model opus` |
| `--permission-mode` | Set permission mode | `claude --permission-mode plan` |
| `--resume` | Resume session by ID | `claude --resume abc123` |
| `--continue` | Load most recent conversation | `claude --continue` |
| `--dangerously-skip-permissions` | Skip permission prompts | Use with caution |

### Dynamic Agents via CLI

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on quality and security.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | When the subagent should be invoked |
| `prompt` | Yes | System prompt for the subagent |
| `tools` | No | Array of tools (inherits all if omitted) |
| `model` | No | `sonnet`, `opus`, or `haiku` |

### System Prompt Flags

| Flag | Behavior | Modes |
|------|----------|-------|
| `--system-prompt` | **Replaces** entire prompt | Interactive + Print |
| `--system-prompt-file` | **Replaces** with file contents | Print only |
| `--append-system-prompt` | **Appends** to default prompt | Interactive + Print |

---

## Interactive Mode

### Keyboard Shortcuts

| Shortcut | Description |
|----------|-------------|
| `Ctrl+C` | Cancel current input/generation |
| `Ctrl+D` | Exit Claude Code session |
| `Ctrl+L` | Clear terminal screen |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+R` | Reverse search command history |
| `Ctrl+V` / `Alt+V` | Paste image from clipboard |
| `Up/Down` | Navigate command history |
| `Esc` + `Esc` | Rewind code/conversation |
| `Tab` | Toggle extended thinking |
| `Shift+Tab` | Toggle permission modes |

### Quick Commands

| Shortcut | Description |
|----------|-------------|
| `#` at start | Add memory to CLAUDE.md |
| `/` at start | Slash command |
| `!` at start | Bash mode (run directly) |
| `@` | File path autocomplete |

### Multiline Input

| Method | Shortcut |
|--------|----------|
| Quick escape | `\` + `Enter` |
| macOS | `Option+Enter` |
| After `/terminal-setup` | `Shift+Enter` |
| Control sequence | `Ctrl+J` |

### Background Commands

Run commands in the background while continuing to work:
- Press `Ctrl+B` to background a running command
- Claude can retrieve output later with `BashOutput` tool
- Useful for dev servers, builds, test runners

---

## Resources

### Official Documentation
- [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)
- [CLI Reference](https://docs.anthropic.com/en/docs/claude-code/cli-reference)
- [Interactive Mode](https://docs.anthropic.com/en/docs/claude-code/interactive-mode)
- [Hooks Reference](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Skills Guide](https://www.anthropic.com/news/skills)
- [Plugins Guide](https://www.anthropic.com/news/claude-code-plugins)
- [Agent SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)

### GitHub Repositories
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)
