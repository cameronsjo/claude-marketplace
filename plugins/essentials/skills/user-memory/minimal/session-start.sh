#!/bin/bash
# Minimal SessionStart hook: Load profile and inject into context
# Zero dependencies (uses jq if available, falls back to cat)

set -euo pipefail

MEMORY_DIR="${USER_MEMORY_DIR:-$HOME/.claude/user-memory}"
PROFILE_PATH="$MEMORY_DIR/profile.json"

# Read hook input from stdin
INPUT=$(cat)

# If no profile exists, exit silently
[[ ! -f "$PROFILE_PATH" ]] && exit 0

# Try to get env file from input (requires jq)
if command -v jq &>/dev/null; then
    ENV_FILE=$(echo "$INPUT" | jq -r '.env_file // empty' 2>/dev/null || true)
fi

# Read and inject profile
PROFILE=$(cat "$PROFILE_PATH")

# If CLAUDE_ENV_FILE available, write there
if [[ -n "${ENV_FILE:-}" && -w "$ENV_FILE" ]]; then
    echo "USER_MEMORY_PROFILE='$(echo "$PROFILE" | tr -d '\n')'" >> "$ENV_FILE"
fi

# Log for debugging
echo "user-memory: loaded profile from $PROFILE_PATH" >&2
