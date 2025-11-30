/**
 * User Profile Storage
 *
 * File-based storage abstraction for user profiles.
 * Can be swapped for DB, Redis, or MCP backend.
 */

import { readFile, writeFile, appendFile, mkdir, unlink, open } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { homedir } from "node:os";
import type {
  UserProfile,
  ChangelogEntry,
  ProfileMetadata,
  PreferenceMeta,
  DecayConfig,
} from "./types.js";

const STORAGE_DIR = process.env.USER_MEMORY_DIR ?? join(homedir(), ".claude", "user-memory");
const CHANGELOG_PATH = join(STORAGE_DIR, "changelog.jsonl");
const METADATA_PATH = join(STORAGE_DIR, "profile-meta.json");
const LOCK_FILE = join(STORAGE_DIR, ".lock");
const LOCK_TIMEOUT_MS = 5000;
const LOCK_RETRY_DELAY_MS = 50;

/**
 * Simple file-based lock to prevent race conditions
 */
async function acquireLock(timeoutMs = LOCK_TIMEOUT_MS): Promise<() => Promise<void>> {
  const startTime = Date.now();

  // Ensure storage directory exists
  if (!existsSync(STORAGE_DIR)) {
    await mkdir(STORAGE_DIR, { recursive: true });
  }

  while (Date.now() - startTime < timeoutMs) {
    try {
      // Try to create lock file exclusively
      const fd = await open(LOCK_FILE, "wx");
      await fd.write(`${process.pid}\n${Date.now()}`);
      await fd.close();

      // Return release function
      return async () => {
        try {
          await unlink(LOCK_FILE);
        } catch {
          // Ignore errors when releasing lock
        }
      };
    } catch (err: unknown) {
      if ((err as NodeJS.ErrnoException).code === "EEXIST") {
        // Lock exists, check if it's stale (older than timeout)
        try {
          const content = await readFile(LOCK_FILE, "utf-8");
          const lockTime = parseInt(content.split("\n")[1] ?? "0", 10);
          if (Date.now() - lockTime > LOCK_TIMEOUT_MS) {
            // Stale lock, remove it
            await unlink(LOCK_FILE);
            continue;
          }
        } catch {
          // If we can't read it, try again
        }

        // Wait and retry
        await new Promise((resolve) => setTimeout(resolve, LOCK_RETRY_DELAY_MS));
        continue;
      }
      throw err;
    }
  }

  throw new Error(`Failed to acquire lock after ${timeoutMs}ms`);
}

/**
 * Execute a function with file locking
 */
export async function withLock<T>(fn: () => Promise<T>): Promise<T> {
  const release = await acquireLock();
  try {
    return await fn();
  } finally {
    await release();
  }
}

// Default configs
const DEFAULT_DECAY_CONFIG: DecayConfig = {
  halfLifeDays: 30,
  minConfidence: 0.1,
  reinforceBoost: 0.3,
};

const CHANGELOG_MAX_ENTRIES = 1000;
const CHANGELOG_MAX_AGE_DAYS = 90;

function getProfilePath(userId: string): string {
  // Sanitize userId for filesystem safety
  const safeId = userId.replace(/[^a-zA-Z0-9_-]/g, "_");
  return join(STORAGE_DIR, `${safeId}.json`);
}

/**
 * Load user profile from storage
 */
export async function loadUserProfile(userId: string): Promise<UserProfile | null> {
  const path = getProfilePath(userId);

  if (!existsSync(path)) {
    return null;
  }

  const content = await readFile(path, "utf-8");
  const profile = JSON.parse(content) as UserProfile;

  // Validate schema version
  if (profile.schemaVersion !== 1) {
    console.warn(`Unknown schema version: ${profile.schemaVersion}`);
  }

  return profile;
}

/**
 * Save user profile to storage
 *
 * For atomic read-modify-write operations, wrap in withLock():
 * ```
 * await withLock(async () => {
 *   const profile = await loadUserProfile(userId);
 *   const merged = mergeProfile(profile, updates, userId);
 *   await saveUserProfile(merged);
 * });
 * ```
 */
export async function saveUserProfile(profile: UserProfile): Promise<void> {
  const path = getProfilePath(profile.userId);

  // Ensure directory exists
  const dir = dirname(path);
  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }

  // Update timestamp
  const updated: UserProfile = {
    ...profile,
    lastUpdated: new Date().toISOString(),
  };

  await writeFile(path, JSON.stringify(updated, null, 2), "utf-8");
}

/**
 * Atomically update user profile (with locking)
 * Prevents race conditions when multiple processes modify the profile
 */
