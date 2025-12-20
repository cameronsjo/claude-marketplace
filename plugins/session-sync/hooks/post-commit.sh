#!/bin/bash
# Session Sync: Auto-log git commits to timeline
# Triggered by PostToolUse hook on Bash(git commit:*)

set -euo pipefail

# Check for required env var
if [[ -z "${CLAUDE_TIMELINE_PATH:-}" ]]; then
    exit 0
fi

# Read hook input from stdin
INPUT=$(cat)

# Try to extract commit info from the tool output
# This hook is triggered after a successful git commit

# Get the last commit message and short SHA
COMMIT_MSG=$(git log -1 --format="%s" 2>/dev/null || echo "")
COMMIT_SHA=$(git log -1 --format="%h" 2>/dev/null || echo "")

if [[ -z "$COMMIT_MSG" || -z "$COMMIT_SHA" ]]; then
    exit 0
fi

# Output reminder to log the commit
echo ""
echo "=== Commit Logged ==="
echo "**Commit**: $COMMIT_MSG ($COMMIT_SHA)"
echo ""
echo "Consider running /session.log commit $COMMIT_MSG ($COMMIT_SHA)"
echo "Or I can add this to the Work Log automatically."
echo "===================="

exit 0
