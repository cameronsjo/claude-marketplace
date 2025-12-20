#!/bin/bash
# Session Sync: Remind to update timeline on session end
# This is a reminder hook - actual update is done via /session.sync or skill

set -euo pipefail

# Check for required env var
if [[ -z "${CLAUDE_TIMELINE_PATH:-}" ]]; then
    exit 0
fi

# Output reminder
echo ""
echo "=== Session Sync Reminder ==="
echo "Don't forget to update the timeline before ending!"
echo "Use /session.sync or ask Claude to update the session log."
echo "============================="

exit 0
