# Properties & Metadata Schema Guide

Design and manage structured metadata across your Obsidian vault.

## Overview

Properties (frontmatter) enable:
- Consistent metadata structure
- Powerful queries with Dataview/Bases
- Type safety and validation
- Scalable organization

## Properties Basics

### YAML Frontmatter

Properties live at the top of notes:

```yaml
---
title: My Note
status: active
created: 2024-01-15
tags:
  - project
  - work
---
```

### Property Types

| Type | Format | Example |
|------|--------|---------|
| Text | `key: "value"` | `title: "My Note"` |
| Number | `key: 123` | `priority: 1` |
| Boolean | `key: true` | `published: false` |
| Date | `key: YYYY-MM-DD` | `created: 2024-01-15` |
| DateTime | `key: YYYY-MM-DDTHH:mm` | `due: 2024-01-15T14:00` |
| List | `key: [a, b, c]` | `tags: [work, project]` |
| Link | `key: "[[Note]]"` | `owner: "[[People/John]]"` |

### Multiline Values

```yaml
---
description: |
  This is a longer description
  that spans multiple lines.
---
```

## Schema Design Principles

### 1. Consistency Over Flexibility

Define standard properties for each note type:

```yaml
# Every project note has these
title: required
status: required (enum)
created: required (date)
tags: required (list)
```

### 2. Type Discipline

Use appropriate types:

```yaml
# Good
priority: 1                    # Number for sorting
due: 2024-01-15               # Date for date queries
active: true                  # Boolean for filtering

# Avoid
priority: "high"              # String - harder to sort
due: "next week"              # Ambiguous
active: "yes"                 # String instead of boolean
```

### 3. Namespace Properties

Prefix related properties:

```yaml
project_status: active
project_priority: high
project_owner: "[[Person]]"
```

Or use nested structure:

```yaml
project:
  status: active
  priority: high
  owner: "[[Person]]"
```

### 4. Avoid Over-Engineering

Start minimal, add properties as needed:

```yaml
# Start here
title:
status:
tags:

# Add later when needed
priority:
due:
owner:
```

## Note Type Schemas

### Daily Note

```yaml
---
date: 2024-01-15           # Required, ISO date
day: Monday                # Derived, day name
week: 2024-W03             # Derived, week number
tags:
  - daily
energy: 7                  # Optional, 1-10 scale
mood: good                 # Optional, enum
---
```

### Project Note

```yaml
---
title: Website Redesign
type: project
status: active             # idea|planning|active|paused|review|done|archived
priority: high             # high|medium|low
created: 2024-01-01
due: 2024-03-01
owner: "[[People/Jane]]"
team:
  - "[[People/John]]"
  - "[[People/Alice]]"
tags:
  - project
  - area/work
related:
  - "[[Q1 Goals]]"
---
```

### Meeting Note

```yaml
---
title: Weekly Standup
type: meeting
date: 2024-01-15T10:00
attendees:
  - "[[People/Jane]]"
  - "[[People/John]]"
project: "[[Projects/Website]]"
tags:
  - meeting
  - recurring
---
```

### Person Note

```yaml
---
name: Jane Doe
type: person
role: Engineering Manager
company: "[[Companies/Acme]]"
email: jane@example.com
tags:
  - person
  - team
---
```

### Reference Note

```yaml
---
title: Article Title
type: reference
source: https://example.com/article
author: Author Name
date_read: 2024-01-15
rating: 4                  # 1-5
tags:
  - reference
  - topic/pkm
---
```

### Book Note

```yaml
---
title: Atomic Habits
type: book
author: James Clear
isbn: "978-0735211292"
status: reading            # to-read|reading|finished|abandoned
started: 2024-01-01
finished:
rating:
tags:
  - book
  - topic/productivity
---
```

## Property Enums

Define allowed values for consistent data:

### Status Values

```yaml
# Project status
status: active | paused | done | archived

# Content status
status: draft | review | published | deprecated

# Task status
status: todo | in-progress | blocked | done
```

### Priority Values

```yaml
# Option A: Text
priority: high | medium | low

# Option B: Numbers (sortable)
priority: 1 | 2 | 3

# Option C: Emoji
priority: 🔴 | 🟡 | 🟢
```

### Type Values

```yaml
type: project | meeting | person | reference | book | article | note
```

## Queryability Patterns

### Optimized for Dataview

```yaml
# Good - easy to query
status: active
priority: 1
due: 2024-01-15

# Query
WHERE status = "active" AND priority <= 2 AND due < date(today)
```

### Inline Fields

Alternative to frontmatter:

```markdown
Status:: Active
Priority:: High
Due:: 2024-01-15
```

Query the same way:
```
WHERE status = "Active"
```

### List Properties

