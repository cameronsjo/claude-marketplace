# MCP Integration Reference

Deep integration guide for Obsidian MCP tools. This reference covers the actual MCP tools available and patterns for effective vault operations.

## Available MCP Tools

### File Discovery

#### `obsidian_list_notes`

List files and subdirectories within a vault folder.

```
Parameters:
- dirPath: string (required) - Vault-relative path ("developer/notes", "/" for root)
- recursionDepth: integer - 0 for no recursion, -1 for infinite (default)
- fileExtensionFilter: string[] - Filter by extension ([".md"])
- nameRegexFilter: string - Regex pattern to filter by name

Returns:
- Formatted tree string of contents
- Total entry count
```

**Examples:**

```markdown
# List all markdown files in Projects folder
List notes in "Projects" with .md extension

# Find all files matching a pattern
List notes matching "meeting-*" in "Journal/2024"

# Shallow listing (no recursion)
List top-level folders only in vault root
```

### Reading Notes

#### `obsidian_read_note`

Read content and metadata of a file.

```
Parameters:
- filePath: string (required) - Vault-relative path
- format: "markdown" | "json" - Output format (default: markdown)
- includeStat: boolean - Include file stats (default: false)

Returns:
- content: File content (string or NoteJson object)
- stats: { creationTime, modifiedTime, tokenCountEstimate }
```

**Examples:**

```markdown
# Read a specific note
Read "Projects/webapp/README.md"

# Read with stats for context
Read "Journal/2024-01-15.md" with stats

# Get structured JSON for programmatic access
Read "Templates/daily.md" as JSON
```

### Searching

#### `obsidian_global_search`

Search across the vault using text or regex.

```
Parameters:
- query: string (required) - Search query or regex pattern
- useRegex: boolean - Treat query as regex (default: false)
- caseSensitive: boolean - Case-sensitive search (default: false)
- searchInPath: string - Limit to specific folder
- modified_since: string - Filter by modification date ("2 weeks ago", "2024-01-15")
- modified_until: string - Filter until date
- contextLength: integer - Characters around matches (default: 100)
- maxMatchesPerFile: integer - Limit matches per file (default: 5)
- page: integer - Pagination (default: 1)
- pageSize: integer - Results per page (default: 50)

Returns:
- results: Array of { path, filename, ctime, mtime, matches[] }
- pagination: { currentPage, totalPages }
- totalFiles, totalMatches
```

**Examples:**

```markdown
# Simple text search
Search for "API endpoint" in vault

# Regex search for patterns
Search for pattern "TODO:?\s+\w+" using regex

# Scoped search with date filter
Search "meeting notes" in "Journal" modified since "1 week ago"

# Find broken links
Search for pattern "\[\[.*\]\]" using regex, then verify targets exist
```

### Modifying Notes

#### `obsidian_update_note`

Modify notes using whole-file operations.

```
Parameters:
- targetType: "filePath" | "activeFile" | "periodicNote"
- targetIdentifier: string - Path or period ("daily", "weekly")
- content: string (required) - Content to add
- modificationType: "wholeFile" (required)
- wholeFileMode: "append" | "prepend" | "overwrite"
- createIfNeeded: boolean - Create if missing (default: true)
- overwriteIfExists: boolean - Allow overwrite (default: false)
- returnContent: boolean - Return final content (default: false)

Returns:
- success, message, timestamp, stats
```

**Examples:**

```markdown
# Append to daily note
Append "## Meeting Notes\n- Discussed roadmap" to today's daily note

# Prepend warning to a file
Prepend "> [!warning] Outdated\n> This doc needs review" to "docs/old-api.md"

# Create new note
Create "Projects/new-project.md" with initial content
```

#### `obsidian_search_replace`

Perform search-and-replace operations within notes.

```
Parameters:
- targetType: "filePath" | "activeFile" | "periodicNote"
- targetIdentifier: string
- replacements: Array of { search: string, replace: string }
- useRegex: boolean - Treat search as regex (default: false)
- caseSensitive: boolean - Case-sensitive (default: true)
- replaceAll: boolean - Replace all occurrences (default: true)
- flexibleWhitespace: boolean - Treat whitespace flexibly (default: false)
- wholeWord: boolean - Match whole words only (default: false)
- returnContent: boolean - Return final content (default: false)

Returns:
- success, message, replacementCount, timestamp, stats
```

