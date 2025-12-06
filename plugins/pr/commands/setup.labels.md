---
description: Setup PR review and issue labels for repository
category: version-control-git
allowed-tools: Bash(gh *)
---

# Setup Repository Labels

Create comprehensive label system for PR reviews, issue management, and project organization.

## Execution Steps

### 1. Create All Labels Quietly

Show simple progress and create all labels silently:

```bash
echo "Creating repository labels..."
echo ""

# Create all labels silently (suppress output)
{
  # PR Review Labels (10)
  gh label create "claude-pm-approved" --color "0E8A16" --description "✅ PM: Approved" --force
  gh label create "claude-pm-changes" --color "D93F0B" --description "⚠️ PM: Changes requested" --force
  gh label create "claude-dev-approved" --color "0E8A16" --description "✅ Dev: Approved" --force
  gh label create "claude-dev-changes" --color "D93F0B" --description "⚠️ Dev: Changes requested" --force
  gh label create "claude-qa-approved" --color "0E8A16" --description "✅ QA: Approved" --force
  gh label create "claude-qa-changes" --color "D93F0B" --description "⚠️ QA: Changes requested" --force
  gh label create "claude-sec-approved" --color "0E8A16" --description "✅ Security: Approved" --force
  gh label create "claude-sec-blocked" --color "B60205" --description "🚨 Security: BLOCKED" --force
  gh label create "claude-quality-passed" --color "0E8A16" --description "✅ Quality Gate: Passed" --force
  gh label create "claude-quality-blocked" --color "B60205" --description "🚨 Quality Gate: BLOCKED" --force

  # Priority Labels (4)
  gh label create "priority-critical" --color "B60205" --description "🚨 Critical: Fix immediately" --force
  gh label create "priority-high" --color "D93F0B" --description "🔴 High: Fix soon" --force
  gh label create "priority-medium" --color "FBCA04" --description "🟡 Medium: Normal priority" --force
  gh label create "priority-low" --color "0E8A16" --description "🟢 Low: When time allows" --force

  # Type Labels (8)
  gh label create "type-bug" --color "D73A4A" --description "🐛 Bug: Something isn't working" --force
  gh label create "type-feature" --color "A2EEEF" --description "✨ Feature: New functionality" --force
  gh label create "type-enhancement" --color "84B6EB" --description "⚡ Enhancement: Improve existing feature" --force
  gh label create "type-docs" --color "0075CA" --description "📚 Documentation: Docs only" --force
  gh label create "type-refactor" --color "5319E7" --description "♻️ Refactor: Code restructuring" --force
  gh label create "type-test" --color "1D76DB" --description "🧪 Test: Testing improvements" --force
  gh label create "type-chore" --color "FEF2C0" --description "🔧 Chore: Maintenance tasks" --force
  gh label create "type-perf" --color "F9D0C4" --description "🚀 Performance: Speed/efficiency" --force

  # Status Labels (5)
  gh label create "status-blocked" --color "B60205" --description "🚫 Blocked: Cannot proceed" --force
  gh label create "status-in-progress" --color "FBCA04" --description "🏗️ In Progress: Actively working" --force
  gh label create "status-ready" --color "0E8A16" --description "✅ Ready: Can start work" --force
  gh label create "status-needs-review" --color "D4C5F9" --description "👀 Needs Review: Awaiting feedback" --force
  gh label create "status-needs-info" --color "D876E3" --description "❓ Needs Info: More details required" --force

  # Area Labels (7)
  gh label create "area-security" --color "B60205" --description "🔒 Security: Security related" --force
  gh label create "area-performance" --color "F9D0C4" --description "⚡ Performance: Speed/efficiency" --force
  gh label create "area-dx" --color "C5DEF5" --description "🛠️ DX: Developer experience" --force
  gh label create "area-api" --color "BFD4F2" --description "🔌 API: API related" --force
  gh label create "area-ui" --color "C2E0C6" --description "🎨 UI: User interface" --force
  gh label create "area-db" --color "D4C5F9" --description "🗄️ Database: Data layer" --force
  gh label create "area-infra" --color "FEF2C0" --description "🏗️ Infrastructure: Deployment/ops" --force

  # Special Labels (8)
  gh label create "good-first-issue" --color "7057FF" --description "👋 Good for newcomers" --force
  gh label create "help-wanted" --color "008672" --description "🙋 Help wanted" --force
  gh label create "needs-investigation" --color "D876E3" --description "🔍 Needs investigation" --force
  gh label create "breaking-change" --color "B60205" --description "💥 Breaking change" --force
  gh label create "tech-debt" --color "E99695" --description "⚙️ Technical debt" --force
  gh label create "wontfix" --color "FFFFFF" --description "❌ Won't fix" --force
  gh label create "duplicate" --color "CFD3D7" --description "♊ Duplicate issue" --force
  gh label create "dependencies" --color "0366D6" --description "📦 Dependency updates" --force
} > /dev/null 2>&1

echo "✅ Done!"
echo ""
```

