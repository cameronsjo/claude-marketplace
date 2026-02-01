# Recipe: Bulk Tag Update

Update, rename, or normalize tags across multiple notes in your vault.

## Use Cases

- Rename a tag across all notes (`#wip` → `#status/in-progress`)
- Add tags to notes matching criteria
- Remove deprecated tags
- Normalize tag hierarchy (`#Project` → `#project`)

## Prerequisites

- Obsidian MCP server connected
- Backup your vault (recommended)

## Recipe: Rename a Tag

**Goal:** Rename `#draft` to `#status/draft` across all notes.

### Step 1: Find affected notes

```markdown
Search for "#draft" in the vault
```

This uses `obsidian_global_search` to find all notes containing the tag.

### Step 2: Review scope

Before making changes, review the search results:
- How many files are affected?
- Are there any false positives (e.g., "#draft" in code blocks)?

### Step 3: Apply the rename

For each affected file:

```markdown
In "[file-path]":
1. Remove tag "draft"
2. Add tag "status/draft"
```

This uses `obsidian_manage_tags` with:
- `operation: "remove"`, `tags: ["draft"]`
- `operation: "add"`, `tags: ["status/draft"]`

### Step 4: Verify

```markdown
Search for "#draft" - should return no results
Search for "#status/draft" - should show all updated notes
```

## Recipe: Add Tags by Folder

**Goal:** Add `#area/work` to all notes in `Work/` folder.

### Step 1: List target notes

```markdown
List all .md files in "Work/" recursively
```

### Step 2: Add tag to each

For each file in the results:

```markdown
Add tag "area/work" to "[file-path]"
```

## Recipe: Normalize Tag Case

**Goal:** Fix inconsistent tag casing (`#Project`, `#PROJECT`, `#project`).

### Step 1: Search for variations

```markdown
Search for "#Project" case-insensitive
Search for "#PROJECT" case-sensitive
```

### Step 2: Standardize to lowercase

For files with uppercase variants:

```markdown
In "[file-path]":
1. Remove tag "Project" (or "PROJECT")
2. Add tag "project"
```

## Recipe: Remove Deprecated Tags

**Goal:** Remove `#old-system` from all notes.

### Step 1: Find and count

```markdown
Search for "#old-system" in vault
```

### Step 2: Bulk remove

For each affected file:

```markdown
Remove tag "old-system" from "[file-path]"
```

## Recipe: Tag Hierarchy Migration

**Goal:** Migrate flat tags to hierarchical structure.

| Old Tag | New Tag |
|---------|---------|
| `#meeting` | `#type/meeting` |
| `#project` | `#type/project` |
| `#idea` | `#type/idea` |
| `#work` | `#area/work` |
| `#personal` | `#area/personal` |

### Approach

Process one tag at a time:

```markdown
1. Search for "#meeting"
2. For each result:
   - Remove "meeting"
   - Add "type/meeting"
3. Repeat for next tag
```

## Safety Checklist

- [ ] Vault backed up
- [ ] Test on single file first
- [ ] Review search results before bulk update
- [ ] Verify results after completion
- [ ] Check for unintended changes in code blocks

## Rollback

If something goes wrong:

1. Use git to revert if vault is version-controlled
2. Restore from backup
3. Reverse the operation (swap add/remove)

## Tips

- **Dry run first**: Ask Claude to show what would change before applying
- **Process in batches**: For large updates, process 10-20 files at a time
- **Check code blocks**: Tags in code blocks may be false positives
- **Preserve inline tags**: `obsidian_manage_tags` handles both frontmatter and inline tags
