# User Memory Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Claude Code Session                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │ SessionStart │───▶│   Conversation│───▶│     Stop     │                  │
│  │    Hook      │    │              │    │     Hook     │                  │
│  └──────┬───────┘    └──────────────┘    └──────┬───────┘                  │
│         │                                        │                          │
│         ▼                                        ▼                          │
│  ┌──────────────┐                        ┌──────────────┐                  │
│  │ Load Profile │                        │   Extract    │                  │
│  │ + Run Decay  │                        │ Preferences  │                  │
│  └──────┬───────┘                        └──────┬───────┘                  │
│         │                                        │                          │
│         ▼                                        ▼                          │
│  ┌──────────────┐                        ┌──────────────┐                  │
│  │   Inject     │                        │    Merge     │                  │
│  │   Context    │                        │   Profile    │                  │
│  └──────────────┘                        └──────────────┘                  │
│                                                                             │
│                    ┌──────────────────────┐                                │
│                    │    MCP Server        │                                │
│                    │  (Real-time Tools)   │                                │
│                    └──────────────────────┘                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ~/.claude/user-memory/                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │  profile.json   │  │ profile-meta.json│  │ changelog.jsonl │             │
│  │                 │  │                 │  │                 │             │
│  │ • Preferences   │  │ • Confidence    │  │ • Audit trail   │             │
│  │ • Work info     │  │ • Last seen     │  │ • All changes   │             │
│  │ • Tools         │  │ • Decay state   │  │ • Timestamps    │             │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘             │
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────────────────────────┐              │
│  │ .processed_turns│  │ sessions/                           │              │
│  │                 │  │  ├── session-abc123.json            │              │
│  │ • Dedup tracker │  │  ├── session-def456.json            │              │
│  │                 │  │  └── ...                            │              │
│  └─────────────────┘  └─────────────────────────────────────┘              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Dual Implementation Modes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   MINIMAL MODE (Shell-only)              MCP MODE (Full TypeScript)        │
│   ═════════════════════════              ══════════════════════════        │
│                                                                             │
│   Dependencies: jq only                  Dependencies: Node, tsx, MCP SDK  │
│                                                                             │
│   ┌─────────────────────┐               ┌─────────────────────┐            │
│   │ minimal/            │               │ mcp/                │            │
│   │  ├── session-start.sh│               │  ├── src/           │            │
│   │  └── stop-memory.sh │               │  │   ├── hooks/     │            │
│   └─────────────────────┘               │  │   ├── mcp-server.ts│           │
│                                         │  │   ├── store.ts   │            │
│   Features:                             │  │   ├── session.ts │            │
│   ✓ Profile loading                     │  │   └── ...        │            │
│   ✓ Heuristic extraction                │  └── package.json   │            │
│   ✓ Changelog logging                   └─────────────────────┘            │
│   ✗ Real-time tools                                                        │
│   ✗ Session continuity                  Features:                          │
│   ✗ Decay/confidence                    ✓ Everything in minimal            │
│                                         ✓ 13 MCP tools                     │
│                                         ✓ Session continuity               │
│                                         ✓ Decay/confidence tracking        │
│                                         ✓ Context injection                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow: SessionStart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SessionStart Hook Flow                            │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────┐
     │  Claude  │
     │  Code    │
     │ Starts   │
     └────┬─────┘
          │
          ▼
     ┌──────────────────────┐
     │ SessionStart Hook    │
     │ Receives:            │
     │ • session_id         │
     │ • cwd                │
     │ • env_file           │
     └──────────┬───────────┘
                │
                ▼
     ┌──────────────────────┐     ┌──────────────────────┐
     │ Run Decay Check?     │────▶│ decay-check.ts       │
     │ (MCP mode only)      │     │                      │
     │                      │     │ • Check last decay   │
     │ If 24+ hours since   │     │ • Apply decay        │
     │ last decay           │     │ • Prune changelog    │
     └──────────┬───────────┘     └──────────────────────┘
                │
                ▼
     ┌──────────────────────┐
     │ Load profile.json    │
     └──────────┬───────────┘
                │
                ▼
     ┌──────────────────────┐
     │ Build Context        │
     │                      │
     │ Extract:             │
     │ • Role               │
     │ • Tone preference    │
     │ • Preferred stacks   │
     │ • Editor             │
     └──────────┬───────────┘
                │
                ▼
     ┌──────────────────────┐
     │ Inject Context       │
     │                      │
     │ Write to:            │
     │ • CLAUDE_ENV_FILE    │
     │ • stderr (logging)   │
     └──────────────────────┘
