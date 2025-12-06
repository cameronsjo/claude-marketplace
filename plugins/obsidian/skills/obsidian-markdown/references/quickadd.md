# QuickAdd Reference

Workflow automation, macros, and quick capture for Obsidian.

## Overview

QuickAdd combines four powerful tools:
- **Templates** - Create notes from templates with a single command
- **Captures** - Quickly append content to existing notes
- **Macros** - Chain multiple operations together
- **Multis** - Organize choices into folders/menus

## Installation

Community Plugins → Search "QuickAdd" → Install → Enable

## Core Concepts

### Choices

A "choice" is any QuickAdd action. Types:
- Template Choice
- Capture Choice
- Macro Choice
- Multi Choice (folder of other choices)

### Settings Access

1. Settings → QuickAdd
2. Or: Command palette → "QuickAdd: Open Settings"

## Template Choices

Create notes from templates with dynamic input.

### Basic Setup

1. Add new choice → Template
2. Name it (e.g., "New Project")
3. Configure:
   - Template path: `Templates/project.md`
   - File name format: `{{VALUE}}` (prompts for name)
   - Folder: `Projects/`

### File Name Formats

| Format | Result |
|--------|--------|
| `{{VALUE}}` | Prompts for input |
| `{{DATE}}` | Current date |
| `{{DATE:YYYY-MM-DD}}` | Formatted date |
| `{{NAME}}` | Prompts for name |
| `{{VALUE:project-{{DATE}}}` | Default value |

### Template Variables

In your template, use:

```markdown
{{VALUE}}      - Main input value
{{NAME}}       - File name
{{DATE}}       - Current date
{{TIME}}       - Current time
{{MACRO:name}} - Result from macro
```

## Capture Choices

Append content to existing notes without opening them.

### Basic Setup

1. Add new choice → Capture
2. Name it (e.g., "Quick Thought")
3. Configure:
   - Capture to: `Inbox.md` or `{{DATE:YYYY-MM-DD}}.md`
   - Format: `- {{VALUE}}`
   - Insert at: End of file

### Capture Formats

```markdown
# Simple bullet
- {{VALUE}}

# Timestamped entry
- {{TIME}}: {{VALUE}}

# Task
- [ ] {{VALUE}}

# With header
\n## {{DATE:HH:mm}}\n{{VALUE}}
```

### Capture Targets

| Target | Description |
|--------|-------------|
| Static file | Always same file: `Inbox.md` |
| Dynamic date | Daily note: `Journal/{{DATE:YYYY-MM-DD}}.md` |
| Active file | Currently open note |
| Prompt | Ask each time |

### Insert Positions

- **End of file** - Append to bottom
- **Beginning of file** - Prepend to top
- **After heading** - Find heading and insert below
- **Cursor position** - Where cursor is in active file

## Macro Choices

Chain multiple operations into automated workflows.

### Creating a Macro

1. Add new choice → Macro
2. Name it (e.g., "Morning Setup")
3. Click configure (gear icon)
4. Add commands:
   - Obsidian commands
   - User scripts
   - Other QuickAdd choices
   - Wait commands

### Command Types

| Type | Description |
|------|-------------|
| Obsidian command | Any command palette action |
| User script | Custom JavaScript |
| QuickAdd choice | Run another choice |
| Wait | Pause between commands |
| Capture | Inline capture |
| Template | Inline template creation |

### Example: Morning Setup Macro

```
1. [Obsidian] Daily notes: Open today's daily note
2. [Wait] 500ms
3. [Capture] Insert morning template
4. [Obsidian] Focus on current file
```

### Variables in Macros

Pass data between macro steps:

```javascript
// In user script
module.exports = async (params) => {
  const { quickAddApi } = params;
  const value = await quickAddApi.inputPrompt("Enter task:");
  // Store for later steps
  params.variables["task"] = value;
};
```

Later steps can use `{{VALUE:task}}`.

## User Scripts

Custom JavaScript for advanced automation.

### Script Location

- Must be in your vault
- NOT in `.obsidian/` folder
- NOT in hidden folders
- Example: `Scripts/quickadd/`

### Script Structure

```javascript
module.exports = async (params) => {
  const {
    app,                    // Obsidian app instance
    quickAddApi,            // QuickAdd API
    variables,              // Shared variables
    obsidian                // Obsidian module
  } = params;

  // Your logic here

  // Optional: return value for {{MACRO:name}}
  return "result";
};
```

### QuickAdd API

