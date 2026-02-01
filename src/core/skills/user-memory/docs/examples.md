# Examples

Real-world examples of user-memory in action.

## Example Profiles

### Backend Engineer Profile

```json
{
  "userId": "cameron",
  "schemaVersion": 1,
  "lastUpdated": "2025-01-15T10:30:00.000Z",
  "work": {
    "role": "senior backend engineer",
    "languages": ["TypeScript", "Python", "Go"],
    "focusAreas": ["APIs", "distributed systems", "performance"]
  },
  "codePreferences": {
    "tone": "direct",
    "detailLevel": "medium",
    "preferredStacks": ["Bun", "FastAPI", "PostgreSQL"],
    "avoidExamples": ["sports metaphors"]
  },
  "tools": {
    "editor": "neovim",
    "infra": ["Docker", "Kubernetes", "Terraform"]
  },
  "interests": ["type safety", "observability"]
}
```

### Frontend Developer Profile

```json
{
  "userId": "alex",
  "schemaVersion": 1,
  "lastUpdated": "2025-01-14T15:00:00.000Z",
  "work": {
    "role": "frontend developer",
    "languages": ["TypeScript", "JavaScript"],
    "focusAreas": ["UI/UX", "accessibility", "performance"]
  },
  "codePreferences": {
    "tone": "friendly",
    "detailLevel": "high",
    "preferredStacks": ["Next.js", "Tailwind", "Prisma"]
  },
  "tools": {
    "editor": "vscode"
  }
}
```

### ML Researcher Profile

```json
{
  "userId": "jordan",
  "schemaVersion": 1,
  "lastUpdated": "2025-01-13T09:00:00.000Z",
  "work": {
    "role": "ML researcher",
    "languages": ["Python", "Julia"],
    "focusAreas": ["NLP", "transformers", "efficiency"]
  },
  "codePreferences": {
    "tone": "neutral",
    "detailLevel": "high",
    "preferredStacks": ["PyTorch", "Hugging Face", "Weights & Biases"]
  },
  "tools": {
    "editor": "cursor",
    "infra": ["Modal", "Lambda Labs"]
  },
  "interests": ["quantization", "distillation"]
}
```

---

## Conversation Examples

### Building Up a Profile

**Session 1:**
```
User: I'm a backend engineer working mostly in TypeScript and Python.
      I use neovim and prefer direct responses.

→ Extracted:
  work.role: "backend engineer"
  work.languages: ["TypeScript", "Python"]
  tools.editor: "neovim"
  codePreferences.tone: "direct"
```

**Session 2:**
```
User: I'm switching to Bun for my TypeScript projects.
      My focus is on APIs and distributed systems.

→ Extracted:
  codePreferences.preferredStacks: ["Bun"]
  work.focusAreas: ["APIs", "distributed systems"]
```

**Session 3:**
```
User: Don't use sports metaphors in examples.
      I prefer FastAPI over Flask for Python.

→ Extracted:
  codePreferences.avoidExamples: ["sports metaphors"]
  codePreferences.preferredStacks: ["FastAPI"]  // Added
  → Removed: codePreferences.preferredStacks.flask
```

### Negation Examples

**Removing a preference:**
```
User: I stopped using Webpack, switched to Vite.

→ Result:
  Updates: { codePreferences: { preferredStacks: ["Vite"] } }
  Removals: ["codePreferences.preferredStacks.webpack"]
```

**Explicit forget:**
```
User: Forget that I prefer tabs over spaces.

→ Result:
  Updates: {}
  Removals: ["codePreferences.preferredStacks.tabs"]
```

**Preference replacement:**
```
User: I prefer Bun over npm for package management.

→ Result:
  Updates: { codePreferences: { preferredStacks: ["Bun"] } }
  Removals: ["codePreferences.preferredStacks.npm"]
```

---

## Session Continuity Examples

### Multi-Session Feature Development

**Session 1 - Start feature:**
```
Claude calls: update_task({
  sessionId: "sess-001",
  id: "auth-feature",
  title: "Implement JWT authentication",
  status: "in_progress"
})

Claude calls: log_decision({
  sessionId: "sess-001",
  decision: "Use RS256 for JWT signing",
  rationale: "Better security than HS256 for multi-service architecture",
  alternatives: ["HS256", "ES256"]
})

Claude calls: set_session_summary({
  sessionId: "sess-001",
  summary: "Started JWT auth, decided on RS256. Need to implement refresh tokens next."
})
```

