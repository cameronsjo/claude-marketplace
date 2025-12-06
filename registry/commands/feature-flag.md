---
description: Create properly-typed feature flags with tests and lifecycle management
argument-hint: "<flag-name> [flag-type]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
disable-model-invocation: true
---

# Claude Command: Feature Flag

Create properly-typed feature flags following best practices with automatic test generation and lifecycle tracking.

## Usage

Create a release flag (default):
```
/feature-flag enable-new-checkout
```

Create a specific flag type:
```
/feature-flag enable-new-checkout release
/feature-flag enable-ab-test-variant experiment
/feature-flag enable-external-api ops
/feature-flag enable-premium-features permission
```

## What This Command Does

This command uses the feature-flags skill to generate properly-typed, tested feature flag implementations.

### Step 1: Activate feature flags skill

Invoke the skill for comprehensive feature flag guidance:
```
Use the feature-flags skill to help create a feature flag.
```

### Step 2: Gather flag information

Collect details about the feature flag:

**Required information:**
1. **Flag name** (from argument or prompt)
   - Must be positive naming (e.g., `enable_feature` not `disable_feature`)
   - Use snake_case for backend, camelCase for frontend
   - Be descriptive but concise

2. **Flag type** (from argument or prompt):
   - `release` - Short-lived (days-weeks), for incomplete features
   - `experiment` - Medium-lived (weeks-months), for A/B testing
   - `ops` - Long-lived, circuit breakers and operational controls
   - `permission` - Long-lived, access control and entitlements

3. **Description** - What does this flag control?
4. **Default value** - What should happen if flag system unavailable?
5. **Target language/framework** - TypeScript, Python, Go, etc.

### Step 3: Detect project structure

Identify where to place flag code:

**Search for existing flag patterns:**
```bash
# Find feature flag files
**/*flag*.{ts,js,py,go}
**/flags/**
**/features/**
```

**If found:**
- Add to existing flag configuration
- Follow existing patterns

**If not found:**
- Create new flag structure
- Set up configuration file

### Step 4: Generate typed flag implementation

Create properly-typed flag code:

#### TypeScript Example

**Flag definition (`src/flags/checkout.ts`):**
```typescript
import { FeatureFlag, FlagType } from './types';

export const enableNewCheckout: FeatureFlag<boolean> = {
  key: 'enable_new_checkout',
  name: 'Enable New Checkout',
  description: 'Enable the redesigned checkout flow with one-click purchase',
  type: FlagType.Release,
  defaultValue: false,

  // Lifecycle metadata
  createdAt: '2025-11-13',
  createdBy: 'cameron',
  targetRemovalDate: '2025-12-31', // 6 weeks for release flags

  // Tracking
  jiraTicket: 'SHOP-1234',
  documentation: 'docs/features/new-checkout.md',
};
```

**Type definitions (`src/flags/types.ts`):**
```typescript
export enum FlagType {
  Release = 'release',
  Experiment = 'experiment',
  Ops = 'ops',
  Permission = 'permission',
}

export interface FeatureFlag<T = boolean> {
  key: string;
  name: string;
  description: string;
  type: FlagType;
  defaultValue: T;

  // Lifecycle
  createdAt: string;
  createdBy: string;
  targetRemovalDate?: string;

  // Tracking
  jiraTicket?: string;
  documentation?: string;
}
```

**Usage helper (`src/flags/index.ts`):**
```typescript
import { enableNewCheckout } from './checkout';
import flagConfig from './config.json';

export function isNewCheckoutEnabled(userId?: string): boolean {
  return getFlagValue(enableNewCheckout, userId);
}

// Simple config-based flag evaluation
function getFlagValue<T>(flag: FeatureFlag<T>, userId?: string): T {
  const config = flagConfig[flag.key];

  // If flag not in config, use default
  if (!config) {
    return flag.defaultValue;
  }

  // Support simple boolean or user-targeted flags
  if (typeof config === 'boolean') {
    return config as T;
  }

  // User-specific overrides
  if (userId && config.users?.[userId] !== undefined) {
    return config.users[userId] as T;
  }

  // Percentage rollout (simple)
  if (config.percentage !== undefined && userId) {
    const hash = simpleHash(userId) % 100;
    return (hash < config.percentage ? true : flag.defaultValue) as T;
  }

  return config.enabled ?? flag.defaultValue;
}

// Simple hash for percentage rollouts
function simpleHash(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return Math.abs(hash);
}
```

**Config file (`src/flags/config.json`):**
```json
{
  "enable_new_checkout": {
    "enabled": false,
    "percentage": 0,
    "users": {
      "user-123": true,
      "user-456": false
    }
  }
}
```

#### Python Example

