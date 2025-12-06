# Recipe: Vault Health Audit

Comprehensive audit of vault structure, links, tags, and metadata consistency.

## Audit Categories

1. **Broken Links** - Wiki links pointing to non-existent notes
2. **Orphan Notes** - Notes with no incoming or outgoing links
3. **Tag Inconsistencies** - Duplicate tags, case variations, unused tags
4. **Frontmatter Issues** - Missing required properties, invalid values
5. **Structural Problems** - Empty folders, misplaced files, naming issues

## Prerequisites

- Obsidian MCP server connected
- Understanding of your vault's intended structure
- Time (large vaults may take a while)

## Audit 1: Broken Links

**Goal:** Find all wiki links pointing to non-existent notes.

### Step 1: Find all wiki links

```markdown
Search for pattern "\[\[[^\]]+\]\]" using regex in vault
```

### Step 2: Extract link targets

Parse each match to get the target note name (before `|` or `#`).

### Step 3: Verify targets exist

```markdown
List notes in vault root recursively
```

Compare link targets against actual files.

### Step 4: Report broken links

Format: `[source-file]: [[broken-link]]`

### Fix Options

- Create missing notes
- Update links to correct targets
- Remove dead links

## Audit 2: Orphan Notes

**Goal:** Find notes with no connections to the rest of the vault.

### Step 1: Build link graph

For each note in vault:
1. Read the note
2. Extract all outgoing wiki links
3. Record: `{file: [outgoing-links]}`

### Step 2: Compute incoming links

Invert the graph to find incoming links for each note.

### Step 3: Find orphans

Notes where:
- `incoming_links.length === 0` AND
- `outgoing_links.length === 0`

Exclude intentional orphans:
- Templates
- Daily notes (linked by date, not wiki links)
- Index/MOC files

### Fix Options

- Add links from relevant MOCs
- Merge content into existing notes
- Archive if obsolete
- Delete if truly unused

## Audit 3: Tag Consistency

**Goal:** Find tag issues across the vault.

### Step 1: Collect all tags

```markdown
For each .md file in vault:
  List tags in "[file-path]"
```

Build a tag frequency map: `{tag: count}`

### Step 2: Find case variations

Group tags by lowercase form:
- `#Project`, `#project`, `#PROJECT` → should be unified

### Step 3: Find low-usage tags

Tags used only 1-2 times may be:
- Typos
- Abandoned experiments
- Should be consolidated

### Step 4: Validate tag hierarchy

Check for inconsistent hierarchies:
- `#status/draft` and `#draft` (flat vs nested)
- `#project/webapp` vs `#projects/webapp` (singular vs plural)

### Report Format

```markdown
## Tag Audit Results

### Case Variations (need normalization)
- project: #Project (5), #project (12), #PROJECT (1)
- meeting: #Meeting (3), #meeting (8)

### Low Usage Tags (review for removal)
- #temp (1 use)
- #fixme (2 uses)

### Hierarchy Inconsistencies
- #draft vs #status/draft
- #work vs #area/work
```

## Audit 4: Frontmatter Validation

**Goal:** Ensure notes have required properties with valid values.

### Define Expected Schema

```yaml
# By folder
Projects/:
  required: [title, status, created]
  status_values: [active, paused, done]

Meetings/:
  required: [title, date, attendees]

Journal/:
  required: [date]
```

### Step 1: List notes by folder

```markdown
List all .md files in "Projects/"
List all .md files in "Meetings/"
List all .md files in "Journal/"
```

### Step 2: Validate each note

For each note:
1. Read the note as JSON (includes frontmatter)
2. Check required properties exist
3. Validate property values against allowed values
4. Check date formats

### Step 3: Report violations

```markdown
## Frontmatter Audit Results

### Missing Required Properties
- Projects/webapp.md: missing "created"
- Projects/api.md: missing "status"

### Invalid Property Values
- Projects/old.md: status="wip" (not in allowed values)

### Type Errors
- Meetings/jan-15.md: attendees is string, should be list
```

## Audit 5: Structural Analysis

**Goal:** Check vault organization and file hygiene.

### Check 1: Empty folders

```markdown
List folders in vault
For each folder, count .md files
Report folders with 0 files
```

### Check 2: Misplaced files

Files in wrong locations based on naming or content:
- Daily notes outside Journal/
- Templates outside Templates/
- Files with no folder

### Check 3: Naming conventions

Check for:
- Spaces vs hyphens vs underscores
- Case consistency
- Date format in filenames
- Special characters

### Check 4: Large files

Find unusually large notes that might need splitting:

```markdown
List all notes with stats
Filter to those with tokenCountEstimate > 10000
```

## Complete Audit Script

Run all audits and generate comprehensive report:

```markdown
Please audit my Obsidian vault for:
1. Broken wiki links
2. Orphan notes (excluding Templates/ and Journal/)
3. Tag inconsistencies (case variations, low usage)
4. Frontmatter issues in Projects/ (require: title, status, created)
5. Structural problems (empty folders, naming issues)

Generate a report with:
- Issue counts per category
- Specific files affected
- Suggested fixes
- Priority ranking (critical/warning/info)
```

## Post-Audit Actions

### Quick Wins (do first)

- [ ] Fix broken links (search-replace)
- [ ] Normalize tag case
- [ ] Add missing required frontmatter

### Medium Effort

- [ ] Connect orphan notes to MOCs
- [ ] Consolidate low-usage tags
- [ ] Reorganize misplaced files

### Larger Projects

- [ ] Restructure folder hierarchy
- [ ] Migrate to new frontmatter schema
- [ ] Split oversized notes

## Scheduling

- **Weekly**: Quick broken link check
- **Monthly**: Full tag audit
- **Quarterly**: Complete vault health audit

## Tips

- **Start small**: Audit one folder at a time for large vaults
- **Fix as you go**: Don't let issues accumulate
- **Automate checks**: Create Dataview queries for ongoing monitoring
- **Document decisions**: Record why you organized things a certain way
