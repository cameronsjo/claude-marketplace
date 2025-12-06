# Data Schemas Reference

## profile.json

The main user profile storage.

```typescript
interface UserProfile {
  userId: string;           // e.g., "cameron" (from $USER)
  schemaVersion: 1;         // Always 1 for now
  lastUpdated: string;      // ISO 8601 timestamp

  bio?: string;             // Free-form bio

  work?: {
    role?: string;          // "backend engineer", "ML researcher"
    focusAreas?: string[];  // ["APIs", "distributed systems"]
    languages?: string[];   // ["TypeScript", "Python", "Rust"]
  };

  codePreferences?: {
    tone?: "direct" | "neutral" | "friendly";
    detailLevel?: "high" | "medium" | "low";
    avoidExamples?: string[];    // ["sports metaphors"]
    preferredStacks?: string[];  // ["Bun", "FastAPI", "Postgres"]
  };

  tools?: {
    editor?: string;        // "neovim", "vscode", "cursor"
    infra?: string[];       // ["Docker", "Kubernetes", "Terraform"]
  };

  interests?: string[];     // ["performance", "type safety"]

  custom?: Record<string, unknown>;  // Extensibility bucket
}
```

### Example

```json
{
  "userId": "cameron",
  "schemaVersion": 1,
  "lastUpdated": "2025-01-15T10:30:00.000Z",
  "work": {
    "role": "backend engineer",
    "languages": ["TypeScript", "Python"],
    "focusAreas": ["APIs", "infrastructure"]
  },
  "codePreferences": {
    "tone": "direct",
    "preferredStacks": ["Bun", "FastAPI"]
  },
  "tools": {
    "editor": "neovim"
  }
}
```

---

## profile-meta.json

Metadata for confidence tracking and decay.

```typescript
interface ProfileMetadata {
  userId: string;
  schemaVersion: 1;
  lastDecay: string;              // ISO 8601 - when decay was last run
  preferences: PreferenceMeta[];  // Tracked preferences
}

interface PreferenceMeta {
  path: string;       // Dot-notation path, e.g., "codePreferences.tone"
  firstSeen: string;  // When preference was first recorded
  lastSeen: string;   // When preference was last reinforced
  confidence: number; // 0.0 to 1.0
  seenCount: number;  // Number of times reinforced
}
```

### Example

```json
{
  "userId": "cameron",
  "schemaVersion": 1,
  "lastDecay": "2025-01-15T08:00:00.000Z",
  "preferences": [
    {
      "path": "codePreferences.preferredStacks",
      "firstSeen": "2025-01-01T10:00:00.000Z",
      "lastSeen": "2025-01-14T15:30:00.000Z",
      "confidence": 0.85,
      "seenCount": 5
    },
    {
      "path": "tools.editor",
      "firstSeen": "2025-01-02T09:00:00.000Z",
      "lastSeen": "2025-01-02T09:00:00.000Z",
      "confidence": 0.45,
      "seenCount": 1
    }
  ]
}
```

---

## changelog.jsonl

Append-only audit trail (JSONL format - one JSON object per line).

```typescript
interface ChangelogEntry {
  timestamp: string;     // ISO 8601
  session_id?: string;   // Session that triggered the change (hooks only)
  action: "extract" | "update" | "clear" | "remove" | "decay";
  source: "minimal/hook" | "mcp/hook" | "mcp/tool" | "system";
  changes: Partial<UserProfile>;  // What was added/modified
  removed?: string[];    // Paths that were removed (for remove/decay)
}
```

### Example

```jsonl
{"timestamp":"2025-01-15T10:30:00Z","session_id":"abc123","action":"extract","source":"mcp/hook","changes":{"codePreferences":{"preferredStacks":["Bun"]}}}
{"timestamp":"2025-01-15T11:00:00Z","action":"update","source":"mcp/tool","changes":{"tools":{"editor":"neovim"}}}
{"timestamp":"2025-01-16T08:00:00Z","action":"decay","source":"system","changes":{},"removed":["codePreferences.tone"]}
{"timestamp":"2025-01-16T09:00:00Z","action":"remove","source":"mcp/tool","changes":{},"removed":["tools.infra"]}
```

---

## sessions/session-{id}.json

Session continuity tracking.

```typescript
interface SessionProgress {
  sessionId: string;
  projectPath?: string;       // Working directory
  startedAt: string;          // ISO 8601
  lastActiveAt: string;       // ISO 8601
  summary?: string;           // Shown at next session start
  tasks: TaskState[];
  decisions: DecisionEntry[];
  context: string[];          // Free-form context notes
}

interface TaskState {
  id: string;                 // Unique identifier
  title: string;
  status: "pending" | "in_progress" | "blocked" | "completed";
  createdAt: string;          // ISO 8601
  updatedAt: string;          // ISO 8601
  notes?: string;
  blockedBy?: string;         // What's blocking (if status=blocked)
  children?: string[];        // IDs of subtasks
}

interface DecisionEntry {
  timestamp: string;          // ISO 8601
  decision: string;
  rationale?: string;
  alternatives?: string[];
}
```

### Example

```json
{
  "sessionId": "abc123",
  "projectPath": "/home/user/my-project",
  "startedAt": "2025-01-15T10:00:00.000Z",
  "lastActiveAt": "2025-01-15T12:30:00.000Z",
  "summary": "Implemented user auth, blocked on database migration",
  "tasks": [
    {
      "id": "auth-1",
      "title": "Implement user authentication",
      "status": "completed",
      "createdAt": "2025-01-15T10:00:00.000Z",
      "updatedAt": "2025-01-15T11:30:00.000Z"
    },
    {
      "id": "db-migration",
      "title": "Add users table migration",
      "status": "blocked",
      "createdAt": "2025-01-15T11:30:00.000Z",
      "updatedAt": "2025-01-15T12:00:00.000Z",
      "blockedBy": "Need DBA approval for schema change"
    }
  ],
  "decisions": [
    {
      "timestamp": "2025-01-15T10:30:00.000Z",
      "decision": "Use JWT for auth tokens",
      "rationale": "Stateless, works well with our API gateway",
      "alternatives": ["Session cookies", "OAuth only"]
    }
  ],
  "context": [
    "User prefers bcrypt over argon2 for password hashing",
    "Project uses PostgreSQL 15"
  ]
}
```

---

## .processed_turns

Deduplication tracker for Stop hook (simple text format).

```
session_id:line_count
```

### Example

```
abc123:45
def456:128
ghi789:23
```

Each line tracks how many transcript lines have been processed for a session, preventing re-extraction of already-processed messages.

---

## Decay Configuration

Internal constants (not stored, hardcoded):

```typescript
interface DecayConfig {
  halfLifeDays: 30;       // Confidence halves every 30 days
  minConfidence: 0.1;     // Remove when below 10%
  reinforceBoost: 0.3;    // Add 30% when preference mentioned again
}

interface ChangelogConfig {
  maxEntries: 1000;       // Keep last 1000 entries
  maxAgeDays: 90;         // Remove entries older than 90 days
}

interface SessionConfig {
  maxAgeDays: 30;         // Prune sessions older than 30 days
  maxDecisions: 50;       // Keep last 50 decisions per session
  maxContextNotes: 20;    // Keep last 20 context notes per session
}
```