**Examples:**

```markdown
# Rename a tag across a file
In "Projects/webapp.md", replace "#status/draft" with "#status/active"

# Fix broken links
In "index.md", replace "[[Old Name]]" with "[[New Name]]"

# Regex replacement
In "notes/*.md", replace pattern "(\d{4})-(\d{2})-(\d{2})" with "$2/$3/$1"
```

### Frontmatter Management

#### `obsidian_manage_frontmatter`

Atomically manage YAML frontmatter properties.

```
Parameters:
- filePath: string (required) - Vault-relative path
- operation: "get" | "set" | "delete"
- key: string (required) - Property name
- value: any - Value for "set" operation (string, number, boolean, array, object)

Returns:
- For "get": The property value
- For "set"/"delete": success confirmation
```

**Examples:**

```markdown
# Get a property
Get frontmatter "status" from "Projects/webapp.md"

# Set a property
Set frontmatter "status" to "active" in "Projects/webapp.md"

# Set a list property
Set frontmatter "tags" to ["project", "webapp", "typescript"] in "Projects/webapp.md"

# Delete a property
Delete frontmatter "draft" from "Projects/webapp.md"
```

### Tag Management

#### `obsidian_manage_tags`

Manage tags in both frontmatter and inline content.

```
Parameters:
- filePath: string (required) - Vault-relative path
- operation: "add" | "remove" | "list"
- tags: string[] - Tag names without # prefix

Returns:
- For "list": Array of all tags in the note
- For "add"/"remove": success confirmation
```

**Examples:**

```markdown
# List all tags in a note
List tags in "Projects/webapp.md"

# Add tags
Add tags ["priority/high", "review-needed"] to "Projects/webapp.md"

# Remove tags
Remove tags ["draft", "wip"] from "Projects/webapp.md"
```

### Deleting Notes

#### `obsidian_delete_note`

Permanently delete a file from the vault.

```
Parameters:
- filePath: string (required) - Vault-relative path

Returns:
- success confirmation
```

**Example:**

```markdown
# Delete a note
Delete "Archive/old-draft.md"
```

## Tool Composition Patterns

### Pattern 1: Search → Read → Update

Find files matching criteria, read them, make targeted updates.

```markdown
1. Search for notes with "status: draft" in frontmatter
2. For each result, read the full note
3. Update frontmatter status to "review"
4. Add review-requested tag
```

### Pattern 2: List → Filter → Batch Process

List directory, filter by criteria, process in batch.

```markdown
1. List all notes in "Projects/" recursively
2. Filter to those modified in last 7 days
3. For each, check if has required frontmatter
4. Report missing properties
```

### Pattern 3: Audit → Report → Fix

Comprehensive vault health check.

```markdown
1. Search for broken wiki links using regex
2. List all orphan notes (no inlinks)
3. Find duplicate tags (case variations)
4. Generate report with fix suggestions
5. Optionally apply fixes
```

## Error Handling

All MCP tools return structured responses. Common error patterns:

| Error | Cause | Solution |
|-------|-------|----------|
| File not found | Path doesn't exist | Check path, use list_notes to verify |
| Permission denied | Vault locked or readonly | Check Obsidian is running, vault unlocked |
| Invalid frontmatter | Malformed YAML | Read file, fix YAML syntax |
| Search timeout | Query too broad | Add path filter, use pagination |

## Performance Tips

1. **Use `searchInPath`** - Scope searches to relevant folders
2. **Pagination** - Use page/pageSize for large result sets
3. **Batch operations** - Group related updates together
4. **Avoid full vault scans** - Use specific paths when possible
5. **Cache file lists** - List once, filter in memory

## See Also

- `recipes/bulk-tag-update.md` - Batch tag operations
- `recipes/frontmatter-migration.md` - Property schema updates
- `recipes/vault-health-audit.md` - Comprehensive vault analysis
- `mcp-server.md` - MCP server setup guide
