---
description: PR review from multiple perspectives (PM, Dev, QA, Security)
category: review
argument-hint: [pr_link_or_number]
allowed-tools: Bash(gh *), Read, Write, Grep, Glob
---

# PR Review: $ARGUMENTS

## Prerequisites

**Check if labels exist** before proceeding:

```bash
gh label list | grep -E "(claude-pm-|claude-dev-|claude-qa-|claude-sec-|claude-quality-)" | wc -l
```

If count < 10, inform user and exit:
```
⚠️ PR review labels not found. Run: /setup-labels
```

## Determine PR to Review

**If $ARGUMENTS empty**: Auto-detect from current branch:
```bash
gh pr view --json number,title,url
```

**If no PR found**, inform user and exit.

## Execution Strategy

1. Fetch PR metadata and diff
2. Read all changed files for context
3. Post 5 perspective comments with persistent markers
4. Apply labels based on review outcomes
5. Write manifest for `/pr-fix` integration
6. Show terminal summary

**Comment Markers** (check if exists, update if yes, create if no):
- `<!-- PR-REVIEW:PM -->` - Product Manager
- `<!-- PR-REVIEW:DEV -->` - Developer
- `<!-- PR-REVIEW:QA -->` - Quality Engineer
- `<!-- PR-REVIEW:SEC -->` - Security Engineer
- `<!-- PR-REVIEW:QUALITY -->` - Code Quality Gate

---

## Constraints

- **Diff-only**: Only flag issues in *changed* lines. Ignore pre-existing problems.
- **Deep review**: Analyze thoroughly regardless of PR size.
- **Report, don't fix**: Report issues; don't push fixes.

## Finding Format

```
- **[SEVERITY]** `file:line` — Problem
  - Why: Impact in one sentence
  - Fix: Solution in one sentence
```

Severities: `BLOCKER` | `MAJOR` | `MINOR` | `NIT`

---

## 1. Product Manager Review

**Marker**: `<!-- PR-REVIEW:PM -->`

Evaluate:
- Business value — does this advance product goals?
- User experience — intuitive, no UX regressions?
- Strategic alignment — fits current direction?

```markdown
<!-- PR-REVIEW:PM -->
## 📊 Product Manager Review
**Status**: ✅ Approved | ⚠️ Changes Requested

### ⚠️ Concerns
| File | Impact | Issue |
|------|--------|-------|
| `file.ts:123` | High | Issue description |

### 💡 Recommendations
- **P1**: Critical recommendation
- **P2**: Important recommendation
```

---

## 2. Developer Review

**Marker**: `<!-- PR-REVIEW:DEV -->`

Evaluate:
- Code quality, readability, maintainability
- Performance (N+1, unbounded loops, missing indexes)
- Standards violations, architectural issues

```markdown
<!-- PR-REVIEW:DEV -->
## 👨‍💻 Developer Review
**Status**: ✅ Approved | ⚠️ Changes Requested

### ⚠️ Issues
| File:Line | Severity | Issue |
|-----------|----------|-------|
| `auth.ts:45` | High | N+1 query - use batch loading |

### 📋 Standards Violations
- `api.ts:67` - CLAUDE.md: Use structured logging
```

---

## 3. Quality Engineer Review

**Marker**: `<!-- PR-REVIEW:QA -->`

Evaluate:
- Missing test coverage for changes
- Unhandled edge cases or error paths
- Regression risks to existing behavior

```markdown
<!-- PR-REVIEW:QA -->
## 🧪 Quality Engineer Review
**Status**: ✅ Approved | ⚠️ Changes Requested

### ⚠️ Missing Tests
| Function/Feature | File | Risk |
|------------------|------|------|
| `authenticateUser()` | `auth.ts:45` | High - critical auth flow |

### 🐛 Edge Cases Not Handled
- `api.ts:67` - Missing null check
```

---

## 4. Security Engineer Review

**Marker**: `<!-- PR-REVIEW:SEC -->`

Evaluate:
- Input validation (injection, XSS, SSRF)
- Auth/authz gaps
- Secrets or sensitive data exposure
- Dependency vulnerabilities, OWASP Top 10

