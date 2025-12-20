#!/bin/bash
# Session Sync: Log when context compaction happens
# Triggered by PreCompact hook

set -euo pipefail

# Check for required env var
if [[ -z "${CLAUDE_TIMELINE_PATH:-}" ]]; then
    exit 0
fi

# Expand ~ in path
TIMELINE_PATH="${CLAUDE_TIMELINE_PATH/#\~/$HOME}"

# Check file exists
if [[ ! -f "$TIMELINE_PATH" ]]; then
    exit 0
fi

# Get current time and date
TIME=$(date +"%H:%M")
TODAY=$(date +"%Y-%m-%d")

# Build the entry
ENTRY="- $TIME **State**: Context compaction triggered"

# Check if today's date section exists
if grep -q "^### $TODAY" "$TIMELINE_PATH"; then
    # Insert after today's date header
    sed -i '' "/^### $TODAY/a\\
$ENTRY
" "$TIMELINE_PATH"
else
    # Insert new date section after "## Work Log"
    sed -i '' "/^## Work Log/a\\
\\
### $TODAY\\
$ENTRY
" "$TIMELINE_PATH"
fi

echo ""
echo "📋 Logged context compaction to timeline"

exit 0
