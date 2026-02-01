# Excalidraw Reference

Visual thinking and hand-drawn diagrams in Obsidian.

## Overview

Excalidraw integrates a powerful whiteboard into Obsidian:
- Hand-drawn aesthetic diagrams
- Bi-directional linking with notes
- Embeddable in markdown
- Script automation
- LaTeX support

## Installation

Community Plugins → Search "Excalidraw" → Install → Enable

## Creating Drawings

### Methods

1. **Command palette**: "Create new drawing"
2. **File explorer**: Right-click → "Create Excalidraw drawing"
3. **From note**: `[[Drawing.excalidraw]]` → Click to create
4. **Ribbon icon**: Click Excalidraw icon

### File Format

Excalidraw files are markdown with embedded JSON:
- `.excalidraw.md` (recommended) - Full features
- `.excalidraw` - Compatible format

## Drawing Tools

### Basic Tools

| Tool | Shortcut | Use |
|------|----------|-----|
| Selection | `1` or `V` | Select elements |
| Rectangle | `2` or `R` | Draw boxes |
| Diamond | `3` or `D` | Decision shapes |
| Ellipse | `4` or `O` | Circles, ovals |
| Arrow | `5` or `A` | Connecting arrows |
| Line | `6` or `L` | Straight lines |
| Free draw | `7` or `P` | Freehand |
| Text | `8` or `T` | Add text |
| Image | `9` | Insert images |
| Eraser | `0` or `E` | Erase elements |

### Modifier Keys

| Key | Action |
|-----|--------|
| `Shift` | Constrain proportions |
| `Alt` | Draw from center |
| `Cmd/Ctrl` | Duplicate while dragging |

## Obsidian Integration

### Linking to Notes

Create clickable links in drawings:

1. Add text element
2. Type wiki link: `[[Note Name]]`
3. Link becomes clickable

Or use the link tool:
1. Select element
2. Click link icon in properties
3. Enter note path

### Embedding in Markdown

Reference drawings in notes:

```markdown
![[Drawing.excalidraw]]
```

With size:

```markdown
![[Drawing.excalidraw|800]]
```

As SVG/PNG (transcluded):

```markdown
![[Drawing.excalidraw#^frame=Frame1|800]]
```

### Back-linking

Drawings appear in:
- Backlinks panel
- Graph view
- Search results

### Transclusion

Embed notes in drawings:

1. Drag markdown file into drawing
2. Or: Add element → Note from vault

Note content renders in the drawing.

## Frames

Create presentation frames:

1. Select elements
2. Right-click → "Add to frame"
3. Name the frame

Export specific frames:

```markdown
![[Drawing.excalidraw#^frame=Introduction]]
```

## Libraries

### Built-in Libraries

- Basic shapes
- Flowchart elements
- Icons

### Custom Libraries

1. Create element
2. Right-click → "Add to library"
3. Available across all drawings

### Community Libraries

- [Excalidraw Libraries](https://libraries.excalidraw.com/)
- Import: Drag `.excalidrawlib` into canvas

## Excalidraw Automate

Script automation for Excalidraw.

### Accessing the API

```javascript
const ea = ExcalidrawAutomate;
ea.reset();
ea.setView("active");
```

### Creating Elements

```javascript
ea.style.strokeColor = "#1e1e1e";
ea.style.backgroundColor = "#a5d8ff";
ea.style.fillStyle = "solid";

// Add rectangle
ea.addRect(0, 0, 200, 100);

// Add text
ea.addText(20, 40, "Hello World");

// Add arrow
ea.addArrow([[0,0], [100,100]]);

await ea.create();
```

### Templater Integration

Create drawing from template:

```javascript
<%*
const ea = ExcalidrawAutomate;
ea.reset();

const title = await tp.system.prompt("Title?");

ea.addText(0, 0, title, {
  fontSize: 32,
  fontFamily: 1
});

ea.addRect(-20, -20, 400, 60);

await ea.create({
  filename: title,
  folder: "Drawings"
});
%>
```

### DataviewJS Integration

Generate diagrams from data:

```javascript
const ea = ExcalidrawAutomate;
ea.reset();

const pages = dv.pages("#project");
let y = 0;

for (const page of pages) {
  ea.addText(0, y, page.file.name);
  y += 50;
}

await ea.create();
```

## Common Diagram Types

### Flowchart

```
[Start] → [Process] → {Decision} → [End]
                         ↓
                     [Alt Path]
```

1. Use rectangles for processes
2. Diamonds for decisions
3. Arrows for flow
4. Color code by type

### Mind Map

```
          [Central]
         /    |    \
    [Topic] [Topic] [Topic]
      |       |       |
   [Sub]   [Sub]   [Sub]
```

1. Central topic in middle
2. Branches radiate outward
3. Use colors for categories
4. Connect with curved lines

### System Architecture

```
┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   API       │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │
                    └─────────────┘
```

1. Boxes for components
2. Arrows for data flow
3. Groups for logical units
4. Labels on connections

### Sequence Diagram

```
User    │     App     │    API
  │         │           │
  │──request──▶│         │
  │         │──call──▶│
  │         │◀─response─│
  │◀─result──│         │
```

1. Vertical lines for actors
2. Horizontal arrows for messages
3. Order top to bottom
4. Label each interaction

## Styling

### Element Styles

- **Stroke color**: Line/border color
- **Background color**: Fill color
- **Fill style**: Hachure, cross-hatch, solid
- **Stroke width**: Thin to thick
- **Stroke style**: Solid, dashed, dotted
- **Roughness**: Hand-drawn feel (0-2)
- **Opacity**: Transparency

### Font Options

- Virgil (hand-drawn)
- Helvetica
- Cascadia (code)
- Custom fonts via settings

### Theme

- Light mode
- Dark mode
- Auto (follows Obsidian)

## Export Options

### Image Export

1. Select elements (or all)
2. Right-click → "Copy as PNG/SVG"
3. Or: File menu → Export

### Settings

- Background: transparent or colored
- Scale: 1x, 2x, 3x
- Embed scene: Include source in image
- Dark mode: Export in dark theme

### Embedding Images

Export creates linkable assets:

```markdown
![[Drawing.excalidraw.svg]]
![[Drawing.excalidraw.png]]
```

## Performance Tips

### Large Drawings

- Use frames to navigate
- Disable render on scroll if slow
- Consider splitting into multiple files

### Many Elements

- Group related elements
- Use libraries for repeated shapes
- Clean up unused elements

## Settings Worth Configuring

| Setting | Recommendation |
|---------|----------------|
| Auto-save | Enable |
| Folder for new drawings | Set default |
| Link brackets | [[link]] style |
| Default filename | Date-based |
| Embed type | Native (not SVG) |
| Theme to match Obsidian | Enable |

## Integration with ExcaliBrain

ExcaliBrain creates visual graphs from links:

1. Install ExcaliBrain plugin
2. Open any note
3. Command: "ExcaliBrain: Start"
4. See visual graph of connections

Combines Excalidraw visuals with graph analysis.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slow rendering | Reduce element count, disable effects |
| Links not working | Check [[syntax]], reload |
| Export issues | Try different format |
| Scripts not running | Check Automate enabled |

## Resources

- [Excalidraw Plugin GitHub](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [Excalidraw Automate Docs](https://zsviczian.github.io/obsidian-excalidraw-plugin/)
- [ExcaliBrain](https://github.com/zsviczian/excalibrain)
- [Excalidraw Libraries](https://libraries.excalidraw.com/)
