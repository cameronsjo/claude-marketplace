# Changelog

All notable changes to the User Memory skill.

## [4.0.0] - 2025-01-27

### Added

- **Session Continuity System** - Track tasks, decisions, and context across sessions
  - `get_session_context` - Resume from previous sessions
  - `update_task` - Track task progress (pending/in_progress/blocked/completed)
  - `log_decision` - Record decisions with rationale and alternatives
  - `add_session_context` - Store context notes
  - `set_session_summary` - Set summary shown at next session start
  - `get_full_context` - Combined profile + session context prompt

- **Context Injection at SessionStart** - Auto-inject profile summary into session
  - Builds natural language context from profile
  - Writes to `CLAUDE_ENV_FILE` for session access
  - Includes decay warnings for preferences needing reinforcement

- **Auto-decay on SessionStart** - Scheduled decay without manual intervention
  - Runs if 24+ hours since last decay
  - Zero latency impact (async execution)
  - Auto-prunes old changelog entries

- **Negation Handling** - Understands removal phrases
  - "I no longer use X", "I stopped using X"
  - "Forget that I prefer X", "Remove my preference for X"
  - Priority-based conflict resolution (negations override additions)

- **Documentation** - Comprehensive docs with ASCII diagrams
  - `docs/architecture.md` - System flowcharts
  - `docs/data-schemas.md` - Full type definitions
  - `docs/quick-reference.md` - Cheatsheet

### Changed

- Bumped to 13 MCP tools total (7 profile + 6 session)
- Pattern extraction now returns both updates and removals
- Stop hook logs to changelog with session_id

## [3.0.0] - 2025-01-26

### Added

- **Decay & Confidence System** - Preferences decay over time if not reinforced
  - Exponential decay: `confidence × 0.5^(days/30)`
  - Auto-remove when confidence < 0.1
  - Reinforcement boost (+0.3) when preference mentioned again
  - `get_preference_metadata` - View confidence scores
  - `run_decay` - Manual decay trigger
  - `remove_preference` - Explicit removal by path

- **Changelog Audit Trail** - Append-only log of all changes
  - `changelog.jsonl` - JSONL format for easy parsing
  - `get_changelog` - Query recent changes
  - Auto-pruning: 1000 entries max, 90 days retention

- **Swizzle Architecture** - Dual implementation modes
  - `minimal/` - Shell-only, jq dependency
  - `mcp/` - Full TypeScript with MCP SDK
  - Both share same `profile.json` format

### Changed

- Reorganized directory structure for swizzle support
- Added `profile-meta.json` for decay tracking

## [2.0.0] - 2025-01-25

### Added

- **MCP Server** - Real-time profile access via MCP tools
  - `get_user_profile` - Read current profile
  - `update_user_profile` - Merge updates
  - `clear_user_profile` - Reset with confirmation

- **Stop Hook Extraction** - Reliable preference capture
  - Runs after every Claude response
  - Deduplication via `.processed_turns` tracker
  - Works on Ctrl+C, terminal close, crashes

### Changed

- Switched from SessionEnd to Stop hook for reliability
- Added MCP SDK dependency

## [1.0.0] - 2025-01-24

### Added

- Initial implementation with SessionStart hook
- Basic profile schema (work, codePreferences, tools)
- Heuristic pattern matching for preference extraction
- File-based storage in `~/.claude/user-memory/`

---

## Version History Summary

| Version | Focus |
|---------|-------|
| 4.0.0 | Session continuity, context injection, negation handling |
| 3.0.0 | Decay system, changelog, swizzle architecture |
| 2.0.0 | MCP server, Stop hook reliability |
| 1.0.0 | Initial release, basic extraction |
