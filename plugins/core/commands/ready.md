---
description: Commit changes logically, push, and create/update PR with automated review trigger
category: version-control-git
argument-hint: "[--open] [--draft] [--fix-markdown] [--skip-markdown] [--skip-untracked] [--protected-branches=...]"
allowed-tools: Bash
---

# Claude Command: Ready

Automates the complete workflow from committing changes to triggering automated PR reviews.

## Instructions

Execute the claude-ready CLI tool with the provided arguments.

**Step 1: Check if installed**
```bash
which claude-ready || echo "NOT_INSTALLED"
```

If NOT_INSTALLED, show:
```
Error: claude-ready CLI not found

Install with:
  cd ~/.claude/cli/claude-ready
  uv pip install --system -e .

Then re-run: /ready
```

**Step 2: Execute**
```bash
claude-ready $ARGUMENTS
```

The tool runs without interactive prompts - it will automatically create commits, push, and manage PRs.

## Command-Line Options

- `--open`, `-o`: Open PR in browser after creation/update
- `--draft`, `-d`: Create PR as draft (allows work-in-progress PRs)
- `--fix-markdown`: Auto-fix markdown formatting issues before checking
- `--skip-markdown`: Skip markdown linting check entirely
- `--skip-untracked`: Skip untracked files check
- `--skip-temporal-docs`: Skip temporal/point-in-time documentation check
- `--protected-branches=<list>`: Comma-separated list of protected branches (default: `main,master`)

**Examples:**
```bash
# Standard workflow
/ready

# Create draft PR and open in browser
/ready --draft --open

# Auto-fix markdown and skip untracked files check
/ready --fix-markdown --skip-untracked

# Skip temporal docs check (when you know the docs are intentional)
/ready --skip-temporal-docs

# Custom protected branches
/ready --protected-branches="main,master,develop,staging"
```

## What claude-ready Does

The CLI tool performs the following:

### Step 0: Pre-flight Checks
- Fetch latest changes from remote
- Verify local branch is up-to-date (blocks if remote is ahead)
- Verify GitHub CLI authentication

### Step 1: Pre-Commit Quality Checks
**CRITICAL**: Blocks commit if ANY issue found:

- **Orphaned TODOs/FIXMEs**: All code markers MUST reference GitHub issues
  - ❌ `// TODO: implement caching`
  - ✅ `// TODO(#123): implement caching`
- **Debug Statements**: Blocks `console.log`, `print()`, `debugger`
- **Commented Code**: Blocks large (>3 lines) blocks of commented code
- **Merge Conflicts**: Blocks unresolved merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- **Large Files**: Warns about files >10MB being committed
  - Suggests Git LFS, compression, or external storage
- **Markdown Lint**: Validates markdown formatting in modified .md files
  - Checks if installed locally first, falls back to `npx markdownlint-cli2`
  - Searches for config: `.markdownlint-cli2.jsonc`, `.markdownlint.json`, `.markdownlintrc`
  - Use `--fix-markdown` to auto-fix issues
  - Use `--skip-markdown` to skip this check
- **Broken Links**: Checks for broken internal links in markdown files
  - Validates relative links to other files in the repo
  - Only checks modified markdown files
- **Untracked Files**: Warns about untracked files that might need to be committed
  - Checks for test files, configs, dependencies in committed directories
  - Smart filtering excludes `.example`, `.sample`, `.bak`, etc.
  - Use `--skip-untracked` to skip this check
- **Temporal Documentation**: Checks for point-in-time docs that may not belong in PR
  - Blocks obvious temporary files (WIP, DRAFT, TEMP, scratch, debug-log)
  - Warns about date-prefixed files, investigation logs, session notes
  - Suggests moving valuable docs to proper location (`docs/`)
  - Use `--skip-temporal-docs` to skip this check

### Step 2: Create Logical Commits
- Analyzes all changes (staged and unstaged)
- Creates commits with conventional commit format
- Each commit gets a clear type and description

### Step 3: Push Commits
- Pushes all commits to remote
- Sets upstream branch if needed

### Step 4: Check Branch and PR Status
- Checks if on protected branch (default: `main`, `master`)
  - Use `--protected-branches` to customize
  - Exits gracefully with informative message for protected branches
- Checks for existing open PR on current branch
- Handles PR creation failures with clear error messages and actionable guidance

