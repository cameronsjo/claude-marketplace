# Roadmap Maintenance Skill

Helps maintain the project roadmap - a living documentation system that tracks what's planned, what shipped, and what was rejected.

## Core Concept

The roadmap is **documentation that grows from planning**. It bridges incoming work and completed features, providing institutional memory for humans and agents.

## Directory Structure

```
docs/roadmap/
├── README.md           # Entry point - explains the system
├── ideas.md            # Prioritized backlog (p0-p4)
├── research.md         # Topics under investigation
├── completed/          # Shipped features - THE DOCS
│   └── {feature}.md
└── rejected/           # Decided against - WHY NOT
    └── {feature}.md
```

## Workflow

```
research.md ──→ ideas.md ──→ (branch/PR) ──→ completed/{feature}.md
                    ↓
              rejected/{feature}.md
```

- **Research**: Needs investigation before estimating
- **Ideas**: Prioritized and estimated, ready to build
- **Completed**: Shipped - becomes feature documentation
- **Rejected**: Decided against - prevents relitigating

Git blame provides all date tracking.

## Files

### ideas.md

```markdown
| Item | Priority | Effort | Details |
|------|----------|--------|---------|
| Feature name | p1 | medium | Brief description |
```

Sorted by priority then item name.

### research.md

```markdown
| Item | Priority | Details |
|------|----------|---------|
| Topic | p1 | What needs investigation |
```

No effort - can't estimate what you don't understand.

### completed/{feature}.md

```markdown
# Feature Name

> One-line summary

## Status

- **Priority**: p1
- **Effort**: medium
- **Shipped**: version or date context

## Problem

What problem does this solve?

## Solution

How it works.

## Usage

How to use it.

## Related

- Links to other features
```

### rejected/{feature}.md

```markdown
# Feature Name

> Rejected - brief reason

## Request

What users asked for.

## Decision

**Won't implement.**

## Reasoning

Why not.

## Alternatives

What to do instead.
```

## Priority

| Value | Alias | Meaning |
|-------|-------|---------|
| `p0` | | Critical - drop everything |
| `p1` | `high` | Core functionality, security |
| `p2` | `medium` | Nice to have |
| `p3` | `low` | Edge case, cosmetic |
| `p4` | | Backlog, opportunistic |

## Effort

| Value | Meaning |
|-------|---------|
| `small` | < 1 day |
| `medium` | 1-3 days |
| `large` | > 3 days |

## Commands

| Command | Purpose |
|---------|---------|
| `/roadmap` | Review status, suggest next steps |
| `/roadmap.add <item>` | Add to ideas or research |
| `/roadmap.suggest <item>` | Return JSON (for subagents) |
| `/roadmap.spec <item>` | Create detail file |
| `/roadmap.archive <item>` | Move to completed/ or rejected/ |
| `/roadmap.dependencies <item>` | Show blockers and unlocks |
| `/roadmap.metrics` | Stats and distribution |

## Behaviors

### Adding Items

1. Determine: research (needs investigation) or idea (ready to estimate)
2. For ideas: priority (p0-p4) and effort
3. For research: just priority
4. Add to appropriate file, maintain sort order

### Completing Work

When feature ships:
1. Remove from ideas.md
2. Create `completed/{feature}.md` with full documentation
3. Update README.md highlights if significant

### Rejecting Ideas

When deciding against something:
1. Remove from ideas.md or research.md
2. Create `rejected/{feature}.md` with reasoning
3. Document alternatives

### For Agents

- Search `completed/` to understand existing functionality
- Search `rejected/` before suggesting previously-declined features
- All files are markdown - grep-friendly, LLM-friendly

## Examples

**User**: "Add caching to p2"
→ Add to ideas.md at p2 priority

**User**: "Research how auth should work"
→ Add to research.md

**User**: "Ship the plugin versioning feature"
→ Create completed/plugin-versioning.md, remove from ideas.md

**User**: "We're not doing cloud sync"
→ Create rejected/cloud-sync.md with reasoning
