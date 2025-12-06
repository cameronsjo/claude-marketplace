---
description: Add item to project roadmap
category: roadmap
argument-hint: <item description>
---

# Add Roadmap Item

Add a new item to the project roadmap.

## Arguments

$ARGUMENTS - The item to add (e.g., "AVIF support" or "p0: auth broken" or "research: how should X work")

## Instructions

1. Parse $ARGUMENTS for item and hints (p0-p4, research, effort)

2. Determine if **Research** or **Idea**:
   - Research: "research:", "investigate", "explore", "figure out"
   - Idea: Everything else

3. Determine Priority (user can specify p0-p4 directly):
   - `p0` - Critical (also: "critical", "urgent")
   - `p1` / `high` - Core functionality, security
   - `p2` / `medium` - Nice to have
   - `p3` / `low` - Edge case, cosmetic
   - `p4` - Backlog

4. For Ideas, determine Effort:
   - `small` (< 1 day)
   - `medium` (1-3 days)
   - `large` (> 3 days)

5. Add to appropriate file:
   - Ideas: `docs/roadmap/ideas.md`
   - Research: `docs/roadmap/research.md`

6. Maintain sort order: priority (p0→p4), then item name ascending

## Concurrency

If multiple agents writing simultaneously, use `/roadmap.suggest` instead.

## Examples

`/roadmap.add AVIF image support`
→ ideas.md: `| AVIF image support | p2 | small | Better compression |`

`/roadmap.add caching to p3`
→ ideas.md: `| Caching | p3 | small | Performance |`

`/roadmap.add p0: auth bypass`
→ ideas.md: `| Auth bypass | p0 | medium | Security vulnerability |`

`/roadmap.add research: plugin dependency resolution`
→ research.md: `| Plugin dependency resolution | p1 | How should deps work? |`
