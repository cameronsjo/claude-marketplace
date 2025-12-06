# Templater Reference

Dynamic templates with JavaScript scripting for Obsidian.

## Overview

Templater transforms static templates into dynamic, interactive powerhouses. It lets you:
- Insert dynamic variables (dates, file info, user input)
- Execute JavaScript code
- Interact with your vault programmatically
- Create reusable automation scripts

## Installation

Community Plugins → Search "Templater" → Install → Enable

**Key Settings:**
- Template folder location: `Templates/`
- Trigger on new file creation: Enable for auto-templating
- Script files folder: `Scripts/` for custom functions

## Syntax

### Basic Variables

| Syntax | Output |
|--------|--------|
| `<% tp.date.now() %>` | Current date |
| `<% tp.date.now("YYYY-MM-DD") %>` | Formatted date |
| `<% tp.file.title %>` | Current file name |
| `<% tp.file.folder() %>` | Parent folder |
| `<% tp.file.creation_date() %>` | File creation date |

### Execution Modes

```markdown
<%  %>   - Output result to note
<%* %>   - Execute JavaScript (no output)
<%- %>   - Output without escaping
```

## Date Functions

### `tp.date.now(format, offset, reference, reference_format)`

```markdown
Today: <% tp.date.now("YYYY-MM-DD") %>
Tomorrow: <% tp.date.now("YYYY-MM-DD", 1) %>
Last Monday: <% tp.date.now("YYYY-MM-DD", 0, tp.date.weekday("Monday", -1)) %>
```

### Common Formats

| Format | Example |
|--------|---------|
| `YYYY-MM-DD` | 2024-01-15 |
| `dddd, MMMM Do` | Monday, January 15th |
| `YYYY-[W]ww` | 2024-W03 |
| `HH:mm` | 14:30 |

## File Functions

### `tp.file.*`

```markdown
Title: <% tp.file.title %>
Path: <% tp.file.path() %>
Folder: <% tp.file.folder() %>
Created: <% tp.file.creation_date("YYYY-MM-DD") %>

<%* await tp.file.rename("New Name") %>
<%* await tp.file.move("Folder/Subfolder") %>
```

### Create new files

```javascript
<%*
const content = "# New Note\n\nContent here";
await tp.file.create_new(content, "new-note", "Projects/");
%>
```

## User Input

### `tp.system.prompt()`

```markdown
<%* const project = await tp.system.prompt("Project name?") %>
# <% project %>
```

### `tp.system.suggester()`

```markdown
<%*
const options = ["High", "Medium", "Low"];
const priority = await tp.system.suggester(options, options);
%>
priority: <% priority %>
```

### Suggester with different display/values

```javascript
<%*
const display = ["🔴 High", "🟡 Medium", "🟢 Low"];
const values = ["high", "medium", "low"];
const priority = await tp.system.suggester(display, values);
%>
```

## Frontmatter Generation

### Dynamic frontmatter

```markdown
---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - <%* const tag = await tp.system.prompt("Primary tag?") %><% tag %>
status: draft
---
```

### Conditional frontmatter

```javascript
<%*
const noteType = await tp.system.suggester(
  ["Project", "Meeting", "Daily"],
  ["project", "meeting", "daily"]
);
%>
---
title: <% tp.file.title %>
type: <% noteType %>
<%* if (noteType === "meeting") { %>
date: <% tp.date.now("YYYY-MM-DD") %>
attendees: []
<%* } %>
<%* if (noteType === "project") { %>
status: active
due:
<%* } %>
---
```

## Control Flow

### Conditionals

```javascript
<%* if (tp.file.folder() === "Projects") { %>
This is a project note.
<%* } else { %>
This is not a project note.
<%* } %>
```

### Loops

```javascript
<%*
const tasks = ["Task 1", "Task 2", "Task 3"];
for (const task of tasks) {
%>
- [ ] <% task %>
<%* } %>
```

## Custom Scripts

### Setup

1. Create `Scripts/` folder in vault
2. Set "Script files folder" in Templater settings
3. Create `.js` files with exported functions

