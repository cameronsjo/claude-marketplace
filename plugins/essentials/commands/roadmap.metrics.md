---
description: Show roadmap statistics and metrics
category: roadmap
---

# Roadmap Metrics

Generate statistics about the project roadmap.

## Instructions

1. Read:
   - `docs/roadmap/ideas.md`
   - `docs/roadmap/research.md`
   - `docs/roadmap/completed/` (count files)
   - `docs/roadmap/rejected/` (count files)

2. Calculate:
   - Ideas by priority (p0-p4)
   - Ideas by effort (small/medium/large)
   - Research items by priority
   - Completed count
   - Rejected count

3. Identify patterns:
   - High priority stuck in research?
   - Large effort without specs?
   - Priority distribution healthy?

## Output Format

```
## Roadmap Metrics

### Active
| Section | Count |
|---------|-------|
| Ideas | X |
| Research | X |

### Ideas by Priority
| Priority | Count |
|----------|-------|
| p0 | X |
| p1 | X |
| p2 | X |
| p3 | X |
| p4 | X |

### Ideas by Effort
| Effort | Count |
|--------|-------|
| small | X |
| medium | X |
| large | X |

### Archive
| Section | Count |
|---------|-------|
| Completed | X |
| Rejected | X |

### Observations
- [Notable patterns]
```
