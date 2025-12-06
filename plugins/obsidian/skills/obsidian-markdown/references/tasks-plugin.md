# Tasks Plugin Reference

Advanced task management with powerful queries for Obsidian.

## Overview

The Tasks plugin transforms Obsidian into a powerful task manager with:
- Custom task statuses beyond done/not done
- Due dates, scheduled dates, start dates
- Recurrence rules
- Powerful query language
- Priority levels
- Dependencies

## Installation

Community Plugins → Search "Tasks" → Install → Enable

## Task Syntax

### Basic Task

```markdown
- [ ] Basic task
- [x] Completed task
```

### With Metadata

```markdown
- [ ] Task with due date 📅 2024-01-15
- [ ] Scheduled task ⏳ 2024-01-10
- [ ] Task with start date 🛫 2024-01-05
- [ ] High priority task ⏫
- [ ] Recurring task 🔁 every week
- [ ] Task with created date ➕ 2024-01-01
```

### Full Example

```markdown
- [ ] Review quarterly report ⏫ 📅 2024-01-15 ⏳ 2024-01-10 🔁 every quarter ➕ 2024-01-01
```

## Date Formats

### Emoji Indicators

| Emoji | Meaning | Example |
|-------|---------|---------|
| 📅 | Due date | `📅 2024-01-15` |
| ⏳ | Scheduled date | `⏳ 2024-01-10` |
| 🛫 | Start date | `🛫 2024-01-05` |
| ➕ | Created date | `➕ 2024-01-01` |
| ✅ | Done date | `✅ 2024-01-14` |
| ❌ | Cancelled date | `❌ 2024-01-12` |

### Date Entry

- Click emoji in edit mode for date picker
- Or type manually: `📅 2024-01-15`

## Priority Levels

| Emoji | Level | Sort Order |
|-------|-------|------------|
| 🔺 | Highest | 1 |
| ⏫ | High | 2 |
| 🔼 | Medium | 3 |
| (none) | Normal | 4 |
| 🔽 | Low | 5 |
| ⏬️ | Lowest | 6 |

## Recurrence

### Syntax

```markdown
🔁 every day
🔁 every week
🔁 every month
🔁 every year
🔁 every 2 weeks
🔁 every 3 months
🔁 every weekday
🔁 every week on Monday
🔁 every month on the 15th
🔁 every month on the last day
```

### Recurrence Behavior

When you complete a recurring task:
1. Original task is marked done with completion date
2. New task is created with next occurrence date

## Custom Statuses

### Default Statuses

| Symbol | Status | Next |
|--------|--------|------|
| ` ` (space) | Todo | `x` |
| `x` | Done | ` ` |
| `/` | In Progress | `x` |
| `-` | Cancelled | ` ` |

### Configure Custom Statuses

Settings → Tasks → Statuses → Add custom statuses

Example custom statuses:
- `[>]` - Deferred
- `[?]` - Question
- `[!]` - Important
- `["]` - Quote
- `[l]` - Location

## Query Blocks

### Basic Query

````markdown
```tasks
not done
due before tomorrow
```
````

### Query Structure

```
filter1
filter2
sort by field
group by field
limit N
```

## Filters

### Status Filters

```
not done           # All incomplete tasks
done               # All completed tasks
status.type is TODO
status.type is DONE
status.type is IN_PROGRESS
status.type is CANCELLED
status.type is NON_TASK
```

### Date Filters

```
# Due date
due today
due before today
due after 2024-01-15
due this week
due next month
has due date
no due date

# Other dates
scheduled today
starts before tomorrow
created last week
done this month
```

### Text Filters

```
description includes meeting
description does not include admin
heading includes Projects
path includes Work/
filename includes 2024
```

### Tag Filters

```
tags include #work
tags do not include #personal
tag includes #project/webapp
```

### Priority Filters

```
priority is high
priority above medium
priority below normal
```

### Property Filters (Inline Fields)

```
# Dataview-style inline fields
filter by function task.file.property('project') === 'webapp'
```

### Recurrence Filters

```
is recurring
is not recurring
```

### File Filters

```
path includes Projects/
path does not include Archive/
filename includes meeting
root includes Work/
folder includes Active/
```

## Sorting

