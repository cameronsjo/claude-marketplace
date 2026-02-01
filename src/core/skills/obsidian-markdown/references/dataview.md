# Dataview Reference

Query vault metadata with DQL. Community plugin - not portable to GitHub.

## Query Types

```dataview
LIST FROM #tag WHERE status = "active" SORT file.mtime DESC
```

```dataview
TABLE author, rating FROM "Books" WHERE rating >= 4 SORT rating DESC
```

```dataview
TASK FROM "Projects" WHERE !completed GROUP BY file.link
```

## FROM Sources

```
FROM "Folder"                    # Folder path
FROM #tag                        # Tag
FROM [[Note]]                    # Links to note
FROM #tag AND "Folder"           # Combine
FROM -#excluded                  # Exclude
```

## WHERE Conditions

```
WHERE status = "active"
WHERE rating >= 4
WHERE contains(tags, "project")
WHERE file.ctime >= date(today) - dur(7 days)
WHERE author AND rating          # Both exist
```

## Common File Fields

| Field | Description |
|-------|-------------|
| `file.name` | Filename (no extension) |
| `file.path` | Full path |
| `file.link` | Clickable link |
| `file.ctime` | Created |
| `file.mtime` | Modified |
| `file.tags` | All tags |
| `file.tasks` | Tasks in file |
| `file.inlinks` | Incoming links |
| `file.outlinks` | Outgoing links |

## Inline DQL

```markdown
Modified: `= this.file.mtime`
Open tasks: `= length(filter(this.file.tasks, (t) => !t.completed))`
```

## Inline Fields

```markdown
Status:: Active
Due:: 2025-03-01
[hidden:: value]                 # Key hidden in reading view
```

## Useful Functions

```
contains(field, value)           # Substring/list membership
length(list)                     # Count
date(today)                      # Today's date
dur(7 days)                      # Duration
dateformat(date, "yyyy-MM-dd")   # Format date
default(field, fallback)         # Null coalescing
```

## Common Patterns

### Recent Notes
```dataview
TABLE file.mtime AS "Modified" FROM "" SORT file.mtime DESC LIMIT 10
```

### Orphan Notes
```dataview
LIST FROM "" WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
```

### By Status
```dataview
TABLE status, due FROM #project WHERE status != "done" SORT due ASC
```
