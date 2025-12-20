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

Create the file with this content:

```markdown
# Claude Code Timeline

Cross-device session continuity for Claude Code.

## Current State

### Services

| Service | Port | Network | Status |
|---------|------|---------|--------|
| *Add running services here* | | | |

### Repositories

| Repo | Purpose | Location |
|------|---------|----------|
| *Add project repos here* | | |

### Secrets

| Secret | Location | Fields |
|--------|----------|--------|
| *Document secret locations* | | |

## TODOs

- [ ] *Add pending tasks here*

## Session Log

*New session entries are added below this line*

---
```

## After Creation

1. Confirm the file was created
2. Suggest updating the Current State section with actual values
3. Remind user to set `CLAUDE_TIMELINE_PATH` in their environment if not already persistent