```

## Data Flow: Stop Hook (Extraction)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Stop Hook Flow                                  │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────────────┐
     │ Claude Response  │
     │ Complete         │
     └────────┬─────────┘
              │
              ▼
     ┌──────────────────────┐
     │ Stop Hook Receives:  │
     │ • session_id         │
     │ • transcript_path    │
     │ • stop_hook_active   │
     └──────────┬───────────┘
              │
              ▼
     ┌──────────────────────┐
     │ Check Dedup          │
     │                      │
     │ Compare transcript   │
     │ line count with      │
     │ .processed_turns     │
     │                      │
     │ Skip if no new turns │
     └──────────┬───────────┘
              │ New turns found
              ▼
     ┌──────────────────────┐
     │ Parse Transcript     │
     │                      │
     │ Extract user         │
     │ messages only        │
     └──────────┬───────────┘
              │
              ▼
     ┌──────────────────────┐
     │ Pattern Matching     │
     │                      │
     │ ┌─────────────────┐  │
     │ │ Negation (P:10) │  │  ← Higher priority
     │ │ "I stopped..."  │  │
     │ │ "No longer..."  │  │
     │ └─────────────────┘  │
     │         │            │
     │         ▼            │
     │ ┌─────────────────┐  │
     │ │ Positive (P:5)  │  │
     │ │ "I prefer..."   │  │
     │ │ "I use..."      │  │
     │ └─────────────────┘  │
     │         │            │
     │         ▼            │
     │ ┌─────────────────┐  │
     │ │ Standard (P:0)  │  │
     │ │ "My editor..."  │  │
     │ │ "I work in..."  │  │
     │ └─────────────────┘  │
     └──────────┬───────────┘
              │
              ├────────────────────┐
              │                    │
              ▼                    ▼
     ┌──────────────┐     ┌──────────────┐
     │   Removals   │     │   Updates    │
     │              │     │              │
     │ Remove from  │     │ Merge into   │
     │ profile.json │     │ profile.json │
     └──────┬───────┘     └──────┬───────┘
            │                    │
            └────────┬───────────┘
                     │
                     ▼
            ┌──────────────┐
            │ Log Change   │
            │              │
            │ Append to    │
            │ changelog    │
            └──────────────┘
```

## Decay System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Confidence Decay Model                            │
└─────────────────────────────────────────────────────────────────────────────┘

  Confidence
      │
  1.0 ┼─●─────────────────────────────────────────────────────────────────────
      │   ╲
      │    ╲  Exponential decay
  0.8 ┼     ╲  confidence × 0.5^(days/30)
      │      ╲
      │       ╲
  0.6 ┼        ╲
      │         ╲
      │          ╲         ●──── Reinforcement (+0.3)
  0.5 ┼───────────●       ╱
      │            ╲     ╱
      │             ╲   ╱
  0.4 ┼              ╲ ╱
      │               ●
      │                ╲
  0.3 ┼                 ╲
      │                  ╲
      │                   ╲
  0.2 ┼                    ╲
      │                     ╲
  0.1 ┼─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ╲─ ─ ─ ─ ─ ─ ─ ─ ─ ─  Removal threshold
      │                       ╲
  0.0 ┼────────────────────────●──────────────────────────────────────────────
      └───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┬──▶
              0      30      60      75      90     120     150     180   Days

  Timeline:
  ─────────────────────────────────────────────────────────────────────────────
  Day 0:   User says "I prefer Bun"           → Confidence = 1.00
  Day 30:  No mention, decay applied          → Confidence = 0.50
  Day 60:  No mention, decay applied          → Confidence = 0.25
  Day 75:  User says "Using Bun for this"     → Confidence = 0.55 (reinforced)
  Day 90:  No mention, decay applied          → Confidence = 0.39
  Day 150: No mention, decay applied          → Confidence = 0.08 (< 0.1)
           ⚠️  AUTO-REMOVED from profile