**Session 2 - Resume and continue:**
```
Claude calls: get_session_context({ projectPath: "/home/user/my-api" })

→ Returns:
  ## Previous Session Summary
  Started JWT auth, decided on RS256. Need to implement refresh tokens next.

  ## Pending Tasks
  - **Implement JWT authentication** (🟡 In progress)

  ## Recent Decisions
  - Use RS256 for JWT signing
    - _Rationale:_ Better security than HS256 for multi-service architecture

Claude calls: update_task({
  sessionId: "sess-002",
  id: "auth-feature",
  status: "completed"
})

Claude calls: update_task({
  sessionId: "sess-002",
  id: "refresh-tokens",
  title: "Implement refresh token rotation",
  status: "in_progress"
})
```

**Session 3 - Hit a blocker:**
```
Claude calls: update_task({
  sessionId: "sess-003",
  id: "refresh-tokens",
  status: "blocked",
  blockedBy: "Need Redis for token storage, waiting on DevOps"
})

Claude calls: add_session_context({
  sessionId: "sess-003",
  context: "Redis cluster will be available next week per DevOps"
})
```

---

## MCP Tool Examples

### Profile Management

**Get profile at session start:**
```typescript
// Claude calls get_user_profile()
{
  "userId": "cameron",
  "work": { "role": "backend engineer" },
  "codePreferences": { "tone": "direct", "preferredStacks": ["Bun"] },
  "tools": { "editor": "neovim" }
}
```

**Update after user reveals preference:**
```typescript
// User: "I'm using PostgreSQL for this project"
// Claude calls update_user_profile({ tools: { infra: ["PostgreSQL"] } })
{
  "message": "Profile updated",
  "updates": ["tools"],
  "trackedPaths": ["tools.infra"]
}
```

**Check decay status:**
```typescript
// Claude calls get_preference_metadata()
{
  "lastDecay": "2025-01-15T08:00:00.000Z",
  "preferences": [
    {
      "path": "codePreferences.preferredStacks",
      "confidence": 0.85,
      "lastSeen": "2025-01-14T15:30:00.000Z",
      "seenCount": 5,
      "daysUntilDecay": 45
    },
    {
      "path": "tools.editor",
      "confidence": 0.32,
      "lastSeen": "2025-01-02T09:00:00.000Z",
      "seenCount": 1,
      "daysUntilDecay": 12  // ⚠️ Low - needs reinforcement
    }
  ]
}
```

### Changelog Queries

**View recent changes:**
```typescript
// Claude calls get_changelog({ limit: 5 })
{
  "count": 5,
  "entries": [
    {
      "timestamp": "2025-01-15T10:30:00Z",
      "action": "extract",
      "source": "mcp/hook",
      "changes": { "codePreferences": { "preferredStacks": ["Bun"] } }
    },
    {
      "timestamp": "2025-01-15T08:00:00Z",
      "action": "decay",
      "source": "system",
      "removed": ["work.focusAreas"]
    },
    // ...
  ]
}
```

---

## Workflow Examples

### New User Onboarding

```
Session 1: User starts fresh

Claude: "I notice you don't have any saved preferences yet.
        As we work together, I'll remember things like your
        preferred tech stack, editor, and communication style."

User: "Great! I'm a full-stack developer, I use VS Code,
      and I prefer TypeScript with Next.js."

→ Profile created with initial preferences

Session 2: Preferences applied

Claude internally loads profile, sees:
- role: full-stack developer
- editor: vscode
- preferredStacks: ["TypeScript", "Next.js"]

Claude adapts responses to use TypeScript examples,
Next.js patterns, and VS Code-specific tips.
```

### Preference Evolution

```
Month 1: User says "I use npm for package management"
         → preferredStacks: ["npm"]
         → confidence: 1.0

Month 2: No mention of npm
         → confidence: 0.5 (decayed)

Month 3: User says "I'm switching to pnpm"
         → preferredStacks: ["pnpm"]
         → npm removed automatically
         → confidence for pnpm: 1.0

Month 4: User mentions "Using pnpm workspaces"
         → confidence reinforced to 1.0
         → seenCount: 2
```

### Team Context Switching

```
Project A (React frontend):
  User: "For this project I'm using React with Vite"
  → Extracted: preferredStacks includes React, Vite

Project B (Python backend):
  User: "This is a FastAPI project"
  → Extracted: preferredStacks includes FastAPI

Result: Profile accumulates both contexts
  preferredStacks: ["React", "Vite", "FastAPI"]

Claude uses context from current directory + profile
to determine which stack is relevant.
```
