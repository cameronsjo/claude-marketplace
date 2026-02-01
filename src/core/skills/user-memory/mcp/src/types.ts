/**
 * User Profile Memory Types
 *
 * Schema for long-term user memory that persists across sessions.
 * Used to adapt assistant behavior based on preferences, tech stack, etc.
 */

export interface UserProfile {
  userId: string;
  schemaVersion: 1;
  lastUpdated: string; // ISO 8601

  bio?: string;

  work?: {
    role?: string;
    focusAreas?: string[];
    languages?: string[];
  };

  codePreferences?: {
    tone?: "direct" | "neutral" | "friendly";
    detailLevel?: "high" | "medium" | "low";
    avoidExamples?: string[]; // e.g., ["sports metaphors"]
    preferredStacks?: string[]; // e.g., ["FastAPI", "Bun"]
  };

  tools?: {
    editor?: string;
    infra?: string[];
  };

  interests?: string[];

  // Free-form bucket for extensibility
  custom?: Record<string, unknown>;
}

/**
 * Memory update payload from model response
 */
export interface MemoryUpdate {
  should_write: boolean;
  updates: Partial<UserProfile>;
}

/**
 * Structured model output with dual-output pattern
 */
export interface ModelOutput {
  reply: string;
  memory: MemoryUpdate;
}

/**
 * Hook context passed through lifecycle
 */
export interface ClaudeCodeContext {
  userId: string;
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
  meta: Record<string, unknown>;
}

/**
 * Hook interface for memory system integration
 */
export interface ClaudeCodeHooks {
  onSessionStart(ctx: ClaudeCodeContext): Promise<void>;
  beforeModelCall(ctx: ClaudeCodeContext): Promise<void>;
  afterModelCall(ctx: ClaudeCodeContext, rawModelOutput: string): Promise<void>;
}

/**
 * Changelog entry for audit trail
 */
export interface ChangelogEntry {
  timestamp: string;
  session_id?: string;
  action: "extract" | "update" | "clear" | "remove" | "decay";
  source: "mcp/hook" | "mcp/tool" | "minimal/hook" | "system";
  changes: Partial<UserProfile>;
  removed?: string[]; // Paths that were removed
}

/**
 * Metadata for preference tracking (confidence/decay)
 */
export interface PreferenceMeta {
  path: string; // e.g., "codePreferences.preferredStacks"
  firstSeen: string; // ISO 8601
  lastSeen: string; // ISO 8601
  confidence: number; // 0.0 - 1.0
  seenCount: number; // Times reinforced
}

/**
 * Profile metadata store (separate from profile for backwards compat)
 */
export interface ProfileMetadata {
  userId: string;
  schemaVersion: 1;
  lastDecay: string; // Last time decay was run
  preferences: PreferenceMeta[];
}

/**
 * Update payload with optional removal
 */
export interface ProfileUpdate extends Partial<UserProfile> {
  $unset?: string[]; // Paths to remove, e.g., ["codePreferences.tone", "tools.editor"]
}

/**
 * Changelog config
 */
export interface ChangelogConfig {
  maxEntries: number; // Default 1000
  maxAgeDays: number; // Default 90
}

/**
 * Decay config
 */
export interface DecayConfig {
  halfLifeDays: number; // Confidence halves every N days (default 30)
  minConfidence: number; // Remove below this threshold (default 0.1)
  reinforceBoost: number; // Confidence boost when seen again (default 0.3)
}

/**
 * Session task state
 */
export interface TaskState {
  id: string;
  title: string;
  status: "pending" | "in_progress" | "blocked" | "completed";
  createdAt: string;
  updatedAt: string;
  notes?: string;
  blockedBy?: string;
  children?: string[];
}

/**
 * Session progress tracking
 */
export interface SessionProgress {
  sessionId: string;
  projectPath?: string;
  startedAt: string;
  lastActiveAt: string;
  summary?: string;
  tasks: TaskState[];
  decisions: DecisionEntry[];
  context: string[];
}

/**
 * Decision log entry
 */
export interface DecisionEntry {
  timestamp: string;
  decision: string;
  rationale?: string;
  alternatives?: string[];
}

/**
 * Resume context for session continuity
 */
export interface ResumeContext {
  lastSession?: SessionProgress;
  pendingTasks: TaskState[];
  recentDecisions: DecisionEntry[];
  projectContext?: string;
}
