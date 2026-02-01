# Canvas Reference

Obsidian's infinite canvas for visual thinking and spatial organization.

## Overview

Canvas provides an infinite 2D space for:
- Visual brainstorming and mind mapping
- Spatial organization of notes
- Flowcharts and diagrams
- Mood boards and collections
- Presentation planning

## Creating Canvas Files

### Methods

1. **Command palette**: "Create new canvas"
2. **File explorer**: Right-click → New canvas
3. **From note**: Link to non-existent `.canvas` file → Create

### File Format

Canvas files are JSON with `.canvas` extension:

```json
{
  "nodes": [],
  "edges": []
}
```

## Node Types

### Text Card

Standalone text content:

```json
{
  "id": "abc123",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 100,
  "text": "Card content here"
}
```

### File Card

Embed existing notes:

```json
{
  "id": "def456",
  "type": "file",
  "file": "Notes/My Note.md",
  "x": 300,
  "y": 0,
  "width": 400,
  "height": 300
}
```

### Link Card

Embed web content:

```json
{
  "id": "ghi789",
  "type": "link",
  "url": "https://example.com",
  "x": 0,
  "y": 200,
  "width": 400,
  "height": 300
}
```

### Group

Container for organizing nodes:

```json
{
  "id": "jkl012",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 600,
  "height": 400,
  "label": "Group Name"
}
```

## Edges (Connections)

Connect nodes with arrows:

```json
{
  "id": "edge1",
  "fromNode": "abc123",
  "toNode": "def456",
  "fromSide": "right",
  "toSide": "left",
  "color": "1",
  "label": "relates to"
}
```

### Edge Properties

| Property | Values |
|----------|--------|
| `fromSide` | `top`, `right`, `bottom`, `left` |
| `toSide` | `top`, `right`, `bottom`, `left` |
| `color` | `1`-`6` (theme colors) or hex |
| `label` | Text label on edge |
| `fromEnd` | `none`, `arrow` |
| `toEnd` | `none`, `arrow` |

## Color Palette

Canvas uses numbered colors (`1`-`6`):

| Number | Default Color |
|--------|--------------|
| `1` | Red |
| `2` | Orange |
| `3` | Yellow |
| `4` | Green |
| `5` | Cyan |
| `6` | Purple |

Apply via right-click menu or JSON:

```json
{
  "id": "node1",
  "type": "text",
  "color": "4",
  "text": "Green card"
}
```

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New text card | Double-click empty space |
| New card from clipboard | `Cmd/Ctrl + V` |
| Connect nodes | Drag from edge |
| Select all | `Cmd/Ctrl + A` |
| Delete selected | `Delete` / `Backspace` |
| Zoom to fit | `Cmd/Ctrl + Shift + F` |
| Pan | Space + drag |
| Zoom | Scroll / pinch |

## Use Cases

### Mind Mapping

```
          [Main Topic]
         /     |      \
    [Branch]  [Branch]  [Branch]
      |         |         |
   [Leaf]    [Leaf]    [Leaf]
```

1. Create central text card
2. Add branch cards around it
3. Connect with edges
4. Color code by theme

### Project Planning

```
[Backlog] → [In Progress] → [Review] → [Done]
   │            │             │          │
[Task]      [Task]        [Task]     [Task]
[Task]      [Task]
[Task]
```

### Concept Mapping

Connect related notes visually:

1. Drag notes onto canvas (creates file cards)
2. Connect with labeled edges
3. Add text cards for annotations
4. Group related concepts

### Storyboarding

1. Create sequence of cards left-to-right
2. Add images/screenshots
3. Connect with arrows showing flow
4. Group into scenes/sections

## Canvas JSON Structure

Complete example:

```json
{
  "nodes": [
    {
      "id": "start",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 200,
      "height": 80,
      "color": "4",
      "text": "Start Here"
    },
    {
      "id": "note1",
      "type": "file",
      "file": "Projects/Project A.md",
      "x": 300,
      "y": 0,
      "width": 400,
      "height": 300
    },
    {
      "id": "group1",
      "type": "group",
      "x": -20,
      "y": -20,
      "width": 750,
      "height": 350,
      "label": "Overview"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "start",
      "toNode": "note1",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow",
      "label": "leads to"
    }
  ]
}
```

## Programmatic Canvas Creation

### With MCP Tools

Claude can create canvas files programmatically:

```markdown
Create a canvas at "Diagrams/system-architecture.canvas" with:
- A "Frontend" group containing cards for React, Next.js
- A "Backend" group containing cards for API, Database
- Arrows showing data flow between them
```

### Canvas JSON Generator

```javascript
function createCanvas(nodes, edges) {
  return JSON.stringify({ nodes, edges }, null, 2);
}

function textCard(id, text, x, y, opts = {}) {
  return {
    id,
    type: "text",
    x,
    y,
    width: opts.width || 250,
    height: opts.height || 100,
    text,
    color: opts.color
  };
}

function fileCard(id, file, x, y, opts = {}) {
  return {
    id,
    type: "file",
    file,
    x,
    y,
    width: opts.width || 400,
    height: opts.height || 300
  };
}

function edge(fromNode, toNode, opts = {}) {
  return {
    id: `${fromNode}-${toNode}`,
    fromNode,
    toNode,
    fromSide: opts.fromSide || "right",
    toSide: opts.toSide || "left",
    toEnd: opts.arrow ? "arrow" : "none",
    label: opts.label
  };
}
```

## Advanced Canvas Plugin

For enhanced capabilities, install [Advanced Canvas](https://github.com/Developer-Mike/obsidian-advanced-canvas):

### Additional Features

- **Canvas Commands**: Efficient manipulation commands
- **Presentation Mode**: Use canvas as slides
- **Stickers**: Quick-add emoji/icons
- **Better Arrows**: More arrow styles
- **Canvas Portals**: Embed canvases in canvases

### Presentation Mode

Convert canvas to presentation:
1. Create groups for each "slide"
2. Number groups (1, 2, 3...)
3. Enter presentation mode
4. Navigate with arrow keys

## Integration Patterns

### Canvas as Index

Create visual MOC:

1. New canvas for topic area
2. Drag in relevant notes
3. Arrange spatially
4. Connect related notes
5. Add navigation groups

### Canvas for Planning

1. Create brainstorm canvas
2. Add ideas as text cards
3. Group into themes
4. Refine into tasks
5. Link to project note

### Canvas + Daily Notes

Reference canvas in daily notes:

```markdown
## Planning
See [[Project Canvas.canvas]] for visual overview
```

## Tips

### Organization

- Use groups liberally
- Color code by type/status
- Keep related items close
- Leave breathing room

### Performance

- Large canvases may lag
- Consider splitting huge canvases
- File cards are heavier than text cards

### Navigation

- Use zoom to fit often
- Create "home base" area
- Use groups as landmarks

## Limitations

- No collaborative editing
- Limited undo history
- Can't embed canvases in notes (without plugins)
- No built-in templates

## Resources

- [Obsidian Canvas Help](https://help.obsidian.md/Plugins/Canvas)
- [Canvas JSON Schema](https://github.com/obsidianmd/obsidian-api/blob/master/canvas.d.ts)
- [Advanced Canvas Plugin](https://github.com/Developer-Mike/obsidian-advanced-canvas)
