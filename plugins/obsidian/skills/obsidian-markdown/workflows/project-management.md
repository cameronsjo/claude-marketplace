# Workflow: Project Management in Obsidian

Manage projects, track progress, and maintain momentum using Obsidian.

## Overview

Obsidian can be a powerful project management system:
- **Flexible**: Adapt to any methodology
- **Connected**: Link projects to notes, people, resources
- **Queryable**: Dataview surfaces what matters
- **Integrated**: Projects live with your knowledge base

## Project Structure

### Single Project Note

For smaller projects (< 20 tasks):

```markdown
---
title: Website Redesign
status: active
start: 2024-01-01
due: 2024-03-01
owner: [[People/Me]]
tags: [project]
---

# Website Redesign

## Overview
Redesign company website for better conversion.

## Goals
- [ ] Improve load time by 50%
- [ ] Increase signup rate by 20%
- [ ] Mobile-first responsive design

## Tasks
### Phase 1: Design
- [x] Stakeholder interviews ✅ 2024-01-10
- [x] Competitive analysis
- [ ] Design mockups 📅 2024-01-20
- [ ] Design review meeting

### Phase 2: Development
- [ ] Frontend implementation
- [ ] Backend integration
- [ ] Performance optimization

### Phase 3: Launch
- [ ] QA testing
- [ ] Staging deployment
- [ ] Production launch

## Resources
- [[Design Brief]]
- [[Brand Guidelines]]
- [Figma mockups](https://figma.com/...)

## Meeting Notes
- [[2024-01-05 - Kickoff Meeting]]
- [[2024-01-12 - Design Review]]

## Log
### 2024-01-15
Completed stakeholder interviews. Key insight: mobile usage is 70%.

### 2024-01-10
Project kickoff. Team aligned on goals.
```

### Project Folder

For larger projects:

```
Projects/
└── Website Redesign/
    ├── README.md           # Project overview
    ├── Tasks.md            # Task list
    ├── Notes/              # Working notes
    │   ├── research.md
    │   └── decisions.md
    ├── Meetings/           # Meeting notes
    │   └── 2024-01-05.md
    └── Resources/          # Reference docs
```

## Project Frontmatter Schema

```yaml
---
title: Project Name
type: project
status: active | paused | done | archived
priority: high | medium | low
start: YYYY-MM-DD
due: YYYY-MM-DD
owner: "[[People/Name]]"
team:
  - "[[People/Person1]]"
  - "[[People/Person2]]"
tags:
  - project
  - area/work
related:
  - "[[Related Project]]"
  - "[[Goal or OKR]]"
---
```

## Status Workflow

```
idea → planning → active → review → done → archived
```

| Status | Meaning |
|--------|---------|
| `idea` | Just captured, not committed |
| `planning` | Defining scope, tasks, resources |
| `active` | Currently being worked on |
| `paused` | Temporarily on hold |
| `review` | Work complete, needs review |
| `done` | Successfully completed |
| `archived` | Completed and closed |

## Task Management

### Task Syntax

Using Tasks plugin:

```markdown
- [ ] Task description 📅 2024-01-20 ⏫
- [x] Completed task ✅ 2024-01-15
- [/] In progress task
- [-] Cancelled task
```

### Task with Context

```markdown
- [ ] Review design mockups 📅 2024-01-20 ⏫
  - Assigned: [[People/Designer]]
  - Depends on: Design completion
  - Notes: Focus on mobile views
```

### Inline Fields (Dataview)

```markdown
- [ ] Review mockups [due:: 2024-01-20] [assigned:: Designer] [effort:: 2h]
```

## Project Views with Dataview

### Active Projects

```dataview
TABLE
  status,
  due,
  owner
FROM #project
WHERE status = "active"
SORT due ASC
```

### Project Tasks

```dataview
TASK
FROM "Projects/Website Redesign"
WHERE !completed
SORT due ASC
```

### All Tasks Due This Week

```dataview
TASK
FROM #project
WHERE !completed AND due <= date(today) + dur(7 days)
SORT due ASC
GROUP BY file.link
```

### Project Progress

```dataview
TABLE
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  length(filter(file.tasks, (t) => !t.completed)) as "Remaining",
  round(length(filter(file.tasks, (t) => t.completed)) / length(file.tasks) * 100) + "%" as "Progress"
FROM #project
WHERE status = "active"
```

## Kanban Approach

Using the Kanban plugin:

### Create Kanban Board

1. Create `Projects/Board.md`
2. Add kanban syntax:

```markdown
---
kanban-plugin: basic
---

## Backlog
- [ ] Task 1
- [ ] Task 2

## In Progress
- [ ] Task 3

## Review
- [ ] Task 4

## Done
- [x] Task 5
```

### Kanban Settings

Configure lanes, colors, and archive behavior in plugin settings.

## Project Templates

### Template: New Project

