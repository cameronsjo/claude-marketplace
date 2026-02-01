---
description: Quick micro-entry to the work log (decision, commit, blocker, idea, etc.)
argument-hint: "<type> <message>"
allowed-tools: Read, Edit, mcp__obsidian-mcp-server__obsidian_read_note, mcp__obsidian-mcp-server__obsidian_update_note
---

# Quick Work Log Entry

Add a single micro-entry to the Work Log section of the timeline.

## Usage

```
/session.log decision Using Redis for caching - better pub/sub support
/session.log commit feat: add user auth (abc1234)
/session.log blocker OAuth redirect not working
/session.log resolved OAuth needed explicit callback URL
/session.log idea Could use webhooks instead of polling
/session.log state Prometheus now running on :9090
```

## Entry Types

| Type | Use For |
|------|---------|
| `decision` | Architecture/tech choices with reasoning |
| `commit` | Git commits (include message + short SHA) |
| `blocker` | Something blocking progress |
| `resolved` | A blocker that was fixed |
| `idea` | Insights, future improvements |
| `state` | System state changes |
| `config` | Configuration changes |

## Format

Entries are added to the Work Log section under today's date:

```markdown
## Work Log

### 2025-12-19

- 23:15 **Decision**: Using Redis for caching - better pub/sub support
- 23:30 **Commit**: feat: add user auth (abc1234)
```

## Process

1. Read timeline from `$CLAUDE_TIMELINE_PATH`
2. Find or create today's date section under `## Work Log`
3. Append the new entry with current time
4. Write back to timeline

## If No Arguments

If called without arguments, prompt for:
1. Entry type (decision, commit, blocker, etc.)
2. Message content
