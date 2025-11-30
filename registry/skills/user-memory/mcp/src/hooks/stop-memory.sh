#!/bin/bash
# MCP Stop hook: Extract preferences using TypeScript extractor
# Full pattern matching via extract-memory.ts

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEMORY_DIR="${USER_MEMORY_DIR:-$HOME/.claude/user-memory}"
PROCESSED_FILE="$MEMORY_DIR/.processed_turns"

mkdir -p "$MEMORY_DIR"
touch "$PROCESSED_FILE"

# Read hook input
INPUT=$(cat)

# Requires jq for JSON parsing
if ! command -v jq &>/dev/null; then
    echo "user-memory[mcp]: jq required" >&2
    exit 0
fi

TRANSCRIPT_PATH=$(echo "$INPUT" | jq -r '.transcript_path // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

[[ -z "$TRANSCRIPT_PATH" || ! -f "$TRANSCRIPT_PATH" ]] && exit 0

# Dedup check
TURN_MARKER="${SESSION_ID}:$(wc -l < "$TRANSCRIPT_PATH" | tr -d ' ')"
grep -qF "$TURN_MARKER" "$PROCESSED_FILE" 2>/dev/null && exit 0

# Run TypeScript extractor
EXTRACTOR="$SCRIPT_DIR/../extract-memory.ts"
if command -v tsx &>/dev/null; then
    tsx "$EXTRACTOR" "$TRANSCRIPT_PATH" "$SESSION_ID" 2>&1 || true
elif command -v npx &>/dev/null; then
    npx tsx "$EXTRACTOR" "$TRANSCRIPT_PATH" "$SESSION_ID" 2>&1 || true
else
    echo "user-memory[mcp]: tsx not found, skipping extraction" >&2
fi

# Mark processed
echo "$TURN_MARKER" >> "$PROCESSED_FILE"

# Prune old markers
tail -n 1000 "$PROCESSED_FILE" > "$PROCESSED_FILE.tmp" && mv "$PROCESSED_FILE.tmp" "$PROCESSED_FILE"