**Flag definition (`flags/checkout.py`):**
```python
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

class FlagType(Enum):
    RELEASE = "release"
    EXPERIMENT = "experiment"
    OPS = "ops"
    PERMISSION = "permission"

@dataclass
class FeatureFlag:
    key: str
    name: str
    description: str
    type: FlagType
    default_value: bool
    created_at: date
    created_by: str
    target_removal_date: Optional[date] = None
    jira_ticket: Optional[str] = None
    documentation: Optional[str] = None

enable_new_checkout = FeatureFlag(
    key="enable_new_checkout",
    name="Enable New Checkout",
    description="Enable the redesigned checkout flow with one-click purchase",
    type=FlagType.RELEASE,
    default_value=False,
    created_at=date(2025, 11, 13),
    created_by="cameron",
    target_removal_date=date(2025, 12, 31),
    jira_ticket="SHOP-1234",
    documentation="docs/features/new-checkout.md",
)
```

**Usage helper (`flags/__init__.py`):**
```python
import json
import hashlib
from pathlib import Path
from .checkout import enable_new_checkout

# Load config file
_config_path = Path(__file__).parent / "config.json"
with open(_config_path) as f:
    _flag_config = json.load(f)

def is_new_checkout_enabled(user_id: str | None = None) -> bool:
    """Check if new checkout flow is enabled."""
    return get_flag_value(enable_new_checkout, user_id)

def get_flag_value(flag, user_id: str | None = None):
    """Simple config-based flag evaluation."""
    config = _flag_config.get(flag.key)

    # If flag not in config, use default
    if not config:
        return flag.default_value

    # Support simple boolean
    if isinstance(config, bool):
        return config

    # User-specific overrides
    if user_id and config.get("users", {}).get(user_id) is not None:
        return config["users"][user_id]

    # Percentage rollout (simple)
    if "percentage" in config and user_id:
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100
        return hash_val < config["percentage"]

    return config.get("enabled", flag.default_value)
```

**Config file (`flags/config.json`):**
```json
{
  "enable_new_checkout": {
    "enabled": false,
    "percentage": 0,
    "users": {
      "user-123": true,
      "user-456": false
    }
  }
}
```

### Step 5: Generate tests

Create tests for BOTH code paths (flag on/off):

#### TypeScript Tests

**Test file (`src/flags/__tests__/checkout.test.ts`):**
```typescript
import { isNewCheckoutEnabled } from '../index';
import { enableNewCheckout } from '../checkout';

describe('enableNewCheckout flag', () => {
  it('should return false by default', () => {
    expect(enableNewCheckout.defaultValue).toBe(false);
  });

  it('should have release type', () => {
    expect(enableNewCheckout.type).toBe(FlagType.Release);
  });

  it('should have target removal date', () => {
    expect(enableNewCheckout.targetRemovalDate).toBeDefined();
  });
});

describe('checkout flow', () => {
  describe('when flag is ENABLED', () => {
    beforeEach(() => {
      mockFlagService.setValue('enable_new_checkout', true);
    });

    it('should use new checkout flow', () => {
      const result = processCheckout(cart);
      expect(result.flow).toBe('new_checkout');
    });

    it('should display one-click purchase option', () => {
      const ui = renderCheckout();
      expect(ui.hasOneClickPurchase()).toBe(true);
    });
  });

  describe('when flag is DISABLED', () => {
    beforeEach(() => {
      mockFlagService.setValue('enable_new_checkout', false);
    });

    it('should use legacy checkout flow', () => {
      const result = processCheckout(cart);
      expect(result.flow).toBe('legacy_checkout');
    });

    it('should not display one-click purchase option', () => {
      const ui = renderCheckout();
      expect(ui.hasOneClickPurchase()).toBe(false);
    });
  });
});
```

#### Python Tests

**Test file (`tests/test_checkout_flag.py`):**
```python
import pytest
from flags import enable_new_checkout, is_new_checkout_enabled
from flags.types import FlagType

def test_flag_metadata():
    """Verify flag is properly configured."""
    assert enable_new_checkout.key == "enable_new_checkout"
    assert enable_new_checkout.type == FlagType.RELEASE
    assert enable_new_checkout.default_value is False
    assert enable_new_checkout.target_removal_date is not None

class TestCheckoutFlow:
    """Test checkout flow with flag enabled/disabled."""

    @pytest.fixture
    def mock_flag_enabled(self, monkeypatch):
        """Mock flag as enabled."""
        monkeypatch.setattr("flags.client.get_flag_value", lambda f, u: True)

    @pytest.fixture
    def mock_flag_disabled(self, monkeypatch):
        """Mock flag as disabled."""
        monkeypatch.setattr("flags.client.get_flag_value", lambda f, u: False)

    def test_new_checkout_when_enabled(self, mock_flag_enabled):
        """Should use new checkout flow when flag enabled."""
        result = process_checkout(cart)
        assert result["flow"] == "new_checkout"
        assert result["features"]["one_click_purchase"] is True

    def test_legacy_checkout_when_disabled(self, mock_flag_disabled):
        """Should use legacy checkout flow when flag disabled."""
        result = process_checkout(cart)
        assert result["flow"] == "legacy_checkout"
        assert "one_click_purchase" not in result["features"]
```

