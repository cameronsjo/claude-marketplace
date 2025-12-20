---
name: session-continuity
description: Aggressive session accountability via Obsidian timeline. PROACTIVELY log decisions, commits, ideas, and blockers AS THEY HAPPEN - don't wait for session end. Triggers on any significant action, decision point, or insight.
---

# Session Continuity

Maintain context across Claude Code sessions and devices using aggressive, real-time logging to an Obsidian timeline.

## Core Principle: Log Early, Log Often

**Don't wait for session end.** Log as things happen:

- Made a decision? Log it immediately.
- Committed code? Log the commit.
- Hit a blocker? Log it before context is lost.
- Had an insight? Capture it now.
- Changed architecture? Document why.

**You are accountable for maintaining context.** The user may forget, the session may crash, context may compact. The timeline is the source of truth.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CLAUDE_TIMELINE_PATH` | Yes | Path to timeline file (e.g., `~/Documents/Obsidian/Vault/Claude Code Timeline.md`) |
| `CLAUDE_CONTEXT_DIR` | No | Additional context directory to read on start |
| `OBSIDIAN_VAULT` | No | Obsidian vault root (for MCP server) |

## When to Log (Triggers)

Log to the Work Log section **immediately** after:

| Trigger | Log Type | Example |
|---------|----------|---------|
| Decision made | `Decision` | "Using Redis over Memcached because..." |
| Git commit | `Commit` | "Added auth middleware (abc123)" |
| Blocker hit | `Blocker` | "OAuth redirect failing, need to debug" |
| Blocker resolved | `Resolved` | "OAuth was missing callback URL" |
| Insight/idea | `Idea` | "Could use webhooks instead of polling" |
| Architecture change | `Architecture` | "Moving to event-driven pattern" |
| Config change | `Config` | "Updated Traefik labels for new route" |
| State change | `State` | "Prometheus now running on :9090" |

**Be aggressive.** When in doubt, log it. A noisy log is better than a silent one.

## Work Log Format

Quick, timestamped micro-entries in the Work Log section:

```markdown
## Work Log

### 2025-12-19

- 23:15 **Decision**: Using Traefik over Nginx - better Docker integration, automatic HTTPS
- 23:30 **Commit**: Added prometheus config (`feat: add prometheus monitoring` abc123)
- 23:45 **Blocker**: Authelia OAuth not redirecting correctly
- 00:10 **Resolved**: OAuth needed explicit redirect_uri in config
- 00:15 **Idea**: Could add Loki for log aggregation next
- 00:30 **State**: Prometheus running on :9090, scraping Traefik metrics
```

Each entry is one line. Include the WHY for decisions. Include commit message and short SHA for commits.

## Session Start Protocol

When a session starts, you **MUST**:

1. Check if `CLAUDE_TIMELINE_PATH` is set
2. Read the timeline file using:
   - **MCP first**: `obsidian_read_note` if `obsidian-mcp-server` is available
   - **Fallback**: Native filesystem read
3. **CHECK THE INBOX FIRST** - this is how the user communicates async
4. Parse the timeline for:
   - Inbox items (address these!)
   - Recent work log entries
   - Current state section
   - Recent session summaries
5. Acknowledge context: "Timeline loaded. Inbox: [N items]. Last activity: [date] on [device]."

## Inbox Protocol

The Inbox is for async capture - the user can add items from any device (phone, tablet, Obsidian mobile).

```markdown
## Inbox

> Add ideas, tasks, or notes here from any device.
> Claude MUST review and address these at session start.

