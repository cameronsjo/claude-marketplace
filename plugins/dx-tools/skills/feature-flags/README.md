# Feature Flags Skill

A comprehensive skill for implementing and managing feature flags following best practices.

## Overview

This skill provides guidance, templates, and automation tools for implementing feature flags in your applications. It covers the complete lifecycle from creation to removal, with emphasis on:

- Typed implementations with proper naming conventions
- Test coverage for both code paths
- Automated staleness detection
- Configuration validation
- Lifecycle management

## Quick Start

### 1. Generate a New Flag

```bash
npm run generate-flag -- \
  --name NewCheckoutFlow \
  --type release \
  --description "New checkout experience" \
  --owner @payments-team \
  --removal-date 2025-12-31
```

This generates:
- Enum entry for type-safe flag reference
- Configuration template
- Unit tests for both paths (enabled/disabled)
- Integration test templates
- Documentation

### 2. Create Flag Configuration

```bash
npm run create-flag-config -- \
  --flag NewCheckoutFlow \
  --type release \
  --rollout 0 \
  --environments dev,staging
```

Generates validated configuration with type-appropriate defaults.

### 3. Check Test Coverage

```bash
npm run flag-coverage
```

Reports:
- Flags fully tested (both paths)
- Flags partially tested (missing one path)
- Flags with no tests
- Coverage percentage

### 4. Detect Stale Flags

```bash
npm run detect-stale -- --days 90 --type release
```

Finds:
- Flags unchanged for 90+ days
- Flags past their removal date
- Recommendations for cleanup

## File Structure

```
feature-flags/
├── skill.md                           # Complete skill documentation
├── package.json                       # NPM scripts for automation
├── README.md                          # This file
├── scripts/
│   ├── generate-flag.ts               # Generate flag boilerplate
│   ├── detect-stale-flags.ts          # Find stale flags
│   ├── flag-coverage.ts               # Check test coverage
│   └── create-flag-config.ts          # Create flag configuration
└── resources/
    ├── flag-template.ts               # Complete TypeScript implementation
    ├── flag-config-schema.json        # JSON schema for validation
    └── test-template.ts               # Comprehensive test template
```

## Feature Flag Types

### Release Flags (Short-lived: days to weeks)
Enable incomplete features in production. Remove after 100% rollout.

**Use for**: Trunk-based development, dark launches, gradual rollouts

### Experiment Flags (Short-medium lived: weeks to months)
A/B testing and experimentation. Remove after experiment concludes.

**Use for**: Testing variants, optimization experiments

### Ops Flags (Long-lived)
Circuit breakers and operational controls. Reviewed quarterly.

**Use for**: Kill switches, external service toggles

### Permission Flags (Long-lived)
Access control and entitlements. Part of product offering.

**Use for**: Feature gating by plan/tier, beta access

## Best Practices

### Naming Conventions

Always use positive naming to avoid confusing double negatives:

```typescript
// ✅ Good: Positive logic
if (featureFlags.isEnabled('new-checkout')) { }

// ❌ Bad: Negative logic
if (!featureFlags.isDisabled('new-checkout')) { }
```

### Test Both Paths

Every flag must have tests for both enabled and disabled states:

```typescript
describe('CheckoutService', () => {
  it('uses new checkout when flag enabled', () => {
    // Test new path
  });

  it('uses legacy checkout when flag disabled', () => {
    // Test legacy path
  });
});
```

### Set Removal Dates

For release and experiment flags, always set a removal date:

```typescript
metadata: {
  type: 'release',
  removalDate: '2025-12-31',
  // Set calendar reminder
}
```

### Implement Both Code Paths

Always implement both enabled and disabled behavior:

```typescript
if (featureFlags.isEnabled(FeatureFlag.NewCheckout)) {
  return this.newCheckoutFlow(cart);  // New path
}
return this.legacyCheckoutFlow(cart);  // Legacy path
```

## Automation Scripts

### generate-flag.ts

Generate complete flag implementation with tests.

**Options**:
- `--name` - Flag name in PascalCase (required)
- `--type` - release|experiment|ops|permission (required)
- `--description` - Brief description (required)
- `--owner` - Team/person responsible
- `--removal-date` - Expected removal date (YYYY-MM-DD)
- `--output` - Output directory