### Step 6: Generate configuration

Create simple JSON/YAML config file:

#### JSON Configuration (Recommended)

**File: `flags/config.json`** or **`config/feature-flags.json`**
```json
{
  "enable_new_checkout": {
    "enabled": false,
    "description": "Enable the redesigned checkout flow with one-click purchase",
    "type": "release",
    "created": "2025-11-13",
    "created_by": "cameron",
    "target_removal": "2025-12-31",
    "jira_ticket": "SHOP-1234",

    "percentage": 0,
    "users": {}
  }
}
```

**Gradual rollout example:**
```json
{
  "enable_new_checkout": {
    "enabled": true,
    "percentage": 20,
    "users": {
      "internal-user-1": true,
      "internal-user-2": true,
      "beta-tester-1": true,
      "blocked-user": false
    }
  }
}
```

#### YAML Configuration (Alternative)

**File: `flags/config.yaml`** or **`config/feature-flags.yaml`**
```yaml
enable_new_checkout:
  enabled: false
  description: Enable the redesigned checkout flow with one-click purchase
  type: release
  created: 2025-11-13
  created_by: cameron
  target_removal: 2025-12-31
  jira_ticket: SHOP-1234

  # Rollout control
  percentage: 0
  users: {}
```

**Rollout progression:**
```yaml
# Week 1: Internal testing
enable_new_checkout:
  enabled: true
  percentage: 0  # Specific users only
  users:
    internal-user-1: true
    internal-user-2: true

# Week 2: Beta users
enable_new_checkout:
  enabled: true
  percentage: 5  # 5% of all users + specific users
  users:
    beta-tester-1: true
    beta-tester-2: true

# Week 3: Gradual rollout
enable_new_checkout:
  enabled: true
  percentage: 20  # 20% of users

# Week 4: Full rollout
enable_new_checkout:
  enabled: true
  percentage: 100  # Everyone
```

**Config features:**
- `enabled`: Master switch (boolean)
- `percentage`: Gradual rollout (0-100)
- `users`: User-specific overrides (userId: true/false)
- Metadata: description, type, dates for tracking

### Step 7: Add lifecycle documentation

Create flag lifecycle tracking:

**File: `flags/README.md` or update existing**
```markdown
# Feature Flags

## Active Flags

### Release Flags (Remove after rollout)

| Flag | Created | Target Removal | Owner | Ticket |
|------|---------|----------------|-------|--------|
| `enable_new_checkout` | 2025-11-13 | 2025-12-31 | cameron | SHOP-1234 |

### Experiment Flags (Remove after conclusion)

| Flag | Created | Target Removal | Owner | Ticket |
|------|---------|----------------|-------|--------|
| (none) | | | | |

### Ops Flags (Long-lived)

| Flag | Created | Last Reviewed | Owner | Purpose |
|------|---------|---------------|-------|---------|
| (none) | | | | |

### Permission Flags (Long-lived)

| Flag | Created | Last Reviewed | Owner | Purpose |
|------|---------|---------------|-------|---------|
| (none) | | | | |

## Flag Lifecycle

### Release Flags
- **Remove after:** 100% rollout + old code path deleted
- **Max lifetime:** 6-8 weeks
- **Review:** Weekly during rollout

### Experiment Flags
- **Remove after:** Experiment concludes + winning variant implemented
- **Max lifetime:** 3 months
- **Review:** After each experiment milestone

### Ops Flags
- **Remove after:** Never (operational controls)
- **Review:** Quarterly
- **Archive if:** Not used in 6 months

### Permission Flags
- **Remove after:** Never (product feature)
- **Review:** Annually
- **Update:** When pricing/plans change
```

### Step 8: Create usage documentation

Add inline documentation showing how to use the flag:

**Example usage docs:**
```typescript
/**
 * Example: Using the new checkout flag
 *
 * ```typescript
 * import { isNewCheckoutEnabled } from './flags';
 *
 * async function renderCheckout(userId: string) {
 *   if (isNewCheckoutEnabled(userId)) {
 *     return <NewCheckout />;
 *   }
 *   return <LegacyCheckout />;
 * }
 * ```
 *
 * Rollout plan:
 * 1. Week 1: Internal users (5%)
 * 2. Week 2: Beta users (20%)
 * 3. Week 3: All users (100%)
 *
 * Removal: After 2 weeks at 100%, delete LegacyCheckout and flag
 */
```

