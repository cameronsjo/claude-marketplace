/**
 * Session Continuity System
 *
 * Tracks task progress across sessions using a simple progress.json file.
 * Inspired by the progress.md pattern for maintaining context between sessions.
 */

import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { homedir } from "node:os";

const STORAGE_DIR = process.env.USER_MEMORY_DIR ?? join(homedir(), ".claude", "user-memory");
const SESSIONS_DIR = join(STORAGE_DIR, "sessions");

export interface TaskState {
  id: string;
  title: string;
  status: "pending" | "in_progress" | "blocked" | "completed";
  createdAt: string;
  updatedAt: string;
  notes?: string;
  blockedBy?: string;
  children?: string[]; // IDs of subtasks
}

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

export interface DecisionEntry {
  timestamp: string;
  decision: string;
  rationale?: string;
  alternatives?: string[];
}

export interface ResumeContext {
  lastSession?: SessionProgress;
  pendingTasks: TaskState[];
  recentDecisions: DecisionEntry[];
  projectContext?: string;
}

/**
 * Load session progress for a specific session
 */
export async function loadSession(sessionId: string): Promise<SessionProgress | null> {
  const path = getSessionPath(sessionId);

  if (!existsSync(path)) {
    return null;
  }

  const content = await readFile(path, "utf-8");
  return JSON.parse(content) as SessionProgress;
}

/**
 * Save session progress
 */
export async function saveSession(session: SessionProgress): Promise<void> {
  const path = getSessionPath(session.sessionId);
  const dir = dirname(path);

  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }

  session.lastActiveAt = new Date().toISOString();
  await writeFile(path, JSON.stringify(session, null, 2), "utf-8");
}

/**
 * Create a new session
 */
export function createSession(sessionId: string, projectPath?: string): SessionProgress {
  return {
    sessionId,
    projectPath,
    startedAt: new Date().toISOString(),
    lastActiveAt: new Date().toISOString(),
    tasks: [],
    decisions: [],
    context: [],
  };
}

/**
 * Add or update a task in the session
 */
export async function updateTask(
  sessionId: string,
  task: Partial<TaskState> & { id: string }
): Promise<SessionProgress> {
  let session = await loadSession(sessionId);

  if (!session) {
    session = createSession(sessionId);
  }

  const existingIdx = session.tasks.findIndex((t) => t.id === task.id);
  const now = new Date().toISOString();

  if (existingIdx >= 0) {
    // Update existing task
    session.tasks[existingIdx] = {
      ...session.tasks[existingIdx],
      ...task,
      updatedAt: now,
    };
  } else {
    // Add new task
    session.tasks.push({
      id: task.id,
      title: task.title ?? "Untitled task",
      status: task.status ?? "pending",
      createdAt: now,
      updatedAt: now,
      notes: task.notes,
      blockedBy: task.blockedBy,
      children: task.children,
    });
  }

  await saveSession(session);
  return session;
}

/**
 * Log a decision
 */
export async function logDecision(
  sessionId: string,
  decision: string,
  rationale?: string,
  alternatives?: string[]
): Promise<SessionProgress> {
  let session = await loadSession(sessionId);

  if (!session) {
    session = createSession(sessionId);
  }

  session.decisions.push({
    timestamp: new Date().toISOString(),
    decision,
    rationale,
    alternatives,
  });

  // Keep only last 50 decisions per session
  if (session.decisions.length > 50) {
    session.decisions = session.decisions.slice(-50);
  }

  await saveSession(session);
  return session;
}

/**
 * Add context note
 */
export async function addContext(
  sessionId: string,
  context: string
): Promise<SessionProgress> {
  let session = await loadSession(sessionId);

  if (!session) {
    session = createSession(sessionId);
  }

  session.context.push(context);

  // Keep only last 20 context notes
  if (session.context.length > 20) {
    session.context = session.context.slice(-20);
  }

  await saveSession(session);
  return session;
}

/**
 * Get resume context by finding the most recent session for a project
 */
