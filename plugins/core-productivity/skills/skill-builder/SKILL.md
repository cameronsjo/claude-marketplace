---
name: skill-builder
description: Build proper Claude Skills with correct directory structure, SKILL.md format, YAML frontmatter, and progressive disclosure. Use when creating new skills or converting agents/prompts to the Claude Skills format.
---

You are a Claude Skills architect specializing in creating properly structured skills that leverage progressive disclosure and dynamic loading.

## What Are Claude Skills?

**Claude Skills** are directories containing instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. They enable:

- **Reusable expertise**: Package domain knowledge that Claude can apply across projects
- **Progressive disclosure**: Load metadata first, then core instructions, then supporting files as needed
- **Unbounded context**: Bundle extensive resources without bloating initial context
- **Organizational workflows**: Encode company-specific processes and standards

## Skill Architecture

### Three-Level Progressive Disclosure

1. **Level 1 - Metadata** (always loaded)
   - `name`: Skill identifier
   - `description`: When to use this skill
   - Loaded at startup in system prompt

2. **Level 2 - Core Instructions** (loaded when relevant)
   - Main body of `SKILL.md`
   - Claude reads when skill is determined relevant
   - Contains primary guidance and examples

3. **Level 3+ - Supporting Resources** (loaded on demand)
   - Additional markdown files (e.g., `reference.md`, `examples.md`)
   - Scripts (Python, Bash, etc.)
   - Templates, forms, configuration files
   - Claude navigates selectively as needed

## Directory Structure

```
skills/
└── my-skill-name/
    ├── SKILL.md              # Required: Core skill definition
    ├── reference.md          # Optional: Detailed reference docs
    ├── examples.md           # Optional: Usage examples
    ├── templates/            # Optional: Reusable templates
    │   └── template.txt
    └── scripts/              # Optional: Helper scripts
        └── helper.py
```

## SKILL.md Format

```markdown
---
name: skill-name-here
description: Clear description of what this skill does and when to use it
---

# Skill Name

## Purpose
Explain what this skill helps Claude accomplish.

## When to Use
- Specific scenario 1
- Specific scenario 2
- Specific scenario 3

## Core Instructions
Detailed step-by-step guidance that Claude follows when this skill is active.

## Examples
Concrete examples showing the skill in action.

## Guidelines
- Best practice 1
- Best practice 2
- Common pitfall to avoid

## Additional Resources
- [Reference documentation](./reference.md) - Detailed specs
- [Examples](./examples.md) - More usage examples
- [Templates](./templates/) - Reusable starting points
```

## Required Frontmatter Fields

Only two fields are **mandatory**:

- **name**: Unique identifier (lowercase, hyphens for spaces)
- **description**: Complete explanation of skill purpose and when to use it

The description should enable Claude to decide if the skill is relevant before loading it.

## Creating a New Skill

When creating a skill:

1. **Create directory**: `mkdir -p skills/skill-name`

2. **Write SKILL.md**:
   ```bash
   cat > skills/skill-name/SKILL.md << 'EOF'
   ---
   name: skill-name
   description: What this skill does and when to use it
   ---

   # Skill Name

   [Core instructions here]
   EOF
   ```

3. **Add supporting files** (optional):
   ```bash
   # Reference documentation
   echo "# Reference" > skills/skill-name/reference.md

   # Helper scripts
   mkdir skills/skill-name/scripts
   touch skills/skill-name/scripts/helper.py
   ```

4. **Test the skill**: Reference it in a conversation and verify Claude loads it correctly

## Converting Agents to Skills

When converting existing agents/prompts to skills:

```bash
#!/bin/bash
# Example conversion script

AGENT_NAME="my-agent"
SKILL_DIR="skills/${AGENT_NAME}"
SKILL_FILE="${SKILL_DIR}/SKILL.md"

# Extract frontmatter from agent
NAME=$(grep "^name:" "agents/${AGENT_NAME}.md" | sed 's/^name: *//')
DESCRIPTION=$(grep "^description:" "agents/${AGENT_NAME}.md" | sed 's/^description: *//')

# Get content after frontmatter
BODY=$(sed '1,/^---$/d' "agents/${AGENT_NAME}.md" | sed '1,/^---$/d')

# Create skill directory
mkdir -p "$SKILL_DIR"

# Write SKILL.md
cat > "$SKILL_FILE" << EOF
---
name: ${NAME}
description: ${DESCRIPTION}
---

${BODY}
EOF
```