```

## Session Continuity

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Session Continuity Flow                            │
└─────────────────────────────────────────────────────────────────────────────┘

  Session 1                    Session 2                    Session 3
  ═════════                    ═════════                    ═════════

  ┌─────────────┐             ┌─────────────┐             ┌─────────────┐
  │ Start       │             │ Start       │             │ Start       │
  └──────┬──────┘             └──────┬──────┘             └──────┬──────┘
         │                           │                           │
         ▼                           ▼                           ▼
  ┌─────────────┐             ┌─────────────┐             ┌─────────────┐
  │ Work on     │             │ get_session │             │ get_session │
  │ Feature A   │             │ _context()  │             │ _context()  │
  └──────┬──────┘             └──────┬──────┘             └──────┬──────┘
         │                           │                           │
         ▼                           │ Resume context:           │
  ┌─────────────┐                    │ • Task: "Feature A"       │
  │ update_task │                    │   Status: blocked         │
  │ id: feat-a  │                    │ • Decision: "Use X"       │
  │ status: wip │                    │                           │
  └──────┬──────┘             ┌──────┴──────┐             ┌──────┴──────┐
         │                    │ Continue    │             │ Complete    │
         ▼                    │ Feature A   │             │ Feature A   │
  ┌─────────────┐             └──────┬──────┘             └──────┬──────┘
  │ log_decision│                    │                           │
  │ "Use X lib" │                    ▼                           ▼
  └──────┬──────┘             ┌─────────────┐             ┌─────────────┐
         │                    │ update_task │             │ update_task │
         ▼                    │ id: feat-a  │             │ id: feat-a  │
  ┌─────────────┐             │ status: wip │             │ status: done│
  │ Hit blocker │             └──────┬──────┘             └──────┬──────┘
  │ update_task │                    │                           │
  │ status:block│                    ▼                           ▼
  └──────┬──────┘             ┌─────────────┐             ┌─────────────┐
         │                    │ set_session │             │ set_session │
         ▼                    │ _summary    │             │ _summary    │
  ┌─────────────┐             └─────────────┘             │ "Completed" │
  │ set_session │                                         └─────────────┘
  │ _summary    │
  │ "Blocked on"│
  └─────────────┘

         │                           │                           │
         ▼                           ▼                           ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │                     sessions/session-xxx.json                        │
  │                                                                      │
  │  {                                                                   │
  │    "sessionId": "xxx",                                               │
  │    "tasks": [{ "id": "feat-a", "status": "completed", ... }],       │
  │    "decisions": [{ "decision": "Use X lib", ... }],                 │
  │    "summary": "Completed Feature A"                                  │
  │  }                                                                   │
  └─────────────────────────────────────────────────────────────────────┘
```

## MCP Tools Reference

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MCP Tools (13 total)                           │
└─────────────────────────────────────────────────────────────────────────────┘

  PROFILE TOOLS                          SESSION TOOLS
  ═════════════                          ═════════════

  ┌─────────────────────┐                ┌─────────────────────┐
  │ get_user_profile    │                │ get_session_context │
  │                     │                │                     │
  │ Read current profile│                │ Resume from previous│
  │ at session start    │                │ session             │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐                ┌─────────────────────┐
  │ update_user_profile │                │ update_task         │
  │                     │                │                     │
  │ Add/update prefs    │                │ Track task progress │
  │ Tracks confidence   │                │ pending → completed │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐                ┌─────────────────────┐
  │ remove_preference   │                │ log_decision        │
  │                     │                │                     │
  │ Explicit removal    │                │ Record decisions    │
  │ by dot-path         │                │ with rationale      │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐                ┌─────────────────────┐
  │ clear_user_profile  │                │ add_session_context │
  │                     │                │                     │
  │ Reset everything    │                │ Store context notes │
  │ Requires confirm    │                │ for future          │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐                ┌─────────────────────┐
  │ get_changelog       │                │ set_session_summary │
  │                     │                │                     │
  │ Audit trail of      │                │ Summary shown at    │
  │ all changes         │                │ next session start  │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐                ┌─────────────────────┐
  │ get_preference_     │                │ get_full_context    │
  │ metadata            │                │                     │
  │                     │                │ Profile + session   │
  │ Confidence scores   │                │ Combined prompt     │
  │ Days until decay    │                │                     │
  └─────────────────────┘                └─────────────────────┘

  ┌─────────────────────┐
  │ run_decay           │
  │                     │
  │ Manual decay cycle  │
  │ Remove stale prefs  │
  └─────────────────────┘
```

## Pattern Matching Priority

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Pattern Priority System                             │
└─────────────────────────────────────────────────────────────────────────────┘

  Input: "I prefer Bun over npm, and I stopped using Webpack"

  ┌───────────────────────────────────────────────────────────────────────────┐
  │ Priority 10: NEGATION PATTERNS                                            │
  │ ─────────────────────────────────                                         │
  │                                                                           │
  │ Match: "I stopped using Webpack"                                          │
  │ Action: REMOVE codePreferences.preferredStacks.webpack                    │
  └───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ Priority 5: COMPARATIVE PATTERNS                                          │
  │ ────────────────────────────────                                          │
  │                                                                           │
  │ Match: "I prefer Bun over npm"                                            │
  │ Action: ADD Bun, REMOVE npm                                               │
  └───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ Priority 0: STANDARD PATTERNS                                             │
  │ ──────────────────────────────                                            │
  │                                                                           │
  │ "I use neovim"       → tools.editor = "neovim"                            │
  │ "I'm a backend dev"  → work.role = "backend developer"                    │
  │ "Be more direct"     → codePreferences.tone = "direct"                    │
  └───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ RESULT                                                                    │
  │ ──────                                                                    │
  │                                                                           │
  │ Updates: { codePreferences: { preferredStacks: ["Bun"] } }               │
  │ Removals: ["codePreferences.preferredStacks.npm",                        │
  │            "codePreferences.preferredStacks.webpack"]                     │
  └───────────────────────────────────────────────────────────────────────────┘
```
