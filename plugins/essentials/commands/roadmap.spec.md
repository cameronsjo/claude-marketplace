---
description: Create detailed spec for roadmap item
category: roadmap
argument-hint: <item name>
---

# Create Roadmap Spec

Create a detailed specification for a roadmap item.

## Arguments

$ARGUMENTS - The item to spec out

## Instructions

1. Find the item in `docs/roadmap/ideas.md` or `docs/roadmap/research.md`

2. Create `docs/roadmap/completed/{kebab-case-name}.md` (as a draft/spec):

```markdown
# Feature Name

> One-line summary

## Status

- **Priority**: p0 | p1 | p2 | p3 | p4
- **Effort**: small | medium | large
- **Status**: Planned

## Problem

What problem does this solve?

## Solution

High-level approach.

## Implementation Details

- List of changes needed

## Alternatives Considered

What else was considered?

## Open Questions

- [ ] Unanswered question?

## Related

- Links to other docs
```

3. Update ideas.md details column to link: `[Spec](completed/item-name.md)`

4. If item was in research.md, move to ideas.md with effort estimate

## Notes

- Creating a spec moves research → idea (with effort estimate)
- The spec becomes the feature doc when shipped (update Status to "Shipped")
