#!/usr/bin/env tsx
/**
 * Decay Check Script
 *
 * Runs on session start to check if decay cycle should run.
 * Only runs decay if it's been more than 24 hours since last decay.
 */

import { loadMetadata, runDecayCycle, pruneChangelog } from "./store.js";

const MIN_DECAY_INTERVAL_HOURS = 24;

async function main(): Promise<void> {
  const userId = process.env.USER ?? "default";
  const meta = await loadMetadata(userId);

  // Check if we should run decay
  const lastDecay = new Date(meta.lastDecay);
  const now = new Date();
  const hoursSinceDecay = (now.getTime() - lastDecay.getTime()) / (1000 * 60 * 60);

  if (hoursSinceDecay < MIN_DECAY_INTERVAL_HOURS) {
    // Too soon, skip decay
    process.exit(0);
  }

  // Run decay cycle
  const result = await runDecayCycle(userId);

  if (result.removed.length > 0) {
    console.error(`user-memory: decay removed ${result.removed.length} stale preferences`);
    for (const path of result.removed) {
      console.error(`  - ${path}`);
    }
  }

  // Prune old changelog entries
  const pruned = await pruneChangelog();
  if (pruned > 0) {
    console.error(`user-memory: pruned ${pruned} old changelog entries`);
  }
}

main().catch((err) => {
  console.error("Decay check failed:", err);
  process.exit(1);
});
