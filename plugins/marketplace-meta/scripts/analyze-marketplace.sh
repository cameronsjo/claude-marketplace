#!/bin/bash
# Analyze local marketplace and provide session context
# Called by SessionStart hook when marketplace is installed locally

MARKETPLACE_PATH="/Users/cameron/Projects/claude-marketplace"

# Check if marketplace exists locally
if [ ! -d "$MARKETPLACE_PATH" ]; then
    exit 0  # Silent exit if not local development
fi

# Check if we're in the marketplace directory or a related project
CWD=$(pwd)
if [[ "$CWD" != *"claude-marketplace"* ]] && [[ "$CWD" != *"Projects"* ]]; then
    exit 0  # Only activate for development contexts
fi

# Gather marketplace stats
PLUGIN_COUNT=$(find "$MARKETPLACE_PATH/plugins" -maxdepth 1 -type d | wc -l | tr -d ' ')
PLUGIN_COUNT=$((PLUGIN_COUNT - 1))  # Subtract 1 for the plugins dir itself

AGENT_COUNT=$(find "$MARKETPLACE_PATH/plugins" -name "*.md" -path "*/agents/*" | wc -l | tr -d ' ')
COMMAND_COUNT=$(find "$MARKETPLACE_PATH/plugins" -name "*.md" -path "*/commands/*" | wc -l | tr -d ' ')
SKILL_COUNT=$(find "$MARKETPLACE_PATH/registry/skills" -name "SKILL.md" | wc -l | tr -d ' ')

# Check for uncommitted changes
cd "$MARKETPLACE_PATH"
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
BRANCH=$(git branch --show-current 2>/dev/null)

# Get recent changes
RECENT_COMMITS=$(git log --oneline -3 2>/dev/null | head -3)

# Output context for Claude
echo "🏪  Local Marketplace Development Mode"
echo "    Path: $MARKETPLACE_PATH"
echo "    Branch: $BRANCH"
echo ""
echo "📊  Stats: $PLUGIN_COUNT plugins, $AGENT_COUNT agents, $COMMAND_COUNT commands, $SKILL_COUNT skills"

if [ "$UNCOMMITTED" -gt 0 ]; then
    echo "⚠️   $UNCOMMITTED uncommitted changes"
fi

echo ""
echo "📝  Recent commits:"
echo "$RECENT_COMMITS" | while read line; do
    echo "    $line"
done

echo ""
echo "💡  Use /marketplace.review for detailed analysis and improvement suggestions"
