/**
 * System Prompt Builder
 *
 * Generates system prompt with user profile injection
 * and dual-output response protocol.
 */

import type { UserProfile } from "./types.js";

/**
 * Build the memory-aware system prompt
 */
export function buildSystemPrompt(profile: UserProfile | null): string {
  const profileJson = profile ? JSON.stringify(profile, null, 2) : "{}";

  return `You are a coding assistant running inside a development environment.

You have long-term memory about this user, available below.
Use it to:
- adapt tone and explanation depth,
- default to their preferred stacks and tools,
- reference recurring projects when helpful.

<UserProfile>
${profileJson}
</UserProfile>

Response protocol:
- You MUST respond using BOTH sections below:
  1) <assistant_reply>...</assistant_reply>
  2) <memory_update>{...}</memory_update>

"memory_update" rules:
- Only set "should_write": true if the user's latest message reveals
  long-term, stable information (preferences, recurring projects, tech stack, etc.).
- If nothing should be stored, use:
  { "should_write": false, "updates": {} }.
- "updates" must be a partial UserProfile object matching this schema:
  {
    bio?: string;
    work?: { role?, focusAreas?[], languages?[] };
    codePreferences?: { tone?, detailLevel?, avoidExamples?[], preferredStacks?[] };
    tools?: { editor?, infra?[] };
    interests?: string[];
    custom?: Record<string, unknown>;
  }
- Do NOT talk about memory in <assistant_reply>.
- Do NOT mention that you are storing information.`;
}

/**
 * Regex patterns for memory-worthy messages
 */
const MEMORY_PATTERNS = [
  /\bremember\b/i,
  /\bfrom now on\b/i,
  /\bi prefer\b/i,
  /\bi like\b/i,
  /\bi dislike\b/i,
  /\bi hate\b/i,
  /\bassume that\b/i,
  /\balways use\b/i,
  /\bnever use\b/i,
  /\bmy (default|preferred|usual)\b/i,
  /\bi('m| am) (a|an)\b/i, // "I'm a backend engineer"
  /\bi work (on|with|at|for)\b/i,
  /\bmy (stack|setup|workflow)\b/i,
];

/**
 * Heuristic check for memory-worthy messages
 * Used to short-circuit memory processing on trivial queries
 */
export function looksMemoryWorthy(message: string): boolean {
  return MEMORY_PATTERNS.some((pattern) => pattern.test(message));
}

/**
 * Build a hint to append to system prompt based on heuristic
 */
export function buildMemoryHint(isMemoryWorthy: boolean): string {
  if (isMemoryWorthy) {
    return "\n\nFor this message, decide normally whether to set memory.should_write.";
  }
  return "\n\nFor this message, you MUST set memory.should_write = false and memory.updates = {}.";
}