```javascript
// Prompt for input
const input = await quickAddApi.inputPrompt("Question?");
const input = await quickAddApi.inputPrompt("Question?", "default");

// Suggester (dropdown)
const choice = await quickAddApi.suggester(
  ["Display 1", "Display 2"],  // What user sees
  ["value1", "value2"]         // Actual values
);

// Wide input (for longer text)
const text = await quickAddApi.wideInputPrompt("Enter description:");

// Yes/No prompt
const confirmed = await quickAddApi.yesNoPrompt("Are you sure?");

// Checkbox prompt
const selected = await quickAddApi.checkboxPrompt(
  ["Option A", "Option B", "Option C"],
  ["Option A"]  // Pre-selected
);
```

### Example: Create Task with Metadata

```javascript
module.exports = async (params) => {
  const { quickAddApi, app } = params;

  // Get task details
  const task = await quickAddApi.inputPrompt("Task description:");
  const priority = await quickAddApi.suggester(
    ["🔴 High", "🟡 Medium", "🟢 Low"],
    ["high", "medium", "low"]
  );
  const dueDate = await quickAddApi.inputPrompt("Due date (YYYY-MM-DD):");

  // Format the task
  const formattedTask = `- [ ] ${task} [priority:: ${priority}]${dueDate ? ` [due:: ${dueDate}]` : ""}`;

  // Store for capture step
  params.variables["formattedTask"] = formattedTask;
};
```

### Example: Fetch Book Info

```javascript
module.exports = async (params) => {
  const { quickAddApi } = params;

  const isbn = await quickAddApi.inputPrompt("Enter ISBN:");

  const response = await fetch(
    `https://openlibrary.org/isbn/${isbn}.json`
  );
  const data = await response.json();

  params.variables["bookTitle"] = data.title;
  params.variables["bookAuthor"] = data.authors?.[0]?.name || "Unknown";
  params.variables["bookYear"] = data.publish_date;
};
```

## Multi Choices

Organize choices into menus/folders.

### Setup

1. Add new choice → Multi
2. Name it (e.g., "Create Note")
3. Add sub-choices inside

### Example Structure

```
QuickAdd Menu
├── 📝 Create Note (Multi)
│   ├── New Project
│   ├── New Meeting
│   └── New Daily
├── 📥 Quick Capture (Multi)
│   ├── Thought
│   ├── Task
│   └── Quote
└── ⚙️ Workflows (Multi)
    ├── Morning Setup
    └── Evening Review
```

## AI Integration

QuickAdd supports AI-powered features (requires API key).

### Setup

1. Settings → AI Assistant
2. Enter OpenAI API key
3. Configure model (GPT-4, etc.)

### AI Prompts

```markdown
Format: prompt-template

Summarize the following text:
{{VALUE}}

---

Generate 3 tags for this note:
{{SELECTED}}
```

### AI in Macros

Add AI Assistant commands to macros for automated content generation.

## External Triggering

### Via URI

```
obsidian://quickadd?choice=Morning%20Setup
```

### Via Advanced URI Plugin

```
obsidian://advanced-uri?vault=MyVault&commandname=QuickAdd:%20Morning%20Setup
```

### Auto-Run on Startup

In Macro settings, enable "Run on plugin load" for startup automation.

## Common Patterns

### Daily Standup

```
Macro: Daily Standup
1. Open today's daily note
2. User script: Prompt for yesterday/today/blockers
3. Capture: Format and insert standup template
```

### Quick Web Clip

```
Macro: Web Clip
1. User script: Prompt for URL
2. User script: Fetch page metadata
3. Template: Create note with metadata
```

### Inbox Processing

```
Macro: Process Inbox
1. Open Inbox.md
2. User script: Get first item
3. Suggester: Choose destination
4. Move item to chosen location
5. Repeat or exit
```

## Keyboard Shortcuts

1. Settings → Hotkeys
2. Search "QuickAdd"
3. Assign shortcuts to frequently used choices

Recommended:
- `Cmd/Ctrl + Shift + N` - Quick capture
- `Cmd/Ctrl + Shift + M` - Open QuickAdd menu

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Choice not appearing | Enable it (lightning bolt icon) |
| Script not found | Check path, not in .obsidian |
| Variables not passing | Use `params.variables` object |
| Template errors | Check Templater syntax if combined |

## Resources

- [QuickAdd Documentation](https://quickadd.obsidian.guide/)
- [GitHub Repository](https://github.com/chhoumann/quickadd)
- [Video Tutorials](https://www.youtube.com/results?search_query=obsidian+quickadd)
