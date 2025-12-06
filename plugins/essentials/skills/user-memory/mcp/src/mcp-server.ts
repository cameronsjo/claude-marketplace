#!/usr/bin/env node
/**
 * User Memory MCP Server
 *
 * Exposes user profile memory via MCP tools:
 * - get_user_profile: Read current profile
 * - update_user_profile: Merge updates into profile
 * - clear_user_profile: Reset profile (with confirmation)
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import {
  loadUserProfile,
  saveUserProfile,
  mergeProfile,
  deleteUserProfile,
  logChange,
  readChangelog,
  trackPreference,
  removePreferences,
  runDecayCycle,
  loadMetadata,
} from "./store.js";
import {
  loadSession,
  saveSession,
  createSession,
  updateTask,
  logDecision,
  addContext,
  getResumeContext,
  buildResumePrompt,
  pruneOldSessions,
} from "./session.js";
import { buildContext } from "./context.js";
import type { UserProfile, TaskState } from "./types.js";

const USER_ID = process.env.USER ?? "default";

// ============================================================================
// Input Validation Helpers
// ============================================================================

/**
 * Validate that a value is a string
 */
function validateString(value: unknown, field: string): string {
  if (typeof value !== "string") {
    throw new Error(`${field} must be a string`);
  }
  return value;
}

/**
 * Validate that a value is a boolean
 */
function validateBoolean(value: unknown, field: string): boolean {
  if (typeof value !== "boolean") {
    throw new Error(`${field} must be a boolean`);
  }
  return value;
}

/**
 * Validate that a value is a number
 */
function validateNumber(value: unknown, field: string): number {
  if (typeof value !== "number" || isNaN(value)) {
    throw new Error(`${field} must be a number`);
  }
  return value;
}

/**
 * Validate that a value is an array of strings
 */
function validateStringArray(value: unknown, field: string): string[] {
  if (!Array.isArray(value)) {
    throw new Error(`${field} must be an array`);
  }
  for (let i = 0; i < value.length; i++) {
    if (typeof value[i] !== "string") {
      throw new Error(`${field}[${i}] must be a string`);
    }
  }
  return value as string[];
}

/**
 * Safely extract and validate optional string
 */
function optionalString(args: Record<string, unknown>, field: string): string | undefined {
  const value = args[field];
  if (value === undefined || value === null) return undefined;
  return validateString(value, field);
}

/**
 * Safely extract and validate optional number
 */
function optionalNumber(args: Record<string, unknown>, field: string): number | undefined {
  const value = args[field];
  if (value === undefined || value === null) return undefined;
  return validateNumber(value, field);
}

/**
 * Safely extract and validate optional boolean
 */
function optionalBoolean(args: Record<string, unknown>, field: string): boolean | undefined {
  const value = args[field];
  if (value === undefined || value === null) return undefined;
  return validateBoolean(value, field);
}

/**
 * Validate profile update structure
 */
