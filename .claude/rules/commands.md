---
paths: plugins/*/commands/*.md
---

# Command Development Rules

Commands are slash commands invoked via `/command-name` in Claude Code.

## Required Structure

```yaml
---
description: Brief description of what the command does
argument-hint: "[optional-args]"  # Shows in autocomplete
allowed-tools: Bash, Read, Write, Edit  # Restrict available tools
---

[Command prompt body here]
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Yes | One-line description shown in `/` menu |
| `argument-hint` | No | Placeholder text like `[file]` or `[--flag]` |
| `allowed-tools` | No | Comma-separated tool restrictions |
| `disable-model-invocation` | No | Set `true` to keep out of AI context |

## Best Practices

- **Be specific**: Description should clearly indicate what the command does
- **Use allowed-tools**: Restrict to only necessary tools for safety
- **Use disable-model-invocation**: For utility commands that don't need AI reasoning about them
- **Keep prompts focused**: Commands should do one thing well
- **Include examples**: Show expected input/output in the prompt body

## Example Command

```yaml
---
description: Run project checks and fix any errors without committing
argument-hint: "[--fix]"
allowed-tools: Bash, Read, Edit, Grep, Glob
---

Run the project's check command (lint, type-check, test) and fix any errors found.

1. Identify the check command from package.json or Makefile
2. Run the check command
3. If errors are found, fix them
4. Re-run checks until passing
5. Do NOT commit changes
```
