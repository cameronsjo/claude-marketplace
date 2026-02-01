# Workflow: Weekly Planning & Review

A structured weekly practice for reflection, planning, and alignment.

## Overview

The weekly review is where the magic happens:
- Daily chaos becomes organized patterns
- Tasks get prioritized against goals
- Progress becomes visible
- Next week gets set up for success

## When to Do It

**Best time:** End of work week (Friday afternoon) or start of week (Sunday evening/Monday morning)

**Duration:** 30-60 minutes

**Frequency:** Every week, same day/time

## The Weekly Review Process

### Phase 1: Clear (15-20 min)

Get everything out of your head and into your system.

#### 1.1 Process Inbox

Empty all collection points:
- Obsidian Inbox.md
- Email inbox → tasks/notes
- Physical notes → digitize
- Phone notes/photos → transfer

For each item:
- **Actionable?** → Create task or project
- **Reference?** → File in relevant note
- **Trash?** → Delete

#### 1.2 Review Daily Notes

Scan each day's note from the past week:
- Incomplete tasks → decide: do, defer, delegate, delete
- Notes → process into project notes or knowledge base
- Follow-ups → create tasks

#### 1.3 Empty Your Head

Brain dump anything still floating:

```markdown
## Brain Dump
- That thing I kept meaning to do
- Idea from Tuesday's shower
- Follow up with John about X
- Research that tool someone mentioned
```

Process each item immediately.

### Phase 2: Review (15-20 min)

Assess the past week objectively.

#### 2.1 Review Goals/OKRs

Check your quarterly/monthly objectives:
- Progress made?
- Blockers encountered?
- Adjustments needed?

```markdown
## Goal Progress

### Q1 Goal: Launch MVP
- [x] Week 1: Design complete
- [x] Week 2: Backend API
- [ ] Week 3: Frontend (in progress)
- [ ] Week 4: Testing
- [ ] Week 5: Launch

Status: On track ✅
```

#### 2.2 Review Projects

For each active project:
- What happened this week?
- What's the next action?
- Any blockers?

```markdown
## Project Status

### Website Redesign
- Progress: Completed homepage mockup
- Next: Get stakeholder feedback
- Blockers: Waiting on brand assets

### API Integration
- Progress: Auth flow working
- Next: Implement data sync
- Blockers: None
```

#### 2.3 Review Areas

Check ongoing responsibilities:
- Work
- Health
- Relationships
- Finance
- Personal growth

Anything neglected? Needs attention?

#### 2.4 Metrics & Reflection

Quantify the week:

```markdown
## Week Stats
- Tasks completed: 24/30 (80%)
- Days exercised: 4/5
- Deep work hours: 12
- Notes created: 8

## Reflection

### Wins
- Shipped feature X ahead of schedule
- Had productive 1:1 with manager
- Started new exercise routine

### Challenges
- Too many meetings on Wednesday
- Got stuck on debugging issue
- Didn't make time for reading

### Learnings
- Batch similar tasks together
- Ask for help earlier
- Protect morning focus time
```

### Phase 3: Plan (10-15 min)

Set up next week for success.

#### 3.1 Identify Big Rocks

What are the 3-5 most important outcomes for next week?

```markdown
## Next Week Big Rocks
1. Complete frontend MVP
2. Prepare quarterly presentation
3. Finish performance reviews
4. Schedule annual physical
```

#### 3.2 Schedule Big Rocks

Block time for important work:

```markdown
## Time Blocks
- Monday AM: Deep work on frontend
- Tuesday PM: Quarterly presentation prep
- Wednesday: Performance review meetings
- Friday AM: Buffer/overflow
```

#### 3.3 Process Task Backlog

Review all open tasks:
- Still relevant? → Keep or delete
- This week? → Add due date
- Delegate? → Assign and track
- Someday? → Move to someday/maybe list

#### 3.4 Review Calendar

Check next week's commitments:
- Prep needed?
- Travel time?
- Conflicts?

#### 3.5 Create Weekly Note

Generate your weekly note with:
- Goals from planning
- Links to daily notes
- Space for weekly outcomes

## Template: Weekly Note

