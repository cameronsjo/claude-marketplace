# Periodic Notes Reference

Daily, weekly, monthly, quarterly, and yearly notes for Obsidian.

## Overview

Periodic Notes extends the core Daily Notes plugin with:
- Weekly notes
- Monthly notes
- Quarterly notes
- Yearly notes
- Calendar integration
- Custom date formats and folders

## Installation

Community Plugins → Search "Periodic Notes" → Install → Enable

**Recommended companion plugins:**
- Calendar (for visual navigation)
- Templater (for dynamic templates)
- Dataview (for aggregating periodic data)

## Configuration

### Settings Location

Settings → Periodic Notes

### Per-Period Settings

Each period (daily, weekly, etc.) has:
- **Enable**: Toggle on/off
- **Format**: Filename date format
- **Folder**: Where notes are stored
- **Template**: Path to template file

## Date Formats

### Daily Notes

| Format | Example |
|--------|---------|
| `YYYY-MM-DD` | 2024-01-15 |
| `DD-MM-YYYY` | 15-01-2024 |
| `YYYY/MM/YYYY-MM-DD` | 2024/01/2024-01-15 |

### Weekly Notes

| Format | Example |
|--------|---------|
| `gggg-[W]ww` | 2024-W03 |
| `YYYY-[Week]-ww` | 2024-Week-03 |
| `gggg/[W]ww` | 2024/W03 |

`gggg` = ISO week year, `ww` = ISO week number

### Monthly Notes

| Format | Example |
|--------|---------|
| `YYYY-MM` | 2024-01 |
| `MMMM YYYY` | January 2024 |
| `YYYY/YYYY-MM` | 2024/2024-01 |

### Quarterly Notes

| Format | Example |
|--------|---------|
| `YYYY-[Q]Q` | 2024-Q1 |
| `YYYY/[Q]Q` | 2024/Q1 |

### Yearly Notes

| Format | Example |
|--------|---------|
| `YYYY` | 2024 |
| `[Year] YYYY` | Year 2024 |

## Folder Organization

### Flat Structure

```
Journal/
├── 2024-01-15.md
├── 2024-01-16.md
├── 2024-W03.md
├── 2024-01.md
└── 2024.md
```

### Hierarchical Structure

```
Journal/
├── Daily/
│   └── 2024-01-15.md
├── Weekly/
│   └── 2024-W03.md
├── Monthly/
│   └── 2024-01.md
├── Quarterly/
│   └── 2024-Q1.md
└── Yearly/
    └── 2024.md
```

### Date-Based Hierarchy

```
Journal/
└── 2024/
    ├── 01/
    │   ├── 2024-01-15.md
    │   ├── 2024-01-16.md
    │   └── 2024-01.md
    ├── 2024-W03.md
    ├── 2024-Q1.md
    └── 2024.md
```

Use format `YYYY/MM/YYYY-MM-DD` to auto-create folder structure.

## Templates

### Template Variables

Periodic Notes uses Obsidian's core template variables:
- `{{date}}` - Note date
- `{{time}}` - Current time
- `{{title}}` - Note title

For advanced templates, use Templater.

### Daily Note Template

```markdown
---
date: {{date}}
tags: [daily]
---

# {{date:dddd, MMMM Do YYYY}}

## Morning
- [ ] Review calendar
- [ ] Top 3 priorities
  1.
  2.
  3.

## Tasks
- [ ]

## Notes


## Evening Reflection
- What went well?
- What could improve?
- Grateful for:
```

### Weekly Note Template

```markdown
---
week: {{date:gggg-[W]ww}}
start: {{date:YYYY-MM-DD}}
tags: [weekly]
---

# Week {{date:ww}}, {{date:YYYY}}

## Weekly Goals
- [ ]
- [ ]
- [ ]

## Days
- [[{{date:YYYY-MM-DD}}]] Monday
- [[{{date+1d:YYYY-MM-DD}}]] Tuesday
- [[{{date+2d:YYYY-MM-DD}}]] Wednesday
- [[{{date+3d:YYYY-MM-DD}}]] Thursday
- [[{{date+4d:YYYY-MM-DD}}]] Friday
- [[{{date+5d:YYYY-MM-DD}}]] Saturday
- [[{{date+6d:YYYY-MM-DD}}]] Sunday

## Review
### Accomplishments


### Challenges


### Learnings


## Next Week Focus

```

### Monthly Note Template

```markdown
---
month: {{date:YYYY-MM}}
tags: [monthly]
---

# {{date:MMMM YYYY}}

## Monthly Goals
- [ ]
- [ ]
- [ ]

## Weeks
- [[{{date:gggg-[W]ww}}]]
- [[{{date+1w:gggg-[W]ww}}]]
- [[{{date+2w:gggg-[W]ww}}]]
- [[{{date+3w:gggg-[W]ww}}]]

## Areas of Focus
### Work


### Personal


### Health


## Month End Review
### Highlights


### Lessons Learned


### Goals for Next Month

```

### Quarterly Note Template

```markdown
---
quarter: {{date:YYYY-[Q]Q}}
tags: [quarterly]
---

# {{date:YYYY}} Q{{date:Q}}

## Quarterly Objectives
1.
2.
3.

## Key Results
- [ ] KR1:
- [ ] KR2:
- [ ] KR3:

## Months
- [[{{date:YYYY-MM}}]]
- [[{{date+1M:YYYY-MM}}]]
- [[{{date+2M:YYYY-MM}}]]

## Projects


## Quarterly Review
### Achievements


### Missed Goals


### Adjustments for Next Quarter

```

### Yearly Note Template

