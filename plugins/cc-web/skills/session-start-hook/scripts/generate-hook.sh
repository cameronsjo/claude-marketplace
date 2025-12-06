#!/bin/bash
# Generate SessionStart hook configuration for a project
# Usage: ./generate-hook.sh [project-type]
# project-type: nodejs, python, fullstack, ruby, go (default: auto-detect)

set -e

PROJECT_TYPE="${1:-auto}"

# Auto-detect project type
if [ "$PROJECT_TYPE" = "auto" ]; then
    if [ -f "package.json" ] && [ -f "requirements.txt" ]; then
        PROJECT_TYPE="fullstack"
    elif [ -f "package.json" ]; then
        PROJECT_TYPE="nodejs"
    elif [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
        PROJECT_TYPE="python"
    elif [ -f "Gemfile" ]; then
        PROJECT_TYPE="ruby"
    elif [ -f "go.mod" ]; then
        PROJECT_TYPE="go"
    else
        PROJECT_TYPE="generic"
    fi
fi

echo "Detected project type: $PROJECT_TYPE"

# Create directories
mkdir -p .claude scripts

# Create settings.json
cat > .claude/settings.json << 'EOF'
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
EOF

echo "Created .claude/settings.json"

# Create appropriate setup script based on project type
case "$PROJECT_TYPE" in
    nodejs)
        cat > scripts/claude-setup.sh << 'SCRIPT'
#!/bin/bash
set -e

# Detect and use appropriate package manager
if [ -f "pnpm-lock.yaml" ]; then
    pnpm install
elif [ -f "yarn.lock" ]; then
    yarn install
elif [ -f "bun.lockb" ]; then
    bun install
else
    npm install
fi

# Build TypeScript if present
if [ -f "tsconfig.json" ]; then
    npm run build 2>/dev/null || true
fi

# Copy example env if needed
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
fi

echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
exit 0
SCRIPT
        ;;

    python)
        cat > scripts/claude-setup.sh << 'SCRIPT'
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
SCRIPT
        ;;

    fullstack)
        cat > scripts/claude-setup.sh << 'SCRIPT'
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

# Root dependencies
if [ -f "package.json" ]; then npm install; fi

echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"
exit 0
SCRIPT
        ;;

    ruby)
        cat > scripts/claude-setup.sh << 'SCRIPT'
#!/bin/bash
set -e

if [ -f ".ruby-version" ]; then
    rbenv local $(cat .ruby-version) 2>/dev/null || true
fi

bundle install

exit 0
SCRIPT
        ;;

    go)
        cat > scripts/claude-setup.sh << 'SCRIPT'
#!/bin/bash
set -e

go mod download
go build ./... 2>/dev/null || true

exit 0
SCRIPT
        ;;

    *)
        cat > scripts/claude-setup.sh << 'SCRIPT'
#!/bin/bash
set -e

# Add your setup commands here
# Example: npm install, pip install -r requirements.txt, etc.

echo "Setup complete"
exit 0
SCRIPT
        ;;
esac

chmod +x scripts/claude-setup.sh
echo "Created scripts/claude-setup.sh"

echo ""
echo "SessionStart hook configured!"
echo "Your project is now ready for Claude Code on the web."
echo ""
echo "Files created:"
echo "  - .claude/settings.json (hook configuration)"
echo "  - scripts/claude-setup.sh (setup script)"
echo ""
echo "Next steps:"
echo "  1. Review scripts/claude-setup.sh and customize as needed"
echo "  2. Commit these files to your repository"
echo "  3. Start a session at claude.ai/code"
