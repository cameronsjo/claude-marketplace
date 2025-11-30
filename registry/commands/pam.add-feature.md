---
description: Add feature to project progress tracker
category: pam
argument-hint: <feature_name>
allowed-tools: Read, Edit, Bash(git *)
---

# Add Feature: $ARGUMENTS

## Purpose

Add a new feature to an existing project's progress tracker. Use this when:
- Scope expands during implementation
- You discover new requirements
- Breaking a large feature into smaller pieces

## Instructions

### 1. Load Current Progress

```bash
cat .claude/progress.yaml
```

### 2. Gather Feature Details

If only a name was provided, determine:
- **Description**: What does this feature do?
- **Acceptance Criteria**: How do we know it's done?
- **Dependencies**: Does it depend on other features?

### 3. Add to Progress File

Find the highest feature ID and add the new feature:

```yaml
features:
  # ... existing features ...

  - id: <next_id>
    name: $ARGUMENTS
    description: |
      <description>
    status: pending
    acceptance_criteria:
      - <criterion 1>
      - <criterion 2>
    dependencies: []  # or [<id>, <id>]
    notes: "Added during session <N>"
```

### 4. Commit the Addition

```bash
git add .claude/progress.yaml
git commit -m "chore: add feature #<id> - $ARGUMENTS

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 5. Confirm

```
## Feature Added

**#<id>**: $ARGUMENTS

**Acceptance Criteria**:
- <criterion 1>
- <criterion 2>

**Dependencies**: <list or "None">

This feature is now queued. Run `/continue <id>` to work on it specifically,
or `/continue` to work on the next available feature.
```

## Constraints

- Don't start implementing the feature - just add it to the tracker
- Ensure acceptance criteria are specific and testable
- Note dependencies accurately to maintain correct ordering
