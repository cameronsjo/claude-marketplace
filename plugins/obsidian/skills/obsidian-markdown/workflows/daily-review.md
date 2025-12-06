# Workflow: Daily Review

A structured daily practice for capturing, processing, and reflecting.

## Overview

The daily review is the heartbeat of a PKM system. It ensures:
- Tasks don't fall through cracks
- Ideas get captured and processed
- Progress is tracked
- Reflection drives improvement

## Morning Routine (10-15 min)

### 1. Open/Create Daily Note

```markdown
Command: Open today's daily note
Or: Click today in Calendar plugin
```

### 2. Review Yesterday

Quick scan of yesterday's note:
- What tasks remain incomplete?
- Any follow-ups needed?
- Notes that need processing?

### 3. Rollover Tasks

Move incomplete tasks to today:

```markdown
## Rolled Over
- [ ] Task from yesterday
- [ ] Another incomplete task
```

Or use the "Rollover Daily Todos" plugin for automation.

### 4. Check Calendar

Review today's commitments:
- Meetings
- Deadlines
- Time blocks

Add to daily note:

```markdown
## Schedule
- 09:00 Team standup
- 14:00 Client call
- 17:00 📅 Project X deadline
```

### 5. Set Priorities

Identify top 3 priorities for the day:

```markdown
## Top 3 Today
1. [ ] Complete report draft ⏫
2. [ ] Review PR for feature branch
3. [ ] Prep for client call
```

### 6. Quick Inbox Check

Scan email/messages for anything urgent.
Capture tasks, don't process everything now.

## Throughout the Day

### Quick Capture

When thoughts/tasks arise, capture immediately:

**Option A: QuickAdd Capture**
```
Hotkey → Type thought → Enter
Automatically appends to daily note
```

**Option B: Inbox Note**
```
Hotkey → Quick note to Inbox.md
Process later
```

**Option C: Direct Entry**
Open daily note, add under Notes section.

### Task Completion

As you complete tasks:
1. Check them off `- [x]`
2. Add brief notes if relevant
3. Don't delete incomplete tasks

### Meeting Notes

During/after meetings:

```markdown
## Meeting: [Topic] @ HH:MM

### Attendees
- [[Person A]]
- [[Person B]]

### Notes
-

### Action Items
- [ ] Me: Follow up on X
- [ ] [[Person A]]: Send documentation
```

## Evening Routine (5-10 min)

### 1. Process Inbox

Review captured items:
- Convert to tasks if actionable
- Move to relevant project notes
- Archive or delete if not needed

### 2. Update Task Status

Review all tasks:
- Mark completed items
- Add notes for partial progress
- Reschedule if needed

### 3. Reflection

Answer reflection prompts:

```markdown
## Evening Reflection

### What went well?
-

### What could improve?
-

### Grateful for:
-

### Key learnings:
-
```

### 4. Tomorrow Prep

Quick look at tomorrow:
- Any early meetings?
- Deadlines approaching?
- Prep needed tonight?

```markdown
## Tomorrow
- [ ] Morning: Review presentation
- Meeting with client at 10:00
```

### 5. Final Review

Scan the day's note:
- All sections completed?
- Any loose threads?
- Satisfying day of work?

## Template: Daily Note

```markdown
---
date: {{date:YYYY-MM-DD}}
day: {{date:dddd}}
week: {{date:gggg-[W]ww}}
tags: [daily]
---

# {{date:dddd, MMMM Do}}

## Top 3 Today
1. [ ]
2. [ ]
3. [ ]

## Schedule
-

## Tasks
- [ ]

## Rolled Over
-

## Notes


## Meetings


## Evening Reflection

### What went well?
-

### What could improve?
-

### Grateful for:
-

## Tomorrow
-

---
← [[{{date-1d:YYYY-MM-DD}}]] | [[{{date+1d:YYYY-MM-DD}}]] →
[[{{date:gggg-[W]ww}}]] | [[{{date:YYYY-MM}}]]
```

## Automation Options

### QuickAdd: Morning Setup Macro

```
1. Open today's daily note
2. Run Templater on it
3. Open yesterday's note in split
4. Focus on today's note
```

### QuickAdd: Quick Task Capture

```
1. Prompt for task description
2. Prompt for priority (optional)
3. Append to daily note Tasks section
```

### Templater: Auto-Rollover

```javascript
<%*
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const file = app.vault.getAbstractFileByPath(`Journal/${yesterday}.md`);
if (file) {
  const content = await app.vault.read(file);
  const tasks = content.match(/- \[ \] .+/g) || [];
  if (tasks.length > 0) {
%>
## Rolled Over
<% tasks.join("\n") %>
<%* } } %>
```

### Dataview: Today's Tasks

```dataview
TASK
FROM "Projects" OR "Areas"
WHERE !completed AND due = date(today)
SORT priority DESC
```

## Tips for Success

### Make It Easy

- Use hotkeys for common actions
- Keep daily note pinned or easily accessible
- Use templates—don't start from blank

### Be Consistent

- Same time each morning
- Same time each evening
- Start small, build the habit

### Don't Overthink

- Notes don't need to be perfect
- Short entries are better than none
- Capture now, organize later

### Review Weekly

Your daily reviews feed your weekly review:
- Patterns emerge
- Trends become visible
- Adjustments become obvious

## Common Problems

| Problem | Solution |
|---------|----------|
| Skipping days | Reduce scope, make it easier |
| Taking too long | Timebox strictly, skip optional sections |
| Inconsistent format | Use templates, QuickAdd |
| Orphaned tasks | Weekly review catches them |
| Too much detail | Save details for project notes |

## Metrics to Track

Optional quantified self data:

```markdown
## Metrics
- Sleep: /10
- Energy: /10
- Focus: /10
- Tasks completed: X/Y
- Mood: 😊 😐 😔
```

## Integration with Larger System

Daily notes are the **input layer** of your PKM:

```
Daily Notes (capture)
    ↓
Weekly Reviews (process)
    ↓
Project Notes (organize)
    ↓
Knowledge Base (connect)
```

Each layer feeds the next, creating a system where nothing is lost and patterns emerge naturally.
