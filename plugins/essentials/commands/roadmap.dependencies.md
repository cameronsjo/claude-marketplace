---
description: Show dependencies for a roadmap item
category: roadmap
argument-hint: <item name>
---

# Roadmap Dependencies

Analyze dependencies for a roadmap item.

## Arguments

$ARGUMENTS - The item to analyze

## Instructions

1. Find the item in `docs/roadmap/ideas.md`, `docs/roadmap/research.md`, or `docs/roadmap/completed/`

2. Analyze for:
   - **Blocked By**: What must be done first?
   - **Unlocks**: What does this enable?
   - **Related**: Shared concerns, not strict dependencies

3. Check:
   - Explicit mentions in specs
   - Implicit dependencies (shared components)
   - Related completed features

## Output Format

```
## Dependencies: [Item]

### Blocked By
- [item] - why

### Unlocks
- [item] - what this enables

### Related
- [item] - shared concern

### Recommendation
Whether to proceed, or what to tackle first.
```

If no dependencies:
```
## Dependencies: [Item]

No blocking dependencies. Can start independently.
```
