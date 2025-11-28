#!/usr/bin/env node
/**
 * Feature Flag Test Coverage Analyzer
 *
 * Verifies that both code paths (flag enabled and disabled) have test coverage.
 * Critical for ensuring safe rollouts and rollbacks.
 */

import * as fs from 'fs';
import * as path from 'path';

interface FlagCoverage {
  flagName: string;
  hasEnabledTests: boolean;
  hasDisabledTests: boolean;
  enabledTestFiles: string[];
  disabledTestFiles: string[];
  implementationFiles: string[];
  hasBothPaths: boolean;
}

interface Options {
  searchPath: string;
  outputFormat: 'console' | 'json' | 'summary';
  failOnMissing: boolean;
  minCoveragePercent: number;
}

function parseArgs(): Options {
  const args = process.argv.slice(2);
  const options: Options = {
    searchPath: process.cwd(),
    outputFormat: 'console',
    failOnMissing: false,
    minCoveragePercent: 100,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--path':
        options.searchPath = args[++i];
        break;
      case '--format':
        options.outputFormat = args[++i] as Options['outputFormat'];
        break;
      case '--fail-on-missing':
        options.failOnMissing = true;
        break;
      case '--min-coverage':
        options.minCoveragePercent = parseInt(args[++i], 10);
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
Usage: flag-coverage.ts [options]

Check test coverage for feature flag code paths (both enabled and disabled).

Options:
  --path <string>          Path to search [default: current directory]
  --format <string>        Output format: console|json|summary [default: console]
  --fail-on-missing        Exit with error code if any flags lack coverage
  --min-coverage <number>  Minimum coverage percentage required [default: 100]
  --help                   Show this help message

Examples:
  # Check coverage in current directory
  flag-coverage.ts

  # Check specific directory and fail in CI if incomplete
  flag-coverage.ts --path ./src --fail-on-missing

  # Get JSON output for reporting
  flag-coverage.ts --format json

  # Require at least 80% coverage
  flag-coverage.ts --min-coverage 80
`);
}

function findFiles(searchPath: string, extensions: string[]): string[] {
  const files: string[] = [];

  function walk(dir: string) {
    if (!fs.existsSync(dir)) {
      return;
    }

    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      if (entry.isDirectory()) {
        if (!['node_modules', '.git', 'dist', 'build', '.next'].includes(entry.name)) {
          walk(fullPath);
        }
        continue;
      }

      if (extensions.some(ext => entry.name.endsWith(ext))) {
        files.push(fullPath);
      }
    }
  }

  walk(searchPath);
  return files;
}

function extractFlags(content: string): Set<string> {
  const flags = new Set<string>();

  // Pattern to match flag definitions and usage
  const patterns = [
    /FeatureFlag\.(\w+)/g,
    /isEnabled\s*\(\s*['"]([a-z-]+)['"]/g,
    /getVariant\s*\(\s*['"]([a-z-]+)['"]/g,
    /hasFeature\s*\(\s*['"]([a-z-]+)['"]/g,
    /(\w+)\s*=\s*['"]([a-z-]+)['"]/g,
  ];

  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(content)) !== null) {
      flags.add(match[1]);
    }
  }

  return flags;
}

function analyzeTestFile(filePath: string, content: string): {
  flags: Set<string>;
  enabledFlags: Set<string>;
  disabledFlags: Set<string>;
} {
  const flags = extractFlags(content);
  const enabledFlags = new Set<string>();
  const disabledFlags = new Set<string>();

  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Look for test contexts that enable/disable flags
    const enabledContexts = [
      /when.*flag.*enabled/i,
      /with.*flag.*enabled/i,
      /flag.*enabled/i,
      /isEnabled.*true/i,
      /enabled:\s*true/i,
    ];

    const disabledContexts = [
      /when.*flag.*disabled/i,
      /with.*flag.*disabled/i,
      /flag.*disabled/i,
      /isEnabled.*false/i,
      /enabled:\s*false/i,
    ];

    // Check if this is an enabled test context
    if (enabledContexts.some(pattern => pattern.test(line))) {
      // Look for flag references in nearby lines
      for (let j = Math.max(0, i - 5); j < Math.min(lines.length, i + 20); j++) {
        const nearbyLine = lines[j];
        const nearbyFlags = extractFlags(nearbyLine);
        nearbyFlags.forEach(flag => enabledFlags.add(flag));
      }
    }

    // Check if this is a disabled test context
    if (disabledContexts.some(pattern => pattern.test(line))) {
      // Look for flag references in nearby lines
      for (let j = Math.max(0, i - 5); j < Math.min(lines.length, i + 20); j++) {
        const nearbyLine = lines[j];
        const nearbyFlags = extractFlags(nearbyLine);
        nearbyFlags.forEach(flag => disabledFlags.add(flag));
      }
    }
  }

  return { flags, enabledFlags, disabledFlags };
}

function analyzeImplementationFile(filePath: string, content: string): {
  flags: Set<string>;
  hasBothPaths: Map<string, boolean>;
} {
  const flags = extractFlags(content);
  const hasBothPaths = new Map<string, boolean>();

  // For each flag, check if there's if/else handling
  for (const flag of flags) {
    const flagPattern = new RegExp(`if.*${flag}|isEnabled.*${flag}`, 'i');
    const lines = content.split('\n');

    let foundIf = false;
    let foundElse = false;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      if (flagPattern.test(line)) {
        foundIf = true;

        // Look for else within next 50 lines
        for (let j = i + 1; j < Math.min(lines.length, i + 50); j++) {
          if (lines[j].match(/^\s*}?\s*else/)) {
            foundElse = true;
            break;
          }
        }
      }
    }

    hasBothPaths.set(flag, foundIf && foundElse);
  }

  return { flags, hasBothPaths };
}

function analyzeCoverage(options: Options): FlagCoverage[] {
  console.error('Analyzing feature flag test coverage...\n');

  const testFiles = findFiles(options.searchPath, ['.test.ts', '.test.js', '.spec.ts', '.spec.js']);
  const sourceFiles = findFiles(options.searchPath, ['.ts', '.js', '.tsx', '.jsx'])
    .filter(f => !f.includes('.test.') && !f.includes('.spec.'));

  // Map flags to their coverage
  const flagCoverageMap = new Map<string, FlagCoverage>();

  // Analyze test files
  for (const testFile of testFiles) {
    try {
      const content = fs.readFileSync(testFile, 'utf-8');
      const { flags, enabledFlags, disabledFlags } = analyzeTestFile(testFile, content);

      for (const flag of flags) {
        let coverage = flagCoverageMap.get(flag);
        if (!coverage) {
          coverage = {
            flagName: flag,
            hasEnabledTests: false,
            hasDisabledTests: false,
            enabledTestFiles: [],
            disabledTestFiles: [],
            implementationFiles: [],
            hasBothPaths: false,
          };
          flagCoverageMap.set(flag, coverage);
        }

        if (enabledFlags.has(flag)) {
          coverage.hasEnabledTests = true;
          coverage.enabledTestFiles.push(testFile);
        }

        if (disabledFlags.has(flag)) {
          coverage.hasDisabledTests = true;
          coverage.disabledTestFiles.push(testFile);
        }
      }
    } catch (error) {
      // Skip files that can't be read
    }
  }

  // Analyze implementation files
  for (const sourceFile of sourceFiles) {
    try {
      const content = fs.readFileSync(sourceFile, 'utf-8');
      const { flags, hasBothPaths } = analyzeImplementationFile(sourceFile, content);

      for (const flag of flags) {
        let coverage = flagCoverageMap.get(flag);
        if (!coverage) {
          coverage = {
            flagName: flag,
            hasEnabledTests: false,
            hasDisabledTests: false,
            enabledTestFiles: [],
            disabledTestFiles: [],
            implementationFiles: [],
            hasBothPaths: false,
          };
          flagCoverageMap.set(flag, coverage);
        }

        coverage.implementationFiles.push(sourceFile);
        coverage.hasBothPaths = coverage.hasBothPaths || (hasBothPaths.get(flag) || false);
      }
    } catch (error) {
      // Skip files that can't be read
    }
  }

  return Array.from(flagCoverageMap.values()).sort((a, b) =>
    a.flagName.localeCompare(b.flagName)
  );
}

function outputResults(coverage: FlagCoverage[], options: Options): void {
  if (coverage.length === 0) {
    console.log('ℹ️  No feature flags found.');
    return;
  }

  const fullyTested = coverage.filter(c => c.hasEnabledTests && c.hasDisabledTests);
  const partiallyTested = coverage.filter(c =>
    (c.hasEnabledTests || c.hasDisabledTests) && !(c.hasEnabledTests && c.hasDisabledTests)
  );
  const untested = coverage.filter(c => !c.hasEnabledTests && !c.hasDisabledTests);
  const missingBothPaths = coverage.filter(c => c.implementationFiles.length > 0 && !c.hasBothPaths);

  const coveragePercent = Math.round((fullyTested.length / coverage.length) * 100);

  switch (options.outputFormat) {
    case 'json':
      console.log(JSON.stringify({
        total: coverage.length,
        fullyTested: fullyTested.length,
        partiallyTested: partiallyTested.length,
        untested: untested.length,
        coveragePercent,
        flags: coverage,
      }, null, 2));
      break;

    case 'summary':
      console.log(`Total flags: ${coverage.length}`);
      console.log(`Fully tested: ${fullyTested.length}`);
      console.log(`Partially tested: ${partiallyTested.length}`);
      console.log(`Untested: ${untested.length}`);
      console.log(`Coverage: ${coveragePercent}%`);
      break;

    case 'console':
    default:
      console.log('FEATURE FLAG TEST COVERAGE REPORT');
      console.log('═'.repeat(80));
      console.log(`\nTotal flags found: ${coverage.length}`);
      console.log(`Coverage: ${coveragePercent}% (${fullyTested.length}/${coverage.length} fully tested)\n`);

      if (fullyTested.length > 0) {
        console.log('✅ FULLY TESTED FLAGS:');
        console.log('─'.repeat(80));
        for (const flag of fullyTested) {
          console.log(`  ${flag.flagName}`);
          console.log(`    Implementation: ${flag.hasBothPaths ? '✓' : '⚠️'} Both paths implemented`);
          console.log(`    Enabled tests: ${flag.enabledTestFiles.length} file(s)`);
          console.log(`    Disabled tests: ${flag.disabledTestFiles.length} file(s)`);
        }
        console.log('');
      }

      if (partiallyTested.length > 0) {
        console.log('⚠️  PARTIALLY TESTED FLAGS:');
        console.log('─'.repeat(80));
        for (const flag of partiallyTested) {
          console.log(`  ${flag.flagName}`);
          if (!flag.hasEnabledTests) {
            console.log(`    ❌ Missing tests for ENABLED state`);
          }
          if (!flag.hasDisabledTests) {
            console.log(`    ❌ Missing tests for DISABLED state`);
          }
          if (flag.implementationFiles.length > 0) {
            console.log(`    Implementation: ${flag.hasBothPaths ? '✓' : '⚠️'} Both paths ${flag.hasBothPaths ? '' : 'not '}implemented`);
          }
        }
        console.log('');
      }

      if (untested.length > 0) {
        console.log('❌ UNTESTED FLAGS:');
        console.log('─'.repeat(80));
        for (const flag of untested) {
          console.log(`  ${flag.flagName}`);
          console.log(`    ❌ No tests found for either state`);
          if (flag.implementationFiles.length > 0) {
            console.log(`    Used in: ${flag.implementationFiles.slice(0, 3).join(', ')}`);
          }
        }
        console.log('');
      }

      if (missingBothPaths.length > 0) {
        console.log('⚠️  FLAGS WITH SINGLE CODE PATH:');
        console.log('─'.repeat(80));
        console.log('These flags may not have both enabled/disabled paths implemented:\n');
        for (const flag of missingBothPaths) {
          console.log(`  ${flag.flagName}`);
          console.log(`    Files: ${flag.implementationFiles.slice(0, 2).join(', ')}`);
        }
        console.log('');
      }

      console.log('RECOMMENDATIONS:');
      console.log('─'.repeat(80));

      if (untested.length > 0) {
        console.log(`\n1. Add tests for ${untested.length} untested flag(s):`);
        console.log('   - Create unit tests with flag enabled');
        console.log('   - Create unit tests with flag disabled');
        console.log('   - Add integration tests for both paths');
      }

      if (partiallyTested.length > 0) {
        console.log(`\n2. Complete coverage for ${partiallyTested.length} partially tested flag(s):`);
        console.log('   - Add missing enabled or disabled tests');
        console.log('   - Ensure both code paths are exercised');
      }

      if (missingBothPaths.length > 0) {
        console.log(`\n3. Review ${missingBothPaths.length} flag(s) with single code path:`);
        console.log('   - Verify both enabled and disabled paths exist');
        console.log('   - Consider if flag is actually being used');
      }

      if (coveragePercent < 100) {
        console.log(`\n4. Current coverage is ${coveragePercent}%. Aim for 100% to ensure:`);
        console.log('   - Safe rollouts (enabled path works)');
        console.log('   - Safe rollbacks (disabled path still works)');
        console.log('   - No breaking changes when removing flags');
      }

      console.log('\n');
      break;
  }

  // Exit with error if requested and coverage is insufficient
  if (options.failOnMissing && (untested.length > 0 || partiallyTested.length > 0)) {
    console.error('❌ Test coverage incomplete. Some flags lack tests for both paths.\n');
    process.exit(1);
  }

  if (coveragePercent < options.minCoveragePercent) {
    console.error(`❌ Coverage ${coveragePercent}% is below required ${options.minCoveragePercent}%\n`);
    process.exit(1);
  }
}

// Main execution
const options = parseArgs();
const coverage = analyzeCoverage(options);
outputResults(coverage, options);
