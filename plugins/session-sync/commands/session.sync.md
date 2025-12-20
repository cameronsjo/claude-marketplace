---
description: Update the session timeline with current session summary
allowed-tools: Read, Edit, Write, mcp__obsidian-mcp-server__obsidian_read_note, mcp__obsidian-mcp-server__obsidian_update_note
---

# Session Sync

Update the session timeline with a summary of this session.

## Requirements

- `CLAUDE_TIMELINE_PATH` environment variable must be set
- Timeline file must exist (run `/session.init` if not)

## Process

1. Read the current timeline from `$CLAUDE_TIMELINE_PATH`
2. Summarize what was accomplished this session
3. Identify any repos that were modified
4. Note any state changes (services, configs, secrets)
5. List any pending TODOs or blockers for next session
6. Add a new session entry to the Session Log section

## Entry Format

Use this format for new entries (insert after "## Session Log"):

```markdown
### {DATE} {TIME} {TIMEZONE} ({DEVICE})

**Session:** Brief description of what was accomplished

**Changes:**
- Change 1 with details
- Change 2 with details

**Repos touched:**
- repo-name - what changed

**State after:** Key state changes

**Next steps:**
- [ ] TODO 1
- [ ] TODO 2

---
```

## Device Detection

- Mac: macOS
- Windows: Windows/WSL
- Web: Claude Code on web
- Linux: Native Linux

## Reading/Writing

**Prefer MCP if available:**
- Read: `mcp__obsidian-mcp-server__obsidian_read_note`
- Write: `mcp__obsidian-mcp-server__obsidian_update_note`

**Fallback to filesystem:**
- Read: `Read` tool
- Write: `Edit` tool

## After Updating

Confirm the update was successful and show a summary of what was logged.
