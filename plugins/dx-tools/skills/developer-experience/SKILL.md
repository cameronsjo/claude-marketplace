# Developer Experience Skill

Optimize development workflows, reduce friction, and make development joyful and productive.

## Overview

This skill provides expert guidance for improving developer experience (DX) through tooling optimization, environment setup automation, and workflow improvements.

## When to Use This Skill

Trigger this skill when:

- Setting up new projects from scratch
- Developers report friction or pain points
- Onboarding time is too long (>15 minutes)
- Build/test times are slow
- Repetitive manual tasks exist
- IDE/editor configuration needed
- Git hooks or automation setup required
- Development workflow optimization
- CLI commands or shortcuts needed
- Documentation is outdated or unclear

**Keywords:** developer experience, DX, workflow optimization, project setup, automation, tooling, IDE configuration, git hooks, development friction

## Core Principles

### DX Philosophy

1. **Pit of Success**: Make the right thing the easiest thing
2. **Fast Feedback**: Minimize time from change to result
3. **Clear Errors**: When things fail, explain why and how to fix
4. **Minimal Setup**: <5 minutes from clone to productive
5. **Automate Everything**: If done more than twice, automate it
6. **Intelligent Defaults**: Works great out of the box
7. **Progressive Disclosure**: Simple start, power available when needed

### Measuring DX

**Time Metrics:**

- Time to first successful build
- Time to run tests
- Time to deploy to dev environment
- Time from code change to seeing results

**Friction Metrics:**

- Manual steps required for common tasks
- Number of tools/commands to remember
- Setup failures (percentage)
- Documentation lookup frequency

**Satisfaction Metrics:**

- Developer NPS
- Onboarding feedback
- Tool adoption rate
- Contribution frequency

## Environment Setup Optimization

### Sub-5-Minute Setup

```bash
#!/bin/bash
# setup.sh - One-command setup script

set -e  # Exit on error

echo "🚀 Setting up development environment..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required. Install from https://nodejs.org"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git required"; exit 1; }

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Setup git hooks
echo "🪝 Installing git hooks..."
npx husky install

# Run initial build
echo "🔨 Running initial build..."
npm run build

# Verify setup
echo "✅ Running verification tests..."
npm run verify

echo "
✨ Setup complete! Next steps:

1. Update .env with your configuration
2. Run: npm run dev
3. Visit: http://localhost:3000

📚 Documentation: README.md
🆘 Help: npm run help
"
```

### Prerequisites Check Script

```javascript
// scripts/check-prerequisites.js
const { execSync } = require('child_process');
const fs = require('fs');

const checks = [
  {
    name: 'Node.js',
    check: () => {
      const version = execSync('node --version').toString().trim();
      const major = parseInt(version.slice(1).split('.')[0]);
      return { pass: major >= 18, message: version };
    },
    required: '>=18.0.0',
    install: 'https://nodejs.org'
  },
  {
    name: 'Git',
    check: () => {
      const version = execSync('git --version').toString().trim();
      return { pass: true, message: version };
    },
    required: 'any',
    install: 'https://git-scm.com'
  },
  {
    name: 'Docker',
    check: () => {
      try {
        const version = execSync('docker --version').toString().trim();
        return { pass: true, message: version };
      } catch {
        return { pass: false, message: 'Not installed' };
      }
    },
    required: 'optional',
    install: 'https://docker.com'
  }
];

console.log('Checking prerequisites...\n');

let allPassed = true;

checks.forEach(({ name, check, required, install }) => {
  const result = check();
  const emoji = result.pass ? '✅' : '❌';

  console.log(`${emoji} ${name}: ${result.message}`);

  if (!result.pass && required !== 'optional') {
    console.log(`   Required: ${required}`);
    console.log(`   Install: ${install}\n`);
    allPassed = false;
  }
});

if (!allPassed) {
  console.log('❌ Prerequisites check failed. Please install required tools.');
  process.exit(1);
}

console.log('\n✅ All prerequisites satisfied!');
```

## IDE Configuration

