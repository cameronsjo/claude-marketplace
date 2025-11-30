#!/bin/bash
# Node.js/TypeScript SessionStart Hook
# Place in: scripts/claude-setup.sh
# Make executable: chmod +x scripts/claude-setup.sh
set -e

echo "Setting up Node.js environment..."

# Detect and use appropriate package manager
if [ -f "pnpm-lock.yaml" ]; then
    echo "Installing with pnpm..."
    pnpm install
elif [ -f "yarn.lock" ]; then
    echo "Installing with yarn..."
    yarn install
elif [ -f "bun.lockb" ]; then
    echo "Installing with bun..."
    bun install
else
    echo "Installing with npm..."
    npm install
fi

# Build TypeScript if present
if [ -f "tsconfig.json" ]; then
    echo "Building TypeScript..."
    npm run build 2>/dev/null || yarn build 2>/dev/null || true
fi

# Copy example env if .env doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

# Set Node environment
echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"

echo "Node.js setup complete!"
exit 0