```markdown
---
week: {{date:gggg-[W]ww}}
start: {{monday:YYYY-MM-DD}}
end: {{sunday:YYYY-MM-DD}}
tags: [weekly]
---

# Week {{date:ww}}, {{date:YYYY}}

## Big Rocks
1. [ ]
2. [ ]
3. [ ]

## Goals from Last Week
- [x] Completed goal
- [ ] Incomplete → moved to this week

## Days
- [[{{monday}}]] Monday
- [[{{tuesday}}]] Tuesday
- [[{{wednesday}}]] Wednesday
- [[{{thursday}}]] Thursday
- [[{{friday}}]] Friday
- [[{{saturday}}]] Saturday
- [[{{sunday}}]] Sunday

## Project Updates
### Project A
- Progress:
- Next:
- Blockers:

## Reflection

### Wins
-

### Challenges
-

### Learnings
-

## Metrics
- Tasks completed: /
- Focus hours:
- Exercise days: /7

---
← [[{{lastweek:gggg-[W]ww}}]] | [[{{nextweek:gggg-[W]ww}}]] →
[[{{date:YYYY-MM}}]] | [[{{date:YYYY-[Q]Q}}]]
```

## Dataview Queries

### Tasks Due This Week

```dataview
TASK
FROM ""
WHERE !completed
AND due >= date(this.start) AND due <= date(this.end)
SORT due ASC
```

### Completed Tasks This Week

```dataview
TASK
FROM ""
WHERE completed
AND completion >= date(this.start)
GROUP BY file.link
```

### Notes Created This Week

```dataview
TABLE file.ctime as "Created"
FROM ""
WHERE file.ctime >= date(this.start) AND file.ctime <= date(this.end)
SORT file.ctime DESC
LIMIT 20
```

### Daily Notes This Week

```dataview
LIST
FROM "Journal/Daily"
WHERE file.day >= date(this.start) AND file.day <= date(this.end)
SORT file.day ASC
```

## Automation Options

### QuickAdd: Weekly Review Macro

```
1. Create weekly note from template
2. Open last week's note in split
3. Run Dataview refresh
4. Open inbox for processing
```

### Templater: Auto-Link Days

```javascript
<%*
const days = [];
for (let i = 0; i < 7; i++) {
  const day = tp.date.now("YYYY-MM-DD", i, tp.date.weekday("Monday", 0));
  const dayName = tp.date.now("dddd", i, tp.date.weekday("Monday", 0));
  days.push(`- [[${day}]] ${dayName}`);
}
%>
## Days
<% days.join("\n") %>
```

### Templater: Pull Last Week's Incomplete Goals

```javascript
<%*
const lastWeek = tp.date.now("gggg-[W]ww", -7);
const lastWeekFile = app.vault.getAbstractFileByPath(`Journal/Weekly/${lastWeek}.md`);
if (lastWeekFile) {
  const content = await app.vault.read(lastWeekFile);
  const incomplete = content.match(/- \[ \] .+/g) || [];
  if (incomplete.length > 0) {
%>
## Rolled Over from Last Week
<% incomplete.slice(0, 5).join("\n") %>
<%* } } %>
```

## Tips for Effective Weekly Reviews

### Create a Ritual

- Same day, same time, same place
- Make it enjoyable (coffee, music)
- Protect the time—it's important

### Use a Checklist

Don't rely on memory:

```markdown
## Weekly Review Checklist
- [ ] Process inbox to zero
- [ ] Review daily notes
- [ ] Brain dump
- [ ] Review goals progress
- [ ] Update project statuses
- [ ] Reflect on wins/challenges
- [ ] Identify next week's big rocks
- [ ] Review calendar
- [ ] Create weekly note
```

### Timebox Each Phase

- Clear: 15 min max
- Review: 15 min max
- Plan: 15 min max

Don't let it expand to fill hours.

### Be Honest

The review is for you:
- Acknowledge what didn't happen
- Celebrate what did
- Learn without judgment

### Adjust as Needed

Your weekly review should evolve:
- Drop sections that don't add value
- Add sections you keep missing
- Optimize for your needs

## Common Problems

| Problem | Solution |
|---------|----------|
| Takes too long | Timebox strictly, simplify template |
| Keep skipping it | Make it enjoyable, block calendar |
| Feels pointless | Simplify, focus on next actions |
| Overwhelmed by backlog | Process smaller batches |
| Not seeing patterns | Add metrics, be consistent |

## Connection to Larger Cycles

```
Daily Reviews → capture & execute
    ↓
Weekly Reviews → reflect & plan
    ↓
Monthly Reviews → adjust & align
    ↓
Quarterly Reviews → strategize
    ↓
Annual Reviews → vision & direction
```

Each cycle feeds the next. Weekly is the sweet spot for course correction—frequent enough to matter, spaced enough to see patterns.
