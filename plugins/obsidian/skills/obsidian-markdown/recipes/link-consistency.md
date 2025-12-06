# Recipe: Link Consistency Check

Ensure wiki links are consistent, valid, and follow your vault's conventions.

## Link Issues to Check

1. **Broken links** - Links to non-existent notes
2. **Case mismatches** - `[[Note]]` vs `[[note]]`
3. **Alias inconsistency** - Same note linked with different display text
4. **Path variations** - `[[note]]` vs `[[folder/note]]`
5. **Duplicate targets** - Multiple notes with same name in different folders
6. **Unlinked mentions** - Text that should be linked but isn't

## Prerequisites

- Obsidian MCP server connected
- Understanding of your linking conventions

## Check 1: Broken Links

### Find all wiki links

```markdown
Search for pattern "\[\[[^\]]+\]\]" using regex in vault
```

### Parse link targets

For each match, extract:
- Target note name (before `|` if aliased)
- Section reference (after `#` if present)
- Display text (after `|` if aliased)

### Verify targets exist

```markdown
List all .md files in vault recursively
```

Compare extracted targets against file list.

### Report broken links

```markdown
## Broken Links Found

| Source File | Broken Link | Suggestion |
|-------------|-------------|------------|
| Projects/webapp.md | [[API Docs]] | Create note or fix typo |
| Journal/2024-01-15.md | [[Meeting Notes#Action Items]] | Section doesn't exist |
```

### Fix Options

1. **Create missing notes**

```markdown
Create "API Docs.md" with basic template
```

2. **Fix typos**

```markdown
In "Projects/webapp.md", replace "[[API Docs]]" with "[[API Documentation]]"
```

3. **Remove dead links**

```markdown
In "Projects/webapp.md", replace "[[API Docs]]" with "API Docs"
```

## Check 2: Case Consistency

Obsidian links are case-insensitive, but inconsistent casing looks messy and can cause issues with external tools.

### Find case variations

```markdown
Search for pattern "\[\[" to find all links
Group by lowercase target
Identify targets with multiple case variations
```

### Example Issues

```markdown
## Case Inconsistencies

Target "project-planning":
- [[Project-Planning]] (5 occurrences)
- [[project-planning]] (3 occurrences)
- [[Project-planning]] (1 occurrence)

Recommendation: Standardize to [[project-planning]]
```

### Fix with search-replace

```markdown
Search in vault for "[[Project-Planning]]"
Replace with "[[project-planning]]"
```

## Check 3: Alias Consistency

When using display text (`[[note|Display Text]]`), ensure consistency.

### Find aliased links

```markdown
Search for pattern "\[\[[^\]]+\|[^\]]+\]\]" using regex
```

### Group by target

```markdown
## Alias Inconsistencies

Target "api-documentation":
- [[api-documentation|API Docs]] (10 uses)
- [[api-documentation|API Documentation]] (5 uses)
- [[api-documentation|API Reference]] (2 uses)
- [[api-documentation]] (8 uses, no alias)

Recommendation: Pick one standard display text
```

### Standardize

```markdown
In affected files, replace:
- "[[api-documentation|API Documentation]]" → "[[api-documentation|API Docs]]"
- "[[api-documentation|API Reference]]" → "[[api-documentation|API Docs]]"
```

## Check 4: Path Consistency

Choose a convention: short links (`[[note]]`) or full paths (`[[folder/note]]`).

### Find path variations

```markdown
## Path Inconsistencies

Note "meeting-template" exists at "Templates/meeting-template.md"

Links found:
- [[meeting-template]] (12 uses)
- [[Templates/meeting-template]] (3 uses)

Recommendation: Use short form [[meeting-template]]
```

### Standardize to short form

Obsidian resolves short links automatically. Prefer them unless disambiguation is needed.

```markdown
Replace "[[Templates/meeting-template]]" with "[[meeting-template]]"
```

## Check 5: Duplicate Note Names

Notes with the same name in different folders cause ambiguous links.

### Find duplicates

```markdown
List all .md files in vault
Group by filename (ignoring path)
Report names appearing more than once
```

### Example Issues

```markdown
## Duplicate Note Names

"README.md" exists in:
- /README.md
- Projects/webapp/README.md
- Projects/api/README.md

Links to [[README]] are ambiguous!
```

### Resolution Options

1. **Rename to be unique**
   - `README.md` → `Home.md`
   - `Projects/webapp/README.md` → `webapp-overview.md`

2. **Use full paths in links**
   - `[[Projects/webapp/README]]`

3. **Add aliases**
   - Add `aliases: [webapp-readme]` to frontmatter
   - Link as `[[webapp-readme]]`

## Check 6: Unlinked Mentions

Find text that matches note names but isn't linked.

### Strategy

1. Build list of all note names and aliases
2. Search for those strings as plain text
3. Filter out already-linked occurrences

### Example

```markdown
Note "TypeScript" exists

Found unlinked mentions:
- Projects/webapp.md: "We use TypeScript for the frontend"
- Journal/2024-01-10.md: "Learning TypeScript today"

These could be linked as [[TypeScript]]
```

### Bulk link

```markdown
In "Projects/webapp.md", replace "TypeScript" with "[[TypeScript]]"
```

**Caution:** Don't over-link. Not every mention needs to be a link.

## Automated Audit Script

```markdown
Please audit link consistency in my vault:

1. Find all wiki links
2. Check for:
   - Broken links (target doesn't exist)
   - Case variations of same target
   - Alias inconsistencies
   - Full path vs short link mixed usage
   - Duplicate note names
3. Generate report with:
   - Issue type
   - Affected files
   - Current state
   - Recommended fix
4. Group by severity (broken = critical, others = warning)
```

## Conventions to Document

Create a `Conventions.md` note documenting your choices:

```markdown
# Linking Conventions

## Link Style
- Use short links: [[note]] not [[folder/note]]
- Exception: When disambiguation is needed

## Casing
- All lowercase with hyphens: [[project-planning]]
- Exception: Proper nouns [[TypeScript]]

## Aliases
- Standard display text for common notes:
  - [[api-docs|API Documentation]]
  - [[ts|TypeScript]]

## When to Link
- First mention in a note
- Key concepts and terms
- People and projects
- Don't link: common words, every occurrence
```

## Prevention

### Templates with link placeholders

```markdown
## Related
- [[]]
```

### Linter plugin

Use Obsidian Linter to enforce link conventions automatically.

### Regular audits

- Weekly: Check for broken links (quick)
- Monthly: Full consistency audit