### Step 5: Create or Update PR
**If NO open PR exists:**
- Creates new PR with title and description
- Title follows conventional commit format
- Can create as draft with `--draft` flag
- Automated `/review` triggered on creation

**If open PR exists:**
- Validates PR title (conventional commit format)
- Updates title if generic or invalid
- Checks for recent `/review` comments (deduplication)
- Adds `/review` comment if not recently added
- Updates or creates persistent summary comment

### Step 6: Display Summary
Shows comprehensive summary with:
- Branch name
- Commits created with SHAs
- PR number and URL
- Beautiful terminal formatting

### Step 7: Browser Action (Optional)
- Opens PR in browser if `--open` flag provided

## Installation

The `claude-ready` CLI tool must be installed first. If not installed:

```bash
cd ~/.claude/cli/claude-ready
uv pip install -e .
```

Or install globally:

```bash
uv tool install ~/.claude/cli/claude-ready
```

## Important Notes

- **Atomic commits**: Each commit contains related changes with single purpose
- **Conventional commit format**: Always uses format without emoji
- **Present tense, imperative mood**: "add feature" not "added feature"
- **PR title validation**: Validates and updates generic/invalid titles
- **Review deduplication**: Only adds `/review` if not recently added (past 5 minutes)
- **Persistent PR summary**: Single comment updated on subsequent runs
- **Minimize PR noise**: Updates existing comments instead of creating new ones
- **GitHub CLI required**: Must have `gh` CLI installed and authenticated
- **Quality checks are BLOCKING**: Will not proceed if issues found

## Quality Check Details

### Orphaned Code Markers
Markers that require issue references:
- `TODO`, `FIXME`, `HACK`, `XXX`, `REFACTOR`, `BUG`, `OPTIMIZE`

Format: `// TODO(#123): description` or `# TODO(#123): description`

See CLAUDE.md - "Code Markers (STRICT)" section for complete policy.

### Debug Statements
Blocked statements:
- `console.log()`, `console.debug()` (unless in logger context)
- `print()` statements (use structured logging instead)
- `debugger` statements

### Commented Code
Blocks: >3 consecutive lines of commented-out code

Rationale: We have git history for this purpose.

## Error Handling

- If `claude-ready` not installed: Shows installation instructions
- If git commands fail: Reports error and stops
- If gh commands fail: Reports error with guidance
- If quality checks fail: Shows all issues and required actions
- If remote branch ahead: Instructs to pull first
- All errors include clear context and actionable steps

## Example Output

```
🔍 Running pre-flight checks...
✓ Pre-flight checks passed

🔍 Running pre-commit quality checks...
✓ Pre-commit quality checks passed

📝 Analyzing changes and creating commits...
✓ Creating commit [1/2]: feat: add user profile page
  └─ SHA: a1b2c3d
✓ Creating commit [2/2]: test: add profile upload tests
  └─ SHA: e4f5g6h

📤 Pushing commits to remote...
✓ Successfully pushed 2 commit(s)

🔎 Checking branch and PR status...
✓ On branch: feature/user-profiles
✓ Found existing PR #42

📋 Updating existing pull request #42...
🔍 Validating PR title...
✓ PR title is valid: feat: add user profile page
✓ Added /review comment to trigger automated review
♻️ Updating persistent summary comment...
✓ Updated persistent summary comment

╭─────────────────── 📊 READY SUMMARY ───────────────────╮
│ Branch: feature/user-profiles                          │
│                                                        │
│ Commits Created: 2                                     │
│ ├─ a1b2c3d feat: add user profile page                │
│ └─ e4f5g6h test: add profile upload tests             │
│                                                        │
│ Pull Request: #42                                      │
│ └─ https://github.com/user/repo/pull/42               │
╰────────────────────────────────────────────────────────╯

You can view the PR at: https://github.com/user/repo/pull/42
```

## Why a CLI Tool?

This command uses a separate CLI tool (`claude-ready`) instead of implementing logic directly because:

1. **Performance**: No token cost, runs in <1 second
2. **Reliability**: Deterministic, tested, consistent behavior
3. **Maintainability**: Easier to test, debug, and enhance
4. **Reusability**: Can be used outside Claude Code

This follows the pattern established by GitHub's Spec Kit (`specify` CLI).

---

**Last Updated:** 2025-11-18
**Version:** 2.0 - Built on claude-ready CLI
**CLI Tool:** ~/.claude/cli/claude-ready
