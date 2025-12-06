/**
 * Tests for store operations
 */

import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { mkdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

// Test utilities - unique dir per test run
const TEST_DIR = join(tmpdir(), "user-memory-test-" + Date.now() + "-" + Math.random().toString(36).slice(2));

// Mock the storage directory BEFORE importing store
process.env.USER_MEMORY_DIR = TEST_DIR;

// Import after setting env
import {
  loadUserProfile,
  saveUserProfile,
  mergeProfile,
  removeFromProfile,
  loadMetadata,
  saveMetadata,
  trackPreference,
  applyDecay,
  logChange,
  readChangelog,
  pruneChangelog,
} from "../store.js";
import type { UserProfile, ProfileMetadata } from "../types.js";

describe("Store Operations", () => {
  beforeAll(async () => {
    // Clean up any existing test dir
    if (existsSync(TEST_DIR)) {
      await rm(TEST_DIR, { recursive: true, force: true });
    }
    await mkdir(TEST_DIR, { recursive: true });
  });

  afterAll(async () => {
    if (existsSync(TEST_DIR)) {
      await rm(TEST_DIR, { recursive: true, force: true });
    }
  });

  beforeEach(async () => {
    // Clean test directory between tests
    if (existsSync(TEST_DIR)) {
      await rm(TEST_DIR, { recursive: true, force: true });
    }
    await mkdir(TEST_DIR, { recursive: true });
  });

  describe("Profile CRUD", () => {
    it("returns null for non-existent profile", async () => {
      const profile = await loadUserProfile("nonexistent");
      expect(profile).toBeNull();
    });

    it("saves and loads profile correctly", async () => {
      const profile: UserProfile = {
        userId: "test-user",
        schemaVersion: 1,
        lastUpdated: new Date().toISOString(),
        work: { role: "engineer" },
      };

      await saveUserProfile(profile);
      const loaded = await loadUserProfile("test-user");

      expect(loaded).not.toBeNull();
      expect(loaded?.userId).toBe("test-user");
      expect(loaded?.work?.role).toBe("engineer");
    });

    it("updates lastUpdated on save", async () => {
      const oldDate = "2020-01-01T00:00:00.000Z";
      const profile: UserProfile = {
        userId: "test-user",
        schemaVersion: 1,
        lastUpdated: oldDate,
      };

      await saveUserProfile(profile);
      const loaded = await loadUserProfile("test-user");

      expect(loaded?.lastUpdated).not.toBe(oldDate);
    });
  });

  describe("Profile Merging", () => {
    it("creates new profile if none exists", () => {
      const merged = mergeProfile(null, { work: { role: "dev" } }, "new-user");

      expect(merged.userId).toBe("new-user");
      expect(merged.schemaVersion).toBe(1);
      expect(merged.work?.role).toBe("dev");
    });

    it("merges work object correctly", () => {
      const existing: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "",
        work: { role: "dev", languages: ["TypeScript"] },
      };

      const merged = mergeProfile(
        existing,
        { work: { focusAreas: ["APIs"] } },
        "test"
      );

      expect(merged.work?.role).toBe("dev");
      expect(merged.work?.languages).toEqual(["TypeScript"]);
      expect(merged.work?.focusAreas).toEqual(["APIs"]);
    });

    it("deduplicates interests array", () => {
      const existing: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "",
        interests: ["TypeScript", "Rust"],
      };

      const merged = mergeProfile(
        existing,
        { interests: ["Rust", "Go"] },
        "test"
      );

      expect(merged.interests).toEqual(["TypeScript", "Rust", "Go"]);
    });

    it("never overwrites userId", () => {
      const existing: UserProfile = {
        userId: "original",
        schemaVersion: 1,
        lastUpdated: "",
      };

      const merged = mergeProfile(
        existing,
        { userId: "hacker" } as Partial<UserProfile>,
        "original"
      );

      expect(merged.userId).toBe("original");
    });
  });

  describe("Profile Removal", () => {
    it("removes simple path", () => {
      const profile: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "",
        work: { role: "dev" },
        tools: { editor: "vim" },
      };

      const result = removeFromProfile(profile, ["tools.editor"]);

      expect(result.tools?.editor).toBeUndefined();
      expect(result.work?.role).toBe("dev"); // Untouched
    });

    it("removes nested path", () => {
      const profile: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "",
        codePreferences: {
          tone: "direct",
          preferredStacks: ["Bun"],
        },
      };

      const result = removeFromProfile(profile, ["codePreferences.tone"]);

      expect(result.codePreferences?.tone).toBeUndefined();
      expect(result.codePreferences?.preferredStacks).toEqual(["Bun"]);
    });

    it("handles non-existent paths gracefully", () => {
      const profile: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "",
      };

      const result = removeFromProfile(profile, ["nonexistent.path"]);

      expect(result.userId).toBe("test");
    });

    it("updates lastUpdated on removal", () => {
      const profile: UserProfile = {
        userId: "test",
        schemaVersion: 1,
        lastUpdated: "2020-01-01T00:00:00.000Z",
        tools: { editor: "vim" },
      };

      const result = removeFromProfile(profile, ["tools.editor"]);

      expect(result.lastUpdated).not.toBe("2020-01-01T00:00:00.000Z");
    });
  });

  describe("Metadata Operations", () => {
    it("returns metadata with preferences array", async () => {
      const meta = await loadMetadata("test-user");

      expect(meta.schemaVersion).toBe(1);
      expect(Array.isArray(meta.preferences)).toBe(true);
    });

    it("tracks new preference with confidence 1.0", async () => {
      await trackPreference("track-user", "tools.editor");
      const meta = await loadMetadata("track-user");

      const pref = meta.preferences.find(p => p.path === "tools.editor");
      expect(pref).toBeDefined();
      expect(pref?.confidence).toBe(1.0);
      expect(pref?.seenCount).toBeGreaterThanOrEqual(1);
    });

    it("reinforces existing preference", async () => {
      // Create initial preference directly with controlled values
      const initialMeta: ProfileMetadata = {
        userId: "reinforce-user",
        schemaVersion: 1,
        lastDecay: new Date().toISOString(),
        preferences: [{
          path: "work.role",
          firstSeen: new Date().toISOString(),
          lastSeen: new Date().toISOString(),
          confidence: 0.5,
          seenCount: 1,
        }],
      };
      await saveMetadata(initialMeta);

      // Reinforce
      await trackPreference("reinforce-user", "work.role");
      const updated = await loadMetadata("reinforce-user");

      const pref = updated.preferences.find(p => p.path === "work.role");
      expect(pref?.confidence).toBe(0.8); // 0.5 + 0.3
      expect(pref?.seenCount).toBe(2);
    });

    it("caps reinforcement at 1.0", async () => {
      // Start with high confidence
      const initialMeta: ProfileMetadata = {
        userId: "cap-user",
        schemaVersion: 1,
        lastDecay: new Date().toISOString(),
        preferences: [{
          path: "tools.infra",
          firstSeen: new Date().toISOString(),
          lastSeen: new Date().toISOString(),
          confidence: 0.9,
          seenCount: 1,
        }],
      };
      await saveMetadata(initialMeta);

      // Reinforce - should cap at 1.0
      await trackPreference("cap-user", "tools.infra");
      const meta = await loadMetadata("cap-user");

      const pref = meta.preferences.find(p => p.path === "tools.infra");
      expect(pref?.confidence).toBe(1.0);
    });
  });

  describe("Decay", () => {
    it("removes preferences below threshold", async () => {
      // Create preference with very low confidence
      const meta: ProfileMetadata = {
        userId: "test-user",
        schemaVersion: 1,
        lastDecay: new Date().toISOString(),
        preferences: [
          {
            path: "tools.editor",
            firstSeen: "2020-01-01T00:00:00.000Z",
            lastSeen: "2020-01-01T00:00:00.000Z", // Very old
            confidence: 0.05, // Below 0.1 threshold
            seenCount: 1,
          },
        ],
      };
      await saveMetadata(meta);

      const removed = await applyDecay("test-user");

      expect(removed).toContain("tools.editor");

      const updated = await loadMetadata("test-user");
      expect(updated.preferences).toHaveLength(0);
    });

    it("updates lastDecay timestamp", async () => {
      const oldDate = "2020-01-01T00:00:00.000Z";
      const meta: ProfileMetadata = {
        userId: "test-user",
        schemaVersion: 1,
        lastDecay: oldDate,
        preferences: [],
      };
      await saveMetadata(meta);

      await applyDecay("test-user");
      const updated = await loadMetadata("test-user");

      expect(updated.lastDecay).not.toBe(oldDate);
    });
  });

  describe("Changelog", () => {
    it("logs changes to changelog file", async () => {
      const before = await readChangelog(100);
      const countBefore = before.length;

      await logChange({
        action: "update",
        source: "mcp/tool",
        changes: { tools: { editor: "vim" } },
      });

      const after = await readChangelog(100);

      expect(after.length).toBe(countBefore + 1);
      expect(after[0].action).toBe("update");
      expect(after[0].source).toBe("mcp/tool");
    });

    it("returns entries in reverse chronological order", async () => {
      await logChange({ action: "clear", source: "mcp/tool", changes: {} });
      await new Promise(r => setTimeout(r, 10)); // Small delay to ensure different timestamps
      await logChange({ action: "decay", source: "system", changes: {} });

      const entries = await readChangelog(2);

      // Most recent first
      expect(entries[0].action).toBe("decay");
      expect(entries[1].action).toBe("clear");
    });

    it("respects limit parameter", async () => {
      // Add several entries
      for (let i = 0; i < 5; i++) {
        await logChange({ action: "remove", source: "mcp/tool", changes: {} });
      }

      const entries = await readChangelog(3);

      expect(entries.length).toBeLessThanOrEqual(3);
    });

    it("pruneChangelog returns a number", async () => {
      // Just verify pruneChangelog runs without error
      const pruned = await pruneChangelog();
      expect(typeof pruned).toBe("number");
      expect(pruned).toBeGreaterThanOrEqual(0);
    });
  });
});