export async function updateUserProfileAtomic(
  userId: string,
  updater: (profile: UserProfile | null) => UserProfile
): Promise<UserProfile> {
  return withLock(async () => {
    const existing = await loadUserProfile(userId);
    const updated = updater(existing);
    await saveUserProfile(updated);
    return updated;
  });
}

/**
 * Deep merge profile updates into existing profile
 */
export function mergeProfile(
  existing: UserProfile | null,
  updates: Partial<UserProfile>,
  userId: string
): UserProfile {
  const base: UserProfile = existing ?? {
    userId,
    schemaVersion: 1,
    lastUpdated: new Date().toISOString(),
  };

  return {
    ...base,
    ...updates,
    userId: base.userId, // Never overwrite userId
    schemaVersion: 1, // Always current schema
    work: updates.work
      ? { ...base.work, ...updates.work }
      : base.work,
    codePreferences: updates.codePreferences
      ? { ...base.codePreferences, ...updates.codePreferences }
      : base.codePreferences,
    tools: updates.tools
      ? { ...base.tools, ...updates.tools }
      : base.tools,
    interests: updates.interests
      ? Array.from(new Set([...(base.interests ?? []), ...updates.interests]))
      : base.interests,
    custom: updates.custom
      ? { ...base.custom, ...updates.custom }
      : base.custom,
    lastUpdated: new Date().toISOString(),
  };
}

/**
 * Delete user profile from storage
 */
export async function deleteUserProfile(userId: string): Promise<boolean> {
  const path = getProfilePath(userId);

  if (!existsSync(path)) {
    return false;
  }

  // Log deletion
  await logChange({
    timestamp: new Date().toISOString(),
    action: "clear",
    source: "mcp/tool",
    changes: { userId },
  });

  const { unlink } = await import("node:fs/promises");
  await unlink(path);
  return true;
}

/**
 * Log a change to the changelog (append-only audit trail)
 */
export async function logChange(
  entry: Omit<ChangelogEntry, "timestamp"> & { timestamp?: string }
): Promise<void> {
  // Ensure directory exists
  if (!existsSync(STORAGE_DIR)) {
    await mkdir(STORAGE_DIR, { recursive: true });
  }

  const fullEntry: ChangelogEntry = {
    timestamp: entry.timestamp ?? new Date().toISOString(),
    session_id: entry.session_id,
    action: entry.action,
    source: entry.source,
    changes: entry.changes,
  };

  await appendFile(CHANGELOG_PATH, JSON.stringify(fullEntry) + "\n", "utf-8");
}

/**
 * Read changelog entries (most recent first)
 */
export async function readChangelog(limit = 100): Promise<ChangelogEntry[]> {
  if (!existsSync(CHANGELOG_PATH)) {
    return [];
  }

  const content = await readFile(CHANGELOG_PATH, "utf-8");
  const lines = content.trim().split("\n").filter(Boolean);

  const entries: ChangelogEntry[] = [];
  for (const line of lines.slice(-limit).reverse()) {
    try {
      entries.push(JSON.parse(line) as ChangelogEntry);
    } catch {
      // Skip malformed lines
    }
  }

  return entries;
}

/**
 * Prune changelog: remove old entries and enforce max size
 */
export async function pruneChangelog(): Promise<number> {
  if (!existsSync(CHANGELOG_PATH)) {
    return 0;
  }

  const content = await readFile(CHANGELOG_PATH, "utf-8");
  const lines = content.trim().split("\n").filter(Boolean);

  const cutoffDate = new Date();
  cutoffDate.setDate(cutoffDate.getDate() - CHANGELOG_MAX_AGE_DAYS);
  const cutoffIso = cutoffDate.toISOString();

  // Filter by age and limit
  const filtered = lines
    .filter((line) => {
      try {
        const entry = JSON.parse(line) as ChangelogEntry;
        return entry.timestamp >= cutoffIso;
      } catch {
        return false;
      }
    })
    .slice(-CHANGELOG_MAX_ENTRIES);

  const removed = lines.length - filtered.length;

  if (removed > 0) {
    await writeFile(CHANGELOG_PATH, filtered.join("\n") + "\n", "utf-8");
  }

  return removed;
}

/**
 * Load profile metadata
 */
export async function loadMetadata(userId: string): Promise<ProfileMetadata> {
  if (!existsSync(METADATA_PATH)) {
    return {
      userId,
      schemaVersion: 1,
      lastDecay: new Date().toISOString(),
      preferences: [],
    };
  }

  const content = await readFile(METADATA_PATH, "utf-8");
  return JSON.parse(content) as ProfileMetadata;
}

