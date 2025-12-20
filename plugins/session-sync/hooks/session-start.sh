#!/bin/bash
# Session Sync: Read timeline on session start
# Surfaces inbox items and recent work log entries

set -euo pipefail

# Check for required env var
if [[ -z "${CLAUDE_TIMELINE_PATH:-}" ]]; then
    exit 0
fi

# Expand ~ in path
TIMELINE_PATH="${CLAUDE_TIMELINE_PATH/#\~/$HOME}"

# Check if file exists
if [[ ! -f "$TIMELINE_PATH" ]]; then
    echo ""
    echo "📋 Timeline not found at $TIMELINE_PATH"
    echo "   Run /session.init to create one"
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
    echo "📋 Timeline is empty"
    exit 0
fi

# Extract inbox items (lines starting with "- [ ]" after "## Inbox")
INBOX_ITEMS=$(echo "$CONTENT" | sed -n '/^## Inbox/,/^## /p' | grep "^- \[.\]" | head -10 || echo "")
INBOX_COUNT=$(echo "$INBOX_ITEMS" | grep -c "^- \[.\]" 2>/dev/null || echo "0")

# Get last work log entry
LAST_ENTRY=$(echo "$CONTENT" | grep "^- [0-9][0-9]:[0-9][0-9] \*\*" | head -1 || echo "")

# Output context for Claude
echo ""
echo "📋 Timeline loaded ($DEVICE)"

if [[ "$INBOX_COUNT" -gt 0 ]]; then
    echo ""
    echo "📥 Inbox ($INBOX_COUNT items):"
    echo "$INBOX_ITEMS"
fi

if [[ -n "$LAST_ENTRY" ]]; then
    echo ""
    echo "📝 Last entry: $LAST_ENTRY"
fi

exit 0
