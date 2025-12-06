# Graph View Reference

Visualize and navigate your knowledge graph in Obsidian.

## Overview

Graph view displays your vault as a network:
- **Nodes**: Notes in your vault
- **Edges**: Links between notes
- **Visual patterns**: Clusters, hubs, orphans

## Graph Types

### Global Graph

Shows all notes in vault:
- Command: "Graph view: Open graph view"
- Hotkey: `Cmd/Ctrl + G` (default)

### Local Graph

Shows connections to current note:
- Right sidebar panel
- Command: "Graph view: Open local graph"
- More focused, less overwhelming

## Basic Controls

### Navigation

| Action | Control |
|--------|---------|
| Pan | Click + drag |
| Zoom | Scroll / pinch |
| Focus node | Click on node |
| Open note | Double-click or Cmd+click |
| Center on note | Right-click → "Reveal in graph" |

### Search & Filter

Top of graph panel:
- Search box filters visible nodes
- Shows only matching notes + connected notes

## Graph Settings

Access via gear icon in graph panel.

### Filters

| Filter | Effect |
|--------|--------|
| Search files | Show only matching names |
| Tags | Show only notes with tags |
| Attachments | Show/hide non-markdown files |
| Existing files only | Hide unresolved links |
| Orphans | Show/hide unlinked notes |

### Groups

Create color-coded groups:

1. Click "New group"
2. Enter search query (path, tag, etc.)
3. Choose color
4. Reorder for priority (first match wins)

#### Example Groups

```
Query: path:Projects     → Blue
Query: tag:#moc          → Green
Query: path:Archive      → Gray
Query: file:("2024")     → Yellow
```

### Display

| Setting | Effect |
|---------|--------|
| Arrows | Show link direction |
| Text fade threshold | When labels disappear |
| Node size | Relative to link count |
| Line thickness | Edge weight |

### Forces

Physics simulation controls:

| Force | Effect |
|-------|--------|
| Center force | Pull toward center |
| Repel force | Push nodes apart |
| Link force | Pull linked nodes together |
| Link distance | Preferred edge length |

Higher repel + lower link distance = tighter clusters.

## Graph Queries

### Filter Syntax

```
path:"Folder/Subfolder"
tag:#project
file:("keyword")
line:("text in note")
-path:Archive            # Exclude
```

### Combine Queries

```
path:Projects tag:#active
tag:#project -tag:#archived
```

## Local Graph Settings

Same settings as global, plus:

| Setting | Effect |
|---------|--------|
| Depth | Levels of connections (1, 2, 3...) |
| Collapse filter | Focus on direct connections |
| Show tags | Display tag nodes |

## Use Cases

### Discover Connections

1. Open global graph
2. Look for unexpected links
3. Follow interesting paths
4. Find bridge notes between clusters

### Find Orphans

1. Enable "Orphans" filter
2. Isolated nodes need connection
3. Or need archiving/deletion

### Identify Hubs

Largest nodes = most connected:
- MOCs (Maps of Content)
- Key concepts
- Important people/projects

### Visualize Projects

Filter to project path:
```
path:"Projects/Active"
```

See project structure and connections.

### Explore Topic

1. Open note on topic
2. Open local graph
3. Set depth to 2-3
4. See related concepts

## Color Coding Strategy

### By Folder

```
path:Projects      → Blue
path:Areas         → Green
path:Resources     → Purple
path:Archive       → Gray
```

### By Type

```
tag:#moc           → Gold
tag:#person        → Orange
tag:#concept       → Cyan
tag:#project       → Blue
```

### By Status

```
tag:#active        → Green
tag:#paused        → Yellow
tag:#archived      → Gray
```

## Graph Analysis Patterns

### Cluster Detection

Dense groups of connected notes:
- Indicate topic areas
- May need MOC to organize
- Could split into sub-vaults

### Bridge Notes

Notes connecting clusters:
- Often key concepts
- Worth developing further
- Critical for navigation

### Orphan Islands

Disconnected notes:
- Need links added
- May be outdated
- Consider archiving

### Hub Imbalance

Single notes with too many connections:
- May need splitting
- Consider sub-notes
- Review link relevance

## Graph View Plugins

### Graph Presets

Save and load graph configurations:

1. Install "Obsidian Graph Presets"
2. Configure graph settings
3. Save as preset
4. Apply to local graphs with hotkey

### Juggl

Alternative graph visualization:

- More customization
- Different layouts
- Embeddable graphs
- Style rules

### ExcaliBrain

Visual graph in Excalidraw:

- Editable graph
- Add notes visually
- Mix with drawings

## Performance

### Large Vaults

Graphs can lag with many notes:

| Optimization | Effect |
|--------------|--------|
| Filter by path | Show subset |
| Reduce depth (local) | Fewer nodes |
| Lower repel force | Less calculation |
| Hide attachments | Fewer nodes |
| Disable animations | Faster render |

### Best Practices

- Use local graph for daily work
- Filter global graph to focus
- Save presets for common views
- Close graph when not needed

## Graph in Workflow

### Morning Routine

1. Open today's daily note
2. View local graph (depth 2)
3. See connected projects/notes
4. Plan what to work on

### Research Mode

1. Filter graph to topic area
2. Expand local graph depth
3. Look for gaps in connections
4. Create bridging notes

### Weekly Review

1. Open global graph
2. Color by creation date
3. See what was created
4. Identify orphans to connect

## Common Questions

### Why are some nodes bigger?

Node size = number of connections. More links = bigger node.

### Why are some links missing?

Check:
- Unresolved links (ghost notes)
- Filtered out by settings
- In excluded folder

### How to show tags as nodes?

Local graph → Settings → "Show tags" toggle

### Can I export the graph?

Not natively. Options:
- Screenshot
- Use Juggl plugin
- External tools (Gephi, etc.)

## Graph Meditation

Spend 5 minutes:
1. Open global graph
2. Let it stabilize
3. Observe clusters
4. Notice what draws your eye
5. Follow interesting connections

This often surfaces forgotten notes or unexpected connections.

## Resources

- [Obsidian Graph Help](https://help.obsidian.md/plugins/graph)
- [Graph Presets Plugin](https://github.com/SkepticMystic/graph-presets)
- [Juggl Plugin](https://juggl.io/)
- [ExcaliBrain](https://github.com/zsviczian/excalibrain)
