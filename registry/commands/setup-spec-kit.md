---
description: Setup or update GitHub's Spec Kit for Spec-Driven Development with intelligent merge of local modifications
category: tooling-setup
argument-hint: "[--update-only]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Claude Command: Setup Spec Kit

Setup or update GitHub's Spec Kit using the official CLI, with intelligent merging of customized templates.

## Usage

Setup Spec Kit in current directory:
```
/setup-spec-kit
```

Update existing Spec Kit (preserving customizations):
```
/setup-spec-kit --update-only
```

## What This Command Does

### Step 1: Check if specify CLI is installed

```bash
which specify || echo "not found"
```

If not found, show installation instructions and exit:
```
Error: 'specify' CLI not found

Install with:
  uv pip install spec-kit
  # or: pip install spec-kit
  # or: pipx install spec-kit

Then re-run: /setup-spec-kit
```

### Step 2: Backup existing customized templates (if updating)

If `.specify/` exists and `--update-only` flag is present:

1. Check for customized templates (templates that differ from spec-kit defaults):
   ```bash
   # Check each template for customizations
   for template in .specify/templates/*.md; do
     # Compare with default to detect customizations
   done
   ```

2. Create backup of customized templates:
   ```bash
   mkdir -p .specify/.backup-$(date +%Y%m%d-%H%M%S)
   cp .specify/templates/*.md .specify/.backup-*/
   ```

3. Report: "✓ Backed up N customized templates"

### Step 3: Run specify init

Run the official Spec Kit initialization:

```bash
specify init --here --ai claude --force
```

This handles:
- Downloading latest Spec Kit templates
- Setting up .specify/ directory structure
- Configuring Claude Code integration
- Creating helper scripts (.specify/scripts/)
- Setting up example specs

Let `specify` do all the heavy lifting for setup!

### Step 4: Merge customized templates (if updating)

If we created a backup in Step 2, intelligently merge customizations:

For each backed-up template:

1. **Detect customization type:**
   - Check if template has custom sections added
   - Check if template sections were modified
   - Check if template structure was changed

2. **Smart merge strategy:**

   **If template has ADDED sections** (custom content):
   - Keep new template structure from `specify init`
   - Append custom sections at the end
   - Add comment: `<!-- Custom sections below -->`

   **If template has MODIFIED sections**:
   - Create `.custom` file alongside new template
   - Keep both versions for manual review
   - Report: "Template X has modifications, review .specify/templates/X.md.custom"

   **If template is heavily customized**:
   - Keep new template as `.new` file
   - Restore customized version as main template
   - Report: "Template X heavily customized, new version saved as X.md.new"

3. **Report merge results:**
   ```
   ✓ Merged customizations:
     - spec.md: Added 2 custom sections
     - adr.md: Unchanged (using new version)
     - research.md: Needs review (see research.md.custom)
   ```

### Step 5: Cleanup and report

1. Clean up backup if merge was clean:
   ```bash
   # Only remove backup if no manual merges needed
   rm -rf .specify/.backup-*
   ```

2. Display summary:
   ```
   ✓ Spec Kit setup complete

   Location: .specify/
   Templates: .specify/templates/
   Scripts: .specify/scripts/bash/

   [If fresh install:]
   Next steps:
   1. Review templates in .specify/templates/
   2. Create feature: .specify/scripts/bash/create-new-feature.sh --json --short-name "my-feature"
   3. Read guide: .specify/README.md

   [If update with manual merges needed:]
   ⚠️  Manual merge needed:
   - .specify/templates/research.md.custom (modified template)
   - .specify/templates/plan.md.new (heavily customized, review new version)

   Compare and merge:
   1. diff .specify/templates/research.md .specify/templates/research.md.custom
   2. Manually merge desired changes
   3. Remove .custom/.new files when done

   Backup preserved: .specify/.backup-20251113-095500/

   Documentation: https://github.com/github/spec-kit
   ```

## Merge Strategy Details

### Auto-merge (Safe)
- New/updated template sections merged automatically
- Custom sections at end of templates preserved
- Helper scripts updated (non-customizable)
- README.md updated with latest info

### Manual merge required
- Templates with modified sections → `.custom` file created
- Heavily customized templates → `.new` file created with updates
- User reviews and merges manually

### Detecting customizations

A template is "customized" if:
- Has sections not in default template
- Has content that differs from default in key sections
- Has structural changes (reordering, removal)

Compare by checking for:
- Section headers that don't exist in defaults
- Content between standard section headers that differs significantly
- Missing standard sections

## Important Notes

- **Uses official CLI**: Leverages `specify init` for all setup
- **Preserves customizations**: Smart merge keeps your template changes
- **Safe updates**: Backups created, manual merge when conflicts
- **Idempotent**: Safe to run multiple times
- **Force mode**: Uses `--force` to allow updates in place

## Error Handling

- If `specify` not installed → show install instructions, exit
- If `specify init` fails → show full error, exit
- If backup fails → warn but continue
- If merge conflicts → create .custom/.new files, report to user
- If git operations fail → report error with context

## What Gets Customized vs. What Gets Updated

**Always updated (not customizable):**
- Helper scripts in `.specify/scripts/`
- `.specify/README.md`
- Directory structure

**Preserve customizations:**
- Templates in `.specify/templates/*.md`
- Any added markdown files
- Custom sections in templates

## Flags

- `--update-only`: Update mode, preserves and merges customizations
- (no flag): Fresh install or update, same behavior

## Example Workflow

**Initial setup:**
```bash
/setup-spec-kit
# Edit .specify/templates/spec.md to add custom sections
```

**Update months later:**
```bash
/setup-spec-kit --update-only
# Your custom sections preserved, new template features added
```

---

**Last Updated:** 2025-11-13
**Version:** 2.1 - Built on specify CLI
**Spec Kit CLI:** https://github.com/github/spec-kit
