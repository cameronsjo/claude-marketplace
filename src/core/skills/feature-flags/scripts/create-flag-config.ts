#!/usr/bin/env node
/**
 * Create Feature Flag Configuration
 *
 * Generates properly validated flag configuration templates based on flag type.
 */

import * as fs from 'fs';
import * as path from 'path';

interface ConfigOptions {
  flag: string;
  type: 'release' | 'experiment' | 'ops' | 'permission';
  enabled: boolean;
  rolloutPercentage?: number;
  environments?: string[];
  allowedUsers?: string[];
  allowedOrgs?: string[];
  outputPath: string;
  format: 'typescript' | 'json' | 'yaml';
}

function parseArgs(): ConfigOptions {
  const args = process.argv.slice(2);
  const options: Partial<ConfigOptions> = {
    enabled: false,
    outputPath: process.cwd(),
    format: 'typescript',
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--flag':
        options.flag = args[++i];
        break;
      case '--type':
        options.type = args[++i] as ConfigOptions['type'];
        break;
      case '--enabled':
        options.enabled = args[++i].toLowerCase() === 'true';
        break;
      case '--rollout':
        options.rolloutPercentage = parseInt(args[++i], 10);
        break;
      case '--environments':
        options.environments = args[++i].split(',');
        break;
      case '--users':
        options.allowedUsers = args[++i].split(',');
        break;
      case '--orgs':
        options.allowedOrgs = args[++i].split(',');
        break;
      case '--output':
        options.outputPath = args[++i];
        break;
      case '--format':
        options.format = args[++i] as ConfigOptions['format'];
        break;
      case '--help':
        printHelp();
        process.exit(0);
    }
  }

  if (!options.flag || !options.type) {
    console.error('Error: --flag and --type are required');
    printHelp();
    process.exit(1);
  }

  return options as ConfigOptions;
}

function printHelp() {
  console.log(`
Usage: create-flag-config.ts [options]

Generate feature flag configuration templates.

Options:
  --flag <string>          Flag name (PascalCase) [required]
  --type <string>          Flag type: release|experiment|ops|permission [required]
  --enabled <boolean>      Initial enabled state [default: false]
  --rollout <number>       Rollout percentage (0-100) [default: based on type]
  --environments <string>  Comma-separated list of enabled environments
  --users <string>         Comma-separated list of allowed user IDs
  --orgs <string>          Comma-separated list of allowed organization IDs
  --output <string>        Output directory [default: current directory]
  --format <string>        Output format: typescript|json|yaml [default: typescript]
  --help                   Show this help message

Examples:
  # Generate release flag config
  create-flag-config.ts --flag NewCheckoutFlow --type release --rollout 0

  # Generate experiment flag with user targeting
  create-flag-config.ts --flag PricingTest --type experiment --users user1,user2

  # Generate ops flag enabled in all environments
  create-flag-config.ts --flag ExternalAPIEnabled --type ops --enabled true --environments dev,staging,prod

  # Generate JSON output
  create-flag-config.ts --flag FeatureName --type release --format json --output ./config
`);
}

function validateConfig(options: ConfigOptions): void {
  // Validate rollout percentage
  if (options.rolloutPercentage !== undefined) {
    if (options.rolloutPercentage < 0 || options.rolloutPercentage > 100) {
      console.error('Error: Rollout percentage must be between 0 and 100');
      process.exit(1);
    }
  }

  // Validate flag type
  const validTypes = ['release', 'experiment', 'ops', 'permission'];
  if (!validTypes.includes(options.type)) {
    console.error(`Error: Type must be one of: ${validTypes.join(', ')}`);
    process.exit(1);
  }
}