### Step 9: Summary and next steps

Provide summary of what was created:

```markdown
✓ Feature flag created: enable_new_checkout

Files created/modified:
- src/flags/checkout.ts (flag definition)
- src/flags/index.ts (usage helper with config loading)
- src/flags/__tests__/checkout.test.ts (tests for both paths)
- flags/config.json (simple JSON configuration)
- flags/README.md (lifecycle tracking)

Next steps:
1. Review flag configuration in config.json
2. Run tests: npm test src/flags/__tests__/checkout.test.ts
3. Implement feature code using isNewCheckoutEnabled()
4. Test both code paths (flag on/off)
5. Roll out gradually:
   - Update config.json: percentage: 5 (internal testing)
   - Update config.json: percentage: 20 (beta users)
   - Update config.json: percentage: 100 (full rollout)
6. Remove flag after 100% rollout + old code deleted

Lifecycle:
- Type: Release flag
- Target removal: 2025-12-31 (6 weeks)
- Review: Weekly during rollout

Documentation: docs/features/new-checkout.md
Ticket: SHOP-1234
```

## Flag Naming Best Practices

### ✅ Good Names (Positive)
- `enable_new_checkout`
- `show_premium_features`
- `allow_external_api`
- `use_new_algorithm`

### ❌ Bad Names (Negative)
- `disable_old_checkout` (double negative risk)
- `hide_legacy_ui` (confusing when false)
- `block_external_api` (hard to reason about)
- `skip_validation` (unsafe default)

### Why Positive Naming Matters

```typescript
// With positive naming (clear)
if (isNewCheckoutEnabled()) {
  useNewCheckout();
}

// With negative naming (confusing)
if (!isOldCheckoutDisabled()) { // double negative!
  useNewCheckout();
}
```

## Flag Types Guide

| Type | Lifetime | Purpose | Remove When |
|------|----------|---------|-------------|
| **Release** | Days-weeks | Incomplete features | 100% rollout + old code deleted |
| **Experiment** | Weeks-months | A/B testing | Experiment done + winner shipped |
| **Ops** | Permanent | Circuit breakers | Never (operational control) |
| **Permission** | Permanent | Access control | Never (product feature) |

## Testing Requirements

For EVERY flag, test BOTH paths:

**Required test coverage:**
- [ ] Flag metadata (name, type, default)
- [ ] Flag enabled path (new code)
- [ ] Flag disabled path (old code)
- [ ] Flag service unavailable (uses default)
- [ ] User-specific overrides (if applicable)

## Config File Management

### Hot Reloading (Optional)

For development, you can add file watching to reload config changes:

**TypeScript with chokidar:**
```typescript
import chokidar from 'chokidar';
import fs from 'fs';

let flagConfig = JSON.parse(fs.readFileSync('./flags/config.json', 'utf8'));

// Watch for changes in development
if (process.env.NODE_ENV === 'development') {
  chokidar.watch('./flags/config.json').on('change', () => {
    console.log('Reloading feature flags...');
    flagConfig = JSON.parse(fs.readFileSync('./flags/config.json', 'utf8'));
  });
}
```

**Python with watchdog:**
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

class FlagConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('config.json'):
            global _flag_config
            with open('flags/config.json') as f:
                _flag_config = json.load(f)
            print('Reloaded feature flags')

# In development only
if os.getenv('ENV') == 'development':
    observer = Observer()
    observer.schedule(FlagConfigHandler(), 'flags/', recursive=False)
    observer.start()
```

### Environment-Specific Configs

Use different config files per environment:

```
flags/
├── config.json          # Base config
├── config.dev.json      # Development overrides
├── config.staging.json  # Staging overrides
└── config.prod.json     # Production overrides
```

**Load with environment merging:**
```typescript
const baseConfig = require('./flags/config.json');
const envConfig = require(`./flags/config.${process.env.NODE_ENV}.json`);

const flagConfig = { ...baseConfig, ...envConfig };
```

### Version Control

**Add to `.gitignore` for local overrides:**
```gitignore
# Allow base config
flags/config.json

# Ignore local dev overrides
flags/config.local.json
```

**In code, merge local overrides:**
```typescript
let config = require('./flags/config.json');
try {
  const localOverrides = require('./flags/config.local.json');
  config = { ...config, ...localOverrides };
} catch {
  // No local overrides, use base config
}
```

---

**Last Updated:** 2025-11-13
**Best Practices Source:** Feature Flag Best Practices & Martin Fowler's Feature Toggles