/**
 * Save profile metadata
 */
export async function saveMetadata(meta: ProfileMetadata): Promise<void> {
  if (!existsSync(STORAGE_DIR)) {
    await mkdir(STORAGE_DIR, { recursive: true });
  }
  await writeFile(METADATA_PATH, JSON.stringify(meta, null, 2), "utf-8");
}

/**
 * Track a preference in metadata (for decay)
 */
export async function trackPreference(
  userId: string,
  path: string,
  config: DecayConfig = DEFAULT_DECAY_CONFIG
): Promise<void> {
  const meta = await loadMetadata(userId);
  const now = new Date().toISOString();

  const existing = meta.preferences.find((p) => p.path === path);
  if (existing) {
    // Reinforce existing preference
    existing.lastSeen = now;
    existing.seenCount += 1;
    existing.confidence = Math.min(1.0, existing.confidence + config.reinforceBoost);
  } else {
    // New preference
    meta.preferences.push({
      path,
      firstSeen: now,
      lastSeen: now,
      confidence: 1.0,
      seenCount: 1,
    });
  }

  await saveMetadata(meta);
}

/**
 * Apply decay to all preferences based on time since last seen
 */
export async function applyDecay(
  userId: string,
  config: DecayConfig = DEFAULT_DECAY_CONFIG
): Promise<string[]> {
  const meta = await loadMetadata(userId);
  const now = new Date();
  const removed: string[] = [];

  // Calculate decay for each preference
  meta.preferences = meta.preferences.filter((pref) => {
    const lastSeen = new Date(pref.lastSeen);
    const daysSince = (now.getTime() - lastSeen.getTime()) / (1000 * 60 * 60 * 24);

    // Exponential decay: confidence * 0.5^(days / halfLife)
    const decayFactor = Math.pow(0.5, daysSince / config.halfLifeDays);
    pref.confidence = pref.confidence * decayFactor;

    if (pref.confidence < config.minConfidence) {
      removed.push(pref.path);
      return false; // Remove from metadata
    }
    return true;
  });

  meta.lastDecay = now.toISOString();
  await saveMetadata(meta);

  return removed;
}

/**
 * Remove specific paths from a profile
 */
export function removeFromProfile(
  profile: UserProfile,
  paths: string[]
): UserProfile {
  const result = JSON.parse(JSON.stringify(profile)) as UserProfile;

  for (const path of paths) {
    const parts = path.split(".");
    let current: Record<string, unknown> = result as unknown as Record<string, unknown>;

    for (let i = 0; i < parts.length - 1; i++) {
      const part = parts[i];
      if (current[part] && typeof current[part] === "object") {
        current = current[part] as Record<string, unknown>;
      } else {
        break; // Path doesn't exist
      }
    }

    const lastPart = parts[parts.length - 1];
    if (lastPart in current) {
      delete current[lastPart];
    }
  }

  result.lastUpdated = new Date().toISOString();
  return result;
}

/**
 * Remove preferences from profile and update metadata
 */
export async function removePreferences(
  userId: string,
  paths: string[]
): Promise<UserProfile | null> {
  const profile = await loadUserProfile(userId);
  if (!profile) return null;

  const updated = removeFromProfile(profile, paths);
  await saveUserProfile(updated);

  // Remove from metadata
  const meta = await loadMetadata(userId);
  meta.preferences = meta.preferences.filter((p) => !paths.includes(p.path));
  await saveMetadata(meta);

  // Log removal
  await logChange({
    action: "remove",
    source: "mcp/tool",
    changes: {},
    removed: paths,
  });

  return updated;
}

/**
 * Run decay and remove stale preferences from profile
 */
export async function runDecayCycle(
  userId: string,
  config: DecayConfig = DEFAULT_DECAY_CONFIG
): Promise<{ removed: string[]; profile: UserProfile | null }> {
  // Apply decay to metadata
  const removed = await applyDecay(userId, config);

  if (removed.length === 0) {
    return { removed: [], profile: await loadUserProfile(userId) };
  }

  // Remove decayed paths from profile
  const profile = await loadUserProfile(userId);
  if (!profile) {
    return { removed, profile: null };
  }

  const updated = removeFromProfile(profile, removed);
  await saveUserProfile(updated);

  // Log decay
  await logChange({
    action: "decay",
    source: "system",
    changes: {},
    removed,
  });

  // Prune changelog while we're at it
  await pruneChangelog();

  return { removed, profile: updated };
}