function getDefaultConfig(options: ConfigOptions): any {
  const baseConfig = {
    enabled: options.enabled,
    metadata: {
      type: options.type,
      createdAt: new Date().toISOString().split('T')[0],
      description: `Feature flag for ${options.flag}`,
    },
  };

  // Type-specific defaults
  switch (options.type) {
    case 'release':
      return {
        ...baseConfig,
        rolloutPercentage: options.rolloutPercentage ?? 0,
        enabledEnvironments: options.environments || ['dev', 'staging'],
        metadata: {
          ...baseConfig.metadata,
          lifecycle: 'Short-lived (days to weeks)',
          purpose: 'Gradual rollout of new feature',
          removalDate: 'TBD - Set after 100% rollout',
        },
      };

    case 'experiment':
      return {
        ...baseConfig,
        rolloutPercentage: options.rolloutPercentage ?? 50,
        enabledEnvironments: options.environments || ['staging', 'production'],
        allowedUsers: options.allowedUsers || [],
        allowedOrgs: options.allowedOrgs || [],
        metadata: {
          ...baseConfig.metadata,
          lifecycle: 'Short to medium-lived (weeks to months)',
          purpose: 'A/B testing and experimentation',
          variants: ['control', 'treatment'],
          removalDate: 'TBD - Set after experiment concludes',
        },
      };

    case 'ops':
      return {
        ...baseConfig,
        enabledEnvironments: options.environments || ['dev', 'staging', 'production'],
        metadata: {
          ...baseConfig.metadata,
          lifecycle: 'Long-lived (reviewed quarterly)',
          purpose: 'Operational control and circuit breaker',
          reviewDate: getNextQuarterlyReviewDate(),
        },
      };

    case 'permission':
      return {
        ...baseConfig,
        enabledEnvironments: options.environments || ['production'],
        allowedUsers: options.allowedUsers || [],
        allowedOrgs: options.allowedOrgs || [],
        metadata: {
          ...baseConfig.metadata,
          lifecycle: 'Long-lived (part of product offering)',
          purpose: 'Access control and entitlements',
          tier: 'TBD - Specify plan/tier requirement',
        },
      };
  }
}

function getNextQuarterlyReviewDate(): string {
  const now = new Date();
  const quarter = Math.floor(now.getMonth() / 3);
  const nextQuarterMonth = (quarter + 1) * 3;

  const reviewDate = new Date(now.getFullYear(), nextQuarterMonth, 1);
  if (nextQuarterMonth >= 12) {
    reviewDate.setFullYear(reviewDate.getFullYear() + 1);
    reviewDate.setMonth(0);
  }

  return reviewDate.toISOString().split('T')[0];
}

function generateTypeScriptConfig(options: ConfigOptions, config: any): string {
  const kebabCase = options.flag
    .replace(/([A-Z])/g, '-$1')
    .toLowerCase()
    .replace(/^-/, '');

  return `import { FeatureFlag } from './feature-flags';

/**
 * Configuration for ${options.flag} feature flag
 *
 * Type: ${options.type}
 * ${config.metadata.lifecycle}
 * ${config.metadata.purpose}
 */
export const ${options.flag}Config = {
  [FeatureFlag.${options.flag}]: ${JSON.stringify(config, null, 2)},
};

// Usage example:
// const flagService = new FeatureFlagService(config);
// if (flagService.isEnabled(FeatureFlag.${options.flag}, context)) {
//   // New code path
// } else {
//   // Legacy code path
// }
`;
}

function generateJSONConfig(options: ConfigOptions, config: any): string {
  return JSON.stringify(
    {
      [options.flag]: config,
    },
    null,
    2
  );
}

function generateYAMLConfig(options: ConfigOptions, config: any): string {
  // Simple YAML generation (no external dependencies)
  function toYAML(obj: any, indent: number = 0): string {
    const spaces = ' '.repeat(indent);
    let yaml = '';

    for (const [key, value] of Object.entries(obj)) {
      if (value === null || value === undefined) {
        yaml += `${spaces}${key}: null\n`;
      } else if (typeof value === 'object' && !Array.isArray(value)) {
        yaml += `${spaces}${key}:\n${toYAML(value, indent + 2)}`;
      } else if (Array.isArray(value)) {
        yaml += `${spaces}${key}:\n`;
        value.forEach(item => {
          yaml += `${spaces}  - ${item}\n`;
        });
      } else if (typeof value === 'string') {
        yaml += `${spaces}${key}: "${value}"\n`;
      } else {
        yaml += `${spaces}${key}: ${value}\n`;
      }
    }

    return yaml;
  }

  return `# Configuration for ${options.flag} feature flag
# Type: ${options.type}
# ${config.metadata.lifecycle}

${options.flag}:
${toYAML(config, 2)}`;
}

