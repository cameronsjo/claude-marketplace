---
paths: plugins/*/skills/*/SKILL.md
---

# Skill Development Rules

Skills provide domain expertise that loads progressively into the main conversation.

## Required Structure

```yaml
---
name: skill-name
description: Clear description of what this skill does and when to use it
---

[Skill content with progressive disclosure]
```

## Directory Layout

```
skills/skill-name/
├── SKILL.md              # Required: Core skill definition
├── README.md             # Optional: Usage documentation
├── resources/            # Optional: Supporting files
│   ├── reference.md      # Detailed specs
│   ├── examples.md       # Usage examples
│   └── templates/        # Reusable templates
└── scripts/              # Optional: Helper scripts
```

## Progressive Disclosure (Three Levels)

1. **Level 1 - Metadata** (always loaded)
   - `name` and `description` from frontmatter
   - Loaded at startup in system prompt

2. **Level 2 - Core Instructions** (loaded when relevant)
   - Main body of `SKILL.md`
   - Claude reads when skill is determined relevant

3. **Level 3+ - Supporting Resources** (loaded on demand)
   - Additional markdown files
   - Scripts, templates, configuration
   - Claude navigates selectively as needed

## Best Practices

- **Descriptive frontmatter**: The description determines when Claude activates the skill
- **Start specific**: Open with clear purpose and use cases
- **Progressive detail**: High-level overview first, then detailed sections
- **Link to resources**: Use relative links `[reference](./resources/reference.md)`
- **Bundle scripts**: Include scripts Claude should execute, not read

## Skill vs Agent

Use skills for ongoing expertise (how to do something). Use agents for autonomous tasks (do something for me).

## Example SKILL.md

```yaml
---
name: api-documentation
description: Create comprehensive API documentation following OpenAPI standards. Use when documenting REST APIs, generating client libraries, or reviewing API design.
---

# API Documentation Skill

## When to Use
- Documenting new API endpoints
- Generating OpenAPI/Swagger specs
- Creating developer-facing API guides
- Reviewing API design for consistency

## Core Approach
1. Identify all endpoints and their purposes
2. Document request/response schemas
3. Include authentication requirements
4. Provide usage examples
5. Note rate limits and error codes

## Resources
- [OpenAPI Reference](./resources/openapi-spec.md)
- [Example Templates](./resources/templates/)
```