### Example Script: `Scripts/utils.js`

```javascript
function formatDate(date, format) {
  // moment.js is available
  return moment(date).format(format);
}

function generateUUID() {
  return crypto.randomUUID();
}

module.exports = { formatDate, generateUUID };
```

### Using custom scripts

```markdown
<%* const utils = tp.user.utils %>
ID: <% utils.generateUUID() %>
```

## Common Templates

### Daily Note

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [daily]
---

# <% tp.date.now("dddd, MMMM Do YYYY") %>

## Morning Review
- [ ] Review calendar
- [ ] Check priorities

## Tasks
- [ ]

## Notes


## Evening Reflection
-
```

### Meeting Note

```markdown
<%*
const attendees = await tp.system.prompt("Attendees (comma-separated)?");
const topic = await tp.system.prompt("Meeting topic?");
%>
---
date: <% tp.date.now("YYYY-MM-DD HH:mm") %>
type: meeting
attendees: [<% attendees.split(",").map(a => `"${a.trim()}"`).join(", ") %>]
tags: [meeting]
---

# <% topic %>

## Attendees
<% attendees.split(",").map(a => `- ${a.trim()}`).join("\n") %>

## Agenda
1.

## Notes


## Action Items
- [ ]

## Next Steps

```

### Project Note

```markdown
<%*
const name = await tp.system.prompt("Project name?");
const status = await tp.system.suggester(
  ["🟢 Active", "🟡 Paused", "🔵 Planning"],
  ["active", "paused", "planning"]
);
await tp.file.rename(name);
%>
---
title: <% name %>
status: <% status %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags: [project]
---

# <% name %>

## Overview


## Goals
- [ ]

## Resources
-

## Notes


## Related
- [[Projects MOC]]
```

### Weekly Review

```markdown
---
week: <% tp.date.now("YYYY-[W]ww") %>
start: <% tp.date.now("YYYY-MM-DD", 0, tp.date.weekday("Monday", 0)) %>
end: <% tp.date.now("YYYY-MM-DD", 0, tp.date.weekday("Sunday", 0)) %>
tags: [weekly, review]
---

# Week <% tp.date.now("ww") %> Review

## Accomplishments
-

## Challenges
-

## Learnings
-

## Next Week Focus
1.
2.
3.

## Metrics
- Tasks completed:
- Notes created:
- Projects advanced:
```

## Advanced Patterns

### Cursor placement

```markdown
Content here...

<% tp.file.cursor() %>

More content...
```

### Include other templates

```markdown
<% tp.file.include("[[Templates/header]]") %>

Main content here

<% tp.file.include("[[Templates/footer]]") %>
```

### Execute on file creation

In Templater settings, enable "Trigger Templater on new file creation" and set folder templates.

### Startup templates

Scripts that run when Obsidian opens:
1. Create a template with your startup logic
2. Add to "Startup templates" in settings

## Debugging

### Console output

```javascript
<%* console.log("Debug value:", someVariable) %>
```

Open Developer Tools (Ctrl+Shift+I) to see output.

### Notice popups

```javascript
<%* new Notice("Template executed!") %>
```

## Integration with Other Plugins

### With Dataview

```javascript
<%*
const dv = app.plugins.plugins.dataview.api;
const projects = dv.pages("#project").where(p => p.status === "active");
%>
## Active Projects
<%* for (const p of projects) { %>
- [[<% p.file.name %>]]
<%* } %>
```

### With QuickAdd

QuickAdd can trigger Templater templates and pass variables.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Template not executing | Check Templater is enabled, file is in template folder |
| Syntax errors | Check `<%` and `%>` are balanced |
| Variables undefined | Use `<%*` for assignments before using values |
| Date wrong | Check timezone settings, use explicit formats |

## Resources

- [Templater Documentation](https://silentvoid13.github.io/Templater/)
- [GitHub Repository](https://github.com/SilentVoid13/Templater)
- [Moment.js Formats](https://momentjs.com/docs/#/displaying/format/)
