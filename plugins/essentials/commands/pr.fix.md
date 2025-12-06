---
description: Fix issues from PR review manifest
category: review
argument-hint: <pr_number>
allowed-tools: Bash(gh *), Read, Edit, Write, Grep, Glob
---

# PR Fix: $ARGUMENTS

## Instructions

1. Load manifest: Read `.claude/reviews/pr-$ARGUMENTS.yaml`
2. Verify branch: Ensure we're on the correct branch (`branch` field in manifest)
3. Process findings by severity: `BLOCKER` → `MAJOR` → `MINOR` (skip `NIT`)
4. For each finding:
   - Read the file and surrounding context
   - Apply the fix described
   - Mark finding as `fixed` in manifest
5. Update manifest with results
6. Summarize changes made

## Pre-flight Checks

```bash
# Verify we can push to this branch
git status
git remote -v

# Check we're on the right branch
git branch --show-current
```

If not on the correct branch or can't push, STOP and report.

## Processing Order

1. **BLOCKERs first** — These must be fixed
2. **MAJORs second** — Should be fixed
3. **MINORs third** — Fix if straightforward
4. **NITs** — Skip unless explicitly requested

Within each severity, **batch by file** to minimize read/write cycles.

## Confidence Levels

- **high**: Auto-apply without confirmation
- **medium**: Apply, but double-check the change makes sense
- **low**: Show proposed fix, ask before applying

## Fix Strategy

For each file with findings:

```
1. Read file once, note all finding locations
2. Apply fixes from bottom-to-top (preserves line numbers)
3. Verify fixes don't conflict with each other
4. Write file once
5. Update manifest for all findings in that file
```

## Constraints

- **Batch by file**: Group fixes per file, but keep commits logical
- **Minimal changes**: Fix only what's described, don't refactor
- **Preserve style**: Match existing code formatting
- **No new issues**: Don't introduce problems while fixing others

## After Fixing

Update the manifest:

```yaml
findings:
  - id: 1
    # ... other fields ...
    status: fixed
    fixed_at: 2025-01-15T11:00:00Z
    commit: abc1234
```

## Committing

Commit fixes with references to finding IDs:

```bash
git commit -m "fix(scope): description [PR-{number}#{finding_id}]"
```

Group related fixes into logical commits by file or feature.

## PR Handling

After committing, handle the PR:

```bash
# Check if PR exists for this branch
gh pr list --head $(git branch --show-current) --json number,url

# If PR exists: push updates
git push

# If no PR exists: create one
gh pr create --title "Fix review findings from PR #$ARGUMENTS" \
  --body "Addresses findings from review manifest."
```

## Resolve Inline Comments

After fixing each finding, resolve the corresponding inline PR comment:

```bash
# Get review comments on the PR
gh api repos/{owner}/{repo}/pulls/$ARGUMENTS/comments --jq '.[] | {id, path, line, body}'

# Find comments matching the finding's file:line
# Reply to the comment indicating it's fixed
gh api repos/{owner}/{repo}/pulls/$ARGUMENTS/comments/{comment_id}/replies \
  -f body="Fixed in \`{commit_sha}\`"
```

If the fix was part of a review thread, mark the conversation as resolved:

```bash
# Get the thread ID from the comment
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {threadId: "{thread_id}"}) {
      thread { isResolved }
    }
  }
'
```

## Re-review Loop

After fixes are pushed, suggest running `/pr-review $ARGUMENTS` again to verify:
- Previously flagged issues are resolved
- No new issues introduced by fixes

## Output

Summarize:
- Findings: X fixed, Y skipped (with reasons)
- Files modified
- Commits created
- PR status (updated existing / created new / push failed)