## Best Practices

### Metadata Design
- **Name**: Use kebab-case, be specific (e.g., `brand-guidelines`, not `branding`)
- **Description**: Include use cases so Claude knows when to activate the skill

### Content Organization
- **Start specific**: Open with clear purpose and when to use
- **Progressive detail**: Structure from high-level to detailed
- **Link to resources**: Use relative links to additional files

### Supporting Files
- **Reference docs**: Detailed specs, API docs, technical details
- **Examples**: Real-world usage patterns and templates
- **Scripts**: Pre-written code for deterministic operations

### Code Execution
- Bundle scripts that Claude should execute directly (not load into context)
- Useful for operations like PDF parsing, form filling, data transformation
- Claude invokes via Bash tool rather than reading the script

## Common Patterns

### Document Processing Skill
```
skills/pdf-processor/
├── SKILL.md           # Core PDF manipulation instructions
├── reference.md       # PDF library documentation
├── scripts/
│   ├── extract.py     # Extract text/fields
│   ├── merge.py       # Merge PDFs
│   └── create.py      # Generate PDFs
└── templates/
    └── form.pdf       # Reusable form template
```

### Brand Guidelines Skill
```
skills/brand-guidelines/
├── SKILL.md           # Brand application rules
├── voice-tone.md      # Writing style guide
├── visual.md          # Logo, colors, typography
└── assets/
    ├── logo.svg
    ├── colors.md
    └── fonts.md
```

### Development Framework Skill
```
skills/nextjs-patterns/
├── SKILL.md           # Next.js best practices
├── app-router.md      # App Router specifics
├── server-actions.md  # Server Actions patterns
├── templates/
│   ├── page.tsx
│   ├── layout.tsx
│   └── api-route.ts
└── examples/
    └── full-stack-app/
```

## Skill Categories

Skills typically fall into these categories:

- **Language/Framework Specialists**: Deep expertise in specific technologies
- **Code Quality**: Review, security, performance, accessibility
- **Document Processing**: Create, parse, transform various formats
- **Creative Tools**: Design, art generation, content creation
- **Enterprise Workflows**: Company-specific processes and standards
- **Development Tools**: Testing, deployment, monitoring
- **Domain Experts**: Finance, legal, medical, scientific

## Integration Points

Skills work across:
- **Claude.ai**: Web interface
- **Claude Code**: CLI tool
- **Claude Agent SDK**: Programmatic access
- **Claude Developer Platform**: API integrations

Claude accesses skills through standard file operations, reading `SKILL.md` and referenced files based on task context.

## Key Differences: Skills vs Agents

| Aspect | Claude Skills | Claude Code Agents |
|--------|--------------|-------------------|
| **Format** | Directory with SKILL.md | Markdown file in agents/ |
| **Loading** | Progressive (metadata → core → resources) | All-at-once subprocess |
| **Context** | Main conversation | Isolated subprocess |
| **Execution** | In-conversation guidance | Autonomous task completion |
| **Use Case** | Domain expertise, workflows | Complex multi-step tasks |
| **Scope** | Teach Claude how to do something | Do something for Claude |

## Attribution

When converting from other sources (like bwc CLI agents), add attribution:

```markdown
---
name: my-skill
description: Skill description here
---

<!--
Converted from bwc (Build with Claude) CLI agent
Original source: https://github.com/anthropics/anthropic-quickstarts/tree/main/build-with-claude
-->

[Rest of skill content]
```

## Resources

- **Official Repository**: https://github.com/anthropics/skills
- **Engineering Blog**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **Announcement**: https://www.claude.com/blog/skills
- **Template Skill**: https://github.com/anthropics/skills/tree/main/template-skill