```markdown
---
year: {{date:YYYY}}
tags: [yearly]
---

# {{date:YYYY}}

## Annual Theme


## Yearly Goals
### Professional
- [ ]

### Personal
- [ ]

### Health
- [ ]

### Financial
- [ ]

## Quarters
- [[{{date:YYYY}}-Q1]]
- [[{{date:YYYY}}-Q2]]
- [[{{date:YYYY}}-Q3]]
- [[{{date:YYYY}}-Q4]]

## Year in Review
### Major Accomplishments


### Lessons Learned


### Memorable Moments


## Next Year Vision

```

## Templater Integration

For dynamic templates, use Templater syntax:

### Daily with Templater

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
day: <% tp.date.now("dddd") %>
week: <% tp.date.now("gggg-[W]ww") %>
tags: [daily]
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

<% tp.file.include("[[Templates/daily-sections]]") %>

## Links
- Yesterday: [[<% tp.date.now("YYYY-MM-DD", -1) %>]]
- Tomorrow: [[<% tp.date.now("YYYY-MM-DD", 1) %>]]
- Week: [[<% tp.date.now("gggg-[W]ww") %>]]
```

### Weekly with Templater

```markdown
<%*
const startOfWeek = tp.date.now("YYYY-MM-DD", 0, tp.date.weekday("Monday", 0));
const endOfWeek = tp.date.now("YYYY-MM-DD", 0, tp.date.weekday("Sunday", 0));
%>
---
week: <% tp.date.now("gggg-[W]ww") %>
start: <% startOfWeek %>
end: <% endOfWeek %>
tags: [weekly]
---

# Week <% tp.date.now("ww") %>, <% tp.date.now("YYYY") %>

## Daily Notes
<%*
for (let i = 0; i < 7; i++) {
  const day = tp.date.now("YYYY-MM-DD", i, tp.date.weekday("Monday", 0));
  const dayName = tp.date.now("dddd", i, tp.date.weekday("Monday", 0));
%>
- [[<% day %>]] <% dayName %>
<%* } %>
```

## Dataview Integration

### Show Week's Daily Notes

```dataview
TABLE WITHOUT ID
  file.link as "Day",
  file.day.weekday as "Weekday"
FROM "Journal/Daily"
WHERE file.day >= date(this.start) AND file.day <= date(this.end)
SORT file.day ASC
```

### Aggregate Tasks from Dailies

```dataview
TASK
FROM "Journal/Daily"
WHERE file.day >= date(this.start) AND file.day <= date(this.end)
WHERE !completed
GROUP BY file.link
```

### Monthly Summary

```dataview
TABLE WITHOUT ID
  file.link as "Week",
  length(file.inlinks) as "Daily Links"
FROM "Journal/Weekly"
WHERE contains(file.name, this.month)
SORT file.name ASC
```

## Calendar Plugin Integration

The Calendar plugin provides visual navigation:
- Click date → Open/create daily note
- Click week number → Open/create weekly note
- Dots indicate existing notes
- Color coding for completed status

### Configure Calendar

1. Install Calendar plugin
2. Settings → Calendar
3. Enable "Show week number"
4. Set week start day
5. Confirm folder/format matches Periodic Notes

## Auto-Creation

### On Startup

Some users create today's daily note automatically:
1. Use Templater startup template
2. Or QuickAdd macro with "Run on plugin load"

### Via Calendar

Click any date in Calendar to create if missing.

## Navigation Patterns

### Header Links

```markdown
# January 15, 2024

← [[2024-01-14]] | [[2024-01-16]] →

[[2024-W03]] | [[2024-01]] | [[2024]]
```

### Breadcrumb Trail

```markdown
[[2024]] > [[2024-Q1]] > [[2024-01]] > [[2024-W03]] > [[2024-01-15]]
```

## Rolling Over Tasks

### Manual Rollover

Copy incomplete tasks from yesterday:

```markdown
## Tasks
### Rolled Over
- [ ] Task from yesterday

### New Today
- [ ]
```

### Automated with Templater

```javascript
<%*
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const yesterdayFile = tp.file.find_tfile(yesterday);
if (yesterdayFile) {
  const content = await app.vault.read(yesterdayFile);
  const incompleteTasks = content.match(/- \[ \] .+/g) || [];
  if (incompleteTasks.length > 0) {
%>
## Rolled Over
<% incompleteTasks.join("\n") %>
<%* } } %>
```

### Rollover Plugin

"Rollover Daily Todos" plugin does this automatically.

## Tips

### Consistent Naming

Pick one format and stick with it:
- ISO format (`YYYY-MM-DD`) sorts correctly
- Readable format (`January 15, 2024`) is friendlier
- Don't mix formats

### Template Inheritance

Weekly templates can include daily template sections:
```markdown
<% tp.file.include("[[Templates/reflection-questions]]") %>
```

### Review Cycles

| Period | Review Contains |
|--------|----------------|
| Daily | Tasks, notes, reflection |
| Weekly | Daily summaries, weekly goals |
| Monthly | Weekly reviews, monthly themes |
| Quarterly | OKRs, major projects |
| Yearly | Life areas, annual themes |

### Linking Strategy

Always link up and down the hierarchy:
- Daily → links to week and month
- Weekly → links to days and month
- Monthly → links to weeks and quarters

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong date format | Check moment.js format string |
| Note in wrong folder | Verify folder path in settings |
| Template not applied | Check template path, restart Obsidian |
| Calendar not syncing | Ensure formats match between plugins |

## Resources

- [Periodic Notes GitHub](https://github.com/liamcain/obsidian-periodic-notes)
- [Calendar Plugin](https://github.com/liamcain/obsidian-calendar-plugin)
- [Moment.js Format Tokens](https://momentjs.com/docs/#/displaying/format/)
