# Feature Flag Implementation Skill

This skill helps you implement, manage, and maintain feature flags following best practices.

## What This Skill Does

This skill provides comprehensive guidance and automation for:

1. **Flag Creation**: Generate typed flag implementations with proper naming conventions
2. **Testing**: Create test coverage for both code paths (flag on/off)
3. **Lifecycle Management**: Track flag staleness and identify removal candidates
4. **Configuration**: Generate properly validated flag configuration
5. **Best Practices**: Enforce positive naming, proper types, and clear documentation

## Feature Flag Types

### 1. Release Flags (Short-lived: days to weeks)
Enable incomplete features in production while under development.

**Usage**: Trunk-based development, dark launches, gradual rollouts

**Lifecycle**: Remove after 100% rollout and old code path deleted

### 2. Experiment Flags (Short to Medium-lived: weeks to months)
A/B testing and experimentation.

**Usage**: Compare variants for metrics and optimization

**Lifecycle**: Remove after experiment concludes and winning variant implemented

### 3. Ops Flags (Long-lived)
Circuit breakers and operational controls.

**Usage**: Kill switches, external service toggles, performance tuning

**Lifecycle**: Permanent, reviewed quarterly

### 4. Permission Flags (Long-lived)
Access control and entitlements.

**Usage**: Feature gating by plan/tier, beta access

**Lifecycle**: Permanent, part of product offering

## Naming Conventions

### Positive Evaluations (Critical!)

Always use positive naming to avoid confusing double negatives.

```typescript
// ✅ Good: Positive logic, clear intent
if (featureFlags.isEnabled('new-checkout')) { /* ... */ }
if (featureFlags.isVisible('banner')) { /* ... */ }
if (featureFlags.isActive('dark-mode')) { /* ... */ }

// ❌ Bad: Negative logic leads to confusion
if (!featureFlags.isDisabled('new-checkout')) { /* ... */ }  // Double negative
if (featureFlags.isHidden('banner')) { /* ... */ }          // Requires negation
```

**Rule**: Name flags and methods so the "true" case is the desired/enabled state.

### Clear, Descriptive Names

```typescript
// ✅ Good: Clear what it does
FeatureFlag.NewCheckoutFlow
FeatureFlag.AIAssistantEnabled
FeatureFlag.AdvancedAnalyticsVisible

// ❌ Bad: Vague or negative
FeatureFlag.Toggle1
FeatureFlag.DisableLegacyCheckout
FeatureFlag.NotV1
```

## Implementation Patterns

### 1. Typed Feature Flags (Required)

Use enums for type-safety and refactor-friendliness:

```typescript
export enum FeatureFlag {
  NewCheckout = 'new-checkout-flow',
  AIChat = 'ai-chat-assistant',
  DarkMode = 'dark-mode-ui',
}

interface FeatureFlagService {
  isEnabled(flag: FeatureFlag, context?: FlagContext): boolean;
  getVariant(flag: FeatureFlag, context?: FlagContext): string;
}
```

**Benefits**: Type-safety, autocomplete, refactor-friendly, prevents typos

### 2. Dependency Injection

Make flags injectable for testability:

```typescript
class CheckoutService {
  constructor(private featureFlags: FeatureFlagService) {}

  async processCheckout(cart: Cart): Promise<Order> {
    if (this.featureFlags.isEnabled(FeatureFlag.NewCheckout)) {
      return this.newCheckoutFlow(cart);
    }
    return this.legacyCheckoutFlow(cart);
  }
}
```

**Benefits**: Testable, mockable, clear dependencies

### 3. Configuration with Validation

Always validate flag configuration:

```typescript
interface FlagConfiguration {
  flags: {
    [key in FeatureFlag]: {
      enabled: boolean;
      rolloutPercentage?: number;
      allowedUsers?: string[];
      allowedOrgs?: string[];
      enabledEnvironments?: string[];
    };
  };
}
```

## Testing Strategy

### Test Both Paths (Critical!)

Every flag must have tests for both enabled and disabled states:

