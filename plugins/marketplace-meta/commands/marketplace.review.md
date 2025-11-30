---
description: Analyze marketplace for gaps, improvements, and composition opportunities
category: development
argument-hint: "[plugin-name | --full | --compositions | --gaps]"
allowed-tools: Bash, Read, Glob, Grep, Task
---

# Claude Command: Marketplace Review

## Usage

```bash
/marketplace.review                    # Quick overview with suggestions
/marketplace.review --full             # Deep analysis of all plugins
/marketplace.review --compositions     # Suggest new plugin bundles
/marketplace.review --gaps             # Identify missing capabilities
/marketplace.review obsidian-plugin-dev  # Review specific plugin
```

## What This Command Does

Analyzes the local marketplace to provide actionable feedback on:

1. **Plugin Quality**: Agent descriptions, command clarity, skill coverage
2. **Composition Opportunities**: Plugins that work well together
3. **Gap Analysis**: Missing agents/skills for common workflows
4. **Consistency**: Naming conventions, structure, categories

## Analysis Process

### 1. Load Marketplace Data

Read the marketplace structure:

```bash
# Get marketplace path
MARKETPLACE="/Users/cameron/Projects/claude-marketplace"

# Parse marketplace.json
cat "$MARKETPLACE/.claude-plugin/marketplace.json"

# Count components
find "$MARKETPLACE/plugins" -name "*.md" -path "*/agents/*"
find "$MARKETPLACE/plugins" -name "*.md" -path "*/commands/*"
find "$MARKETPLACE/registry/skills" -name "SKILL.md"
```

### 2. Plugin Analysis

For each plugin, evaluate:

**Agent Quality Checklist**:
- [ ] Description includes "Use PROACTIVELY for..."
- [ ] Category matches agent purpose
- [ ] Contains concrete code examples
- [ ] Lists when to use and when NOT to use
- [ ] Covers edge cases and gotchas

**Command Quality Checklist**:
- [ ] Clear argument-hint if arguments accepted
- [ ] allowed-tools specified
- [ ] Step-by-step process documented
- [ ] Example usage provided
- [ ] Output format described

**Skill Quality Checklist**:
- [ ] Trigger conditions described
- [ ] Progressive disclosure (SKILL.md + reference files)
- [ ] Code patterns included
- [ ] References to sources

### 3. Gap Analysis

Check for missing capabilities:

**Common Workflows Without Coverage**:
- Database migrations
- Docker/container workflows
- CI/CD pipeline debugging
- Performance profiling
- Logging and monitoring
- GraphQL development
- Mobile development (React Native, Flutter)
- Testing frameworks (Playwright, Cypress)

**Language Coverage Gaps**:
- Check plugins exist for: Python, TypeScript, Rust, Go, Java, C#
- Each should have: expert agent, common commands, patterns skill

### 4. Composition Analysis

Suggest plugin bundles:

**By Project Type**:
- Web App: typescript-toolkit + api-development + security-suite
- Data Pipeline: python-toolkit + data-science + cloud-ops
- CLI Tool: python-toolkit + dx-tools + core-productivity
- Obsidian Plugin: obsidian-plugin-dev + typescript-toolkit + core-productivity

**By Role**:
- Backend Dev: api-development + security-suite + cloud-ops
- Frontend Dev: typescript-toolkit + dx-tools
- DevOps: cloud-ops + security-suite + core-productivity
- Data Engineer: data-science + python-toolkit + cloud-ops

### 5. Consistency Check

Verify naming and structure:

**Naming Conventions**:
- Plugin names: kebab-case
- Agent files: kebab-case.md
- Command files: verb.noun.md or verb-noun.md
- Skill directories: kebab-case/

**Structure Requirements**:
- Every plugin has .claude-plugin/plugin.json
- plugin.json has: name, description, version, author, category
- Categories are one of: productivity, language, architecture, security, workflow, research, development, infrastructure, data

## Output Format

### Quick Review

```
📊 Marketplace Health Report
═══════════════════════════════════════

✅ Strengths
   • 14 plugins covering major workflows
   • Strong TypeScript/Python coverage
   • Consistent naming conventions

⚠️  Areas for Improvement
   • 3 agents missing "PROACTIVELY" trigger
   • 2 commands without allowed-tools
   • No GraphQL coverage

💡 Quick Wins
   1. Add allowed-tools to /review.api command
   2. Create graphql-development plugin
   3. Add Playwright testing agent to dx-tools

🔗 Suggested Compositions
   • "full-stack-web": typescript + api + security
   • "data-pipeline": python + data-science + cloud
```

### Full Analysis

Detailed per-plugin breakdown with:
- Component inventory
- Quality scores
- Specific improvement suggestions
- Code snippets for fixes

### Gap Report

```
🔍 Capability Gap Analysis
═══════════════════════════════════════

Missing Agents
   ❌ graphql-expert (GraphQL schema design, resolvers)
   ❌ playwright-expert (E2E testing, browser automation)
   ❌ mobile-expert (React Native, Flutter patterns)

Missing Commands
   ❌ /docker.debug (container troubleshooting)
   ❌ /perf.profile (performance profiling workflow)
   ❌ /migration.run (database migration runner)

Missing Skills
   ❌ graphql-patterns
   ❌ testing-strategies
   ❌ docker-patterns

Partial Coverage
   ⚡ cloud-ops: Has AWS, missing GCP/Azure depth
   ⚡ security-suite: Has OWASP, missing supply chain
```

## Meta: Improving This Plugin

When you identify improvements for marketplace-meta itself:

1. Note them in the review output
2. Offer to implement immediately
3. Update this command if new analysis needed

This plugin should eat its own dog food!
