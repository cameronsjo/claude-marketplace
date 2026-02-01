#!/bin/bash
# Full-Stack Application SessionStart Hook
# Place in: scripts/claude-setup.sh
# Make executable: chmod +x scripts/claude-setup.sh
set -e

echo "Setting up full-stack application..."

# Backend setup (Python)
if [ -d "backend" ]; then
    echo "Setting up backend..."
    cd backend

    if [ -f "pyproject.toml" ]; then
        if command -v uv &> /dev/null; then
            uv sync
        else
            pip install -e .
        fi
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi

    cd ..
fi

# Alternative: backend in api/ directory
if [ -d "api" ]; then
    echo "Setting up API..."
    cd api

    if [ -f "package.json" ]; then
        npm install
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi

    cd ..
fi

# Frontend setup (Node.js)
if [ -d "frontend" ]; then
    echo "Setting up frontend..."
    cd frontend

    if [ -f "pnpm-lock.yaml" ]; then
        pnpm install
    elif [ -f "yarn.lock" ]; then
        yarn install
    elif [ -f "bun.lockb" ]; then
        bun install
    else
        npm install
    fi

    cd ..
fi

# Alternative: frontend in web/ or client/ directory
for dir in web client app; do
    if [ -d "$dir" ] && [ -f "$dir/package.json" ]; then
        echo "Setting up $dir..."
        cd "$dir"
        npm install
        cd ..
    fi
done

# Root-level dependencies (monorepo)
if [ -f "package.json" ]; then
    echo "Installing root dependencies..."
    npm install
fi

# Start services if docker-compose exists
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    if command -v docker &> /dev/null; then
        echo "Starting database services..."
        docker-compose up -d db redis postgres 2>/dev/null || true
    fi
fi

# Copy example env files
for env_example in .env.example backend/.env.example frontend/.env.example api/.env.example; do
    if [ -f "$env_example" ]; then
        env_file="${env_example%.example}"
        if [ ! -f "$env_file" ]; then
            cp "$env_example" "$env_file"
            echo "Created $env_file from $env_example"
        fi
    fi
done

# Set environment
echo "NODE_ENV=development" >> "$CLAUDE_ENV_FILE"
echo "PYTHONPATH=$(pwd)" >> "$CLAUDE_ENV_FILE"

echo "Full-stack setup complete!"
exit 0