function generateSchema(): string {
  return `{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Feature Flag Configuration Schema",
  "type": "object",
  "patternProperties": {
    "^[A-Z][a-zA-Z0-9]*$": {
      "type": "object",
      "required": ["enabled", "metadata"],
      "properties": {
        "enabled": {
          "type": "boolean",
          "description": "Whether the flag is enabled globally"
        },
        "rolloutPercentage": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "Percentage of users who will see the feature (0-100)"
        },
        "enabledEnvironments": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": ["dev", "staging", "production"]
          },
          "description": "Environments where the flag can be enabled"
        },
        "allowedUsers": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "User IDs allowed to see the feature"
        },
        "allowedOrgs": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Organization IDs allowed to see the feature"
        },
        "metadata": {
          "type": "object",
          "required": ["type", "createdAt", "description"],
          "properties": {
            "type": {
              "type": "string",
              "enum": ["release", "experiment", "ops", "permission"]
            },
            "createdAt": {
              "type": "string",
              "format": "date"
            },
            "description": {
              "type": "string"
            },
            "lifecycle": {
              "type": "string"
            },
            "purpose": {
              "type": "string"
            },
            "removalDate": {
              "type": "string",
              "format": "date"
            },
            "reviewDate": {
              "type": "string",
              "format": "date"
            },
            "owner": {
              "type": "string"
            }
          }
        }
      }
    }
  }
}`;
}

function generateFiles(options: ConfigOptions): void {
  validateConfig(options);

  console.log('\nGenerating feature flag configuration...\n');

  const config = getDefaultConfig(options);
  const outputDir = options.outputPath;

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  let content: string;
  let filename: string;

  switch (options.format) {
    case 'json':
      content = generateJSONConfig(options, config);
      filename = `${options.flag.toLowerCase()}-flag.json`;
      break;

    case 'yaml':
      content = generateYAMLConfig(options, config);
      filename = `${options.flag.toLowerCase()}-flag.yaml`;
      break;

    case 'typescript':
    default:
      content = generateTypeScriptConfig(options, config);
      filename = `${options.flag.toLowerCase()}-flag.config.ts`;
      break;
  }

  const outputPath = path.join(outputDir, filename);
  fs.writeFileSync(outputPath, content);
  console.log(`✓ Generated configuration: ${outputPath}`);

  // Also generate schema file if it doesn't exist
  const schemaPath = path.join(outputDir, 'flag-config-schema.json');
  if (!fs.existsSync(schemaPath)) {
    fs.writeFileSync(schemaPath, generateSchema());
    console.log(`✓ Generated JSON schema: ${schemaPath}`);
  }

  console.log('\n✅ Configuration generated successfully!\n');
  console.log('Next steps:');
  console.log(`1. Review configuration in ${filename}`);
  console.log('2. Update metadata fields (description, owner, dates)');
  console.log('3. Add configuration to your feature flag service');
  console.log('4. Validate against schema if using JSON format');
  console.log('');

  // Type-specific recommendations
  if (options.type === 'release') {
    console.log('Release Flag Reminders:');
    console.log('- Set removal date after creating flag');
    console.log('- Plan rollout schedule (1% → 10% → 50% → 100%)');
    console.log('- Schedule cleanup after 100% rollout');
  } else if (options.type === 'experiment') {
    console.log('Experiment Flag Reminders:');
    console.log('- Define success metrics before enabling');
    console.log('- Set experiment duration and end date');
    console.log('- Plan for winner implementation and flag removal');
  } else if (options.type === 'ops') {
    console.log('Ops Flag Reminders:');
    console.log(`- Schedule quarterly review on ${config.metadata.reviewDate}`);
    console.log('- Document operational procedures');
    console.log('- Set up monitoring and alerts');
  } else if (options.type === 'permission') {
    console.log('Permission Flag Reminders:');
    console.log('- Define which plan/tier requires this feature');
    console.log('- Set up entitlement checking');
    console.log('- Document access control logic');
  }

  console.log('');
}

// Main execution
const options = parseArgs();
generateFiles(options);
