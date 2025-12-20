# Session Sync Plugin

Cross-device session continuity via Obsidian timeline. Aggressive accountability logging for decisions, commits, ideas, and blockers.

## Features

- **Inbox**: Async capture from any device (phone, tablet, Obsidian mobile)
- **Work Log**: Real-time micro-entries as things happen
- **Session Summaries**: End-of-session recaps
- **Cross-device**: Device tagging (Mac/Windows/Linux/Web)
- **MCP + Fallback**: Uses Obsidian MCP if available, falls back to filesystem

## Installation

```bash
/plugin install session-sync@cameronsjo
```

## Configuration

### Required Environment Variable

Set `CLAUDE_TIMELINE_PATH` to your timeline file location:

```bash
# In your shell profile (.zshrc, .bashrc, etc.)
export CLAUDE_TIMELINE_PATH="~/Documents/The Compendium/Claude Code Timeline.md"
```

Or in `.claude/settings.local.json` for per-project:

```json
{
  "env": {
    "CLAUDE_TIMELINE_PATH": "~/Documents/The Compendium/Claude Code Timeline.md"
  }
}
```

### Optional Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_CONTEXT_DIR` | Additional context directory to read on start |
| `OBSIDIAN_VAULT` | Obsidian vault root (for MCP server) |

### Hook Configuration

Add these hooks to `~/.claude/settings.json` for automatic behavior:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/cameronsjo/session-sync/*/hooks/session-start.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/cameronsjo/session-sync/*/hooks/session-end.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash(git commit:*)",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/plugins/cache/cameronsjo/session-sync/*/hooks/post-commit.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/session.init` | Create a new timeline file |
| `/session.sync` | Update timeline with session summary |
| `/session.log <type> <message>` | Quick work log entry |

### Log Types

```bash
/session.log decision Using Redis - better pub/sub
/session.log commit feat: add auth (abc123)
/session.log blocker OAuth not redirecting
/session.log resolved OAuth needed callback URL
/session.log idea Could use webhooks
/session.log state Prometheus on :9090
```

## Timeline Structure

```markdown
# Claude Code Timeline

## Inbox
> Add items from any device. Claude addresses these at session start.
- [ ] Task from phone

## Current State
### Services
| Service | Port | Status |
|---------|------|--------|

## Work Log
### 2025-12-19
- 23:15 **Decision**: Using Traefik - better Docker integration
- 23:30 **Commit**: feat: add prometheus (abc123)

## Session Log
### 2025-12-19 23:00 CST (Mac)
**Session:** Added monitoring stack
...
```

## Workflow

1. **Session Start**: Timeline is read, inbox items surfaced
2. **During Session**: Log decisions, commits, blockers as they happen
3. **Session End**: Run `/session.sync` for summary

## Philosophy

**Log early, log often.** Don't wait for session end. The user may forget, the session may crash, context may compact. The timeline is the source of truth.