### VS Code Settings

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.exclude": {
    "**/node_modules": true,
    "**/.git": true,
    "**/dist": true,
    "**/.next": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/.next": true,
    "**/coverage": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.wordWrap": "on"
  }
}
```

### Recommended Extensions

```json
// .vscode/extensions.json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",
    "eamodio.gitlens",
    "github.copilot",
    "bradlc.vscode-tailwindcss",
    "prisma.prisma",
    "ms-azuretools.vscode-docker",
    "humao.rest-client"
  ]
}
```

## Git Hooks

### Using Husky + lint-staged

```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ]
  }
}
```

### Pre-commit Hook

```bash
#!/bin/sh
# .husky/pre-commit

echo "🔍 Running pre-commit checks..."

# Run lint-staged
npx lint-staged

# Run type check
echo "📝 Type checking..."
npm run typecheck

# Check for console.logs in staged files
if git diff --cached --name-only | grep -E '\.(js|jsx|ts|tsx)$' | xargs grep -n 'console\.log' --color=always; then
    echo "❌ Found console.log statements. Please remove them."
    exit 1
fi

echo "✅ Pre-commit checks passed!"
```

### Pre-push Hook

```bash
#!/bin/sh
# .husky/pre-push

echo "🔍 Running pre-push checks..."

# Run tests
echo "🧪 Running tests..."
npm run test

# Run build
echo "🔨 Building..."
npm run build

echo "✅ Pre-push checks passed!"
```

## Task Automation

### Makefile for Common Tasks

```makefile
# Makefile

.PHONY: help install dev build test clean deploy

help: ## Show this help message
 @echo "Available commands:"
 @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
 npm install
 cp -n .env.example .env || true

dev: ## Start development server
 npm run dev

build: ## Build for production
 npm run build

test: ## Run tests
 npm run test

test-watch: ## Run tests in watch mode
 npm run test:watch

typecheck: ## Run type checking
 npm run typecheck

lint: ## Run linter
 npm run lint

lint-fix: ## Fix linting issues
 npm run lint:fix

clean: ## Clean build artifacts
 rm -rf dist .next node_modules/.cache

reset: clean ## Reset to clean state
 rm -rf node_modules
 npm install

deploy-dev: ## Deploy to development
 npm run build
 npm run deploy:dev

deploy-prod: ## Deploy to production
 npm run build
 npm run deploy:prod

db-migrate: ## Run database migrations
 npx prisma migrate dev

db-reset: ## Reset database
 npx prisma migrate reset

db-seed: ## Seed database
 npx prisma db seed

docker-up: ## Start Docker containers
 docker-compose up -d

docker-down: ## Stop Docker containers
 docker-compose down

docker-logs: ## View Docker logs
 docker-compose logs -f

verify: ## Verify setup
 node scripts/check-prerequisites.js
 npm run typecheck
 npm run lint
 npm run test
```

### Package.json Scripts Organization

```json
{
  "scripts": {
    "// Development": "",
    "dev": "next dev",
    "dev:turbo": "next dev --turbo",
    "dev:https": "next dev --experimental-https",

    "// Building": "",
    "build": "next build",
    "build:analyze": "ANALYZE=true next build",
    "start": "next start",

    "// Testing": "",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:e2e": "playwright test",

    "// Quality": "",
    "typecheck": "tsc --noEmit",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{js,jsx,ts,tsx,json,md}\"",

    "// Database": "",
    "db:migrate": "prisma migrate dev",
    "db:push": "prisma db push",
    "db:seed": "prisma db seed",
    "db:studio": "prisma studio",

    "// Git": "",
    "prepare": "husky install",

    "// Utilities": "",
    "clean": "rm -rf .next dist coverage",
    "verify": "npm run typecheck && npm run lint && npm run test",
    "help": "node scripts/show-help.js"
  }
}
```

## Error Messages and Feedback

### Helpful Error Messages

```javascript
// Bad: Cryptic error
Error: ENOENT

// Good: Actionable error
Error: Configuration file not found: .env
→ Run: cp .env.example .env
→ Then update with your settings
→ Documentation: docs/configuration.md
```

### Error Handler Utility

```javascript
// scripts/utils/error-handler.js

class DXError extends Error {
  constructor(message, { solution, docs, code } = {}) {
    super(message);
    this.name = 'DXError';
    this.solution = solution;
    this.docs = docs;
    this.code = code;
  }

  toString() {
    let output = `\n❌ ${this.message}\n`;

    if (this.solution) {
      output += `\n💡 Solution:\n${this.solution}\n`;
    }

    if (this.docs) {
      output += `\n📚 Documentation: ${this.docs}\n`;
    }

    if (this.code) {
      output += `\nError code: ${this.code}`;
    }

    return output;
  }
}