**Example**:
```bash
npm run generate-flag -- \
  --name AIAssistant \
  --type release \
  --description "AI-powered chat assistant" \
  --owner @ai-team \
  --removal-date 2025-11-30
```

### detect-stale-flags.ts

Find flags that haven't been modified recently.

**Options**:
- `--days` - Consider stale after N days (default: 90)
- `--type` - Filter by type
- `--include-tests` - Include flags only in tests
- `--format` - console|json|csv

**Example**:
```bash
npm run detect-stale -- --days 90 --type release --format console
```

### flag-coverage.ts

Verify test coverage for both code paths.

**Options**:
- `--path` - Path to search
- `--format` - console|json|summary
- `--fail-on-missing` - Exit with error if incomplete
- `--min-coverage` - Minimum coverage percentage (default: 100)

**Example**:
```bash
npm run flag-coverage -- --fail-on-missing --min-coverage 100
```

### create-flag-config.ts

Generate flag configuration from schema.

**Options**:
- `--flag` - Flag name (required)
- `--type` - release|experiment|ops|permission (required)
- `--enabled` - Initial state (default: false)
- `--rollout` - Rollout percentage (0-100)
- `--environments` - Comma-separated list
- `--users` - Comma-separated user IDs
- `--orgs` - Comma-separated org IDs
- `--format` - typescript|json|yaml

**Example**:
```bash
npm run create-flag-config -- \
  --flag NewFeature \
  --type release \
  --rollout 10 \
  --environments dev,staging,production
```

## Resources

### flag-template.ts

Complete TypeScript implementation including:
- Enum definitions with JSDoc comments
- Configuration interfaces
- Simple implementation with validation
- Mock service for testing
- Usage examples

### flag-config-schema.json

JSON schema for validating flag configurations:
- Required fields by flag type
- Valid value ranges
- Environment constraints
- Type-specific validation rules

### test-template.ts

Comprehensive test template with:
- Unit tests for both paths
- Integration test structure
- Flag evaluation tests
- Comparison tests
- Test utilities and helpers

## Common Pitfalls

### 1. Flag Sprawl
**Problem**: Hundreds of stale flags accumulate
**Solution**: Regular cleanup, automated staleness detection

### 2. Complex Flag Logic
**Problem**: Hard to reason about nested flag conditions
**Solution**: Single flags with clear meaning

### 3. Testing Only One Path
**Problem**: Old code path breaks when flag enabled
**Solution**: Test both paths in CI

### 4. No Telemetry
**Problem**: Cannot measure impact
**Solution**: Add metrics from day one

### 5. Exposing Sensitive Flags
**Problem**: Leaking upcoming features to clients
**Solution**: Only return evaluated flags, not all configurations

## Integration with CI/CD

Add to your CI pipeline:

```yaml
# .github/workflows/ci.yml (or equivalent)
steps:
  - name: Check feature flag test coverage
    run: npm run flag-coverage -- --fail-on-missing --min-coverage 100

  - name: Detect stale flags
    run: npm run detect-stale -- --days 90 --type release
    continue-on-error: true  # Warning only
```

## Project Size Recommendations

### Small Projects (< 10 flags)
- Use provided templates directly
- Simple config file with type-safe enum
- Manual toggling via environment variables
- Quarterly review for removal

### Medium Projects (10-50 flags)
- Feature flag library (e.g., unleash-client)
- CI/CD integration with automation scripts
- Automated staleness detection
- Monthly flag review meetings

### Large Projects (50+ flags)
- Dedicated service (LaunchDarkly, Statsig, ConfigCat)
- Centralized management UI
- Automated rollout strategies
- Real-time telemetry and alerting
- Weekly automated staleness reports

## References

- **Skill Documentation**: `skill.md` - Complete implementation guide
- **Source Material**: `~/.claude/docs/architecture/feature-flags.md`
- **Martin Fowler**: [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html)
- **LaunchDarkly**: [Best Practices](https://docs.launchdarkly.com/guides/best-practices)

## Setup

To use the automation scripts:

```bash
cd ~/.claude/skills/feature-flags
npm install
```

Then run scripts as documented above.

## License

MIT