- [ ] Add Sonarr to Traefik routes
- [ ] Look into why n8n keeps disconnecting
- [ ] Can we add a health check dashboard?
```

**At session start, you MUST:**
1. Check the Inbox section for any items
2. Acknowledge what's in the inbox
3. Ask if the user wants to address inbox items now or continue with something else
4. When an inbox item is addressed:
   - Work on it
   - Log the work in Work Log
   - Remove from Inbox (or mark `[x]` if user prefers history)

**Don't ignore the Inbox.** It's how the user communicates between sessions.

## Session End Protocol

Before ending a session, you **MUST**:

1. Summarize what was done this session
2. Update the timeline with a new entry using the template
3. Note any state changes (new services, config changes, etc.)
4. Flag any blockers or TODOs for next session

## Timeline File Format

The timeline file (`Claude Code Timeline.md`) has two main sections:

### Current State Section

```markdown
## Current State

### Services
| Service | Port | Network | Status |
|---------|------|---------|--------|
| traefik | 80/443 | proxy | running |

### Repositories
| Repo | Purpose | Location |
|------|---------|----------|
| dotfiles | Infrastructure | ~/.dotfiles |

### Secrets
| Secret | Location | Fields |
|--------|----------|--------|
| traefik-creds | 1Password | username, password |
```

### Session Log Section

```markdown
## Session Log

### 2025-12-19 23:00 CST (Mac)

**Session:** Brief description of what was accomplished

**Changes:**
- Change 1 with details
- Change 2 with details

**Repos touched:**
- repo-name - what changed

**State after:** Key state changes

**Next steps:** TODOs or blockers for future sessions

---
```

## Reading Timeline

### Via MCP (preferred)

```
Use mcp__obsidian-mcp-server__obsidian_read_note with:
- filePath: path from CLAUDE_TIMELINE_PATH (vault-relative)
- format: "markdown"
```

### Via Filesystem (fallback)

```
Use Read tool with:
- file_path: full path from CLAUDE_TIMELINE_PATH
```

## Writing Timeline

### Via MCP (preferred)

```
Use mcp__obsidian-mcp-server__obsidian_update_note with:
- targetType: "filePath"
- targetIdentifier: path from CLAUDE_TIMELINE_PATH
- modificationType: "wholeFile"
- wholeFileMode: "prepend" (for new entries at top of Session Log)
```

### Via Filesystem (fallback)

```
Use Edit tool to insert new entry after "## Session Log" heading
```

## Injecting Obsidian TODOs

If the timeline contains a `## TODOs` section or links to TODO notes:

1. Parse any `- [ ]` checkboxes
2. Surface incomplete TODOs at session start
3. Offer to mark TODOs complete when addressed

## Cross-Device Context

Each session entry includes the device identifier:

- `(Mac)` - macOS session
- `(Windows)` - Windows/WSL session
- `(Web)` - Claude Code on web
- `(Linux)` - Linux session

This helps debug device-specific issues and track where work was done.

## Boundaries and Scoping

This skill is **per-project**. Each project can have its own timeline, or share a central one.

For per-project timelines, set `CLAUDE_TIMELINE_PATH` in:
- `.claude/settings.local.json` (gitignored, per-machine)
- Or use project-specific environment variables

## Example Session Start

```
Session started. Reading timeline from ~/Documents/Obsidian/Vault/Claude Code Timeline.md

Timeline loaded:
- Last session: 2025-12-19 22:00 CST on Mac
- Current state: Traefik running on ports 80/443, Authelia configured
- Pending TODOs:
  - [ ] Set up Prometheus monitoring
  - [ ] Configure backup automation

Ready to continue. What would you like to work on?
```

## Example Session End

```
Before we end, let me update the timeline:

### 2025-12-19 23:30 CST (Mac)

**Session:** Added Prometheus monitoring to homelab

**Changes:**
- Created prometheus.yml config
- Added Prometheus container to docker-compose
- Configured Traefik metrics endpoint

**Repos touched:**
- dotfiles/infrastructure - added prometheus config

**State after:** Prometheus running on :9090, scraping Traefik metrics

**Next steps:**
- [ ] Add Grafana dashboards
- [ ] Configure alerting rules

Timeline updated. Session complete.
```
