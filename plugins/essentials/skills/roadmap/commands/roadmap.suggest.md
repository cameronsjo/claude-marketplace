---
description: Suggest roadmap items (returns JSON, doesn't write)
category: roadmap
argument-hint: <item description>
---

# Suggest Roadmap Item

Return structured JSON WITHOUT writing to files. For subagents or concurrent operations.

## Arguments

$ARGUMENTS - The item to suggest

## Instructions

1. Parse $ARGUMENTS
2. Determine if Research or Idea
3. Estimate priority p0-p4 (and effort for Ideas)
4. Return JSON:

```json
{
  "item": "Short item name",
  "type": "idea",
  "priority": "p1",
  "effort": "medium",
  "details": "Brief description"
}
```

For research, omit `effort`:

```json
{
  "item": "Plugin versioning",
  "type": "research",
  "priority": "p1",
  "details": "How should semantic versioning work?"
}
```

## When to Use

- Running as Task/subagent
- Multiple agents concurrently
- Parent will batch-write to `docs/roadmap/ideas.md` or `docs/roadmap/research.md`
