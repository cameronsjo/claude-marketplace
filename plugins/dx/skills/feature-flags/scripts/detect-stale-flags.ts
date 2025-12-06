#!/usr/bin/env node
/**
 * Detect Stale Feature Flags
 *
 * Identifies feature flags that haven't been modified recently and should
 * potentially be removed or reviewed.
 */

import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

interface FlagInfo {
  name: string;
  type: 'release' | 'experiment' | 'ops' | 'permission' | 'unknown';
  lastModified: Date;
  daysStale: number;
  filePath: string;
  lineNumber: number;
  owner?: string;
  removalDate?: string;
}

interface Options {
  days: number;
  type?: string;
  includeTests: boolean;
  outputFormat: 'console' | 'json' | 'csv';
  searchPath: string;
}

function parseArgs(): Options {
  const args = process.argv.slice(2);
  const options: Options = {
    days: 90,
    includeTests: false,
    outputFormat: 'console',
    searchPath: process.cwd(),
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--days':
        options.days = parseInt(args[++i], 10);
        break;
      case '--type':
        options.type = args[++i];
        break;
      case '--include-tests':
        options.includeTests = true;
        break;
      case '--format':
        options.outputFormat = args[++i] as Options['outputFormat'];
        break;
      case '--path':
        options.searchPath = args[++i];
        break;
      case '--help':
        printHelp();
        process.exit(0);
    }
  }

  return options;
}

function printHelp() {
  console.log(`
Usage: detect-stale-flags.ts [options]

Detect feature flags that haven't been modified recently.

Options:
  --days <number>        Consider flags stale after N days [default: 90]
  --type <string>        Filter by flag type: release|experiment|ops|permission
  --include-tests        Include flags only found in tests
  --format <string>      Output format: console|json|csv [default: console]
  --path <string>        Path to search [default: current directory]
  --help                 Show this help message

Examples:
  # Find release flags older than 90 days
  detect-stale-flags.ts --type release --days 90

  # Find all stale flags and output JSON
  detect-stale-flags.ts --days 120 --format json

  # Check specific directory
  detect-stale-flags.ts --path ./src --days 60
`);
}

function findFeatureFlagFiles(searchPath: string): string[] {
  const files: string[] = [];

  function walk(dir: string) {
    if (!fs.existsSync(dir)) {
      return;
    }

    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      // Skip node_modules, .git, dist, build directories
      if (entry.isDirectory()) {
        if (!['node_modules', '.git', 'dist', 'build', '.next'].includes(entry.name)) {
          walk(fullPath);
        }
        continue;
      }

      // Include TypeScript, JavaScript, and config files
      if (entry.name.match(/\.(ts|tsx|js|jsx|json)$/)) {
        files.push(fullPath);
      }
    }
  }

  walk(searchPath);
  return files;
}

