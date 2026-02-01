#!/usr/bin/env tsx
/**
 * Memory Extraction Script
 *
 * Reads conversation transcript and extracts long-term user preferences.
 * Uses heuristic pattern matching first, LLM fallback for complex cases.
 */

import { readFileSync, existsSync } from "node:fs";
import {
  loadUserProfile,
  saveUserProfile,
  mergeProfile,
  removePreferences,
  logChange,
} from "./store.js";
import type { UserProfile } from "./types.js";

/**
 * Extraction result with optional removal paths
 */
export interface ExtractionResult {
  updates: Partial<UserProfile>;
  removals: string[];
}

/**
 * Pattern definition for memory extraction
 */
export interface PatternDefinition {
  pattern: RegExp;
  extract: (match: RegExpMatchArray, text: string) => ExtractionResult;
  priority?: number; // Higher priority patterns override lower ones
}

/**
 * Memory extraction patterns - exported for testing
 */
export const MEMORY_PATTERNS: PatternDefinition[] = [
  // === NEGATION PATTERNS (higher priority) ===

  // "I no longer use X", "I stopped using X", "I'm not using X anymore"
  {
    pattern: /(?:i(?:'m| am)? no longer|i stopped|i(?:'m| am) not.*anymore)\s+(?:using|with)\s+(\w+)/i,
    priority: 10,
    extract: (match) => ({
      updates: {},
      removals: [`codePreferences.preferredStacks.${match[1].toLowerCase()}`],
    }),
  },

  // "Don't remember that I use X", "Forget that I prefer X"
  {
    pattern: /(?:don't|do not|forget|remove|delete)\s+(?:remember|store|save|that)\s+(?:i (?:use|prefer|like))\s+(\w+)/i,
    priority: 10,
    extract: (match) => ({
      updates: {},
      removals: [`codePreferences.preferredStacks.${match[1].toLowerCase()}`],
    }),
  },

  // "I don't use X anymore", "I switched away from X"
  {
    pattern: /(?:i don't use|i switched away from|i moved away from)\s+(\w+)/i,
    priority: 10,
    extract: (match) => ({
      updates: {},
      removals: [`codePreferences.preferredStacks.${match[1].toLowerCase()}`],
    }),
  },

  // "Clear my preference for X", "Remove my X preference"
  {
    pattern: /(?:clear|remove|delete)\s+(?:my )?(?:preference|setting)\s+(?:for\s+)?(\w+)/i,
    priority: 10,
    extract: (match) => ({
      updates: {},
      removals: [match[1].toLowerCase()],
    }),
  },

  // === POSITIVE PATTERNS ===

  // Tech stack preferences
  {
    pattern: /(?:i prefer|i like|always use|from now on.*use)\s+(\w+)\s+(?:over|instead of|not)\s+(\w+)/i,
    priority: 5,
    extract: (match) => ({
      updates: {
        codePreferences: {
          preferredStacks: [match[1]],
        },
      },
      removals: [`codePreferences.preferredStacks.${match[2].toLowerCase()}`],
    }),
  },

  // Runtime/framework preferences
  {
    pattern: /(?:i(?:'m| am) switching to|i(?:'m| am) using|my (?:preferred|default) (?:is|stack is))\s+([A-Za-z][A-Za-z0-9.]*(?:\s*\+\s*[A-Za-z][A-Za-z0-9.]*)*)/i,
    extract: (match) => ({
      updates: {
        codePreferences: {
          preferredStacks: match[1].split(/\s*\+\s*/),
        },
      },
      removals: [],
    }),
  },

  // Role/job
  {
    pattern: /i(?:'m| am) (?:a|an)\s+([\w\s]+?)(?:engineer|developer|architect|lead|manager|designer)/i,
    extract: (match) => ({
      updates: {
        work: {
          role: match[0].replace(/^i(?:'m| am) (?:a|an)\s+/i, "").trim(),
        },
      },
      removals: [],
    }),
  },

  // Editor preference
  {
    pattern: /(?:i use|my editor is|i(?:'m| am) using)\s+(vscode|vim|neovim|nvim|emacs|cursor|zed|sublime|intellij|webstorm)/i,
    extract: (match) => ({
      updates: {
        tools: {
          editor: match[1].toLowerCase(),
        },
      },
      removals: [],
    }),
  },

  // Communication tone
  {
    pattern: /(?:be more|i prefer|i like)\s+(direct|concise|detailed|verbose|friendly|casual|formal)/i,
    extract: (match) => {
      const tone = match[1].toLowerCase();
      const toneMap: Record<string, "direct" | "neutral" | "friendly"> = {
        direct: "direct",
        concise: "direct",
        formal: "direct",
        detailed: "neutral",
        verbose: "neutral",
        friendly: "friendly",
        casual: "friendly",
      };
      return {
        updates: {
          codePreferences: {
            tone: toneMap[tone] ?? "neutral",
          },
        },
        removals: [],
      };
    },
  },

  // Languages
  {
    pattern: /(?:i work (?:mostly )?(?:in|with)|my (?:main )?languages? (?:is|are))\s+([\w\s,+]+)/i,
    extract: (match) => ({
      updates: {
        work: {
          languages: match[1]
            .split(/[,+]|\s+and\s+/)
            .map((l) => l.trim())
            .filter(Boolean),
        },
      },
      removals: [],
    }),
  },

  // Focus areas
  {
    pattern: /(?:i (?:work on|focus on|specialize in)|my focus is)\s+([\w\s,]+)/i,
    extract: (match) => ({
      updates: {
        work: {
          focusAreas: match[1]
            .split(/[,]|\s+and\s+/)
            .map((a) => a.trim())
            .filter(Boolean),
        },
      },
      removals: [],
    }),
  },

  // Avoid patterns
  {
    pattern: /(?:don't|do not|never|avoid)\s+(?:use|give me|show me)\s+([\w\s]+?)(?:\s+examples?|\s+metaphors?)?(?:\.|$)/i,
    extract: (match) => ({
      updates: {
        codePreferences: {
          avoidExamples: [match[1].trim()],
        },
      },
      removals: [],
    }),
  },
];

interface TranscriptEntry {
  type: string;
  message?: {
    role: string;
    content: string | Array<{ type: string; text?: string }>;
  };
}

function parseTranscript(path: string): string[] {
  const content = readFileSync(path, "utf-8");
  const lines = content.trim().split("\n");
  const userMessages: string[] = [];

  for (const line of lines) {
    try {
      const entry = JSON.parse(line) as TranscriptEntry;
      if (entry.type === "user" || entry.message?.role === "user") {
        const msg = entry.message;
        if (typeof msg?.content === "string") {
          userMessages.push(msg.content);
        } else if (Array.isArray(msg?.content)) {
          const text = msg.content
            .filter((c) => c.type === "text" && c.text)
            .map((c) => c.text)
            .join(" ");
          if (text) userMessages.push(text);
        }
      }
    } catch {
      // Skip malformed lines
    }
  }

  return userMessages;
}

/**
 * Aggregated extraction result from multiple messages
 */
export interface AggregatedExtraction {
  updates: Partial<UserProfile>;
  removals: string[];
}

/**
 * Extract memory-worthy information from a single message
 * Exported for testing
 */
export function extractFromMessage(message: string): ExtractionResult {
  const sortedPatterns = [...MEMORY_PATTERNS].sort(
    (a, b) => (b.priority ?? 0) - (a.priority ?? 0)
  );

  for (const { pattern, extract } of sortedPatterns) {
    const match = message.match(pattern);
    if (match) {
      return extract(match, message);
    }
  }

  return { updates: {}, removals: [] };
}

/**
 * Extract memory-worthy information from a list of messages
 * Exported for testing
 */
export function extractFromMessages(messages: string[]): AggregatedExtraction {
  let accumulated: Partial<UserProfile> = {};
  const allRemovals: string[] = [];

  // Sort patterns by priority (higher first)
  const sortedPatterns = [...MEMORY_PATTERNS].sort(
    (a, b) => (b.priority ?? 0) - (a.priority ?? 0)
  );

  for (const message of messages) {
    for (const { pattern, extract } of sortedPatterns) {
      const match = message.match(pattern);
      if (match) {
        const { updates, removals } = extract(match, message);
        accumulated = mergePartial(accumulated, updates);
        allRemovals.push(...removals);
      }
    }
  }

  return { updates: accumulated, removals: [...new Set(allRemovals)] };
}

function mergePartial(
  base: Partial<UserProfile>,
  updates: Partial<UserProfile>
): Partial<UserProfile> {
  return {
    ...base,
    ...updates,
    work: { ...base.work, ...updates.work },
    codePreferences: { ...base.codePreferences, ...updates.codePreferences },
    tools: { ...base.tools, ...updates.tools },
    interests: [
      ...new Set([...(base.interests ?? []), ...(updates.interests ?? [])]),
    ],
  };
}

function hasContent(obj: Partial<UserProfile>): boolean {
  return Object.keys(obj).some((key) => {
    const val = obj[key as keyof UserProfile];
    if (val === undefined || val === null) return false;
    if (typeof val === "object" && Object.keys(val).length === 0) return false;
    return true;
  });
}

async function main(): Promise<void> {
  const [transcriptPath, sessionId] = process.argv.slice(2);

  if (!transcriptPath || !existsSync(transcriptPath)) {
    console.error("Usage: extract-memory.ts <transcript_path> [session_id]");
    process.exit(1);
  }

  // Parse transcript for user messages
  const userMessages = parseTranscript(transcriptPath);
  if (userMessages.length === 0) {
    process.exit(0);
  }

  // Extract using heuristics
  const { updates, removals } = extractFromMessages(userMessages);

  const hasUpdates = hasContent(updates);
  const hasRemovals = removals.length > 0;

  if (!hasUpdates && !hasRemovals) {
    // Nothing memory-worthy found
    process.exit(0);
  }

  const userId = process.env.USER ?? "default";

  // Handle removals first (negation patterns take priority)
  if (hasRemovals) {
    await removePreferences(userId, removals);
    console.log(`Removed preferences: ${removals.join(", ")}`);
  }

  // Then apply updates
  if (hasUpdates) {
    const existing = await loadUserProfile(userId);
    const merged = mergeProfile(existing, updates, userId);
    await saveUserProfile(merged);

    // Log the extraction
    await logChange({
      action: "extract",
      source: "mcp/hook",
      session_id: sessionId,
      changes: updates,
    });

    console.log(
      `Updated profile for ${userId}:`,
      JSON.stringify(updates, null, 2)
    );
  }
}

// Only run main when executed directly, not when imported
const isMainModule = process.argv[1]?.endsWith("extract-memory.ts") ||
                     process.argv[1]?.includes("extract-memory");

if (isMainModule) {
  main().catch((err) => {
    console.error("Extract memory failed:", err);
    process.exit(1);
  });
}
