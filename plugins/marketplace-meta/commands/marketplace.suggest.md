---
description: Suggest a new plugin based on current project context or described need
category: development
argument-hint: "[description or --from-context]"
allowed-tools: Bash, Read, Glob, Grep, Task
---

# Claude Command: Marketplace Suggest

## Usage

```bash
/marketplace.suggest GraphQL development    # Suggest plugin for GraphQL
/marketplace.suggest --from-context         # Analyze current project, suggest plugins
/marketplace.suggest "E2E testing with Playwright"
```

## What This Command Does

1. Analyzes the need or current project context
2. Checks existing marketplace for gaps
3. Proposes a new plugin structure
4. Optionally scaffolds the plugin

## Process

### 1. Understand the Need

If `--from-context`:
- Scan current project for technologies used
- Check package.json, requirements.txt, Cargo.toml, etc.
- Identify frameworks and tools
- Find patterns that could benefit from automation

If description provided:
- Parse the domain/technology
- Identify key workflows
- Research best practices

### 2. Check Existing Coverage

```bash
# Search marketplace for related plugins
grep -r "description" /Users/cameron/Projects/claude-marketplace/plugins/*/plugin.json

# Check for existing agents
find /Users/cameron/Projects/claude-marketplace -name "*.md" -path "*/agents/*" | xargs grep -l "keyword"

# Check for existing skills
find /Users/cameron/Projects/claude-marketplace/registry/skills -name "SKILL.md" | xargs grep -l "keyword"
```

### 3. Propose Plugin Structure

Output a complete proposal:

```markdown
## Proposed Plugin: graphql-development

### Justification
- No existing GraphQL coverage in marketplace
- Common workflow: schema design, resolver patterns, code generation
- Complements: api-development, typescript-toolkit

### Components

**Agent: graphql-expert.md**
- Schema design patterns (SDL)
- Resolver architecture
- N+1 query prevention
- DataLoader patterns
- Federation/stitching
- Type generation (codegen)

**Commands:**
- `/graphql.schema` - Generate/validate schema
- `/graphql.mock` - Create mock resolvers

**Skill: graphql-patterns/**
- SKILL.md: Core patterns
- federation.md: Distributed GraphQL
- security.md: Query complexity, depth limiting

### Composition Updates
Add to:
- full-stack-web: [...existing, "graphql-development"]
- api-focused: ["api-development", "graphql-development", "security-suite"]

### Category
architecture

### Tags
graphql, api, schema, resolvers, federation
```

### 4. Scaffold Option

If user approves:

```bash
# Create plugin structure
mkdir -p /Users/cameron/Projects/claude-marketplace/plugins/graphql-development/{.claude-plugin,agents,commands}

# Create plugin.json
# Create agent file
# Create command files
# Update marketplace.json
# Update compositions.md
```

## Output Format

```
🔍 Analyzing need: "GraphQL development"

📊 Existing Coverage Check
   ✓ api-development - REST focus, no GraphQL
   ✓ typescript-toolkit - Types, but no GraphQL codegen
   ✗ No GraphQL-specific plugin found

💡 Recommendation: Create new plugin

📦 Proposed: graphql-development
   ├── agents/graphql-expert.md
   ├── commands/graphql.schema.md
   ├── commands/graphql.mock.md
   └── skill → registry/skills/graphql-patterns/

🔗 Compositions: Add to full-stack-web, create api-focused

Scaffold now? [Y/n]
```

## From-Context Analysis

When using `--from-context`:

```
🔍 Analyzing current project...

📁 Project: /Users/cameron/Projects/my-app
   Type: Next.js + GraphQL
   Dependencies: @apollo/client, graphql, graphql-codegen

📊 Marketplace Coverage
   ✓ typescript-toolkit - Covered
   ✓ api-development - Partially relevant
   ✗ graphql-development - MISSING

💡 Suggestion: Install graphql-development plugin
   This would provide:
   • Schema design patterns
   • Resolver best practices
   • Apollo Client patterns
   • Codegen configuration

   Create this plugin? [Y/n]
```
