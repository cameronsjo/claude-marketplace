# Deep Research Skill

Enables automatic deep research mode when trigger phrases are detected in user prompts.

## Overview

This skill provides a UserPromptSubmit hook that detects natural language cues indicating the user wants thorough, comprehensive research. When triggered, it injects instructions for Claude to use enhanced research capabilities.

## When This Skill Activates

The hook automatically detects these trigger phrases (case-insensitive):

- "deep dive"
- "use your noodle"
- "pull out the stops"
- "dig deep"
- "really research"
- "thorough investigation"
- "comprehensive analysis"
- "leave no stone unturned"

## What Deep Research Mode Does

When activated, Claude will:

1. **Use WebSearch extensively** - Ground responses with current information from the web
2. **Spawn Explore agents** - Thoroughly investigate the codebase with specialized agents
3. **Think systematically** - Work through the problem methodically before responding
4. **Synthesize multiple sources** - Combine findings from various sources into a cohesive answer
5. **Provide citations** - Include sources for web-based findings

## Installation

### Hook Configuration

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "command": "~/.claude/skills/deep-research/scripts/detect-research-mode.sh"
      }
    ]
  }
}
```

### Manual Setup

1. Copy the skill to your Claude skills directory:
   ```bash
   cp -r registry/skills/deep-research ~/.claude/skills/
   ```

2. Make the hook script executable:
   ```bash
   chmod +x ~/.claude/skills/deep-research/scripts/detect-research-mode.sh
   ```

3. Add the hook configuration above to your settings

## Usage Examples

### Automatic Activation

Simply use trigger phrases naturally in your prompts:

```
"I need to deep dive into how authentication works in this codebase"
"Use your noodle on this one - why is the build failing?"
"Let's pull out the stops and figure out the best caching strategy"
```

### What Happens

When a trigger phrase is detected, you'll see output like:

```
Deep research mode: Use WebSearch for current info, spawn Explore agents for codebase investigation, think systematically, synthesize findings from multiple sources.
```

This instructs Claude to use enhanced research capabilities for your question.

## Customization

### Adding Trigger Phrases

Edit `scripts/detect-research-mode.sh` and add patterns to the grep regex:

```bash
if echo "$input" | grep -qiE "(your-phrase|another-phrase)"; then
```

### Modifying Research Instructions

Edit the output message in the script to customize what research behaviors are triggered.

## Scripts

- `scripts/detect-research-mode.sh` - UserPromptSubmit hook that detects trigger phrases

## Related Skills

- **research-tools** plugin - Commands for structured research workflows
- **comprehensive-researcher** agent - Agent specialized in multi-source research
