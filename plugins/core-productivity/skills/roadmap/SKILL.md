# Roadmap Maintenance Skill

Helps maintain the project roadmap and enhancement tracking system.

## Files

- **MOC**: `docs/ROADMAP.md` - Main index with categorized tables
- **Details**: `docs/roadmap/*.md` - Detailed specs for complex items
- **Template**: `docs/roadmap/_template.md` - Template for new detail files

## Categories

| Category | Purpose |
|----------|---------|
| Active Migration Projects | Large ongoing refactoring efforts |
| Performance | Speed, rendering, caching improvements |
| Features | New user-facing functionality |
| Technical Debt | Cleanup, refactoring, modernization |
| UX Improvements | User experience enhancements |
| Infrastructure | DevOps, monitoring, logging |

## Status Values

- `idea` - Captured, not yet evaluated
- `planned` - Evaluated, will implement
- `in-progress` - Currently being worked on
- `done` - Completed (archive to CHANGELOG)
- `wontfix` - Decided against

## Commands

### Add a new item

When user says "add to roadmap" or "track this for later":

1. Determine the appropriate category
2. Ask for: title, impact (high/medium/low), effort (small/medium/large)
3. Add row to the category table in `docs/ROADMAP.md`
4. If complex (effort > small), create a detail file using the template

### Create a detail spec

When user says "spec out [item]" or "plan [feature]":

1. Copy `docs/roadmap/_template.md` to `docs/roadmap/{kebab-case-name}.md`
2. Fill in sections based on discussion
3. Update the ROADMAP.md table to link to the new file

### Update status

When user says "mark [item] as [status]":

1. Find the item in `docs/ROADMAP.md`
2. Update the status column
3. If `done`, suggest moving to CHANGELOG

### Review roadmap

When user says "review roadmap" or "what's stale":

1. Read `docs/ROADMAP.md`
2. Identify items that might need attention:
   - `idea` items older than 30 days without activity
   - `in-progress` items that may be stuck
   - `planned` items ready to start
3. Summarize findings and suggest actions

### Prioritize

When user asks "what should I work on next":

1. List `planned` items sorted by impact (high first)
2. Consider effort vs impact ratio
3. Note any blockers or dependencies

## Detail File Template

```markdown
# Feature: [Title]

> One-line summary

## Status

- **Status**: idea | planned | in-progress | done
- **Priority**: high | medium | low
- **Effort**: small (< 1 day) | medium (1-3 days) | large (> 3 days)

## Problem

What problem does this solve?

## Proposed Solution

High-level approach.

## Implementation Details

### Backend Changes
### Frontend Changes

## Alternatives Considered

## Open Questions

- [ ] Question 1?

## References
```

## Examples

**User**: "Add thumbnail generation to the roadmap"
**Action**: Already exists - show current status and link

**User**: "I want to add AVIF support as an idea"
**Action**: Add row to Performance table with status `idea`, impact Medium, effort Small

**User**: "Spec out the keyboard shortcuts feature"
**Action**: Create `docs/roadmap/keyboard-shortcuts.md` from template, fill in details

**User**: "Mark sort enums as done"
**Action**: Update status in Technical Debt table to `done`

**User**: "What's next on the roadmap?"
**Action**: List high-impact planned items, suggest starting point
