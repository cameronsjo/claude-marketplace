# Workflow: Capture & Inbox Processing

A system for capturing thoughts quickly and processing them effectively.

## The Capture Problem

Ideas and tasks appear at inconvenient times:
- In meetings
- While reading
- In the shower
- Just before sleep

If not captured immediately, they're lost forever.

## Capture Principles

### 1. Capture Everything

Don't filter during capture. If it crosses your mind, write it down.

### 2. Capture Quickly

Speed matters. The faster you capture, the less context switching.

### 3. Capture to One Place

All captures go to the inbox. Sort later.

### 4. Process Regularly

Inbox is temporary. Process daily, or it becomes a graveyard.

## Setting Up Your Inbox

### Option A: Single Inbox File

Create `Inbox.md` at vault root:

```markdown
# Inbox

Captured items awaiting processing. Review daily.

---

```

### Option B: Inbox Folder

Create `Inbox/` folder for separate notes:

```
Inbox/
├── 2024-01-15-meeting-idea.md
├── 2024-01-15-task-followup.md
└── 2024-01-16-article-to-read.md
```

### Option C: Daily Note Capture

Capture directly to today's daily note under a dedicated section:

```markdown
## Inbox
- Quick thought captured here
- Another thing
- Task to do
```

## Capture Methods

### Method 1: QuickAdd Capture

**Setup:**
1. Create Capture choice
2. Capture to: `Inbox.md`
3. Format: `- [ ] {{VALUE}} ➕ {{DATE:YYYY-MM-DD}}`
4. Assign hotkey (e.g., `Cmd+Shift+I`)

**Usage:**
```
Press hotkey → Type thought → Enter
Done in 2 seconds
```

### Method 2: Command Palette

```
Cmd+P → "Quick" → Select QuickAdd capture
```

### Method 3: Mobile Quick Capture

On Obsidian Mobile:
1. Add QuickAdd to mobile toolbar
2. Tap → Type → Save

### Method 4: Templater Capture

Create a capture template triggered by hotkey:

```markdown
<%*
const input = await tp.system.prompt("Capture:");
const date = tp.date.now("YYYY-MM-DD HH:mm");
const entry = `- [ ] ${input} ➕ ${date}`;
const inbox = app.vault.getAbstractFileByPath("Inbox.md");
await app.vault.append(inbox, entry + "\n");
new Notice("Captured!");
%>
```

### Method 5: External Capture

From outside Obsidian:
- **Raycast/Alfred**: Quick entry → append to file
- **iOS Shortcuts**: Share sheet → append to Inbox.md
- **Apple Notes**: Quick capture → transfer later

## Capture Formats

### Simple Capture

```markdown
- Quick thought about project X
```

### Task Capture

```markdown
- [ ] Call dentist to reschedule
```

### Timestamped Capture

```markdown
- [ ] Review report ➕ 2024-01-15 09:32
```

### Contextual Capture

```markdown
- [ ] #work Follow up with Sarah about budget
- [ ] #personal Buy birthday gift
- [ ] #read Article on PKM systems
```

### Rich Capture

```markdown
- [ ] Implement caching for API
  - From: Team meeting
  - Context: Performance issues in prod
  - Priority: High
  - Related: [[API Project]]
```

## Processing the Inbox

### When to Process

- **Daily**: Part of evening routine (5-10 min)
- **Weekly**: Full processing in weekly review
- **Trigger-based**: When inbox exceeds 10 items

### The 4 D's Framework

For each inbox item, decide:

| Decision | Action |
|----------|--------|
| **Do** | Takes < 2 min? Do it now |
| **Defer** | Add to task list with due date |
| **Delegate** | Assign to someone, track it |
| **Delete** | Not needed? Remove it |

### Processing Questions

For each item ask:

1. **What is it?**
   - Task, idea, reference, project?

2. **Is it actionable?**
   - Yes → Define next action
   - No → Reference or trash?

3. **Does it need a date?**
   - Deadline? Add due date
   - Best done on specific day? Schedule it
   - Someday? Move to someday/maybe list