```
sort by due
sort by due reverse
sort by priority
sort by description
sort by path
sort by filename
sort by created
sort by scheduled
sort by start
sort by done
sort by status.name
sort by urgency
```

### Multiple Sort Fields

```
sort by priority
sort by due
sort by description
```

Tasks sorts by first field, then second for ties, etc.

## Grouping

```
group by due
group by filename
group by folder
group by heading
group by priority
group by recurrence
group by status.name
group by tags
group by path
```

### Group Headings

```
group by due
# Shows: 2024-01-15, 2024-01-16, No due date, etc.

group by filename
# Shows: File name as heading
```

## Limiting Results

```
limit 10                    # First 10 results
limit to 5 tasks
limit groups to 3           # When grouping
limit groups 3 tasks        # 3 tasks per group
```

## Boolean Logic

### AND (default)

```
not done
due today
tags include #work
# All conditions must match
```

### OR

```
(due today) OR (priority is high)
```

### NOT

```
NOT (path includes Archive/)
```

### Complex Logic

```
(due today OR due tomorrow) AND (priority is high)
```

## Filter by Function

For advanced filtering with JavaScript:

```
filter by function task.description.length > 50
filter by function task.due.moment?.isBefore(moment().add(7, 'days'))
filter by function task.file.property('project') === 'webapp'
filter by function task.tags.includes('#urgent')
```

### Available Properties

| Property | Description |
|----------|-------------|
| `task.description` | Task text |
| `task.status.name` | Status name |
| `task.priority` | Priority number |
| `task.due.moment` | Due date (moment) |
| `task.scheduled.moment` | Scheduled date |
| `task.start.moment` | Start date |
| `task.created.moment` | Created date |
| `task.done.moment` | Done date |
| `task.file.path` | File path |
| `task.file.property(name)` | Frontmatter property |
| `task.tags` | Array of tags |
| `task.heading` | Parent heading |
| `task.isRecurring` | Boolean |
| `task.recurrence` | Recurrence rule |

## Common Queries

### Today's Tasks

````markdown
```tasks
not done
(due today) OR (scheduled today) OR (starts today)
sort by priority
```
````

### Overdue Tasks

````markdown
```tasks
not done
due before today
sort by due
```
````

### This Week's Tasks

````markdown
```tasks
not done
due after last saturday
due before next sunday
sort by due
sort by priority
```
````

### High Priority Inbox

````markdown
```tasks
not done
priority is high
no due date
```
````

### Project Tasks

````markdown
```tasks
not done
path includes Projects/webapp/
group by heading
```
````

### Completed This Week

````markdown
```tasks
done
done after last saturday
done before next sunday
sort by done reverse
```
````

### Waiting/Blocked Tasks

````markdown
```tasks
status.type is IN_PROGRESS
group by filename
```
````

### Tasks Without Dates

````markdown
```tasks
not done
no due date
no scheduled date
sort by path
```
````

## Display Options

### Hide Elements

```
hide edit button
hide backlink
hide priority
hide created date
hide start date
hide scheduled date
hide due date
hide done date
hide recurrence rule
hide task count
hide urgency
```

### Short Mode

```
short mode
# Displays tasks more compactly
```

### Explain Query

```
explain
# Shows how the query is interpreted
```

## Urgency

Tasks calculates urgency automatically based on:
- Due date proximity
- Priority level
- Scheduled date
- Start date

Sort by urgency for smart task ordering:

```
sort by urgency reverse
```

## Tips

### Quick Entry

- Use hotkey to create task with metadata
- Configure default date format in settings
- Use templates for recurring task patterns

### Organization

- Use headings to group related tasks
- Consistent tagging: `#project/name`, `#area/work`
- Archive completed tasks periodically

### Integration

- Works with Dataview inline fields
- Combine with Daily Notes for daily task views
- Use with Templater for task templates

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tasks not appearing | Check query syntax, filters |
| Dates not parsing | Use correct format: `📅 YYYY-MM-DD` |
| Recurrence not working | Complete task (don't just check box) |
| Custom status issues | Configure in Tasks settings |

## Resources

- [Tasks Documentation](https://publish.obsidian.md/tasks/)
- [Filters Reference](https://publish.obsidian.md/tasks/Queries/Filters)
- [GitHub Repository](https://github.com/obsidian-tasks-group/obsidian-tasks)
