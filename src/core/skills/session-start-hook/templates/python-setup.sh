#!/bin/bash
# Python SessionStart Hook
# Place in: scripts/claude-setup.sh
# Make executable: chmod +x scripts/claude-setup.sh
set -e

echo "Setting up Python environment..."

# Determine Python setup method
if [ -f "pyproject.toml" ]; then
    # Modern Python project
    if command -v uv &> /dev/null; then
        echo "Installing with uv..."
        uv sync
    elif command -v poetry &> /dev/null; then
        echo "Installing with poetry..."
        poetry install
    else
        echo "Installing with pip (editable)..."
        pip install -e .
    fi
elif [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    pip install -r requirements.txt

    # Also install dev requirements if present
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
    fi
fi

# Set up environment variables
echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"
echo "PYTHONDONTWRITEBYTECODE=1" >> "$CLAUDE_ENV_FILE"

# Copy example env if .env doesn't exist
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo "Python setup complete!"
exit 0
