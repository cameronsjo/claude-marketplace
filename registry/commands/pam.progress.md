---
description: Show project progress - features, blockers, next steps
category: pam
allowed-tools: Bash(cat *), Bash(git *), Read
---

# Project Progress

## Purpose

Quick status check for multi-session projects. Shows what's done, what's next, and any blockers.

## Instructions

### 1. Load and Display Progress

```bash
# Check if progress file exists
if [ ! -f .claude/progress.yaml ]; then
  echo "No progress file found. Run /init-project first."
  exit 1
fi

cat .claude/progress.yaml
```

### 2. Generate Summary

Parse the progress file and display:

```
## Project: <name>

**Goal**: <goal summary>

### Features Progress

| # | Feature | Status | Notes |
|---|---------|--------|-------|
| 1 | <name>  | ✅ completed | <notes> |
| 2 | <name>  | 🔄 in_progress | <notes> |
| 3 | <name>  | ⏳ pending | - |
| 4 | <name>  | 🚫 blocked | <blocker> |

**Progress**: <completed>/<total> (<percentage>%)

### Recent Activity

<Last 3 sessions from sessions log>

### Blockers

<List any blocked features with their blockers, or "None">

### Decisions Made

<List key decisions, or "None yet">

### Next Up

**Feature #<id>**: <name>
<description>

Run `/continue` to start working on it.
```

### 3. Git Context

Also show recent git activity:

```bash
# Recent commits
git log --oneline -5

# Any uncommitted changes
git status --short
```

## Output Format

Keep it scannable:
- Use tables for feature lists
- Use emoji for status (✅ 🔄 ⏳ 🚫)
- Highlight blockers prominently
- Show clear next action
