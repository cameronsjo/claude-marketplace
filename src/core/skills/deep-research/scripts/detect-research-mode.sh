#!/bin/bash
# Deep Research Mode Detection Hook
#
# UserPromptSubmit hook that detects natural language cues for thorough research.
# When trigger phrases are detected, injects instructions for enhanced research.
#
# Installation: Add to .claude/settings.json:
# {
#   "hooks": {
#     "UserPromptSubmit": [{
#       "command": "~/.claude/skills/deep-research/scripts/detect-research-mode.sh"
#     }]
#   }
# }

# Read user prompt from stdin
input=$(cat)

# Check for trigger phrases (case-insensitive)
# Add or remove phrases as desired
if echo "$input" | grep -qiE "(deep dive|use your noodle|pull out the stops|dig deep|really research|thorough investigation|comprehensive analysis|leave no stone unturned|investigate thoroughly|research this hard)"; then
    cat << 'EOF'
Deep research mode: Use WebSearch for current info, spawn Explore agents for codebase investigation, think systematically, synthesize findings from multiple sources.
EOF
fi
