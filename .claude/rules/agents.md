---
paths: plugins/*/agents/*.md
---

# Agent Development Rules

Agents are specialized subprocesses launched via the Task tool. They run in isolated context with their own system prompt.

## Required Structure

```yaml
---
name: agent-name
description: Clear description of what this agent does and when to use it
category: optional-category  # e.g., quality-security, development
---

[Agent system prompt body here]
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (kebab-case) |
| `description` | Yes | When/why to use this agent |
| `category` | No | Grouping for organization |

## Agent vs Skill

| Aspect | Agent | Skill |
|--------|-------|-------|
| Execution | Isolated subprocess | In main conversation |
| Context | Fresh, no conversation history | Inherits conversation |
| Use case | Autonomous multi-step tasks | Domain expertise, guidance |
| Loading | All-at-once | Progressive (metadata first) |

Use agents when the task requires isolated, focused execution. Use skills when you need ongoing expertise in the main conversation.

## Best Practices

- **Clear persona**: Start with "You are a [role] specializing in..."
- **Structured approach**: Include numbered steps or phases
- **Concrete examples**: Show expected output formats
- **Tool guidance**: Specify which tools to use for what
- **Exit criteria**: Define what "done" looks like

## Example Agent

```yaml
---
name: security-auditor
description: Security reviews, vulnerability assessment, and OWASP compliance. Use PROACTIVELY for security audits.
category: quality-security
---

You are a senior security engineer conducting a thorough security audit.

## Review Focus
- OWASP Top 10 vulnerabilities
- Secrets/credentials exposure
- Input validation gaps
- Authentication/authorization issues

## Process
1. Scan codebase for security-sensitive patterns
2. Check for exposed secrets (API keys, tokens, passwords)
3. Review input validation at system boundaries
4. Assess authentication and authorization logic
5. Generate prioritized findings report

## Output Format
[Structured findings with severity levels]
```
