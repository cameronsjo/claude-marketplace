#!/bin/bash
# MCP SessionStart hook: Load profile, run decay, inject context
# Uses TypeScript store for consistency with MCP server

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_DIR="${USER_MEMORY_DIR:-$HOME/.claude/user-memory}"
PROFILE_PATH="$MEMORY_DIR/profile.json"
META_PATH="$MEMORY_DIR/profile-meta.json"
MCP_DIR="$(dirname "$SCRIPT_DIR")"

# Read hook input from stdin
INPUT=$(cat)

# Log file for debugging (optional)
LOG_FILE="${MEMORY_DIR}/hook.log"

# Try to run scheduled decay if TypeScript available
if command -v npx &>/dev/null && [[ -f "$MCP_DIR/src/decay-check.ts" ]]; then
    if ! npx --yes tsx "$MCP_DIR/src/decay-check.ts" 2>>"$LOG_FILE"; then
        echo "user-memory[mcp]: decay check failed, see $LOG_FILE" >&2
    fi
fi

# If no profile exists, exit silently
[[ ! -f "$PROFILE_PATH" ]] && exit 0

# Try to get env file from input
if command -v jq &>/dev/null; then
    ENV_FILE=$(echo "$INPUT" | jq -r '.env_file // empty' 2>/dev/null || true)
    SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null || true)
    CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null || true)
fi

# Read profile
PROFILE=$(cat "$PROFILE_PATH")

# Build context for injection
CONTEXT=""

# Add user profile summary
if command -v jq &>/dev/null; then
    ROLE=$(echo "$PROFILE" | jq -r '.work.role // empty')
    TONE=$(echo "$PROFILE" | jq -r '.codePreferences.tone // empty')
    STACKS=$(echo "$PROFILE" | jq -r '.codePreferences.preferredStacks // [] | join(", ")')
    EDITOR=$(echo "$PROFILE" | jq -r '.tools.editor // empty')

    if [[ -n "$ROLE" || -n "$TONE" || -n "$STACKS" || -n "$EDITOR" ]]; then
        CONTEXT="## User Profile\n"
        [[ -n "$ROLE" ]] && CONTEXT+="- Role: $ROLE\n"
        [[ -n "$TONE" ]] && CONTEXT+="- Tone preference: $TONE\n"
        [[ -n "$STACKS" ]] && CONTEXT+="- Preferred stacks: $STACKS\n"
        [[ -n "$EDITOR" ]] && CONTEXT+="- Editor: $EDITOR\n"
    fi
fi

# If CLAUDE_ENV_FILE available, write context safely
# Use base64 encoding to avoid shell escaping issues with JSON
if [[ -n "${ENV_FILE:-}" && -w "$ENV_FILE" ]]; then
    # Base64 encode profile to avoid quote/escape issues
    PROFILE_B64=$(echo "$PROFILE" | tr -d '\n' | base64 -w 0 2>/dev/null || echo "$PROFILE" | tr -d '\n' | base64)
    echo "USER_MEMORY_PROFILE_B64='${PROFILE_B64}'" >> "$ENV_FILE"

    # Context is simpler - escape single quotes by replacing ' with '\''
    if [[ -n "$CONTEXT" ]]; then
        ESCAPED_CONTEXT="${CONTEXT//\'/\'\\\'\'}"
        echo "USER_MEMORY_CONTEXT='${ESCAPED_CONTEXT}'" >> "$ENV_FILE"
    fi
fi

# Output context to stderr for logging
if [[ -n "$CONTEXT" ]]; then
    echo -e "user-memory[mcp]: loaded context:\n$CONTEXT" >&2
else
    echo "user-memory[mcp]: loaded profile from $PROFILE_PATH" >&2
fi
