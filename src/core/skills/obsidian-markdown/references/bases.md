# Bases Reference

Obsidian's native database views (v1.9+). Core plugin - not portable to GitHub.

## File Format

`.base` files use YAML. Can also embed as code blocks.

```yaml
filters:
  file.hasTag("project")

formulas:
  days_old: "(now() - file.ctime) / 86400000"

properties:
  file.name:
    displayName: Note
  status:
    displayName: Status

views:
  - type: table
    name: "Projects"
    filters:
      status != "done"
    order:
      - file.name
      - status
      - due
    sort:
      - column: due
        direction: ASC
```

## Filters

```yaml
# Simple
filters:
  status == "active"

# Compound
filters:
  and:
    - file.hasTag("project")
    - status != "done"
    - or:
        - priority == "high"
        - due < now()
```

## Property Access

```yaml
status                           # Frontmatter property
note.status                      # Explicit note property
note["Due Date"]                 # Bracket notation for spaces
file.name                        # File property
file.ctime                       # Created time
formula.days_old                 # Computed formula
```

## File Methods

```yaml
file.hasTag("tag")               # Has tag
file.hasLink("Note")             # Links to note
file.inFolder("Folder")          # In folder
file.inFolder("Folder", true)    # Recursive
```

## String/Array Methods

```yaml
name.contains("search")
name.lower()
tags.length
tags.contains("value")
tags.join(", ")
tags[0]                          # First element
```

## Functions

```yaml
now()                            # Current datetime
date("2025-01-15")               # Parse date
datetime.format("YYYY-MM-DD")    # Format
if(condition, true, false)       # Conditional
coalesce(a, b, c)                # First non-null
round(num)
```

## Views

```yaml
views:
  - type: table                  # table | card | map
    name: "View Name"
    limit: 50
    filters: status != "done"    # View-specific filter
    order: [file.name, status]
    sort:
      - column: due
        direction: ASC
    group_by: status
```

## Embed in Notes

````markdown
```base
filters:
  file.hasTag("meeting")
views:
  - type: table
    name: "Meetings"
    order: [file.name, date]
```
````

## Context-Aware

Use `this` for current file:

```yaml
filters:
  file.hasLink(this.file.name)   # Backlinks to this note
```