```markdown
<!-- PR-REVIEW:SEC -->
## 🔒 Security Engineer Review
**Status**: ✅ Approved | ❌ Blocked

### 🚨 Critical Vulnerabilities
| File:Line | Vulnerability | Severity |
|-----------|--------------|----------|
| `api.ts:45` | SQL injection | Critical |

### 📦 Dependency Issues
- `package.json` - `lodash@4.17.15` CVE-2020-8203
```

---

## 5. Code Quality Gate (BLOCKING)

**Marker**: `<!-- PR-REVIEW:QUALITY -->`

Scan for and BLOCK on:

1. **Orphaned Code Markers** - `TODO`, `FIXME`, `HACK` without `(#issue-number)`
2. **Invalid Issue References** - Referenced issues don't exist
3. **Debug Statements** - `console.log`, `print()`, `debugger`
4. **Commented-Out Code** - >3 lines
5. **Placeholder Text** - "test", "dummy", "lorem ipsum"
6. **Type Safety** - Excessive `any`, missing type hints
7. **Error Handling** - Empty catch blocks
8. **Temporal Documentation** - WIP, DRAFT, TEMP files

```bash
# Scan examples
gh pr diff | grep -E "(TODO|FIXME|HACK)" | grep -v "(#"
gh pr diff | grep -E "(console\.(log|debug)|print\(|debugger)"
```

```markdown
<!-- PR-REVIEW:QUALITY -->
## ⚠️ Code Quality Gate
**Status**: ❌ BLOCKED

### 🚫 Orphaned TODOs (X found)
| File:Line | Marker |
|-----------|--------|
| `auth.ts:45` | TODO |

### Required Actions
1. Create GitHub issues for orphaned TODOs
2. Remove debug statements
3. Delete commented code
```

---

## 6. Apply Labels

Remove old labels, then apply based on outcomes:

| Perspective | Approved | Changes/Blocked |
|-------------|----------|-----------------|
| PM | `claude-pm-approved` | `claude-pm-changes` |
| Developer | `claude-dev-approved` | `claude-dev-changes` |
| QA | `claude-qa-approved` | `claude-qa-changes` |
| Security | `claude-sec-approved` | `claude-sec-blocked` |
| Quality | `claude-quality-passed` | `claude-quality-blocked` |

```bash
gh pr edit --remove-label "claude-pm-approved,claude-pm-changes,..." 2>/dev/null || true
gh pr edit --add-label "claude-pm-approved,claude-dev-changes,..."
```

---

## 7. Write Manifest

Save findings to `.claude/reviews/pr-{number}.yaml` for `/pr-fix`:

```yaml
pr: 123
url: https://github.com/owner/repo/pull/123
branch: feature-branch
base: main
reviewed_at: 2025-01-15T10:30:00Z
verdict: REQUESTING_CHANGES

findings:
  - id: 1
    perspective: DEV
    severity: BLOCKER
    file: src/api/handler.ts
    line: 42
    problem: Missing null check
    why: Request body could be undefined
    fix: Add early return if req.body?.id is undefined
    confidence: high
    status: open
    comment_id: 12345678
```

Ensure `.claude/reviews/` is in `.gitignore`.

---

## 8. Terminal Summary

```
═══════════════════════════════════════════════════
PR REVIEW COMPLETE
═══════════════════════════════════════════════════

PR #<number>: <title>

📊 Product Manager:    [✅ Approved | ⚠️ Changes]
👨‍💻 Developer:          [✅ Approved | ⚠️ Changes]
🧪 Quality Engineer:   [✅ Approved | ⚠️ Changes]
🔒 Security Engineer:  [✅ Approved | ❌ Blocked]
⚠️ Code Quality Gate:  [✅ Passed | ❌ Blocked]

Overall: [✅ APPROVED | ⚠️ CHANGES REQUESTED | ❌ BLOCKED]

Labels Applied: claude-pm-approved, claude-dev-changes, ...

═══════════════════════════════════════════════════
```

Do NOT post a 6th summary comment - all feedback is in the 5 perspective comments.
