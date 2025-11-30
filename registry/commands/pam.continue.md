---
description: Continue multi-session project - pick one feature, implement, commit
category: pam
argument-hint: [feature_id]
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep, TodoWrite
---

# Continue Project Work

## Purpose

Make incremental progress on a multi-session project. This command implements the "coding agent" pattern from Anthropic's research on long-running agents.

**Core principle**: One feature per session. Complete it fully before stopping.

## Instructions

### 1. Load Context

```bash
# Read progress file
cat .claude/progress.yaml

# Check git history for recent work
git log --oneline -10

# See what changed recently
git diff HEAD~3..HEAD --stat 2>/dev/null || git log --oneline -3
```

Parse the progress file to understand:
- Project goal
- Which features are completed
- Which features are in progress (shouldn't be any - indicates interrupted session)
- Which features are pending
- Any blockers or decisions

### 2. Select Feature

If `$ARGUMENTS` specifies a feature ID, use that.

Otherwise, select the next feature to work on:
1. **First**: Any feature marked `in_progress` (recover from interrupted session)
2. **Then**: First `pending` feature with all dependencies satisfied
3. **Consider**: Feature priority and logical ordering

**Announce your selection**:
```
## Selected Feature: #<id> - <name>

**Description**: <description>

**Acceptance Criteria**:
- [ ] <criterion 1>
- [ ] <criterion 2>

**Dependencies**: <list or "None">
```

### 3. Update Progress File

Mark the selected feature as `in_progress`:

```yaml
features:
  - id: <selected_id>
    status: in_progress
    started_at: <ISO timestamp>
```

Commit this status change:
```bash
git add .claude/progress.yaml
git commit -m "chore: start work on feature #<id> - <name>

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 4. Implement Feature

Work through the feature systematically:

1. **Understand**: Read relevant existing code
2. **Plan**: Break into small steps (use TodoWrite)
3. **Implement**: Write the code
4. **Test**: Verify acceptance criteria are met
5. **Clean up**: Remove debug code, ensure style consistency

**Important**:
- Make atomic commits as you go (don't batch everything at the end)
- If you hit a blocker, document it and mark the feature as `blocked`
- If scope creep appears, note it as a new feature instead of expanding current work

### 5. Verify Completion

Before marking complete, verify ALL acceptance criteria:

```
## Verification: Feature #<id>

- [x] <criterion 1> - <how verified>
- [x] <criterion 2> - <how verified>
...

All criteria met: YES/NO
```

If any criterion fails, continue working or document the blocker.

### 6. Update Progress File

Mark feature as completed and log the session:

```yaml
features:
  - id: <id>
    status: completed
    completed_at: <ISO timestamp>
    notes: |
      <brief notes on implementation approach or gotchas>

sessions:
  - session_id: <next_id>
    started_at: <timestamp>
    ended_at: <timestamp>
    type: coding
    summary: |
      Implemented feature #<id> - <name>.
      <1-2 sentences on what was done>
    features_touched:
      - <id>
    commits:
      - <sha1>
      - <sha2>
```

Add any architectural decisions made:

```yaml
decisions:
  - date: <ISO date>
    feature: <id>
    decision: |
      <what was decided>
    rationale: |
      <why this approach>
```

### 7. Final Commit

```bash
git add .claude/progress.yaml
git commit -m "feat: complete feature #<id> - <name>

<brief description of what was implemented>

Acceptance criteria:
- <criterion 1>: verified
- <criterion 2>: verified

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 8. Session Summary

Output a summary for the human:

```
## Session Complete

**Feature Completed**: #<id> - <name>

**Changes**:
- <file1>: <what changed>
- <file2>: <what changed>

**Commits**:
- <sha1> - <message>
- <sha2> - <message>

**Progress**: <completed>/<total> features done

**Next Feature**: #<next_id> - <name>
(Run `/continue` in next session)

**Blockers**: <any blockers or "None">
```

## Handling Edge Cases

### Interrupted Session (feature still `in_progress`)
- Resume where you left off
- Check git status for uncommitted changes
- Review the feature's notes for context

### Blocked Feature
- Document the blocker clearly in progress file
- Mark as `blocked` with explanation
- Move to next available feature
- Alert the user about the blocker

### All Features Complete
```
## Project Complete!

All <N> features have been implemented.

**Summary**:
- Features: <N> completed
- Sessions: <M> total
- Decisions: <K> documented

Consider:
- Running final tests/build
- Creating release/PR
- Archiving progress file
```

### No Progress File Found
```
No .claude/progress.yaml found.

Run `/init-project <goal>` first to set up the project.
```

## Constraints

- **ONE feature per session**: Do not start a second feature
- **Complete fully**: Don't leave features half-done
- **Commit often**: Small, atomic commits with clear messages
- **Document decisions**: Future sessions need context
- **No scope creep**: New ideas become new features, not expansions
