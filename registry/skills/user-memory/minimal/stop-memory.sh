#!/bin/bash
# Minimal Stop hook: Extract preferences with dedup
# Uses jq for JSON, pure bash patterns for extraction

set -euo pipefail

MEMORY_DIR="${USER_MEMORY_DIR:-$HOME/.claude/user-memory}"
PROFILE_PATH="$MEMORY_DIR/profile.json"
PROCESSED_FILE="$MEMORY_DIR/.processed_turns"
CHANGELOG_PATH="$MEMORY_DIR/changelog.jsonl"

mkdir -p "$MEMORY_DIR"
touch "$PROCESSED_FILE"

# Read hook input
INPUT=$(cat)

# Extract transcript path (requires jq)
if ! command -v jq &>/dev/null; then
    echo "user-memory: jq required for extraction" >&2
    exit 0
fi

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# Dedup check: session:linecount as marker
TURN_MARKER="${SESSION_ID}:$(wc -l < "$TRANSCRIPT_PATH" | tr -d ' ')"
grep -qF "$TURN_MARKER" "$PROCESSED_FILE" 2>/dev/null && exit 0

# Extract user messages from JSONL
USER_MESSAGES=$(cat "$TRANSCRIPT_PATH" | while read -r line; do
    ROLE=$(echo "$line" | jq -r '.message.role // .type // empty' 2>/dev/null)
    if [[ "$ROLE" == "user" ]]; then
        echo "$line" | jq -r '.message.content // empty' 2>/dev/null | head -c 1000
    fi
done)

# Pattern matching for preferences
UPDATES=""

# Tech stack: "I prefer X" or "I'm switching to X"
if echo "$USER_MESSAGES" | grep -qiE '(i prefer|from now on|i.m switching to|always use)\s+\w+'; then
    STACK=$(echo "$USER_MESSAGES" | grep -oiE '(i prefer|from now on|i.m switching to|always use)\s+\w+' | head -1 | sed 's/.*\s//')
    [[ -n "$STACK" ]] && UPDATES="$UPDATES\"preferredStacks\":[\"$STACK\"],"
fi

# Editor: "I use vim/neovim/vscode/etc"
if echo "$USER_MESSAGES" | grep -qiE '(i use|my editor is)\s+(vim|neovim|nvim|vscode|emacs|cursor|zed)'; then
    EDITOR=$(echo "$USER_MESSAGES" | grep -oiE '(vim|neovim|nvim|vscode|emacs|cursor|zed)' | head -1 | tr '[:upper:]' '[:lower:]')
    [[ -n "$EDITOR" ]] && UPDATES="$UPDATES\"editor\":\"$EDITOR\","
fi

# Tone: "be more direct/concise/friendly"
if echo "$USER_MESSAGES" | grep -qiE '(be more|i prefer)\s+(direct|concise|friendly|detailed)'; then
    TONE=$(echo "$USER_MESSAGES" | grep -oiE '(direct|concise|friendly|detailed)' | head -1 | tr '[:upper:]' '[:lower:]')
    case "$TONE" in
        direct|concise) TONE="direct" ;;
        friendly) TONE="friendly" ;;
        *) TONE="neutral" ;;
    esac
    UPDATES="$UPDATES\"tone\":\"$TONE\","
fi

# If no updates, mark processed and exit
if [[ -z "$UPDATES" ]]; then
    echo "$TURN_MARKER" >> "$PROCESSED_FILE"
    exit 0
fi

# Remove trailing comma
UPDATES="${UPDATES%,}"

# Load or create profile
if [[ -f "$PROFILE_PATH" ]]; then
    EXISTING=$(cat "$PROFILE_PATH")
else
    EXISTING='{"userId":"'${USER:-default}'","schemaVersion":1}'
fi

# Merge updates (simple jq merge)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
NEW_PROFILE=$(echo "$EXISTING" | jq --argjson updates "{\"codePreferences\":{$UPDATES},\"tools\":{},\"lastUpdated\":\"$TIMESTAMP\"}" '
    . * $updates |
    .codePreferences = (.codePreferences // {}) * ($updates.codePreferences // {}) |
    .tools = (.tools // {}) * ($updates.tools // {}) |
    .lastUpdated = $updates.lastUpdated
')

# Log to changelog (append-only audit trail)
CHANGELOG_ENTRY=$(jq -cn \
    --arg ts "$TIMESTAMP" \
    --arg sid "$SESSION_ID" \
    --arg action "extract" \
    --arg source "minimal/hook" \
    --argjson changes "{\"codePreferences\":{$UPDATES}}" \
    '{timestamp: $ts, session_id: $sid, action: $action, source: $source, changes: $changes}')
echo "$CHANGELOG_ENTRY" >> "$CHANGELOG_PATH"

echo "$NEW_PROFILE" > "$PROFILE_PATH"
echo "$TURN_MARKER" >> "$PROCESSED_FILE"

# Prune old markers
tail -n 1000 "$PROCESSED_FILE" > "$PROCESSED_FILE.tmp" && mv "$PROCESSED_FILE.tmp" "$PROCESSED_FILE"

echo "user-memory: updated profile" >&2
