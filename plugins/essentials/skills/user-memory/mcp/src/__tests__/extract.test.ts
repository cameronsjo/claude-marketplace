/**
 * Tests for pattern extraction
 *
 * Imports patterns and functions from the real extract-memory module
 * to ensure tests stay in sync with implementation.
 */

import { describe, it, expect } from "vitest";
import {
  MEMORY_PATTERNS,
  extractFromMessage,
  extractFromMessages,
  type ExtractionResult,
  type PatternDefinition,
} from "../extract-memory.js";

describe("Pattern Extraction", () => {
  describe("Tech Stack Preferences", () => {
    it("extracts 'I prefer X over Y' pattern", () => {
      const result = extractFromMessage("I prefer Bun over npm");
      expect(result.updates).toEqual({
        codePreferences: { preferredStacks: ["Bun"] },
      });
      expect(result.removals).toContain("codePreferences.preferredStacks.npm");
    });

    it("extracts 'I'm switching to X' pattern", () => {
      const result = extractFromMessage("I'm switching to FastAPI");
      expect(result.updates).toEqual({
        codePreferences: { preferredStacks: ["FastAPI"] },
      });
    });

    it("extracts 'I'm using X' pattern", () => {
      const result = extractFromMessage("I'm using TypeScript");
      expect(result.updates).toEqual({
        codePreferences: { preferredStacks: ["TypeScript"] },
      });
    });

    it("extracts multiple stacks with + separator", () => {
      const result = extractFromMessage("I'm using React + TypeScript");
      expect(result.updates).toEqual({
        codePreferences: { preferredStacks: ["React", "TypeScript"] },
      });
    });

    it("extracts 'my preferred stack is X' pattern", () => {
      const result = extractFromMessage("My preferred stack is Next.js");
      expect(result.updates).toEqual({
        codePreferences: { preferredStacks: ["Next.js"] },
      });
    });
  });

  describe("Role Extraction", () => {
    it("extracts backend engineer role", () => {
      const result = extractFromMessage("I'm a backend engineer");
      expect(result.updates).toEqual({
        work: { role: "backend engineer" },
      });
    });

    it("extracts senior frontend developer role", () => {
      const result = extractFromMessage("I'm a senior frontend developer");
      expect(result.updates).toEqual({
        work: { role: "senior frontend developer" },
      });
    });

    it("extracts ML engineer role", () => {
      const result = extractFromMessage("I am an ML engineer");
      expect(result.updates).toEqual({
        work: { role: "ML engineer" },
      });
    });
  });

  describe("Editor Preferences", () => {
    it("extracts 'I use X' pattern", () => {
      const result = extractFromMessage("I use neovim");
      expect(result.updates).toEqual({
        tools: { editor: "neovim" },
      });
    });

    it("extracts 'my editor is X' pattern", () => {
      // Note: pattern requires exact match "vscode"
      const result = extractFromMessage("My editor is vscode");
      expect(result.updates).toEqual({
        tools: { editor: "vscode" },
      });
    });

    it("extracts 'I use X' for known editors", () => {
      // Note: "I'm using Cursor" matches the stack pattern first
      // because "I'm using X" is a stack pattern. Use "I use cursor" instead.
      const result = extractFromMessage("I use cursor");
      expect(result.updates).toEqual({
        tools: { editor: "cursor" },
      });
    });

    it("normalizes editor names to lowercase", () => {
      const result = extractFromMessage("I use NEOVIM");
      expect(result.updates).toEqual({
        tools: { editor: "neovim" },
      });
    });
  });

  describe("Tone Preferences", () => {
    it("maps 'direct' to direct tone", () => {
      const result = extractFromMessage("Be more direct");
      expect(result.updates).toEqual({
        codePreferences: { tone: "direct" },
      });
    });

    it("maps 'concise' to direct tone", () => {
      const result = extractFromMessage("I prefer concise responses");
      expect(result.updates).toEqual({
        codePreferences: { tone: "direct" },
      });
    });

    it("maps 'friendly' to friendly tone", () => {
      const result = extractFromMessage("Be more friendly");
      expect(result.updates).toEqual({
        codePreferences: { tone: "friendly" },
      });
    });

    it("maps 'casual' to friendly tone", () => {
      const result = extractFromMessage("I like casual conversation");
      expect(result.updates).toEqual({
        codePreferences: { tone: "friendly" },
      });
    });

    it("maps 'detailed' to neutral tone", () => {
      const result = extractFromMessage("I prefer detailed explanations");
      expect(result.updates).toEqual({
        codePreferences: { tone: "neutral" },
      });
    });
  });

  describe("Negation Patterns", () => {
    it("handles 'I stopped using X'", () => {
      const result = extractFromMessage("I stopped using React");
      expect(result.updates).toEqual({});
      expect(result.removals).toContain("codePreferences.preferredStacks.react");
    });

    it("handles 'I switched away from X'", () => {
      const result = extractFromMessage("I switched away from npm");
      expect(result.updates).toEqual({});
      expect(result.removals).toContain("codePreferences.preferredStacks.npm");
    });

    it("handles 'I don't use X' (without anymore)", () => {
      const result = extractFromMessage("I don't use Grunt");
      expect(result.updates).toEqual({});
      expect(result.removals).toContain("codePreferences.preferredStacks.grunt");
    });

    it("handles 'I moved away from X'", () => {
      const result = extractFromMessage("I moved away from Webpack");
      expect(result.updates).toEqual({});
      expect(result.removals).toContain("codePreferences.preferredStacks.webpack");
    });
  });

  describe("Priority System", () => {
    it("negation patterns have higher priority than positive patterns", () => {
      // This tests that the sorting works - negations (priority 10)
      // should be checked before comparisons (priority 5)
      const patterns = [...MEMORY_PATTERNS].sort(
        (a, b) => (b.priority ?? 0) - (a.priority ?? 0)
      );

      const negationIndex = patterns.findIndex(
        (p) => p.pattern.source.includes("no longer")
      );
      const positiveIndex = patterns.findIndex(
        (p) => p.pattern.source.includes("i prefer")
      );

      expect(negationIndex).toBeLessThan(positiveIndex);
    });
  });

  describe("Edge Cases", () => {
    it("returns empty result for non-matching input", () => {
      const result = extractFromMessage("Hello, how are you?");
      expect(result.updates).toEqual({});
      expect(result.removals).toEqual([]);
    });

    it("is case insensitive", () => {
      const result = extractFromMessage("I'M A BACKEND ENGINEER");
      expect(result.updates).toEqual({
        work: { role: "BACKEND ENGINEER" },
      });
    });

    it("handles contractions", () => {
      const result1 = extractFromMessage("I'm using TypeScript");
      const result2 = extractFromMessage("I am using TypeScript");

      expect(result1.updates).toEqual(result2.updates);
    });
  });

  describe("Multi-message extraction", () => {
    it("aggregates results from multiple messages", () => {
      const messages = [
        "I'm a backend engineer",
        "I use neovim",
        "I prefer Bun over npm",
      ];

      const result = extractFromMessages(messages);

      expect(result.updates.work?.role).toBe("backend engineer");
      expect(result.updates.tools?.editor).toBe("neovim");
      expect(result.updates.codePreferences?.preferredStacks).toContain("Bun");
      expect(result.removals).toContain("codePreferences.preferredStacks.npm");
    });

    it("deduplicates removals", () => {
      const messages = [
        "I don't use Webpack",
        "I switched away from Webpack",
      ];

      const result = extractFromMessages(messages);

      // Should only have one removal for webpack, not duplicates
      const webpackRemovals = result.removals.filter(r => r.includes("webpack"));
      expect(webpackRemovals).toHaveLength(1);
    });
  });
});

