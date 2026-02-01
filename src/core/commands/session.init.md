---
description: Initialize a new session timeline file
allowed-tools: Read, Write, mcp__obsidian-mcp-server__obsidian_update_note
---

# Initialize Session Timeline

Create a new session timeline file for cross-device session continuity.

## Requirements

- `CLAUDE_TIMELINE_PATH` environment variable must be set

## Process

1. Check if `$CLAUDE_TIMELINE_PATH` is set
2. Check if file already exists (warn if so, don't overwrite without confirmation)
3. Create the timeline file with initial template

## Template

```markdown
# Claude Code Timeline

## Inbox

> Async capture from any device. Claude reviews at session start.

## Work Log

### *Date*

- *HH:MM* **Type**: *message*
```

## After Creation

Confirm the file was created and remind user to set `CLAUDE_TIMELINE_PATH` in their environment if not already persistent.
