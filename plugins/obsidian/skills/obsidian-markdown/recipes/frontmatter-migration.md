# Recipe: Frontmatter Migration

Migrate, standardize, or transform frontmatter properties across your vault.

## Use Cases

- Add required properties to notes missing them
- Rename properties (`date` → `created`)
- Transform values (`"draft"` → `"status/draft"`)
- Enforce property schema across note types
- Clean up legacy or inconsistent metadata

## Prerequisites

- Obsidian MCP server connected
- Backup your vault (recommended)
- Document your target schema

## Recipe: Add Missing Properties

**Goal:** Ensure all notes in `Projects/` have `status` and `created` properties.

### Step 1: List target notes

```markdown
List all .md files in "Projects/" recursively
```

### Step 2: Check each note

For each file:

```markdown
Get frontmatter "status" from "[file-path]"
Get frontmatter "created" from "[file-path]"
```

### Step 3: Add missing properties

If property is missing:

```markdown
Set frontmatter "status" to "active" in "[file-path]"
Set frontmatter "created" to "2024-01-15" in "[file-path]"
```

## Recipe: Rename a Property

**Goal:** Rename `date` property to `created` across all notes.

### Step 1: Find notes with old property

```markdown
Search for "date:" in frontmatter (first 50 lines of files)
```

### Step 2: Migrate each note

For each affected file:

```markdown
1. Get frontmatter "date" from "[file-path]"
2. Set frontmatter "created" to [that value] in "[file-path]"
3. Delete frontmatter "date" from "[file-path]"
```

## Recipe: Transform Property Values

**Goal:** Convert string status to hierarchical format.

| Old Value | New Value |
|-----------|-----------|
| `draft` | `status/draft` |
| `active` | `status/active` |
| `done` | `status/done` |
| `archived` | `status/archived` |

### Step 1: Find notes with old format

```markdown
Search for "status: draft" OR "status: active" OR "status: done"
```

### Step 2: Transform values

For each file, based on current value:

```markdown
Set frontmatter "status" to "status/active" in "[file-path]"
```

## Recipe: Enforce Schema by Note Type

**Goal:** Different note types require different properties.

### Project Notes Schema

```yaml
---
title: required
status: required (active|paused|done)
created: required (date)
tags: required (must include "project")
owner: optional
due: optional
---
```

### Meeting Notes Schema

```yaml
---
title: required
date: required
attendees: required (list)
tags: required (must include "meeting")
action-items: optional
---
```

### Validation Script

```markdown
For each note in "Projects/":
1. Read the note with stats
2. Check required properties exist
3. Check property types are correct
4. Report violations

For each note in "Meetings/":
1. Read the note with stats
2. Validate against meeting schema
3. Report violations
```

## Recipe: Clean Up Legacy Properties

**Goal:** Remove deprecated properties from all notes.

Deprecated properties: `old_status`, `legacy_id`, `temp_flag`

### Step 1: Search for each property

```markdown
Search for "old_status:" in vault
Search for "legacy_id:" in vault
Search for "temp_flag:" in vault
```

### Step 2: Remove from each file

```markdown
Delete frontmatter "old_status" from "[file-path]"
Delete frontmatter "legacy_id" from "[file-path]"
Delete frontmatter "temp_flag" from "[file-path]"
```

## Recipe: Bulk Property Update

**Goal:** Set `reviewed: true` on all notes modified before 2024.

### Step 1: Find old notes

```markdown
Search in vault for notes modified_until "2024-01-01"
```

### Step 2: Update each

```markdown
Set frontmatter "reviewed" to false in "[file-path]"
```

## Schema Definition Template

Document your target schema for consistency:

```yaml
# Note Type: Project
required_properties:
  - title: string
  - status: enum [active, paused, done, archived]
  - created: date
  - tags: list (must include "project")

optional_properties:
  - owner: string
  - due: date
  - priority: enum [low, medium, high]
  - related: list of links

defaults:
  status: active
  priority: medium
```

## Migration Checklist

- [ ] Document current state (what properties exist)
- [ ] Define target schema
- [ ] Backup vault
- [ ] Test on single file
- [ ] Run migration in batches
- [ ] Verify results
- [ ] Update templates to match new schema
- [ ] Document changes for future reference

## Rollback Strategy

1. **Git-based vault**: `git checkout -- .` or `git revert`
2. **Backup restore**: Copy from backup location
3. **Reverse migration**: Swap old/new values and re-run

## Tips

- **Atomic operations**: `obsidian_manage_frontmatter` is atomic - won't corrupt YAML
- **Preserve order**: Property order in frontmatter is preserved
- **Handle missing gracefully**: "get" returns null for missing properties
- **Type coercion**: Values are stored as-is; ensure correct types
- **Batch wisely**: Process 20-50 files at a time for large vaults