```yaml
tags:
  - project
  - work
  - area/development
```

Query:
```
WHERE contains(tags, "project")
```

## Validation Strategies

### Manual Checklist

Before saving, verify:
- [ ] Required properties present
- [ ] Values match allowed enums
- [ ] Dates in ISO format
- [ ] Links use [[syntax]]

### Templater Validation

```javascript
<%*
const status = tp.frontmatter.status;
const validStatuses = ["active", "paused", "done", "archived"];
if (!validStatuses.includes(status)) {
  new Notice(`Invalid status: ${status}`);
}
%>
```

### Dataview Audit

```dataview
TABLE status, created
FROM #project
WHERE !contains(list("active","paused","done","archived"), status)
```

Finds projects with invalid status.

### Linter Plugin

Configure Obsidian Linter for:
- Required frontmatter keys
- YAML formatting
- Date formats

## Metadata Menu Plugin

Advanced property management:

### Features

- Property type definitions
- Dropdown selectors for enums
- Autocomplete for links
- Bulk updates
- Field validation

### FileClass System

Define schemas per note type:

```yaml
# fileClass: Project
fields:
  - name: status
    type: select
    options:
      - active
      - paused
      - done
  - name: priority
    type: number
    min: 1
    max: 5
  - name: owner
    type: link
    folder: People
```

Apply to notes:
```yaml
---
fileClass: Project
status: active
priority: 2
owner: "[[People/Jane]]"
---
```

## Migration Patterns

### Adding New Property

1. Define the property
2. Set default value
3. Batch update existing notes

```markdown
For all notes in Projects/:
- Add "priority: medium" if missing
```

### Renaming Property

1. Search for old property
2. Add new property with same value
3. Remove old property

```markdown
For all notes with "date:" property:
- Copy value to "created:"
- Remove "date:"
```

### Changing Property Type

```markdown
# Old: priority as text
priority: high

# New: priority as number
priority: 1

# Migration map:
high → 1
medium → 2
low → 3
```

## Best Practices

### Do

- Keep schemas simple
- Document your schema
- Use consistent naming (snake_case or camelCase)
- Set sensible defaults
- Review/audit periodically

### Don't

- Over-engineer from the start
- Create properties you don't query
- Mix naming conventions
- Leave properties undocumented
- Forget to migrate old notes

## Schema Documentation Template

Create `_Schema.md` in your vault:

```markdown
# Vault Schema

## Note Types

### Project
Required: title, status, created, tags
Optional: due, owner, priority

### Meeting
Required: title, date, attendees
Optional: project, action_items

## Property Definitions

### status
Type: enum
Values: active, paused, done, archived
Default: active

### priority
Type: number
Range: 1-5
Default: 3

### created
Type: date
Format: YYYY-MM-DD
Default: today

## Conventions

- Dates always ISO format
- Links always [[bracketed]]
- Tags lowercase with hyphens
- Types singular not plural
```

## MCP-Assisted Schema Management

Claude can help maintain schemas:

### Audit Frontmatter

```markdown
Audit all notes in Projects/ for:
- Missing required properties (title, status, created)
- Invalid status values
- Malformed dates
Generate a report of violations.
```

### Bulk Updates

```markdown
For all project notes missing "priority":
Set priority to "medium"
```

### Schema Migration

```markdown
Migrate all notes from old schema to new:
- Rename "date" to "created"
- Convert status "wip" to "active"
- Add type: "project" if missing
```

## Integration Points

### With Dataview

```dataview
TABLE status, priority, due
FROM #project
WHERE status = "active"
SORT priority ASC
```

### With Bases

```yaml
filters:
  file.hasTag("project")
  status == "active"
views:
  - type: table
    order: [title, status, priority, due]
```

### With Templater

Auto-populate from prompts:

```yaml
---
title: <% tp.file.title %>
status: <%* const s = await tp.system.suggester(["active","paused"], ["active","paused"]) %><% s %>
created: <% tp.date.now("YYYY-MM-DD") %>
---
```

### With Tasks

Combine frontmatter and task metadata:

```yaml
---
project: webapp
---

- [ ] Task for this project [project:: webapp]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| YAML parse error | Check indentation, quotes |
| Property not querying | Verify exact key name |
| Date not recognized | Use ISO format: YYYY-MM-DD |
| List not working | Use proper YAML list syntax |
| Link not resolving | Quote the [[brackets]] |

## Resources

- [Obsidian Properties Help](https://help.obsidian.md/properties)
- [Metadata Menu Plugin](https://mdelobelle.github.io/metadatamenu/)
- [Dataview Metadata](https://blacksmithgu.github.io/obsidian-dataview/annotation/metadata-pages/)
- [YAML Specification](https://yaml.org/spec/1.2.2/)
