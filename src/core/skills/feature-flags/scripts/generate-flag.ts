#!/usr/bin/env node
/**
 * Generate Feature Flag Implementation
 *
 * Creates a complete feature flag implementation including:
 * - Enum entry
 * - Configuration template
 * - Unit tests for both paths
 * - Integration test templates
 * - Documentation
 */

import * as fs from 'fs';
import * as path from 'path';

interface FlagOptions {
  name: string;
  type: 'release' | 'experiment' | 'ops' | 'permission';
  description: string;
  owner?: string;
  removalDate?: string;
  kebabCase: string;
  outputDir: string;
}

function parseArgs(): FlagOptions {
  const args = process.argv.slice(2);
  const options: Partial<FlagOptions> = {
    type: 'release',
    outputDir: process.cwd(),
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    switch (arg) {
      case '--name':
        options.name = args[++i];
        break;
      case '--type':
        options.type = args[++i] as FlagOptions['type'];
        break;
      case '--description':
        options.description = args[++i];
        break;
      case '--owner':
        options.owner = args[++i];
        break;
      case '--removal-date':
        options.removalDate = args[++i];
        break;
      case '--output':
        options.outputDir = args[++i];
        break;
      case '--help':
        printHelp();
        process.exit(0);
    }
  }

  if (!options.name || !options.description) {
    console.error('Error: --name and --description are required');
    printHelp();
    process.exit(1);
  }

  // Convert PascalCase to kebab-case
  options.kebabCase = options.name!
    .replace(/([A-Z])/g, '-$1')
    .toLowerCase()
    .replace(/^-/, '');

  return options as FlagOptions;
}

function printHelp() {
  console.log(`
Usage: generate-flag.ts [options]

Generate a complete feature flag implementation with tests and configuration.

Options:
  --name <string>         Flag name in PascalCase (e.g., NewCheckoutFlow) [required]
  --type <string>         Flag type: release|experiment|ops|permission [default: release]
  --description <string>  Brief description of the flag [required]
  --owner <string>        Team or person responsible for the flag
  --removal-date <string> Expected removal date (YYYY-MM-DD) for release/experiment flags
  --output <string>       Output directory [default: current directory]
  --help                  Show this help message

Examples:
  # Generate a release flag
  generate-flag.ts --name NewCheckoutFlow --type release --description "New checkout experience" --owner @payments-team --removal-date 2025-12-31

  # Generate an ops flag
  generate-flag.ts --name ExternalAPIEnabled --type ops --description "Circuit breaker for external API"

  # Generate an experiment flag
  generate-flag.ts --name PricingTestVariant --type experiment --description "A/B test for pricing display" --removal-date 2025-06-30
`);
}

function generateEnumEntry(options: FlagOptions): string {
  return `
/**
 * ${options.description}
 *
 * Type: ${options.type}
 * Owner: ${options.owner || 'TBD'}
 * ${options.removalDate ? `Removal Date: ${options.removalDate}` : 'Long-lived flag'}
 */
${options.name} = '${options.kebabCase}',`;
}

function generateConfigEntry(options: FlagOptions): string {
  const baseConfig = {
    enabled: false,
    enabledEnvironments: ['dev', 'staging'],
  };

  if (options.type === 'release' || options.type === 'experiment') {
    return `
  [FeatureFlag.${options.name}]: {
    enabled: false,
    rolloutPercentage: 0,
    enabledEnvironments: ['dev', 'staging'],
    metadata: {
      type: '${options.type}',
      owner: '${options.owner || 'TBD'}',
      description: '${options.description}',
      ${options.removalDate ? `removalDate: '${options.removalDate}',` : ''}
      createdAt: '${new Date().toISOString().split('T')[0]}',
    },
  },`;
  }

  return `
  [FeatureFlag.${options.name}]: {
    enabled: false,
    enabledEnvironments: ['dev', 'staging'],
    metadata: {
      type: '${options.type}',
      owner: '${options.owner || 'TBD'}',
      description: '${options.description}',
      createdAt: '${new Date().toISOString().split('T')[0]}',
    },
  },`;
}