function validateProfileUpdates(args: unknown): Partial<UserProfile> {
  if (!args || typeof args !== "object") {
    return {};
  }

  const input = args as Record<string, unknown>;
  const updates: Partial<UserProfile> = {};

  if (input.bio !== undefined) {
    updates.bio = validateString(input.bio, "bio");
  }

  if (input.work !== undefined) {
    if (typeof input.work !== "object" || input.work === null) {
      throw new Error("work must be an object");
    }
    const work = input.work as Record<string, unknown>;
    updates.work = {};
    if (work.role !== undefined) updates.work.role = validateString(work.role, "work.role");
    if (work.focusAreas !== undefined) updates.work.focusAreas = validateStringArray(work.focusAreas, "work.focusAreas");
    if (work.languages !== undefined) updates.work.languages = validateStringArray(work.languages, "work.languages");
  }

  if (input.codePreferences !== undefined) {
    if (typeof input.codePreferences !== "object" || input.codePreferences === null) {
      throw new Error("codePreferences must be an object");
    }
    const prefs = input.codePreferences as Record<string, unknown>;
    updates.codePreferences = {};
    if (prefs.tone !== undefined) {
      const tone = validateString(prefs.tone, "codePreferences.tone");
      if (!["direct", "neutral", "friendly"].includes(tone)) {
        throw new Error("codePreferences.tone must be 'direct', 'neutral', or 'friendly'");
      }
      updates.codePreferences.tone = tone as "direct" | "neutral" | "friendly";
    }
    if (prefs.detailLevel !== undefined) {
      const level = validateString(prefs.detailLevel, "codePreferences.detailLevel");
      if (!["high", "medium", "low"].includes(level)) {
        throw new Error("codePreferences.detailLevel must be 'high', 'medium', or 'low'");
      }
      updates.codePreferences.detailLevel = level as "high" | "medium" | "low";
    }
    if (prefs.avoidExamples !== undefined) {
      updates.codePreferences.avoidExamples = validateStringArray(prefs.avoidExamples, "codePreferences.avoidExamples");
    }
    if (prefs.preferredStacks !== undefined) {
      updates.codePreferences.preferredStacks = validateStringArray(prefs.preferredStacks, "codePreferences.preferredStacks");
    }
  }

  if (input.tools !== undefined) {
    if (typeof input.tools !== "object" || input.tools === null) {
      throw new Error("tools must be an object");
    }
    const tools = input.tools as Record<string, unknown>;
    updates.tools = {};
    if (tools.editor !== undefined) updates.tools.editor = validateString(tools.editor, "tools.editor");
    if (tools.infra !== undefined) updates.tools.infra = validateStringArray(tools.infra, "tools.infra");
  }

  if (input.interests !== undefined) {
    updates.interests = validateStringArray(input.interests, "interests");
  }

  return updates;
}