describe("Decay Math", () => {
  it("calculates correct decay after 30 days", () => {
    const initial = 1.0;
    const halfLife = 30;
    const days = 30;

    const decayed = initial * Math.pow(0.5, days / halfLife);
    expect(decayed).toBeCloseTo(0.5, 5);
  });

  it("calculates correct decay after 60 days", () => {
    const initial = 1.0;
    const halfLife = 30;
    const days = 60;

    const decayed = initial * Math.pow(0.5, days / halfLife);
    expect(decayed).toBeCloseTo(0.25, 5);
  });

  it("calculates correct decay after 90 days", () => {
    const initial = 1.0;
    const halfLife = 30;
    const days = 90;

    const decayed = initial * Math.pow(0.5, days / halfLife);
    expect(decayed).toBeCloseTo(0.125, 5);
  });

  it("reinforcement caps at 1.0", () => {
    const current = 0.85;
    const boost = 0.3;
    const reinforced = Math.min(1.0, current + boost);

    expect(reinforced).toBe(1.0);
  });
});

describe("Pattern Coverage", () => {
  it("all patterns have valid regex", () => {
    for (const { pattern } of MEMORY_PATTERNS) {
      expect(() => "test".match(pattern)).not.toThrow();
    }
  });

  it("all extract functions return valid structure", () => {
    const dummyMatch = ["test", "value1", "value2"] as RegExpMatchArray;

    for (const { extract } of MEMORY_PATTERNS) {
      const result = extract(dummyMatch, "test");
      expect(result).toHaveProperty("updates");
      expect(result).toHaveProperty("removals");
      expect(Array.isArray(result.removals)).toBe(true);
    }
  });
});