// Usage
throw new DXError('Database connection failed', {
  solution: '1. Check DATABASE_URL in .env\n2. Ensure database is running\n3. Run: docker-compose up -d',
  docs: 'docs/database-setup.md',
  code: 'DB_CONNECTION_FAILED'
});
```

## Performance Optimization

### Build Time Optimization

```javascript
// next.config.js
module.exports = {
  // Faster builds
  swcMinify: true,

  // Parallel builds
  experimental: {
    workerThreads: true,
  },

  // Only type-check in production
  typescript: {
    ignoreBuildErrors: process.env.NODE_ENV === 'development',
  },

  // Skip ESLint in development
  eslint: {
    ignoreDuringBuilds: process.env.NODE_ENV === 'development',
  },
};
```

### Test Performance

```javascript
// jest.config.js
module.exports = {
  // Run tests in parallel
  maxWorkers: '50%',

  // Only run changed tests in watch mode
  changedFilesWithAncestor: true,

  // Cache test results
  cache: true,
  cacheDirectory: '.jest-cache',
};
```

## CLI Helpers and Aliases

### Custom CLI Tool

```javascript
#!/usr/bin/env node
// bin/dev.js

const { program } = require('commander');
const { execSync } = require('child_process');

program
  .name('dev')
  .description('Development helper CLI')
  .version('1.0.0');

program
  .command('setup')
  .description('Setup development environment')
  .action(() => {
    console.log('🚀 Setting up...');
    execSync('bash scripts/setup.sh', { stdio: 'inherit' });
  });

program
  .command('reset')
  .description('Reset to clean state')
  .action(() => {
    console.log('🔄 Resetting...');
    execSync('make reset', { stdio: 'inherit' });
  });

program
  .command('fix')
  .description('Auto-fix all issues')
  .action(() => {
    console.log('🔧 Fixing issues...');
    execSync('npm run lint:fix && npm run format', { stdio: 'inherit' });
  });

program.parse();
```

### Shell Aliases

```bash
# Add to .bashrc or .zshrc

alias dev='npm run dev'
alias build='npm run build'
alias test='npm run test'
alias tw='npm run test:watch'
alias fix='npm run lint:fix && npm run format'
alias check='npm run verify'
```

## Documentation Improvements

### Interactive README

```markdown
# Project Name

One-line description of what this does.

## Quick Start

```bash
# Clone and setup (< 5 minutes)
git clone <repo>
cd <project>
make install
make dev
```

Visit http://localhost:3000

## Common Tasks

| Task | Command | Description |
|------|---------|-------------|
| Start dev server | `make dev` | Hot-reload development |
| Run tests | `make test` | Run test suite |
| Type check | `make typecheck` | Check TypeScript types |
| Fix linting | `make lint-fix` | Auto-fix code issues |
| Deploy dev | `make deploy-dev` | Deploy to development |

See `make help` for all commands.

## Project Structure

```
src/
  ├── app/          # Next.js app router
  ├── components/   # React components
  ├── lib/          # Utility functions
  └── styles/       # CSS/Tailwind
```

## Development Guide

- [Setup](docs/setup.md) - Detailed setup instructions
- [Architecture](docs/architecture.md) - System design
- [Contributing](docs/contributing.md) - How to contribute
- [Troubleshooting](docs/troubleshooting.md) - Common issues

## Need Help?

- 💬 Slack: #project-help
- 📧 Email: team@example.com
- 🐛 Issues: GitHub Issues

```

### Troubleshooting Guide

```markdown
# Troubleshooting

## Common Issues

### "Port 3000 already in use"

**Symptom:** Cannot start dev server

**Solution:**
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

### "Module not found"

**Symptom:** Import errors after pulling changes

**Solution:**

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### "Type errors after upgrade"

**Symptom:** TypeScript errors after dependency update

**Solution:**

```bash
# Clear TypeScript cache
rm -rf node_modules/.cache
npm run typecheck
```

## Getting Help

1. Check [Documentation](docs/)
2. Search [GitHub Issues](issues)
3. Ask in Slack #dev-help
4. Create new issue with reproduction

```

## Onboarding Automation

### New Developer Checklist

```markdown
# New Developer Onboarding

