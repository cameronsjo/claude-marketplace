#!/bin/bash
# Session Sync: Read timeline on session start
# Tries MCP server first, falls back to filesystem

set -euo pipefail

# Check for required env var
if [[ -z "${CLAUDE_TIMELINE_PATH:-}" ]]; then
    exit 0
fi

# Expand ~ in path
TIMELINE_PATH="${CLAUDE_TIMELINE_PATH/#\~/$HOME}"

# Check if file exists
if [[ ! -f "$TIMELINE_PATH" ]]; then
    echo "session-sync: Timeline not found at $TIMELINE_PATH" >&2
    echo "session-sync: Run /session.init to create one" >&2
    exit 0
fi

# Get device identifier
case "$(uname -s)" in
    Darwin) DEVICE="Mac" ;;
    Linux)
        if [[ -n "${WSL_DISTRO_NAME:-}" ]]; then
            DEVICE="Windows"
        elif [[ "${CLAUDE_CODE_REMOTE:-}" == "true" ]]; then
            DEVICE="Web"
        else
            DEVICE="Linux"
        fi
        ;;
    MINGW*|CYGWIN*) DEVICE="Windows" ;;
    *) DEVICE="Unknown" ;;
esac

# Read timeline content
CONTENT=$(cat "$TIMELINE_PATH" 2>/dev/null || echo "")

if [[ -z "$CONTENT" ]]; then
    echo "session-sync: Timeline is empty" >&2
    exit 0
fi

# Extract last session info (find first ### heading in Session Log)
LAST_SESSION=$(echo "$CONTENT" | grep -A1 "^### [0-9]" | head -2 | tr '\n' ' ' || echo "No previous sessions")

# Extract pending TODOs
PENDING_TODOS=$(echo "$CONTENT" | grep "^- \[ \]" | head -5 || echo "")

# Output context for Claude
echo ""
echo "=== Session Sync ==="
echo "Timeline: $TIMELINE_PATH"
echo "Device: $DEVICE"
echo ""

if [[ -n "$LAST_SESSION" && "$LAST_SESSION" != "No previous sessions" ]]; then
    echo "Last session: $LAST_SESSION"
fi

if [[ -n "$PENDING_TODOS" ]]; then
    echo ""
    echo "Pending TODOs:"
    echo "$PENDING_TODOS"
fi

echo ""
echo "Use /session.sync to update the timeline before ending."
echo "==================="

# Also read additional context directory if specified
if [[ -n "${CLAUDE_CONTEXT_DIR:-}" && -d "${CLAUDE_CONTEXT_DIR/#\~/$HOME}" ]]; then
    CONTEXT_DIR="${CLAUDE_CONTEXT_DIR/#\~/$HOME}"
    echo ""
    echo "Additional context available in: $CONTEXT_DIR"
fi

exit 0