export async function getResumeContext(projectPath?: string): Promise<ResumeContext> {
  const sessions = await listRecentSessions(5);

  // Find most relevant session
  let lastSession: SessionProgress | undefined;

  if (projectPath) {
    // Prefer session from same project
    lastSession = sessions.find((s) => s.projectPath === projectPath);
  }

  if (!lastSession && sessions.length > 0) {
    lastSession = sessions[0];
  }

  // Collect pending tasks from all recent sessions
  const pendingTasks: TaskState[] = [];
  const seenTaskIds = new Set<string>();

  for (const session of sessions) {
    for (const task of session.tasks) {
      if (
        (task.status === "pending" || task.status === "in_progress" || task.status === "blocked") &&
        !seenTaskIds.has(task.id)
      ) {
        pendingTasks.push(task);
        seenTaskIds.add(task.id);
      }
    }
  }

  // Collect recent decisions
  const recentDecisions: DecisionEntry[] = [];
  for (const session of sessions.slice(0, 3)) {
    recentDecisions.push(...session.decisions.slice(-5));
  }

  return {
    lastSession,
    pendingTasks: pendingTasks.slice(0, 10),
    recentDecisions: recentDecisions.slice(0, 10),
    projectContext: lastSession?.context.join("\n"),
  };
}

/**
 * List recent sessions sorted by last activity
 */
async function listRecentSessions(limit = 10): Promise<SessionProgress[]> {
  if (!existsSync(SESSIONS_DIR)) {
    return [];
  }

  const { readdir } = await import("node:fs/promises");
  const files = await readdir(SESSIONS_DIR);

  const sessions: SessionProgress[] = [];

  for (const file of files) {
    if (!file.endsWith(".json")) continue;

    try {
      const content = await readFile(join(SESSIONS_DIR, file), "utf-8");
      sessions.push(JSON.parse(content) as SessionProgress);
    } catch {
      // Skip malformed files
    }
  }

  // Sort by last activity, most recent first
  sessions.sort((a, b) =>
    new Date(b.lastActiveAt).getTime() - new Date(a.lastActiveAt).getTime()
  );

  return sessions.slice(0, limit);
}

/**
 * Clean up old sessions (keep last N days)
 */
export async function pruneOldSessions(maxAgeDays = 30): Promise<number> {
  if (!existsSync(SESSIONS_DIR)) {
    return 0;
  }

  const { readdir, unlink } = await import("node:fs/promises");
  const files = await readdir(SESSIONS_DIR);

  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - maxAgeDays);

  let removed = 0;

  for (const file of files) {
    if (!file.endsWith(".json")) continue;

    const filePath = join(SESSIONS_DIR, file);

    try {
      const content = await readFile(filePath, "utf-8");
      const session = JSON.parse(content) as SessionProgress;

      if (new Date(session.lastActiveAt) < cutoff) {
        await unlink(filePath);
        removed++;
      }
    } catch {
      // Skip malformed files
    }
  }

  return removed;
}

/**
 * Build resume prompt from context
 */
export function buildResumePrompt(ctx: ResumeContext): string {
  const sections: string[] = [];

  if (ctx.lastSession?.summary) {
    sections.push("## Previous Session Summary");
    sections.push(ctx.lastSession.summary);
    sections.push("");
  }

  if (ctx.pendingTasks.length > 0) {
    sections.push("## Pending Tasks");
    for (const task of ctx.pendingTasks) {
      const status = task.status === "blocked" ? `🔴 Blocked: ${task.blockedBy}` :
                     task.status === "in_progress" ? "🟡 In progress" : "⚪ Pending";
      sections.push(`- **${task.title}** (${status})`);
      if (task.notes) {
        sections.push(`  - ${task.notes}`);
      }
    }
    sections.push("");
  }

  if (ctx.recentDecisions.length > 0) {
    sections.push("## Recent Decisions");
    for (const decision of ctx.recentDecisions.slice(0, 5)) {
      sections.push(`- ${decision.decision}`);
      if (decision.rationale) {
        sections.push(`  - _Rationale:_ ${decision.rationale}`);
      }
    }
    sections.push("");
  }

  if (ctx.projectContext) {
    sections.push("## Context Notes");
    sections.push(ctx.projectContext);
    sections.push("");
  }

  return sections.join("\n");
}

function getSessionPath(sessionId: string): string {
  const safeId = sessionId.replace(/[^a-zA-Z0-9_-]/g, "_");
  return join(SESSIONS_DIR, `${safeId}.json`);
}
