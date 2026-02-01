# Recipe: Orphan Note Cleanup

Find and resolve notes that have no connections to the rest of your knowledge graph.

## What Are Orphan Notes?

Orphan notes are files with:
- **No incoming links** - No other note links to them
- **No outgoing links** - They don't link to any other notes

These notes are "islands" in your knowledge graph, disconnected from your PKM system.

## Why Orphans Matter

- **Lost knowledge** - Great ideas buried and forgotten
- **Duplicated effort** - You might recreate content that already exists
- **Weak graph** - Fewer connections = less serendipitous discovery
- **Clutter** - Outdated notes that should be archived/deleted

## Prerequisites

- Obsidian MCP server connected
- Understanding of your vault structure
- Time for review (can't fully automate decisions)

## Step 1: Identify Orphans

### Find all notes

```markdown
List all .md files in vault recursively
```

### Build link graph

For each note:
1. Read the note content
2. Extract all `[[wiki links]]` (outgoing)
3. Record the mapping

### Compute incoming links

Invert the outgoing link map to find what links TO each note.

### Filter to orphans

Notes where:
```
incoming_links.length === 0 AND outgoing_links.length === 0
```

## Step 2: Exclude Intentional Orphans

Some notes are orphaned by design:

### Templates

```markdown
Exclude notes in "Templates/" folder
```

Templates aren't meant to be linked.

### Daily/Periodic Notes

```markdown
Exclude notes in "Journal/" or "Daily/" folders
Exclude notes matching pattern "\d{4}-\d{2}-\d{2}"
```

Daily notes connect via dates, not wiki links.

### Index/MOC Files

```markdown
Exclude notes with "MOC" or "Index" in filename
Exclude notes with tags: #moc, #index
```

These are navigation hubs that may not need incoming links.

### Attachments/Assets

```markdown
Exclude non-.md files
Exclude notes in "Assets/" or "Attachments/"
```

## Step 3: Categorize Orphans

Review each orphan and categorize:

| Category | Action | Criteria |
|----------|--------|----------|
| **Valuable** | Connect to graph | Good content, just missing links |
| **Stub** | Expand or merge | Minimal content, could be useful |
| **Outdated** | Archive | Old information, no longer relevant |
| **Duplicate** | Merge & delete | Same content exists elsewhere |
| **Junk** | Delete | Notes with no value |

## Step 4: Resolution Actions

### For Valuable Orphans

1. **Find related notes**

```markdown
Search for keywords from the orphan note's title/content
```

2. **Add incoming links**

Update related notes or MOCs to link to the orphan:

```markdown
Append "- [[orphan-note]]" to "[related-moc].md"
```

3. **Add outgoing links**

Edit the orphan to reference related content:

```markdown
In "[orphan-note].md", search-replace to add wiki links
```

### For Stub Orphans

1. **Merge into existing note**

```markdown
Read "[orphan].md"
Append content to "[existing-note].md"
Delete "[orphan].md"
```

2. **Expand with more content**

Add detail and connections, then categorize as "Valuable."

### For Outdated Orphans

1. **Archive**

```markdown
Create note "Archive/[orphan].md" with content from "[orphan].md"
Delete "[orphan].md"
```

Or add archived frontmatter:

```markdown
Set frontmatter "status" to "archived" in "[orphan].md"
Add tag "archived" to "[orphan].md"
```

### For Duplicate Orphans

1. **Identify the primary note**
2. **Merge unique content**

```markdown
Read "[orphan].md"
Read "[primary].md"
Append unique sections from orphan to primary
Delete "[orphan].md"
```

3. **Update any links** (if orphan had any)

### For Junk Orphans

```markdown
Delete "[junk-orphan].md"
```

## Automation Script

Ask Claude to run this workflow:

```markdown
Please find orphan notes in my vault:

1. List all .md files
2. Build a link graph (what links to what)
3. Find notes with no incoming AND no outgoing links
4. Exclude:
   - Templates/ folder
   - Journal/ folder
   - Files matching YYYY-MM-DD pattern
   - Notes tagged #moc or #index
5. For each orphan, show:
   - File path
   - Title/first heading
   - Created date
   - Word count
   - First 100 characters of content

Group by folder and sort by created date (oldest first).
```

## Prevention Strategies

### Link as you create

When creating a new note:
1. Add at least one outgoing link
2. Add to a relevant MOC
3. Tag appropriately

### Regular reviews

- Weekly: Quick scan of recent notes for links
- Monthly: Full orphan audit
- Quarterly: Deep cleanup session

### Use templates

Create templates that prompt for links:

```markdown
## Related
- [[]]
- [[]]

## See Also
-
```

### Dataview monitoring

Add to a dashboard:

```dataview
LIST
FROM ""
WHERE length(file.inlinks) = 0 AND length(file.outlinks) = 0
AND !contains(file.path, "Templates")
AND !contains(file.path, "Journal")
LIMIT 10
```

## Metrics to Track

| Metric | Goal |
|--------|------|
| Total orphan count | < 5% of vault |
| New orphans per week | 0 (catch them early) |
| Average links per note | > 2 |
| Notes without tags | 0 |

## Tips

- **Don't force connections** - Some notes are legitimately standalone
- **Quality over quantity** - One meaningful link beats five forced ones
- **Review oldest first** - Old orphans are most likely to be outdated
- **Batch processing** - Set aside dedicated time for cleanup
- **Document decisions** - Note why you archived/deleted for future reference
