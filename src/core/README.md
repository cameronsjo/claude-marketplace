# Core Plugin

Consolidated collection of agents, commands, and skills from the claude-marketplace.

## Contents

- **46 agents** - Specialized assistants for various domains (API, cloud, data, security, etc.)
- **38 commands** - Slash commands for common workflows
- **26 skills** - Composite skill packages with resources and templates

## Installation

```bash
/plugin install core@cameronsjo
```

## Categories

### Agents

| Domain | Agents |
|--------|--------|
| API/Web | api-documenter, api-security-audit, graphql-architect, frontend-developer |
| Cloud | cloud-architect, deployment-engineer, terraform-specialist, network-engineer |
| Data | data-analyst, data-engineer, data-scientist, database-optimizer, ml-engineer |
| Development | debugger, code-reviewer, dx-optimizer, error-detective |
| Research | academic-researcher, comprehensive-researcher, research-coordinator |
| Security | security-auditor, mcp-security-auditor |
| Language | python-expert, typescript-expert, javascript-expert, sql-expert |
| MCP | mcp-expert, mcp-server-architect, mcp-testing-engineer |

### Commands

| Category | Commands |
|----------|----------|
| Workflow | check, clean, commit, ready, turbo |
| Context | catchup, context-prime, explore |
| Code Analysis | review.api, review.architecture, review.security |
| PR | pr.fix, pr.review |
| Roadmap | roadmap.add, roadmap.suggest, roadmap.spec |
| Testing | test-gen |

### Skills (Composite)

Multi-file skill packages with resources, templates, and sub-commands:

- **api-design** - API development patterns
- **cloud-native-checklist** - Cloud deployment checklists
- **deep-research** - Research methodology
- **executive-presence** - Communication frameworks
- **mcp-development** - MCP server building
- **prompt-engineering** - Prompt design patterns
- **python-development** - Python best practices
- **security-review** - Security audit workflows
- **session-continuity** - Session management
