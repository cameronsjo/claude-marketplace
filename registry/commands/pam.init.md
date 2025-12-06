---
description: Initialize project for multi-session agent work with progress tracking
argument-hint: [goal_or_issue_url]
allowed-tools: Bash(gh *), Bash(git *), Read, Write, Glob, Grep
disable-model-invocation: true
---

# Initialize Project: $ARGUMENTS

## Purpose

Set up a new project for multi-session agent work. This creates the scaffolding that allows future sessions to pick up where previous sessions left off.

Based on Anthropic's research on effective harnesses for long-running agents.

## Instructions

### 1. Understand the Goal

If `$ARGUMENTS` is provided:
- If it's a GitHub issue URL: fetch with `gh issue view`
- If it's text: use as the project goal
- If empty: ask the user for the project goal

### 2. Analyze the Codebase

```bash
# Check if this is a new or existing project
ls -la
git status 2>/dev/null || echo "Not a git repo"

# If existing, understand structure
find . -type f -name "*.md" | head -20
```

### 3. Create Feature List

Break down the goal into discrete, testable features. Each feature should be:
- **Atomic**: Can be completed in one session
- **Testable**: Has clear success criteria
- **Independent**: Minimal dependencies on other features (when possible)

### 4. Create Progress File

Write `.claude/progress.yaml`:

```yaml
# Claude Agent Progress Tracker
# This file maintains state across agent sessions
# See: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

project:
  name: <project_name>
  goal: |
    <one paragraph description of the overall goal>
  created_at: <ISO timestamp>
  source: <issue URL or "user request">

features:
  - id: 1
    name: <feature_name>
    description: |
      <what this feature does>
    status: pending  # pending | in_progress | completed | blocked
    acceptance_criteria:
      - <criterion 1>
      - <criterion 2>
    dependencies: []  # list of feature IDs this depends on
    notes: ""

  - id: 2
    name: <next_feature>
    # ... etc

sessions:
  - session_id: 1
    started_at: <ISO timestamp>
    type: initializer
    summary: |
      Set up project structure and progress tracking.
    features_touched: []
    commits: []

decisions:
  # Architectural decisions made during implementation
  - date: <ISO date>
    decision: |
      <what was decided>
    rationale: |
      <why>

blockers:
  # Issues that need human intervention
  []
```

### 5. Create Init Script (if applicable)

If the project needs setup (dependencies, env, etc.), create `init.sh`:

```bash
#!/bin/bash
# Project initialization script
# Run this to set up the development environment

set -e

echo "Setting up project..."

# Install dependencies
# npm install / pip install -r requirements.txt / etc.

# Set up environment
# cp .env.example .env (if needed)

# Run initial build/check
# npm run build / make / etc.

echo "Setup complete!"
```

Make executable: `chmod +x init.sh`

### 6. Git Setup

```bash
# Initialize git if needed
git init 2>/dev/null || true

# Create .gitignore if missing
if [ ! -f .gitignore ]; then
  echo "Creating .gitignore..."
fi

# Ensure .claude/ is tracked (progress file should be in version control)
# But exclude any sensitive files

# Initial commit
git add .
git commit -m "feat: initialize project with agent progress tracking

- Add .claude/progress.yaml for multi-session memory
- Set up feature list with acceptance criteria
- Create init.sh for environment setup

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 7. Output Summary

After setup, display:

```
## Project Initialized

**Goal**: <goal summary>

**Features** (X total):
1. [ ] Feature 1 - <brief description>
2. [ ] Feature 2 - <brief description>
...

**Next Steps**:
- Run `/continue` in your next session to start implementing
- Each session will pick ONE feature and complete it
- Progress is tracked in `.claude/progress.yaml`

**Files Created**:
- .claude/progress.yaml - Progress tracker
- init.sh - Setup script (if applicable)
```

## Constraints

- **One-time setup**: This command should only be run once per project
- **Don't implement**: This command sets up the project, it doesn't build features
- **Atomic features**: Each feature should be completable in a single session
- **Clear criteria**: Every feature needs testable acceptance criteria