```markdown
---
title: {{VALUE:Project Name}}
type: project
status: planning
priority: medium
start: {{DATE:YYYY-MM-DD}}
due:
owner: "[[People/Me]]"
tags: [project]
---

# {{VALUE:Project Name}}

## Overview
What is this project and why does it matter?

## Goals
- [ ] Goal 1
- [ ] Goal 2

## Success Criteria
- Measurable outcome 1
- Measurable outcome 2

## Scope
### In Scope
-

### Out of Scope
-

## Tasks
- [ ] Define requirements
- [ ] Create plan
- [ ]

## Resources
-

## Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| | | |

## Timeline
- **Start**: {{DATE}}
- **Milestone 1**:
- **Due**:

## Log

### {{DATE}}
Project created.
```

### QuickAdd: Create Project

1. Template choice: "New Project"
2. Template path: `Templates/project.md`
3. File name: `Projects/{{VALUE}}.md`

## Weekly Project Review

Part of your weekly review:

### Review Each Active Project

```markdown
## Project Reviews

### Project A
- **Progress**: What happened this week?
- **Blockers**: What's stuck?
- **Next**: What's the next action?
- **Status**: Still active? Needs pause?

### Project B
...
```

### Questions to Ask

1. What did I accomplish?
2. What's the next concrete action?
3. Is this project still relevant?
4. Are there blockers I need to escalate?
5. Does the due date still make sense?

## Project MOC (Map of Content)

Central hub for all projects:

```markdown
---
title: Projects
tags: [moc, project]
---

# Projects

## Active
```dataview
TABLE status, due, owner
FROM #project
WHERE status = "active"
SORT due ASC
```

## Paused
```dataview
LIST
FROM #project
WHERE status = "paused"
```

## Recently Completed
```dataview
TABLE done as "Completed"
FROM #project
WHERE status = "done"
SORT done DESC
LIMIT 5
```

## By Area
### Work
- [[Project A]]
- [[Project B]]

### Personal
- [[Project C]]

## Archive
[[Projects Archive]]
```

## Integration Patterns

### Link to Goals/OKRs

```markdown
## Related to
- [[2024 Goals#Career]] - Supports promotion goal
- [[Q1 OKRs#Launch Product]] - Key result 2
```

### Link to People

```markdown
## Team
- [[People/Alice]] - Design lead
- [[People/Bob]] - Development
- [[People/Carol]] - PM
```

### Link to Meeting Notes

```markdown
## Meetings
- [[2024-01-05 - Project Kickoff]]
- [[2024-01-12 - Design Review]]
```

### Link to Decisions

```markdown
## Key Decisions
- [[ADR-001 - Use React]] - Frontend framework choice
- [[ADR-002 - PostgreSQL]] - Database selection
```

## Automation

### QuickAdd: Add Task to Project

```javascript
module.exports = async (params) => {
  const { quickAddApi, app } = params;

  // Get active projects
  const projects = app.vault.getMarkdownFiles()
    .filter(f => f.path.startsWith("Projects/"));

  const projectNames = projects.map(p => p.basename);
  const selected = await quickAddApi.suggester(projectNames, projects);

  const task = await quickAddApi.inputPrompt("Task:");
  const priority = await quickAddApi.suggester(
    ["⏫ High", "🔼 Medium", "Normal", "🔽 Low"],
    ["⏫", "🔼", "", "🔽"]
  );

  const entry = `- [ ] ${task} ${priority}`.trim();
  await app.vault.append(selected, `\n${entry}`);
  new Notice(`Added to ${selected.basename}`);
};
```

### Templater: Project Status Update

```javascript
<%*
const status = await tp.system.suggester(
  ["🟢 Active", "🟡 Paused", "🔵 Review", "✅ Done"],
  ["active", "paused", "review", "done"]
);
await tp.frontmatter.set("status", status);
%>
```

## Common Patterns

### Sprint/Cycle Planning

```markdown
## Sprint 23 (Jan 15-28)

### Goals
1. Complete feature X
2. Fix critical bugs

### Committed
- [ ] Task 1 (3 pts)
- [ ] Task 2 (2 pts)
- [ ] Task 3 (1 pt)

Total: 6 points

### Stretch
- [ ] Nice to have task
```

### Milestone Tracking

```markdown
## Milestones

### M1: Design Complete (Jan 20) ✅
- [x] Mockups approved
- [x] Design system documented

### M2: MVP Ready (Feb 15)
- [ ] Core features implemented
- [ ] Basic testing complete

### M3: Launch (Mar 1)
- [ ] Full testing
- [ ] Documentation
- [ ] Marketing ready
```

### Risk Register

```markdown
## Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| Designer leaves | Low | High | Cross-train team | PM |
| API changes | Medium | Medium | Version lock deps | Dev |
```

## Tips

### Keep It Simple

- Start with single-file projects
- Add structure only when needed
- Don't over-engineer the system

### Regular Reviews

- Daily: Check today's project tasks
- Weekly: Review all active projects
- Monthly: Archive completed, reassess priorities

### Link Liberally

- Connect projects to related notes
- Reference meeting notes
- Link to relevant people
- Build the knowledge graph

### Use Templates

- Consistent project structure
- Pre-populated sections
- QuickAdd for fast creation
