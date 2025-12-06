# Plugin Guide

Understanding how Claude Code plugins work and how to get the most out of them.

## Plugin Components

Each plugin can contain three types of components:

### Commands

Slash commands that trigger specific workflows. Start with `/` in your Claude Code session.

```bash
/commit          # Create a well-formatted git commit
/review.security # Run a security audit
/test-gen        # Generate tests for your code
```

### Agents

Specialized AI personas that Claude can become for specific tasks. Agents are invoked automatically when appropriate or via the Task tool.

```
code-reviewer    # Reviews code for quality, security, maintainability
python-expert    # Deep Python expertise for complex patterns
security-auditor # Finds vulnerabilities and security issues
```

### Skills

Contextual knowledge and patterns that enhance Claude's capabilities. Skills are loaded when relevant to provide domain expertise.

```
api-design       # REST API design patterns and standards
obsidian-markdown # Obsidian-specific markdown conventions
mcp-development  # MCP server development patterns
```

## Plugin Categories

### Essential (Everyone)

| Plugin | Purpose |
|--------|---------|
| **core-productivity** | Git workflows, code review, project checks |

### Language-Specific

| Plugin | Languages/Frameworks |
|--------|---------------------|
| **python-toolkit** | Python, uv, pytest, async |
| **typescript-toolkit** | TypeScript, React, Next.js, Node |

### Domain-Specific

| Plugin | Domain |
|--------|--------|
| **api-development** | REST APIs, OpenAPI, microservices |
| **security-suite** | OWASP, vulnerability detection |
| **mcp-development** | Model Context Protocol servers |
| **data-science** | SQL, ML pipelines, data engineering |
| **cloud-ops** | AWS/Azure/GCP, Kubernetes, Terraform |

### Workflow

| Plugin | Workflow |
|--------|----------|
| **pr-workflow** | Pull request reviews and automation |
| **dx-tools** | Debugging, optimization, developer experience |
| **research-tools** | Research and information gathering |

### Personal

| Plugin | Purpose |
|--------|---------|
| **obsidian-pkm** | Personal knowledge management with Obsidian |

## How Plugins Work Together

Plugins are designed to complement each other:

```
core-productivity (base)
    ├── python-toolkit (language support)
    │   └── security-suite (security checks)
    │
    └── api-development (API design)
        └── security-suite (API security)
```

## Best Practices

### 1. Start with Core

Always install `core-productivity` first - it provides essential git and code review workflows.

### 2. Add Language Support

Install the toolkit for your primary language(s):
- Python → `python-toolkit`
- TypeScript/JavaScript → `typescript-toolkit`

### 3. Layer in Domain Plugins

Add domain-specific plugins as needed:
- Building APIs → `api-development`
- Security-sensitive → `security-suite`
- Cloud infrastructure → `cloud-ops`

### 4. Use Workflow Plugins

Enhance your development workflow:
- Team collaboration → `pr-workflow`
- Debugging → `dx-tools`
- Research → `research-tools`

## Tips for Effective Use

### Triggering Commands

Commands are triggered with `/`:

```bash
/commit          # After making changes
/check           # Before committing
/ready           # When ready to create a PR
/review.security # Before deployment
```

### Working with Agents

Agents activate automatically when Claude determines they're needed, or you can request them:

```
"Use the security-auditor agent to review this code"
"Have the python-expert look at this async implementation"
```

### Leveraging Skills

Skills provide background knowledge. Reference them when you need specific expertise:

```
"Following the api-design skill patterns, design an endpoint for..."
"Use obsidian-markdown conventions for this note"
```

## Command Authoring Tips

### Reducing Context Usage with `disable-model-invocation`

By default, Claude Code loads all command metadata into context so it can suggest and invoke commands automatically. For commands that are:

- **One-time setup** (e.g., `setup.linting`, `init-project`)
- **Rarely used** (e.g., `modernize-deps`, `create-onboarding-guide`)
- **Large prompts** that consume significant context

Add `disable-model-invocation: true` to the frontmatter:

```yaml
---
description: Setup code linting and quality tools
allowed-tools: Bash(npm *)
disable-model-invocation: true
---
```

This removes the command's metadata from context, reducing token usage. The command still works when manually invoked with `/command-name`.

**When to use:**

- Setup/initialization commands (run once per project)
- Specialized utilities (rarely needed)
- Commands with large prompt bodies
- Any command you only invoke manually

**When NOT to use:**

- Frequently used commands (`/commit`, `/check`, `/ready`)
- Commands Claude should suggest proactively (`/review.security`)
- Workflow commands that benefit from auto-suggestion
