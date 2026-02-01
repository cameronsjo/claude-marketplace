---
description: Add end-of-session summary to the work log
allowed-tools: Read, Edit, mcp__obsidian-mcp-server__obsidian_read_note, mcp__obsidian-mcp-server__obsidian_update_note
---

# Session Sync

Add a brief end-of-session summary line to the Work Log.

## Requirements

- `CLAUDE_TIMELINE_PATH` environment variable must be set

## Process

1. Read timeline from `$CLAUDE_TIMELINE_PATH`
2. Summarize what was accomplished this session (1-2 sentences)
3. Add entry: `- HH:MM **Session**: summary`
4. Review any Inbox items and address or acknowledge them

## Example

```markdown
- 21:30 **Session**: Refactored auth module, fixed 3 bugs, PR ready for review
```

## MCP Preferred

Use `mcp__obsidian-mcp-server__*` if available, fall back to Read/Edit.