## Day 1: Environment Setup

- [ ] Install prerequisites (Node.js, Git, Docker)
- [ ] Clone repository
- [ ] Run `make setup`
- [ ] Configure .env file
- [ ] Start dev server successfully
- [ ] Run tests successfully
- [ ] Make a small change and see it live

**Time goal:** 30 minutes

## Day 1: Orientation

- [ ] Read README.md
- [ ] Review architecture docs
- [ ] Understand project structure
- [ ] Join Slack channels
- [ ] Meet the team

## Week 1: First Contribution

- [ ] Pick "good first issue"
- [ ] Create feature branch
- [ ] Make changes
- [ ] Run tests
- [ ] Create pull request
- [ ] Address review feedback
- [ ] Merge!

## Resources

- Setup guide: docs/setup.md
- Architecture: docs/architecture.md
- Team wiki: wiki/
```

## Monitoring and Metrics

### DX Metrics Dashboard

```javascript
// scripts/dx-metrics.js

const fs = require('fs');
const { execSync } = require('child_process');

function measureSetupTime() {
  // Measure time from clone to first successful build
  const start = Date.now();

  try {
    execSync('npm install', { stdio: 'inherit' });
    execSync('npm run build', { stdio: 'inherit' });

    const duration = (Date.now() - start) / 1000;
    console.log(`✅ Setup completed in ${duration}s`);

    return duration;
  } catch (error) {
    console.log(`❌ Setup failed`);
    return null;
  }
}

function measureTestSpeed() {
  const start = Date.now();

  execSync('npm run test', { stdio: 'pipe' });

  const duration = (Date.now() - start) / 1000;
  console.log(`🧪 Tests completed in ${duration}s`);

  return duration;
}

function measureBuildSpeed() {
  const start = Date.now();

  execSync('npm run build', { stdio: 'pipe' });

  const duration = (Date.now() - start) / 1000;
  console.log(`🔨 Build completed in ${duration}s`);

  return duration;
}

// Track metrics over time
const metrics = {
  date: new Date().toISOString(),
  setupTime: measureSetupTime(),
  testSpeed: measureTestSpeed(),
  buildSpeed: measureBuildSpeed(),
};

console.log('\n📊 DX Metrics:', metrics);
```

## Resources

### Templates

- `resources/setup-script-template.sh` - Setup script template
- `resources/makefile-template` - Makefile for common tasks
- `resources/vscode-settings.json` - VS Code configuration
- `resources/git-hooks/` - Pre-commit and pre-push hooks

### Scripts

- `scripts/check-prerequisites.js` - Prerequisites checker
- `scripts/dx-metrics.js` - DX measurement tool
- `scripts/setup-wizard.js` - Interactive setup

## Related Skills

- **cli-development**: Building CLI tools and command interfaces
- **python-development**: Python-specific DX improvements
- **kubernetes-deployment**: Deployment workflow optimization

## Required Development Tools

### Essential Tools

**Linting/Formatting:**

- **JavaScript/TypeScript:** ESLint + Prettier
- **Python:** ruff + black + isort

**Type Checking:**

- **Python:** mypy, pylance, pyright
- **TypeScript:** TypeScript strict mode enabled

**Observability:**

- **Structured Logging:** Required for all projects (implement early and often)
- **OpenTelemetry:** Distributed tracing (non-negotiable)

**Feature Flags:**

- For gradual rollouts, A/B testing, risk mitigation
- Prefer typed flags with validation

**Spec Kit:**

- For Spec-Driven Development: https://github.com/github/spec-kit

### Git Hooks

**Use Husky** for team repositories:

- **Pre-commit:** Linting, formatting, type checking
- **Pre-push:** Tests (if fast enough, <30 seconds)

## Best Practices Summary

1. **< 5 Minute Setup**: From clone to productive
2. **Intelligent Defaults**: Works great out of the box
3. **Clear Errors**: Actionable error messages
4. **Automate Everything**: No repeated manual steps
5. **Fast Feedback**: Quick test/build cycles
6. **IDE Integration**: Proper editor configuration
7. **Git Hooks**: Catch issues before push
8. **Good Documentation**: Clear, up-to-date, actionable
9. **Measure DX**: Track setup time, build speed, test speed
10. **Iterate**: Improve based on developer feedback
11. **Required Tools**: Linting, type checking, observability from day one
