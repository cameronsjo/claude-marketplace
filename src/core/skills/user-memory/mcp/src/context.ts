/**
 * Context Injection
 *
 * Builds system prompt context from user profile for injection at SessionStart.
 * Formats profile data into natural language for Claude to understand.
 */

import type { UserProfile, ProfileMetadata, PreferenceMeta } from "./types.js";

interface ContextOptions {
  includeConfidence?: boolean;
  includeDecayWarnings?: boolean;
  warningThreshold?: number; // Days until decay to warn about
}

const DEFAULT_OPTIONS: ContextOptions = {
  includeConfidence: false,
  includeDecayWarnings: true,
  warningThreshold: 14,
};

/**
 * Build a natural language context block from user profile
 */
export function buildContext(
  profile: UserProfile,
  metadata?: ProfileMetadata,
  options: ContextOptions = {}
): string {
  const opts = { ...DEFAULT_OPTIONS, ...options };
  const sections: string[] = [];

  // Header
  sections.push("## User Profile (Long-term Memory)");
  sections.push("");

  // Bio
  if (profile.bio) {
    sections.push(`**About:** ${profile.bio}`);
    sections.push("");
  }

  // Work
  if (profile.work) {
    const workLines: string[] = [];
    if (profile.work.role) {
      workLines.push(`- **Role:** ${profile.work.role}`);
    }
    if (profile.work.languages?.length) {
      workLines.push(`- **Languages:** ${profile.work.languages.join(", ")}`);
    }
    if (profile.work.focusAreas?.length) {
      workLines.push(`- **Focus areas:** ${profile.work.focusAreas.join(", ")}`);
    }
    if (workLines.length > 0) {
      sections.push("### Work");
      sections.push(...workLines);
      sections.push("");
    }
  }

  // Code preferences
  if (profile.codePreferences) {
    const prefLines: string[] = [];
    if (profile.codePreferences.tone) {
      const toneDescriptions = {
        direct: "Be direct and concise",
        neutral: "Balanced detail level",
        friendly: "Friendly and approachable",
      };
      prefLines.push(`- **Tone:** ${toneDescriptions[profile.codePreferences.tone]}`);
    }
    if (profile.codePreferences.detailLevel) {
      const detailDescriptions = {
        high: "Provide detailed explanations",
        medium: "Moderate detail",
        low: "Keep explanations brief",
      };
      prefLines.push(`- **Detail:** ${detailDescriptions[profile.codePreferences.detailLevel]}`);
    }
    if (profile.codePreferences.preferredStacks?.length) {
      prefLines.push(`- **Preferred stacks:** ${profile.codePreferences.preferredStacks.join(", ")}`);
    }
    if (profile.codePreferences.avoidExamples?.length) {
      prefLines.push(`- **Avoid:** ${profile.codePreferences.avoidExamples.join(", ")}`);
    }
    if (prefLines.length > 0) {
      sections.push("### Preferences");
      sections.push(...prefLines);
      sections.push("");
    }
  }

  // Tools
  if (profile.tools) {
    const toolLines: string[] = [];
    if (profile.tools.editor) {
      toolLines.push(`- **Editor:** ${profile.tools.editor}`);
    }
    if (profile.tools.infra?.length) {
      toolLines.push(`- **Infrastructure:** ${profile.tools.infra.join(", ")}`);
    }
    if (toolLines.length > 0) {
      sections.push("### Tools");
      sections.push(...toolLines);
      sections.push("");
    }
  }

  // Interests
  if (profile.interests?.length) {
    sections.push("### Interests");
    sections.push(`- ${profile.interests.join(", ")}`);
    sections.push("");
  }

  // Decay warnings
  if (opts.includeDecayWarnings && metadata?.preferences?.length) {
    const warnings = getDecayWarnings(metadata.preferences, opts.warningThreshold ?? 14);
    if (warnings.length > 0) {
      sections.push("### Preferences Needing Reinforcement");
      sections.push("_These preferences haven't been mentioned recently and may be removed:_");
      for (const warning of warnings) {
        sections.push(`- \`${warning.path}\` (${warning.daysLeft} days until removal)`);
      }
      sections.push("");
    }
  }

  // Footer
  sections.push("---");
  sections.push("_Use this information to personalize responses. Update preferences via MCP tools when the user expresses new preferences._");

  return sections.join("\n");
}

/**
 * Build a compact JSON context for env var injection
 */
export function buildCompactContext(profile: UserProfile): string {
  const compact: Record<string, unknown> = {};

  if (profile.work?.role) compact.role = profile.work.role;
  if (profile.work?.languages?.length) compact.langs = profile.work.languages;
  if (profile.codePreferences?.tone) compact.tone = profile.codePreferences.tone;
  if (profile.codePreferences?.preferredStacks?.length) {
    compact.stacks = profile.codePreferences.preferredStacks;
  }
  if (profile.tools?.editor) compact.editor = profile.tools.editor;

  return JSON.stringify(compact);
}

interface DecayWarning {
  path: string;
  daysLeft: number;
  confidence: number;
}

function getDecayWarnings(preferences: PreferenceMeta[], thresholdDays: number): DecayWarning[] {
  const warnings: DecayWarning[] = [];
  const halfLife = 30;
  const minConfidence = 0.1;

  for (const pref of preferences) {
    // Estimate days until decay below threshold
    // Solve: confidence * 0.5^(days/halfLife) = minConfidence
    // days = halfLife * log2(confidence/minConfidence)
    const daysUntilDecay = halfLife * Math.log2(pref.confidence / minConfidence);
    const daysLeft = Math.max(0, Math.round(daysUntilDecay));

    if (daysLeft <= thresholdDays && daysLeft > 0) {
      warnings.push({
        path: pref.path,
        daysLeft,
        confidence: Math.round(pref.confidence * 100) / 100,
      });
    }
  }

  // Sort by urgency (least days left first)
  return warnings.sort((a, b) => a.daysLeft - b.daysLeft);
}

/**
 * Format profile for CLAUDE.md injection
 */
export function buildClaudeMdSection(profile: UserProfile): string {
  const lines: string[] = [
    "## User Preferences (Auto-loaded)",
    "",
    "This section is automatically managed by the user-memory skill.",
    "",
  ];

  if (profile.codePreferences?.tone) {
    const toneInstructions = {
      direct: "Be direct and concise in responses.",
      neutral: "Use a balanced, neutral tone.",
      friendly: "Be friendly and approachable.",
    };
    lines.push(`- ${toneInstructions[profile.codePreferences.tone]}`);
  }

  if (profile.codePreferences?.preferredStacks?.length) {
    lines.push(`- Prefer using: ${profile.codePreferences.preferredStacks.join(", ")}`);
  }

  if (profile.codePreferences?.avoidExamples?.length) {
    lines.push(`- Avoid: ${profile.codePreferences.avoidExamples.join(", ")}`);
  }

  if (profile.tools?.editor) {
    lines.push(`- User's editor: ${profile.tools.editor}`);
  }

  if (profile.work?.languages?.length) {
    lines.push(`- Primary languages: ${profile.work.languages.join(", ")}`);
  }

  return lines.join("\n");
}
