# Quick Reference

## Setup Cheatsheet

### Minimal Mode (Shell-only)

```bash
# No install needed - just configure hooks

# ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/minimal/session-start.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/minimal/stop-memory.sh"
      }]
    }]
  }
}
```

### MCP Mode (Full)

```bash
# Install dependencies
cd ~/.claude/skills/user-memory/mcp
npm install

# ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/mcp/src/hooks/session-start.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/user-memory/mcp/src/hooks/stop-memory.sh"
      }]
    }]
  },
  "mcpServers": {
    "user-memory": {
      "command": "npx",
      "args": ["tsx", "~/.claude/skills/user-memory/mcp/src/mcp-server.ts"]
    }
  }
}
```

---

## Trigger Phrases

### Tech Stack

| Say this... | Stores... |
|-------------|-----------|
| "I prefer Bun" | `preferredStacks: ["Bun"]` |
| "I'm switching to FastAPI" | `preferredStacks: ["FastAPI"]` |
| "I always use TypeScript + React" | `preferredStacks: ["TypeScript", "React"]` |
| "My default stack is Next.js" | `preferredStacks: ["Next.js"]` |

### Editor

| Say this... | Stores... |
|-------------|-----------|
| "I use neovim" | `editor: "neovim"` |
| "My editor is VS Code" | `editor: "vscode"` |
| "I'm using Cursor" | `editor: "cursor"` |

### Tone

| Say this... | Stores... |
|-------------|-----------|
| "Be more direct" | `tone: "direct"` |
| "I prefer concise responses" | `tone: "direct"` |
| "Be friendly" | `tone: "friendly"` |
| "I like detailed explanations" | `tone: "neutral"` |

### Role

| Say this... | Stores... |
|-------------|-----------|
| "I'm a backend engineer" | `role: "backend engineer"` |
| "I'm an ML researcher" | `role: "ML researcher"` |
| "I'm a senior developer" | `role: "senior developer"` |

### Languages

| Say this... | Stores... |
|-------------|-----------|
| "I work mostly in TypeScript" | `languages: ["TypeScript"]` |
| "My main languages are Python and Rust" | `languages: ["Python", "Rust"]` |

### Avoid

| Say this... | Stores... |
|-------------|-----------|
| "Don't use sports metaphors" | `avoidExamples: ["sports"]` |
| "Avoid foo examples" | `avoidExamples: ["foo"]` |

---

## Removal Phrases

| Say this... | Effect |
|-------------|--------|
| "I no longer use Webpack" | Removes Webpack from stacks |
| "I stopped using React" | Removes React from stacks |
| "I don't use npm anymore" | Removes npm from tools |
| "Forget that I prefer tabs" | Removes that preference |
| "Remove my preference for X" | Removes X preference |
| "I switched away from npm" | Removes npm |

---

## MCP Tool Quick Reference

### Profile Tools

```
get_user_profile()
  → Returns full profile JSON

update_user_profile({ work: { role: "..." } })
  → Merges updates into profile

remove_preference({ paths: ["tools.editor"] })
  → Removes specific preferences

clear_user_profile({ confirm: true })
  → Deletes entire profile

get_changelog({ limit: 20 })
  → Returns recent changes

get_preference_metadata()
  → Returns confidence scores, decay estimates

run_decay()
  → Forces decay cycle, returns removed prefs
```

### Session Tools

```
get_session_context({ projectPath: "/path" })
  → Returns resume context from previous sessions

update_task({ sessionId: "x", id: "task-1", status: "in_progress" })
  → Creates/updates task

log_decision({ sessionId: "x", decision: "Use X", rationale: "..." })
  → Records decision

add_session_context({ sessionId: "x", context: "Note..." })
  → Adds context note

set_session_summary({ sessionId: "x", summary: "Did X, blocked on Y" })
  → Sets summary for next session

get_full_context({ projectPath: "/path" })
  → Returns combined profile + session context
```

---

## File Locations

```
~/.claude/user-memory/
├── profile.json          # Your preferences
├── profile-meta.json     # Confidence tracking
├── changelog.jsonl       # Audit trail
├── .processed_turns      # Dedup tracker
└── sessions/
    └── session-xxx.json  # Session progress
```

Override: `USER_MEMORY_DIR=/custom/path`

---

## Decay Math

```
Confidence after N days = initial × 0.5^(N/30)

Day 0:   1.00  (new preference)
Day 30:  0.50  (halved)
Day 60:  0.25  (quartered)
Day 90:  0.125 (below 0.1 → REMOVED)

Reinforcement: +0.30 confidence (capped at 1.0)
```

---

## Debugging

```bash
# Check profile
cat ~/.claude/user-memory/profile.json | jq

# Check confidence scores
cat ~/.claude/user-memory/profile-meta.json | jq '.preferences'

# Check recent changes
tail -20 ~/.claude/user-memory/changelog.jsonl | jq -s

# Check processed turns
cat ~/.claude/user-memory/.processed_turns

# Check sessions
ls ~/.claude/user-memory/sessions/
```

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Profile not loading | Check hook paths in settings.json |
| Preferences not extracting | Check transcript_path in Stop hook input |
| Decay running too often | Decay only runs if 24+ hours since last |
| MCP server not starting | Run `npm install` in mcp/ directory |
| jq not found | Install jq or use MCP mode |
