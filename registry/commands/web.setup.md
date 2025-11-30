---
description: Configure this repository for Claude Code on the web with SessionStart hooks
category: development-setup
argument-hint: "[nodejs|python|fullstack|ruby|go]"
allowed-tools: Bash, Read, Write, Edit
---

# Claude Command: Web Setup

Set up this repository for Claude Code on the web by configuring SessionStart hooks for automatic dependency installation.

## Instructions

### Step 1: Detect Project Type

If no argument provided, auto-detect based on files:

- `package.json` + `requirements.txt` or `pyproject.toml` → fullstack
- `package.json` only → nodejs
- `pyproject.toml` or `requirements.txt` → python
- `Gemfile` → ruby
- `go.mod` → go

### Step 2: Check Existing Configuration

Check if `.claude/settings.json` already exists:

```bash
ls -la .claude/settings.json 2>/dev/null
```

If exists, inform user and ask if they want to overwrite or merge.

### Step 3: Create Directory Structure

```bash
mkdir -p .claude scripts
```

### Step 4: Create settings.json

Create `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/claude-setup.sh",
            "timeout": 120,
            "statusMessage": "Setting up development environment..."
          }
        ]
      }
    ]
  }
}
```

### Step 5: Create Setup Script

Based on detected/specified project type, create `scripts/claude-setup.sh`:

#### Node.js

```bash
#!/bin/bash
set -e

if [ -f "pnpm-lock.yaml" ]; then
    pnpm install
elif [ -f "yarn.lock" ]; then
    yarn install
elif [ -f "bun.lockb" ]; then
    bun install
else
    npm install
fi

if [ -f "tsconfig.json" ]; then
    npm run build 2>/dev/null || true
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
exit 0
```

#### Python

```bash
#!/bin/bash
set -e

if [ -f "pyproject.toml" ]; then
    if command -v uv &> /dev/null; then
        uv sync
    elif command -v poetry &> /dev/null; then
        poetry install
    else
        pip install -e .
    fi
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"
exit 0
```

#### Full-Stack

```bash
#!/bin/bash
set -e

# Backend
if [ -d "backend" ]; then
    cd backend
    if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi
    if [ -f "pyproject.toml" ]; then uv sync 2>/dev/null || pip install -e .; fi
    cd ..
fi

# Frontend
if [ -d "frontend" ]; then
    cd frontend
    npm install
    cd ..
fi

# Root
if [ -f "package.json" ]; then npm install; fi

echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"
exit 0
```

#### Ruby

```bash
#!/bin/bash
set -e

if [ -f ".ruby-version" ]; then
    rbenv local $(cat .ruby-version) 2>/dev/null || true
fi

bundle install

exit 0
```

#### Go

```bash
#!/bin/bash
set -e

go mod download
go build ./... 2>/dev/null || true

exit 0
```

### Step 6: Make Script Executable

```bash
chmod +x scripts/claude-setup.sh
```

### Step 7: Report Success

Display summary:

```
Claude Code web setup complete!

Files created:
  - .claude/settings.json (hook configuration)
  - scripts/claude-setup.sh (setup script)

Project type: {detected_type}

Next steps:
  1. Review scripts/claude-setup.sh and customize if needed
  2. Commit these files: git add .claude scripts && git commit -m "feat: add Claude Code web hooks"
  3. Push to your repository
  4. Start a session at claude.ai/code

Environment variables can be added by appending to $CLAUDE_ENV_FILE in your script.
```

## Notes

- The setup script should always `exit 0` on success
- Use `$CLAUDE_ENV_FILE` to persist environment variables
- Check `$CLAUDE_CODE_REMOTE` to detect web vs local execution
- Default timeout is 120 seconds (adjust for large projects)
