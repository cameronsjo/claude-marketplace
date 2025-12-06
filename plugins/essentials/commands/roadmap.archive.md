---
description: Archive completed or rejected roadmap items
category: roadmap
argument-hint: <item> [done|rejected] [reason]
---

# Archive Roadmap Item

Move an item from active roadmap to completed/ or rejected/.

## Arguments

$ARGUMENTS - Item name and disposition (e.g., "plugin versioning done" or "cloud sync rejected - too complex")

## Instructions

### For Completed Items

1. Remove from `docs/roadmap/ideas.md`
2. Create or update `docs/roadmap/completed/{item}.md`:

```markdown
# Feature Name

> One-line summary

## Status

- **Priority**: p1
- **Effort**: medium
- **Shipped**: [context]

## Problem

What problem does this solve?

## Solution

How it works.

## Usage

How to use it.

## Related

- Links
```

3. Update `docs/roadmap/README.md` highlights if significant

### For Rejected Items

1. Remove from `docs/roadmap/ideas.md` or `docs/roadmap/research.md`
2. Create `docs/roadmap/rejected/{item}.md`:

```markdown
# Feature Name

> Rejected - [brief reason]

## Request

What users asked for.

## Decision

**Won't implement.**

## Reasoning

Why not.

## Alternatives

What to do instead.
```

3. Update `docs/roadmap/README.md` if commonly requested

## Examples

`/roadmap.archive plugin versioning done`
→ Create completed/plugin-versioning.md, remove from ideas.md

`/roadmap.archive cloud sync rejected - git handles this`
→ Create rejected/cloud-sync.md with reasoning