function extractFlagInfo(filePath: string, content: string): FlagInfo[] {
  const flags: FlagInfo[] = [];
  const lines = content.split('\n');

  // Pattern to match flag definitions
  const flagPatterns = [
    // Enum definitions: FlagName = 'flag-name'
    /(\w+)\s*=\s*['"]([a-z-]+)['"]/g,
    // isEnabled('flag-name') or getVariant('flag-name')
    /(?:isEnabled|getVariant|hasFeature)\s*\(\s*['"]([a-z-]+)['"]/g,
    // FeatureFlag.FlagName
    /FeatureFlag\.(\w+)/g,
  ];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNumber = i + 1;

    for (const pattern of flagPatterns) {
      let match;
      while ((match = pattern.exec(line)) !== null) {
        const flagName = match[1];

        // Try to determine flag type from context
        let type: FlagInfo['type'] = 'unknown';
        let owner: string | undefined;
        let removalDate: string | undefined;

        // Look at previous lines for JSDoc comments
        for (let j = i - 1; j >= Math.max(0, i - 10); j--) {
          const prevLine = lines[j];
          if (prevLine.includes('@type') || prevLine.includes('Type:')) {
            if (prevLine.includes('release')) type = 'release';
            else if (prevLine.includes('experiment')) type = 'experiment';
            else if (prevLine.includes('ops')) type = 'ops';
            else if (prevLine.includes('permission')) type = 'permission';
          }
          if (prevLine.includes('@owner') || prevLine.includes('Owner:')) {
            const ownerMatch = prevLine.match(/[@Oo]wner:?\s*(\S+)/);
            if (ownerMatch) owner = ownerMatch[1];
          }
          if (prevLine.includes('Removal Date:') || prevLine.includes('removalDate')) {
            const dateMatch = prevLine.match(/\d{4}-\d{2}-\d{2}/);
            if (dateMatch) removalDate = dateMatch[0];
          }
        }

        flags.push({
          name: flagName,
          type,
          lastModified: new Date(),
          daysStale: 0,
          filePath,
          lineNumber,
          owner,
          removalDate,
        });
      }
    }
  }

  return flags;
}

function getLastModifiedDate(filePath: string): Date {
  try {
    // Try to get git log date first (more accurate for flag changes)
    const gitDate = execSync(
      `git log -1 --format=%ct -- "${filePath}"`,
      { encoding: 'utf-8' }
    ).trim();

    if (gitDate) {
      return new Date(parseInt(gitDate, 10) * 1000);
    }
  } catch (error) {
    // Fall back to file system date if git fails
  }

  const stats = fs.statSync(filePath);
  return stats.mtime;
}

function detectStaleFlags(options: Options): FlagInfo[] {
  console.error('Searching for feature flags...\n');

  const files = findFeatureFlagFiles(options.searchPath);
  const flagMap = new Map<string, FlagInfo>();

  for (const file of files) {
    // Skip test files unless explicitly included
    if (!options.includeTests && file.includes('.test.') || file.includes('.spec.')) {
      continue;
    }

    try {
      const content = fs.readFileSync(file, 'utf-8');
      const flags = extractFlagInfo(file, content);

      for (const flag of flags) {
        const existing = flagMap.get(flag.name);

        // Keep the most recent occurrence
        if (!existing) {
          flag.lastModified = getLastModifiedDate(file);
          flagMap.set(flag.name, flag);
        } else {
          const fileDate = getLastModifiedDate(file);
          if (fileDate > existing.lastModified) {
            flag.lastModified = fileDate;
            flagMap.set(flag.name, flag);
          }
        }
      }
    } catch (error) {
      // Skip files that can't be read
    }
  }

  // Calculate staleness
  const now = new Date();
  const staleFlags: FlagInfo[] = [];

  for (const flag of flagMap.values()) {
    const daysStale = Math.floor(
      (now.getTime() - flag.lastModified.getTime()) / (1000 * 60 * 60 * 24)
    );
    flag.daysStale = daysStale;

    // Check if flag is stale based on criteria
    const isStale = daysStale >= options.days;
    const matchesType = !options.type || flag.type === options.type;

    if (isStale && matchesType) {
      staleFlags.push(flag);
    }
  }

  return staleFlags.sort((a, b) => b.daysStale - a.daysStale);
}

function outputResults(flags: FlagInfo[], options: Options): void {
  if (flags.length === 0) {
    console.log('✅ No stale flags found!');
    return;
  }

  switch (options.outputFormat) {
    case 'json':
      console.log(JSON.stringify(flags, null, 2));
      break;

    case 'csv':
      console.log('Name,Type,Days Stale,Last Modified,Owner,Removal Date,File,Line');
      for (const flag of flags) {
        console.log(
          `${flag.name},${flag.type},${flag.daysStale},${flag.lastModified.toISOString()},${flag.owner || ''},${flag.removalDate || ''},${flag.filePath},${flag.lineNumber}`
        );
      }
      break;

    case 'console':
    default:
      console.log(`\n🚨 Found ${flags.length} stale feature flag(s)\n`);

      // Group by type
      const byType = new Map<string, FlagInfo[]>();
      for (const flag of flags) {
        const existing = byType.get(flag.type) || [];
        existing.push(flag);
        byType.set(flag.type, existing);
      }

      for (const [type, typeFlags] of byType.entries()) {
        console.log(`\n${type.toUpperCase()} FLAGS (${typeFlags.length}):`);
        console.log('─'.repeat(80));

        for (const flag of typeFlags) {
          console.log(`\n  📍 ${flag.name}`);
          console.log(`     Days stale: ${flag.daysStale}`);
          console.log(`     Last modified: ${flag.lastModified.toISOString().split('T')[0]}`);
          if (flag.owner) console.log(`     Owner: ${flag.owner}`);
          if (flag.removalDate) console.log(`     Removal date: ${flag.removalDate}`);
          console.log(`     Location: ${flag.filePath}:${flag.lineNumber}`);

          // Add recommendations
          if (flag.type === 'release' && flag.daysStale > 90) {
            console.log(`     ⚠️  RECOMMENDATION: Release flags should be removed after rollout`);
          } else if (flag.type === 'experiment' && flag.daysStale > 180) {
            console.log(`     ⚠️  RECOMMENDATION: Experiment should have concluded by now`);
          } else if (flag.removalDate) {
            const removalDate = new Date(flag.removalDate);
            const isPastDue = removalDate < new Date();
            if (isPastDue) {
              console.log(`     ❌ OVERDUE: Past removal date!`);
            }
          }
        }
      }

      console.log('\n');
      console.log('SUMMARY:');
      console.log('─'.repeat(80));
      console.log(`Total stale flags: ${flags.length}`);
      console.log(`Flags over 180 days: ${flags.filter(f => f.daysStale > 180).length}`);
      console.log(`Flags with past removal date: ${flags.filter(f => f.removalDate && new Date(f.removalDate) < new Date()).length}`);

      // Provide actionable recommendations
      console.log('\n');
      console.log('RECOMMENDED ACTIONS:');
      console.log('─'.repeat(80));

      const releaseFlags = flags.filter(f => f.type === 'release');
      if (releaseFlags.length > 0) {
        console.log(`\n1. Review ${releaseFlags.length} release flag(s):`);
        console.log('   - If at 100% rollout: Remove old code path and flag');
        console.log('   - If not at 100%: Complete rollout or remove new code path');
      }

      const experimentFlags = flags.filter(f => f.type === 'experiment');
      if (experimentFlags.length > 0) {
        console.log(`\n2. Review ${experimentFlags.length} experiment flag(s):`);
        console.log('   - If experiment concluded: Implement winning variant and remove flag');
        console.log('   - If not concluded: Complete experiment or cancel');
      }

      const overdueFlags = flags.filter(f => f.removalDate && new Date(f.removalDate) < new Date());
      if (overdueFlags.length > 0) {
        console.log(`\n3. ${overdueFlags.length} flag(s) are past their removal date - prioritize cleanup`);
      }

      console.log('\n');
      break;
  }
}

// Main execution
const options = parseArgs();
const staleFlags = detectStaleFlags(options);
outputResults(staleFlags, options);

// Exit with error code if stale flags found (useful for CI)
if (staleFlags.length > 0) {
  process.exit(1);
}
