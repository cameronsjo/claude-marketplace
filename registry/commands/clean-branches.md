---
description: Clean up merged and stale git branches
category: utilities-debugging
argument-hint: "[--dry-run] [--remote] [--stale-days N] [--force]"
allowed-tools: Bash
---

# Clean Branches Command

Clean up merged and stale git branches safely with automated detection and protection.

## Instructions

Execute the claude-clean-branches CLI tool. Since Claude doesn't handle interactive prompts, use this workflow:

**Step 1: Check if installed**
```bash
which claude-clean-branches || echo "NOT_INSTALLED"
```

If NOT_INSTALLED, show:
```
Error: claude-clean-branches CLI not found

Install with:
  cd ~/.claude/cli/claude-clean-branches
  uv pip install --system -e .

Then re-run: /clean-branches
```

**Step 2: Show what would be deleted (dry-run)**
```bash
claude-clean-branches --dry-run $ARGUMENTS
```

**Step 3: Ask user for confirmation**

Display the dry-run output, then ask:
```
The above branches will be deleted. Proceed? [yes/no]
```

**Step 4: If user confirms, execute with --force**
```bash
claude-clean-branches --force $ARGUMENTS
```

The --force flag skips interactive prompts in the CLI since Claude can't handle them.

## What claude-clean-branches Does

The CLI tool performs the following:

### Step 1: Pre-flight Checks
- Verifies you're in a git repository
- Warns about uncommitted changes
- Auto-detects main branch (main or master)

### Step 2: Repository Update
- Switches to main branch
- Pulls latest changes
- Ensures clean working state

### Step 3: Branch Identification
Finds two types of branches:

**Merged Branches (Safe to Delete):**
- Branches that have been merged into main
- No risk of losing code
- Marked with ✓ in green

**Stale Branches (No Recent Activity):**
- Branches with no commits in N days (default: 30)
- Might have unmerged work
- Marked with ⚠️ in yellow

**Protected Branches (Never Deleted):**
- main, master, develop, development
- staging, production, qa

### Step 4: Display Summary
Shows beautiful tables with:
- All merged branches
- All stale branches
- Total count

### Step 5: Confirmation
- Prompts for confirmation before deletion
- Unless `--force` flag is used
- Separate confirmation for remote branches

### Step 6: Local Branch Cleanup
- Deletes merged branches with `git branch -d`
- Force deletes stale branches with `git branch -D` (if needed)
- Shows progress for each deletion

### Step 7: Remote Cleanup (Optional)
If `--remote` flag provided:
- Lists merged remote branches
- Prompts for confirmation
- Deletes remote branches with `git push origin --delete`
- Prunes stale remote tracking references

### Step 8: Summary
Displays final count of deleted branches.

## Options

- `--stale-days N` / `-s N` - Consider branches stale if no commits in N days (default: 30)
- `--dry-run` / `-d` - Show what would be deleted without deleting
- `--remote` / `-r` - Also clean up remote branches (use with caution)
- `--force` / `-f` - Skip confirmation prompts (use with caution)

## Installation

The `claude-clean-branches` CLI tool must be installed first. If not installed:

```bash
cd ~/.claude/cli/claude-clean-branches
uv pip install -e .
```

Or install globally:

```bash
uv tool install ~/.claude/cli/claude-clean-branches
```

## Safety Features

- ✅ **Protected branches**: Never deletes main, master, develop, staging, production, qa
- ✅ **Uncommitted changes warning**: Warns before proceeding
- ✅ **Main branch checkout**: Switches to main before cleanup
- ✅ **Latest changes**: Pulls latest before analysis
- ✅ **Confirmation prompts**: Asks before deletion (unless --force)
- ✅ **Dry run mode**: Preview without deletion
- ✅ **Separate remote confirmation**: Extra prompt for remote deletion
- ✅ **Force delete fallback**: Handles unmerged changes with warning

## Example Workflows

**Safe workflow (recommended):**
```bash
# 1. Preview what would be deleted
/clean-branches --dry-run

# 2. Clean up local branches
/clean-branches

# 3. Clean up remote branches (if needed)
/clean-branches --remote
```

**Quick cleanup:**
```bash
/clean-branches --force
```

**Custom stale threshold:**
```bash
/clean-branches --stale-days 90
```

**Aggressive cleanup (use with caution):**
```bash
/clean-branches --remote --force --stale-days 14
```

## Example Output

```
🔍 Analyzing repository...
✓ Main branch: main
Pulling latest changes...
✓ Repository up-to-date

📋 Identifying branches...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Merged Branches (Safe to Delete)   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
✓ feature/user-authentication
✓ bugfix/login-error
✓ refactor/api-cleanup

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Stale Branches (No activity in 30 days)     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
⚠️  feature/old-experiment
⚠️  wip/prototype

Total branches to delete: 5

Proceed with deletion? [y/N]: y

🗑️  Cleaning up local branches...
✓ Deleted: feature/user-authentication
✓ Deleted: bugfix/login-error
✓ Deleted: refactor/api-cleanup
✓ Deleted: feature/old-experiment
⚠️  Force deleted: wip/prototype (had unmerged changes)

╭─────────────────────────────────────╮
│ ✓ Cleanup complete!                 │
│                                     │
│ Local branches deleted: 5           │
╰─────────────────────────────────────╯
```

## Error Handling

- If not in git repository: Exits with error
- If cannot determine main branch: Exits with error
- If branch deletion fails: Shows error, continues with others
- If remote deletion fails: Shows error, continues with others
- All errors include clear context

## Recovery

If you accidentally delete a branch, recover it using reflog:

```bash
# Find the commit hash
git reflog --no-merges --since="2 weeks ago"

# Recreate the branch
git checkout -b recovered-branch <commit-hash>
```

## Why a CLI Tool?

This command uses a separate CLI tool (`claude-clean-branches`) instead of implementing logic directly because:

1. **Performance**: No token cost, runs in <1 second
2. **Reliability**: Deterministic git operations, tested
3. **Maintainability**: Easy to test, debug, and enhance
4. **Safety**: Consistent behavior with proper error handling
5. **Reusability**: Can be used outside Claude Code

This follows the pattern established by GitHub's Spec Kit and claude-ready.

---

**Last Updated:** 2025-11-18
**Version:** 2.0 - Built on claude-clean-branches CLI
**CLI Tool:** ~/.claude/cli/claude-clean-branches