### 2. Show Summary

```bash
echo "═══════════════════════════════════════════════════"
echo "LABEL SETUP COMPLETE"
echo "═══════════════════════════════════════════════════"
echo ""
echo "📊 PR Review Labels (10):"
echo "   - claude-pm-approved, claude-pm-changes"
echo "   - claude-dev-approved, claude-dev-changes"
echo "   - claude-qa-approved, claude-qa-changes"
echo "   - claude-sec-approved, claude-sec-blocked"
echo "   - claude-quality-passed, claude-quality-blocked"
echo ""
echo "🎯 Priority Labels (4):"
echo "   - priority-critical, priority-high, priority-medium, priority-low"
echo ""
echo "📝 Type Labels (8):"
echo "   - type-bug, type-feature, type-enhancement, type-docs"
echo "   - type-refactor, type-test, type-chore, type-perf"
echo ""
echo "📊 Status Labels (5):"
echo "   - status-blocked, status-in-progress, status-ready"
echo "   - status-needs-review, status-needs-info"
echo ""
echo "🗂️ Area Labels (7):"
echo "   - area-security, area-performance, area-dx, area-api"
echo "   - area-ui, area-db, area-infra"
echo ""
echo "⭐ Special Labels (8):"
echo "   - good-first-issue, help-wanted, needs-investigation"
echo "   - breaking-change, tech-debt, wontfix, duplicate, dependencies"
echo ""
echo "═══════════════════════════════════════════════════"
echo "Total: 42 labels created"
echo ""
echo "View labels: gh label list"
echo "═══════════════════════════════════════════════════"
```

## Notes

**Using `--force` flag**:
- Updates existing labels with new colors/descriptions
- Creates labels that don't exist
- Safe to run multiple times (idempotent)

**Label naming conventions**:
- **PR reviews**: `claude-{perspective}-{status}`
- **Priority**: `priority-{level}`
- **Type**: `type-{category}`
- **Status**: `status-{state}`
- **Area**: `area-{component}`

**Colors**:
- 🔴 Red (`B60205`, `D73A4A`, `D93F0B`) - Critical, blocked, bugs
- 🟢 Green (`0E8A16`) - Approved, ready, passed
- 🟡 Yellow (`FBCA04`, `FEF2C0`) - In progress, medium priority
- 🔵 Blue (`0075CA`, `1D76DB`, `BFD4F2`) - Info, docs, API
- 🟣 Purple (`5319E7`, `D4C5F9`, `D876E3`) - Refactor, review, investigation
- ⚫ Gray (`FFFFFF`, `CFD3D7`) - Won't fix, duplicate

**Best practices**:
1. **PR labels**: Applied automatically by `/pr-review`
2. **Priority + Type**: Use both on issues (e.g., `priority-high` + `type-bug`)
3. **Area labels**: Add to help organize large codebases
4. **Status labels**: Update as work progresses
5. **Special labels**: Use sparingly, only when relevant