function generateUnitTest(options: FlagOptions): string {
  return `import { describe, it, expect, beforeEach } from '@jest/globals';
import { FeatureFlag } from '../feature-flags';
import { YourService } from '../your-service'; // Update import path

/**
 * Unit tests for ${options.name} feature flag
 *
 * ${options.description}
 */
describe('${options.name} feature flag', () => {
  let service: YourService;

  describe('when flag is enabled', () => {
    beforeEach(() => {
      const mockFlags = {
        isEnabled: (flag: FeatureFlag) => flag === FeatureFlag.${options.name},
      };
      service = new YourService(mockFlags);
    });

    it('should use new code path', async () => {
      // TODO: Add test for new behavior
      const result = await service.someMethod();

      expect(result).toBeDefined();
      // Add assertions for new behavior
    });

    it('should handle errors in new code path', async () => {
      // TODO: Add error handling test for new path
      await expect(service.someMethodWithError()).rejects.toThrow();
    });

    it('should produce expected metrics for new path', async () => {
      // TODO: Add metrics/telemetry verification
      const result = await service.someMethod();

      // Verify telemetry was recorded
      expect(mockTelemetry.recorded).toContain('${options.kebabCase}-enabled');
    });
  });

  describe('when flag is disabled', () => {
    beforeEach(() => {
      const mockFlags = {
        isEnabled: () => false,
      };
      service = new YourService(mockFlags);
    });

    it('should use legacy code path', async () => {
      // TODO: Add test for legacy behavior
      const result = await service.someMethod();

      expect(result).toBeDefined();
      // Add assertions for legacy behavior
    });

    it('should handle errors in legacy code path', async () => {
      // TODO: Add error handling test for legacy path
      await expect(service.someMethodWithError()).rejects.toThrow();
    });

    it('should maintain backward compatibility', async () => {
      // TODO: Verify legacy behavior is unchanged
      const result = await service.someMethod();

      // Verify legacy behavior
      expect(result).toMatchSnapshot();
    });
  });

  describe('flag evaluation', () => {
    it('should evaluate flag with context', () => {
      const mockFlags = {
        isEnabled: (flag: FeatureFlag, context?: any) => {
          expect(context).toBeDefined();
          expect(context.userId).toBeDefined();
          return true;
        },
      };
      service = new YourService(mockFlags);

      // TODO: Add context-aware flag evaluation test
    });

    it('should handle flag evaluation errors gracefully', () => {
      const mockFlags = {
        isEnabled: () => {
          throw new Error('Flag service unavailable');
        },
      };
      service = new YourService(mockFlags);

      // TODO: Verify graceful degradation
      expect(() => service.someMethod()).not.toThrow();
    });
  });
});
`;
}