```typescript
describe('CheckoutService', () => {
  it('uses new checkout when flag enabled', async () => {
    const mockFlags = { isEnabled: () => true };
    const service = new CheckoutService(mockFlags);
    const order = await service.processCheckout(cart);
    expect(order.version).toBe('v2');
  });

  it('uses legacy checkout when flag disabled', async () => {
    const mockFlags = { isEnabled: () => false };
    const service = new CheckoutService(mockFlags);
    const order = await service.processCheckout(cart);
    expect(order.version).toBe('v1');
  });
});
```

### Integration Tests

Test both code paths in E2E tests:

```typescript
describe('Checkout flow', () => {
  describe('with new-checkout-flow enabled', () => {
    beforeEach(() => setFlag('new-checkout-flow', true));
    // tests for new path
  });

  describe('with new-checkout-flow disabled', () => {
    beforeEach(() => setFlag('new-checkout-flow', false));
    // tests for legacy path
  });
});
```

## Flag Lifecycle Management

### Creation Checklist

When creating a new flag:

- [ ] Add flag to enum/registry with clear, positive name
- [ ] Document: purpose, owner, flag type, expected removal date
- [ ] Default to `false` (disabled)
- [ ] Implement both code paths
- [ ] Add unit tests for both paths
- [ ] Add integration tests for both paths
- [ ] Add telemetry/metrics
- [ ] Add to feature flag tracking system

### Rollout Strategy

1. **Dev/Staging First**: Test in non-production environments
2. **Gradual Production Rollout**: 1% → 10% → 50% → 100%
3. **Monitor Metrics**: Track errors, performance, user behavior
4. **Rollback Plan**: Have instant disable capability

### Removal (Critical!)

Set removal date when flag is created. Stale flags are technical debt.

When removing a flag:

- [ ] Delete old code path
- [ ] Remove flag checks from codebase
- [ ] Remove flag from configuration
- [ ] Remove flag from enum/registry
- [ ] Remove tests specific to flag behavior
- [ ] Update documentation
- [ ] Deploy and verify

**Schedule**: Review all flags quarterly, mark stale flags for removal.

## Common Pitfalls

### 1. Flag Sprawl
**Problem**: Hundreds of stale flags accumulate over time
**Solution**: Regular cleanup, automated staleness detection, removal deadlines

### 2. Complex Flag Logic
```typescript
// ❌ Bad: Hard to reason about
if ((flagA && flagB) || (!flagA && flagC)) { }

// ✅ Good: Single flag with clear meaning
if (featureFlags.isEnabled(FeatureFlag.ComplexFeature)) { }
```

### 3. Flag Coupling
**Problem**: Flags depend on each other
**Solution**: Create composite flags or refactor architecture

### 4. Testing Only One Path
**Problem**: Old code path breaks when flag is enabled
**Solution**: Test both paths in CI, enforce with coverage tooling

### 5. No Telemetry
**Problem**: Cannot measure impact or usage
**Solution**: Add metrics from day one

### 6. Exposing Sensitive Flags
```typescript
// ❌ Bad: Leaks upcoming features
return res.json(allFlags);

// ✅ Good: Only return evaluated flags
const evaluatedFlags = {
  newCheckout: featureFlags.isEnabled('new-checkout', user),
};
return res.json(evaluatedFlags);
```

## Available Scripts

This skill includes automation scripts in `/scripts/`:

### generate-flag.ts
Generate complete flag implementation with tests.

```bash
npm run generate-flag -- --name NewCheckoutFlow --type release --description "New checkout experience"
```

Generates:
- Enum entry in feature flags
- Configuration template
- Unit test template covering both paths
- Integration test template

### detect-stale-flags.ts
Find flags that haven't been modified recently.

```bash
npm run detect-stale -- --days 90
```

Identifies:
- Flags unchanged for X days
- Release/experiment flags that should be removed
- Suggested removal candidates

### flag-coverage.ts
Verify test coverage for both code paths.

```bash
npm run flag-coverage
```

Reports:
- Flags missing tests for enabled state
- Flags missing tests for disabled state
- Overall coverage by flag

### create-flag-config.ts
Generate flag configuration from schema.

```bash
npm run create-flag-config -- --flag NewCheckoutFlow --type release
```