const server = new Server(
  {
    name: "user-memory",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_user_profile",
        description:
          "Get the current user's profile with their preferences, tech stack, role, and other long-term information. Use this at the start of a session to personalize responses.",
        inputSchema: {
          type: "object" as const,
          properties: {},
          required: [],
        },
      },
      {
        name: "update_user_profile",
        description:
          "Update the user's profile with new preferences or information. Use this when the user reveals long-term, stable information about themselves (tech stack, role, preferences). Do not announce that you are saving this information.",
        inputSchema: {
          type: "object" as const,
          properties: {
            bio: {
              type: "string",
              description: "Short bio or description of the user",
            },
            work: {
              type: "object",
              properties: {
                role: { type: "string", description: "Job title or role" },
                focusAreas: {
                  type: "array",
                  items: { type: "string" },
                  description: "Areas of focus (e.g., 'backend', 'ML')",
                },
                languages: {
                  type: "array",
                  items: { type: "string" },
                  description: "Programming languages used",
                },
              },
            },
            codePreferences: {
              type: "object",
              properties: {
                tone: {
                  type: "string",
                  enum: ["direct", "neutral", "friendly"],
                  description: "Preferred communication tone",
                },
                detailLevel: {
                  type: "string",
                  enum: ["high", "medium", "low"],
                  description: "Preferred level of detail in explanations",
                },
                avoidExamples: {
                  type: "array",
                  items: { type: "string" },
                  description: "Types of examples to avoid",
                },
                preferredStacks: {
                  type: "array",
                  items: { type: "string" },
                  description: "Preferred tech stacks/frameworks",
                },
              },
            },
            tools: {
              type: "object",
              properties: {
                editor: { type: "string", description: "Preferred editor" },
                infra: {
                  type: "array",
                  items: { type: "string" },
                  description: "Infrastructure tools used",
                },
              },
            },
            interests: {
              type: "array",
              items: { type: "string" },
              description: "Technical interests",
            },
          },
          required: [],
        },
      },
      {
        name: "clear_user_profile",
        description:
          "Clear the user's profile. Only use when explicitly requested by the user.",
        inputSchema: {
          type: "object" as const,
          properties: {
            confirm: {
              type: "boolean",
              description: "Must be true to confirm deletion",
            },
          },
          required: ["confirm"],
        },
      },
      {
        name: "get_changelog",
        description:
          "Get the changelog of profile updates. Use this to see what preferences have been recorded and when.",
        inputSchema: {
          type: "object" as const,
          properties: {
            limit: {
              type: "number",
              description: "Maximum number of entries to return (default: 20)",
            },
          },
          required: [],
        },
      },
      {
        name: "remove_preference",
        description:
          "Remove specific preferences from the user's profile. Use when the user explicitly says they no longer want a preference stored.",
        inputSchema: {
          type: "object" as const,
          properties: {
            paths: {
              type: "array",
              items: { type: "string" },
              description:
                "Dot-notation paths to remove, e.g., ['codePreferences.tone', 'tools.editor']",
            },
          },
          required: ["paths"],
        },
      },
      {
        name: "run_decay",
        description:
          "Run the decay cycle to remove stale preferences that haven't been reinforced recently. Returns list of removed preferences.",
        inputSchema: {
          type: "object" as const,
          properties: {},
          required: [],
        },
      },
      {
        name: "get_preference_metadata",
        description:
          "Get metadata about preferences including confidence scores and when they were last seen. Useful for understanding which preferences may decay soon.",
        inputSchema: {
          type: "object" as const,
          properties: {},
          required: [],
        },
      },
      // Session continuity tools
      {
        name: "get_session_context",
        description:
          "Get context from the current or previous session including pending tasks, recent decisions, and project context. Use at session start to understand where the user left off.",
        inputSchema: {
          type: "object" as const,
          properties: {
            sessionId: {
              type: "string",
              description: "Current session ID (optional, will use resume context if not provided)",
            },
            projectPath: {
              type: "string",
              description: "Current project path for context matching",
            },
          },
          required: [],
        },
      },
      {
        name: "update_task",
        description:
          "Create or update a task in the current session. Use to track multi-step work and maintain progress across sessions.",
        inputSchema: {
          type: "object" as const,
          properties: {
            sessionId: {
              type: "string",
              description: "Current session ID",
            },
            id: {
              type: "string",
              description: "Unique task identifier",
            },
            title: {
              type: "string",
              description: "Task title/description",
            },
            status: {
              type: "string",
              enum: ["pending", "in_progress", "blocked", "completed"],
              description: "Task status",
            },
            notes: {
              type: "string",
              description: "Additional notes about the task",
            },
            blockedBy: {
              type: "string",
              description: "What's blocking this task (if status is blocked)",
            },
          },
          required: ["sessionId", "id"],
        },
      },
      {
        name: "log_decision",
        description:
          "Log an important decision made during the session. Helps maintain context for future sessions.",
        inputSchema: {
          type: "object" as const,
          properties: {
            sessionId: {
              type: "string",
              description: "Current session ID",
            },
            decision: {
              type: "string",
              description: "The decision that was made",
            },
            rationale: {
              type: "string",
              description: "Why this decision was made",
            },
            alternatives: {
              type: "array",
              items: { type: "string" },
              description: "Other options that were considered",
            },
          },
          required: ["sessionId", "decision"],
        },
      },
      {
        name: "add_session_context",
        description:
          "Add a context note to the current session. Use for important information that should persist.",
        inputSchema: {
          type: "object" as const,
          properties: {
            sessionId: {
              type: "string",
              description: "Current session ID",
            },
            context: {
              type: "string",
              description: "Context note to add",
            },
          },
          required: ["sessionId", "context"],
        },
      },
      {
        name: "set_session_summary",
        description:
          "Set a summary for the current session. This summary will be shown at the start of the next session.",
        inputSchema: {
          type: "object" as const,
          properties: {
            sessionId: {
              type: "string",
              description: "Current session ID",
            },
            summary: {
              type: "string",
              description: "Brief summary of what was accomplished or in progress",
            },
          },
          required: ["sessionId", "summary"],
        },
      },
      {
        name: "get_full_context",
        description:
          "Get the full context prompt including user profile and session resume context. Returns formatted markdown suitable for system prompt injection.",
        inputSchema: {
          type: "object" as const,
          properties: {
            projectPath: {
              type: "string",
              description: "Current project path for context matching",
            },
            includeDecayWarnings: {
              type: "boolean",
              description: "Include warnings about preferences that may decay soon (default: true)",
            },
          },
          required: [],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "get_user_profile": {
      const profile = await loadUserProfile(USER_ID);
      if (!profile) {
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify({ message: "No profile found", userId: USER_ID }, null, 2),
            },
          ],
        };
      }
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(profile, null, 2),
          },
        ],
      };
    }

    case "update_user_profile": {
      // Validate input structure
      const updates = validateProfileUpdates(args);
      const existing = await loadUserProfile(USER_ID);
      const merged = mergeProfile(existing, updates, USER_ID);
      await saveUserProfile(merged);

      // Track preferences for decay
      const paths = getUpdatedPaths(updates);
      for (const path of paths) {
        await trackPreference(USER_ID, path);
      }

      // Log the update
      await logChange({
        action: "update",
        source: "mcp/tool",
        changes: updates,
      });

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: "Profile updated",
                updates: Object.keys(updates),
                trackedPaths: paths,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "clear_user_profile": {
      const input = (args ?? {}) as Record<string, unknown>;
      const confirm = optionalBoolean(input, "confirm") ?? false;
      if (!confirm) {
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify({ error: "Confirmation required" }, null, 2),
            },
          ],
        };
      }

      const deleted = await deleteUserProfile(USER_ID);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: deleted ? "Profile cleared" : "No profile to clear",
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "get_changelog": {
      const input = (args ?? {}) as Record<string, unknown>;
      const limit = optionalNumber(input, "limit") ?? 20;
      const entries = await readChangelog(limit);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                count: entries.length,
                entries,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "remove_preference": {
      const input = (args ?? {}) as Record<string, unknown>;
      if (!input.paths) {
        throw new Error("paths is required");
      }
      const paths = validateStringArray(input.paths, "paths");
      const updated = await removePreferences(USER_ID, paths);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: updated ? "Preferences removed" : "No profile found",
                removed: paths,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "run_decay": {
      const result = await runDecayCycle(USER_ID);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: result.removed.length > 0
                  ? `Removed ${result.removed.length} stale preferences`
                  : "No preferences decayed",
                removed: result.removed,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "get_preference_metadata": {
      const meta = await loadMetadata(USER_ID);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                lastDecay: meta.lastDecay,
                preferences: meta.preferences.map((p) => ({
                  path: p.path,
                  confidence: Math.round(p.confidence * 100) / 100,
                  lastSeen: p.lastSeen,
                  seenCount: p.seenCount,
                  daysUntilDecay: estimateDaysUntilDecay(p.confidence),
                })),
              },
              null,
              2
            ),
          },
        ],
      };
    }

    // Session continuity handlers
    case "get_session_context": {
      const input = (args ?? {}) as Record<string, unknown>;
      const sessionId = optionalString(input, "sessionId");
      const projectPath = optionalString(input, "projectPath");

      if (sessionId) {
        const session = await loadSession(sessionId);
        return {
          content: [
            {
              type: "text" as const,
              text: JSON.stringify(
                session ?? { message: "No session found", sessionId },
                null,
                2
              ),
            },
          ],
        };
      }

      // Get resume context from previous sessions
      const ctx = await getResumeContext(projectPath);
      const prompt = buildResumePrompt(ctx);

      return {
        content: [
          {
            type: "text" as const,
            text: prompt || "No previous session context found.",
          },
        ],
      };
    }

    case "update_task": {
      const input = (args ?? {}) as Record<string, unknown>;
      if (!input.sessionId) throw new Error("sessionId is required");
      if (!input.id) throw new Error("id is required");

      const sessionId = validateString(input.sessionId, "sessionId");
      const id = validateString(input.id, "id");
      const title = optionalString(input, "title");
      const notes = optionalString(input, "notes");
      const blockedBy = optionalString(input, "blockedBy");
      const status = optionalString(input, "status") as TaskState["status"] | undefined;

      if (status && !["pending", "in_progress", "blocked", "completed"].includes(status)) {
        throw new Error("status must be 'pending', 'in_progress', 'blocked', or 'completed'");
      }

      const session = await updateTask(sessionId, { id, title, status, notes, blockedBy });

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: "Task updated",
                task: session.tasks.find((t) => t.id === id),
                totalTasks: session.tasks.length,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "log_decision": {
      const { sessionId, decision, rationale, alternatives } = args as {
        sessionId: string;
        decision: string;
        rationale?: string;
        alternatives?: string[];
      };

      const session = await logDecision(sessionId, decision, rationale, alternatives);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: "Decision logged",
                totalDecisions: session.decisions.length,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "add_session_context": {
      const { sessionId, context } = args as { sessionId: string; context: string };

      const session = await addContext(sessionId, context);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(
              {
                message: "Context added",
                totalContextNotes: session.context.length,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    case "set_session_summary": {
      const { sessionId, summary } = args as { sessionId: string; summary: string };

      let session = await loadSession(sessionId);
      if (!session) {
        session = createSession(sessionId);
      }
      session.summary = summary;
      await saveSession(session);

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ message: "Session summary set", sessionId }, null, 2),
          },
        ],
      };
    }

    case "get_full_context": {
      const { projectPath, includeDecayWarnings = true } = args as {
        projectPath?: string;
        includeDecayWarnings?: boolean;
      };

      const sections: string[] = [];

      // Get user profile context
      const profile = await loadUserProfile(USER_ID);
      if (profile) {
        const metadata = await loadMetadata(USER_ID);
        const profileContext = buildContext(profile, metadata, { includeDecayWarnings });
        sections.push(profileContext);
      }

      // Get session resume context
      const resumeCtx = await getResumeContext(projectPath);
      const resumePrompt = buildResumePrompt(resumeCtx);
      if (resumePrompt) {
        sections.push("");
        sections.push("## Session Continuity");
        sections.push(resumePrompt);
      }

      // Prune old sessions while we're at it
      await pruneOldSessions();

      return {
        content: [
          {
            type: "text" as const,
            text: sections.join("\n") || "No context available.",
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

/**
 * Helper: Extract dot-notation paths from an update object
 */
function getUpdatedPaths(obj: Record<string, unknown>, prefix = ""): string[] {
  const paths: string[] = [];

  for (const [key, value] of Object.entries(obj)) {
    const path = prefix ? `${prefix}.${key}` : key;

    if (value && typeof value === "object" && !Array.isArray(value)) {
      paths.push(...getUpdatedPaths(value as Record<string, unknown>, path));
    } else if (value !== undefined) {
      paths.push(path);
    }
  }

  return paths;
}

/**
 * Helper: Estimate days until preference decays below threshold
 */
function estimateDaysUntilDecay(confidence: number, halfLife = 30, threshold = 0.1): number {
  if (confidence <= threshold) return 0;
  // Solve: confidence * 0.5^(days/halfLife) = threshold
  // days = halfLife * log2(confidence/threshold)
  const days = halfLife * Math.log2(confidence / threshold);
  return Math.max(0, Math.round(days));
}

// Start server
async function main(): Promise<void> {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("User Memory MCP server running on stdio");
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