function generateIntegrationTest(options: FlagOptions): string {
  return `import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { FeatureFlag } from '../feature-flags';
import { setupTestEnvironment, teardownTestEnvironment } from './test-helpers';

/**
 * Integration tests for ${options.name} feature flag
 *
 * ${options.description}
 *
 * These tests verify end-to-end behavior with the flag enabled and disabled.
 */
describe('${options.name} integration tests', () => {
  beforeEach(async () => {
    await setupTestEnvironment();
  });

  afterEach(async () => {
    await teardownTestEnvironment();
  });

  describe('with flag enabled', () => {
    beforeEach(() => {
      process.env.FEATURE_FLAG_${options.name.toUpperCase()} = 'true';
    });

    it('should complete full workflow with new behavior', async () => {
      // TODO: Add end-to-end test with flag enabled

      // Example:
      // const response = await request(app).get('/api/endpoint');
      // expect(response.status).toBe(200);
      // expect(response.body).toMatchObject({ version: 'v2' });
    });

    it('should maintain data consistency', async () => {
      // TODO: Verify data consistency with new code path
    });

    it('should meet performance requirements', async () => {
      // TODO: Add performance test for new path
      const startTime = Date.now();
      // await performOperation();
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(1000); // Adjust threshold
    });
  });

  describe('with flag disabled', () => {
    beforeEach(() => {
      process.env.FEATURE_FLAG_${options.name.toUpperCase()} = 'false';
    });

    it('should complete full workflow with legacy behavior', async () => {
      // TODO: Add end-to-end test with flag disabled

      // Example:
      // const response = await request(app).get('/api/endpoint');
      // expect(response.status).toBe(200);
      // expect(response.body).toMatchObject({ version: 'v1' });
    });

    it('should maintain backward compatibility', async () => {
      // TODO: Verify legacy behavior is unchanged
    });

    it('should meet performance requirements', async () => {
      // TODO: Add performance test for legacy path
      const startTime = Date.now();
      // await performOperation();
      const duration = Date.now() - startTime;

      expect(duration).toBeLessThan(1000); // Adjust threshold
    });
  });

  describe('flag rollout scenarios', () => {
    it('should handle gradual rollout (10%)', async () => {
      // TODO: Test partial rollout behavior
    });

    it('should support rollback', async () => {
      // TODO: Test that disabling flag reverts to legacy behavior
    });

    it('should work with user targeting', async () => {
      // TODO: Test user-specific flag evaluation
    });
  });
});
`;
}

function generateDocumentation(options: FlagOptions): string {
  return `# ${options.name} Feature Flag

**Type**: ${options.type}
**Status**: Draft
**Owner**: ${options.owner || 'TBD'}
**Created**: ${new Date().toISOString().split('T')[0]}
${options.removalDate ? `**Expected Removal**: ${options.removalDate}` : '**Lifecycle**: Long-lived'}

## Description

${options.description}

## Motivation

<!-- Why is this flag needed? What problem does it solve? -->

TODO: Add motivation

## Implementation

### Flag Definition

\`\`\`typescript
enum FeatureFlag {
  ${options.name} = '${options.kebabCase}',
}
\`\`\`

### Configuration

\`\`\`typescript
{
  [FeatureFlag.${options.name}]: {
    enabled: false,
    rolloutPercentage: 0,
    enabledEnvironments: ['dev', 'staging'],
  }
}
\`\`\`

## Rollout Plan

${options.type === 'release' || options.type === 'experiment' ? `
### Phase 1: Development (Week 1)
- [ ] Implement both code paths
- [ ] Add unit tests for both paths
- [ ] Add integration tests
- [ ] Enable in dev environment
- [ ] Manual testing

### Phase 2: Staging (Week 2)
- [ ] Enable in staging
- [ ] QA testing
- [ ] Performance testing
- [ ] Security review

### Phase 3: Production Rollout (Weeks 3-4)
- [ ] Deploy with flag disabled
- [ ] Enable for 1% of users
- [ ] Monitor metrics for 24 hours
- [ ] Increase to 10%
- [ ] Monitor metrics for 48 hours
- [ ] Increase to 50%
- [ ] Monitor metrics for 72 hours
- [ ] Increase to 100%

### Phase 4: Cleanup (Week 5)
- [ ] Verify 100% rollout stable
- [ ] Remove legacy code path
- [ ] Remove flag checks
- [ ] Remove flag from configuration
- [ ] Update documentation
` : `
### Deployment
- [ ] Implement feature
- [ ] Add tests
- [ ] Enable in dev/staging
- [ ] Deploy to production (disabled)
- [ ] Enable as needed for operations

### Maintenance
- [ ] Quarterly review
- [ ] Update documentation
- [ ] Monitor usage
`}

## Metrics to Monitor

- [ ] Error rate comparison (flag on vs off)
- [ ] Performance comparison (latency p50, p95, p99)
- [ ] User engagement metrics
- [ ] Conversion metrics (if applicable)
- [ ] Resource utilization

## Rollback Plan

If issues are detected:

1. **Immediate**: Disable flag via configuration (no deployment needed)
2. **Short-term**: Reduce rollout percentage
3. **Long-term**: Fix issues and restart rollout

## Testing Strategy

### Unit Tests
- [x] Tests for flag enabled
- [x] Tests for flag disabled
- [x] Error handling in both paths
- [x] Context-aware evaluation

### Integration Tests
- [x] E2E with flag enabled
- [x] E2E with flag disabled
- [x] Performance tests for both paths
- [x] Data consistency verification

## Security Considerations

<!-- Any security implications of this flag? -->

TODO: Document security considerations

## Dependencies

<!-- What other systems/flags/features does this depend on? -->

TODO: Document dependencies

## Success Criteria

<!-- How do we measure success? When can we remove this flag? -->

${options.type === 'release' || options.type === 'experiment' ? `
- [ ] New code path has < X% error rate
- [ ] Performance is within Y% of legacy
- [ ] User metrics show Z% improvement
- [ ] 100% rollout stable for 2 weeks
- [ ] Legacy code path removed
- [ ] Flag removed from codebase
` : `
- [ ] Flag provides operational value
- [ ] Usage is documented and understood
- [ ] Quarterly review shows continued need
`}

## References

- Ticket/Issue: <!-- Link to ticket -->
- Design Doc: <!-- Link to design doc -->
- Related Flags: <!-- Links to related flags -->

## Changelog

- ${new Date().toISOString().split('T')[0]}: Flag created
`;
}