4. **Where does it belong?**
   - Task list
   - Project note
   - Area/topic note
   - Reference folder
   - Someday/maybe
   - Trash

### Processing Flow

```
Inbox Item
    ↓
Is it actionable?
    ├── No → Is it useful?
    │         ├── Yes → File as reference
    │         └── No → Delete
    │
    └── Yes → What's the next action?
              ├── < 2 min → Do it now
              └── > 2 min → Where does it go?
                            ├── Task → Add to task list
                            ├── Project task → Add to project
                            └── Multi-step → Create project
```

## MCP-Assisted Processing

With Obsidian MCP tools, Claude can help process:

### Batch Categorization

```markdown
Here are my inbox items. For each one, suggest:
1. Type (task/note/reference/trash)
2. Destination (which note/project)
3. Next action if applicable
```

### Create Notes from Items

```markdown
This inbox item needs its own note:
"Research PKM systems - interested in Zettelkasten method"

Create a note in Research/ with proper frontmatter and link to relevant MOCs.
```

### Move Items to Projects

```markdown
Move this task to the correct project note:
"Fix authentication bug" → [[Projects/Auth System]]
```

## Inbox Zero Goal

The inbox should be empty (or near-empty) after each processing session.

### Not Empty? Common Causes

| Issue | Solution |
|-------|----------|
| Too many items | Capture less, or process more often |
| Items too vague | Improve capture quality |
| Don't know where to put | Create a "Decide Later" area |
| Resistance to processing | Make it easier, timebox it |

### Acceptable Non-Zero States

Sometimes items legitimately stay:
- Waiting for more info
- Need to batch with similar items
- Requires focused thinking time

Mark these explicitly:
```markdown
- [ ] Complex decision about X #waiting-for-info
```

## Template: Inbox Processing Session

```markdown
## Inbox Processing - {{date}}

### Stats
- Items in inbox: X
- Processed: Y
- Remaining: Z

### Decisions Made
- "Task X" → Added to [[Project A]] ✅
- "Idea Y" → Created [[New Note]] ✅
- "Random Z" → Deleted 🗑️

### Blocked Items
- "Thing requiring research" → #waiting

### Notes
- Need to create project for recurring theme
- Several items about Topic X - maybe create MOC?
```

## Capture Best Practices

### Capture with Context

Instead of:
```
- Call John
```

Capture:
```
- Call John about project timeline (from Monday meeting)
```

### Use Tags for Quick Routing

```
- #call Schedule dentist
- #email Send report to boss
- #buy New notebook
- #read Article on productivity
```

### Capture Links When Possible

```
- Read this article: https://example.com/article
- Follow up on [[Meeting with Client]]
```

### Voice Capture for Mobile

On mobile, use voice input for speed:
1. Trigger capture
2. Dictate thought
3. Review/edit briefly
4. Save

## Common Patterns

### Meeting Captures

During meetings, capture to inbox:
```
- [ ] #followup Send docs to Sarah
- [ ] #task Review proposal by Friday
- Interesting point about X - explore later
```

### Reading Captures

While reading:
```
- Key insight: "Quote from book"
- [ ] Apply concept X to Project Y
- Research term: Zettelkasten
```

### Idea Captures

Random thoughts:
```
- App idea: Tool that does X
- Blog post topic: How I use Obsidian
- Question: Why does Y work this way?
```

## Tools & Plugins

| Tool | Use Case |
|------|----------|
| QuickAdd | Fast capture with templates |
| Hotkeys | Instant capture triggers |
| Mobile toolbar | Phone capture |
| Raycast/Alfred | Capture from anywhere on Mac |
| iOS Shortcuts | Capture from share sheet |
| Obsidian Web Clipper | Capture web content |

## Metrics

Track inbox health:

```markdown
## Inbox Metrics
- Average items captured per day: X
- Processing frequency: daily/2x week
- Average time to process: X minutes
- Inbox zero streak: X days
```

Healthy inbox:
- Processed daily or every other day
- Rarely exceeds 15-20 items
- Processing takes < 15 minutes
- No item older than 1 week