Creates validated configuration with:
- Type-appropriate defaults
- Environment settings
- Rollout percentage configuration

## Templates

### flag-template.ts
Complete TypeScript flag implementation template including:
- Enum definition
- Configuration interface
- Service implementation with DI
- Context handling

### flag-config-schema.json
JSON schema for flag configuration validation covering:
- Required fields
- Valid value ranges
- Environment constraints
- Type-specific validation

### test-template.ts
Comprehensive test template with:
- Unit tests for both paths
- Integration test structure
- Mock service setup
- Common test utilities

## Recommendations by Project Size

### Small Projects (< 10 flags)
- Simple config file with type-safe enum
- Manual toggling via environment variables
- Quarterly review for removal
- Use provided templates directly

### Medium Projects (10-50 flags)
- Feature flag library (e.g., `unleash-client`)
- CI/CD integration
- Automated staleness detection with `detect-stale-flags.ts`
- Monthly flag review meetings

### Large Projects (50+ flags)
- Dedicated feature flag service (LaunchDarkly, Statsig)
- Centralized flag management UI
- Automated rollout strategies
- Real-time telemetry and alerting
- Weekly automated staleness reports

## Observability

### Metrics to Track

- **Flag evaluation count**: How often flag is checked
- **Variant distribution**: For A/B tests, verify actual distribution
- **Feature usage by state**: User behavior with flag on vs off
- **Error rates by state**: Compare error rates between paths
- **Performance by state**: Compare latency/performance
- **Flag staleness**: Time since last configuration change

### Logging

```typescript
logger.info('Feature flag evaluated', {
  flag: FeatureFlag.NewCheckout,
  enabled: true,
  userId: user.id,
  evaluationTime: Date.now(),
});
```

### Alerting

- Alert if flag evaluation fails
- Alert if flag causes error rate spike
- Alert if flag causes performance degradation
- Alert when flags become stale (90+ days for release flags)

## Security Considerations

### Validation

Always validate flag configuration:

```typescript
const rollout = config.flags[flag].rolloutPercentage;
if (rollout < 0 || rollout > 100) {
  throw new Error(`Invalid rollout percentage: ${rollout}`);
}
```

### Audit Logging

Log changes to sensitive flags:

```typescript
auditLog.record({
  action: 'FLAG_CHANGED',
  flag: FeatureFlag.AdminPanel,
  oldValue: false,
  newValue: true,
  changedBy: user.id,
  timestamp: Date.now(),
});
```

### Client-Side Safety

Never expose all flags to client. Only send evaluated results:

```typescript
// ✅ Good: Only evaluated flags for current user
const evaluatedFlags = {
  newCheckout: featureFlags.isEnabled('new-checkout', user),
  darkMode: featureFlags.isEnabled('dark-mode', user),
};
return res.json(evaluatedFlags);
```

## Usage Examples

### Creating a New Release Flag

1. Run flag generator:
```bash
npm run generate-flag -- --name NewPaymentFlow --type release --description "Updated payment processing" --owner @yourteam --removal-date 2025-12-31
```

2. Implement both code paths:
```typescript
if (this.flags.isEnabled(FeatureFlag.NewPaymentFlow)) {
  return this.processPaymentV2(order);
}
return this.processPaymentV1(order);
```

3. Add tests for both paths using generated template

4. Deploy with flag disabled, enable gradually

5. Set calendar reminder for removal date

### Cleaning Up Stale Flags

1. Run staleness detection:
```bash
npm run detect-stale -- --days 90 --type release
```

2. Review flagged items with team

3. For each flag to remove:
   - Delete old code path
   - Remove flag from enum
   - Remove tests
   - Deploy changes

### Verifying Test Coverage

1. Run coverage check:
```bash
npm run flag-coverage
```

2. For each flag missing coverage:
   - Add tests using test template
   - Verify both paths are tested
   - Run tests to confirm

## References

- Martin Fowler: Feature Toggles (https://martinfowler.com/articles/feature-toggles.html)
- LaunchDarkly Best Practices: https://docs.launchdarkly.com/guides/best-practices
- Full documentation: ~/.claude/docs/architecture/feature-flags.md