function generateFiles(options: FlagOptions): void {
  const outputDir = options.outputDir;

  console.log('\nGenerating feature flag implementation...\n');

  // Create output structure
  const dirs = [
    path.join(outputDir, 'feature-flags'),
    path.join(outputDir, 'tests/unit/feature-flags'),
    path.join(outputDir, 'tests/integration/feature-flags'),
    path.join(outputDir, 'docs/feature-flags'),
  ];

  dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });

  // Generate enum entry
  const enumFile = path.join(outputDir, 'feature-flags', `${options.name}-enum.ts`);
  fs.writeFileSync(enumFile, generateEnumEntry(options));
  console.log(`✓ Generated enum entry: ${enumFile}`);

  // Generate config entry
  const configFile = path.join(outputDir, 'feature-flags', `${options.name}-config.ts`);
  fs.writeFileSync(configFile, generateConfigEntry(options));
  console.log(`✓ Generated config entry: ${configFile}`);

  // Generate unit tests
  const unitTestFile = path.join(outputDir, 'tests/unit/feature-flags', `${options.kebabCase}.test.ts`);
  fs.writeFileSync(unitTestFile, generateUnitTest(options));
  console.log(`✓ Generated unit tests: ${unitTestFile}`);

  // Generate integration tests
  const integrationTestFile = path.join(outputDir, 'tests/integration/feature-flags', `${options.kebabCase}.test.ts`);
  fs.writeFileSync(integrationTestFile, generateIntegrationTest(options));
  console.log(`✓ Generated integration tests: ${integrationTestFile}`);

  // Generate documentation
  const docFile = path.join(outputDir, 'docs/feature-flags', `${options.kebabCase}.md`);
  fs.writeFileSync(docFile, generateDocumentation(options));
  console.log(`✓ Generated documentation: ${docFile}`);

  console.log('\n✅ Feature flag implementation generated successfully!\n');
  console.log('Next steps:');
  console.log('1. Add enum entry to your main feature-flags.ts file');
  console.log('2. Add config entry to your flag configuration');
  console.log('3. Implement both code paths');
  console.log('4. Complete TODO items in generated tests');
  console.log('5. Complete documentation in generated docs');
  console.log('6. Run tests to verify both paths work');
  if (options.removalDate) {
    console.log(`7. Set calendar reminder for removal on ${options.removalDate}`);
  }
  console.log('');
}

// Main execution
const options = parseArgs();
generateFiles(options);
