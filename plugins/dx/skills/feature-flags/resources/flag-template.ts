/**
 * Feature Flag Implementation Template
 *
 * This template provides a complete, production-ready feature flag system
 * following best practices including:
 * - Typed flags with enums
 * - Dependency injection
 * - Context-aware evaluation
 * - Validation and error handling
 */

// ============================================================================
// Flag Definitions
// ============================================================================

/**
 * Feature flag enumeration
 *
 * Use positive naming: isEnabled, isVisible, isActive
 * Avoid negative naming: isDisabled, isHidden, isInactive
 */
export enum FeatureFlag {
  /**
   * Example: New checkout flow
   *
   * Type: Release flag
   * Owner: @payments-team
   * Removal Date: 2025-12-31
   */
  NewCheckoutFlow = 'new-checkout-flow',

  /**
   * Example: AI chat assistant
   *
   * Type: Release flag
   * Owner: @ai-team
   * Removal Date: 2025-11-30
   */
  AIAssistant = 'ai-assistant',

  /**
   * Example: External API circuit breaker
   *
   * Type: Ops flag
   * Owner: @platform-team
   * Long-lived: Reviewed quarterly
   */
  ExternalAPIEnabled = 'external-api-enabled',

  /**
   * Example: Advanced analytics for premium users
   *
   * Type: Permission flag
   * Owner: @analytics-team
   * Long-lived: Part of product offering
   */
  AdvancedAnalytics = 'advanced-analytics',
}

// ============================================================================
// Context and Configuration
// ============================================================================

/**
 * Context for flag evaluation
 *
 * Extend with additional fields as needed for targeting
 */
export interface FlagContext {
  userId?: string;
  orgId?: string;
  email?: string;
  environment?: 'dev' | 'staging' | 'production';
  customAttributes?: Record<string, any>;
}

/**
 * Configuration for a single flag
 */
export interface FlagConfiguration {
  enabled: boolean;
  rolloutPercentage?: number;
  enabledEnvironments?: string[];
  allowedUsers?: string[];
  allowedOrgs?: string[];
  metadata?: {
    type: 'release' | 'experiment' | 'ops' | 'permission';
    owner?: string;
    description?: string;
    createdAt?: string;
    removalDate?: string;
  };
}

/**
 * Complete flag configuration
 */
export type FlagsConfig = {
  [key in FeatureFlag]: FlagConfiguration;
};

// ============================================================================
// Service Interface
// ============================================================================

/**
 * Feature flag service interface
 *
 * Implement this interface for your specific flag provider
 * (LaunchDarkly, Unleash, ConfigCat, custom implementation, etc.)
 */
export interface FeatureFlagService {
  /**
   * Check if a feature flag is enabled
   *
   * @param flag - The feature flag to check
   * @param context - Optional context for evaluation
   * @returns True if flag is enabled, false otherwise
   */
  isEnabled(flag: FeatureFlag, context?: FlagContext): boolean;

  /**
   * Get the variant for an experiment flag
   *
   * @param flag - The feature flag to check
   * @param context - Optional context for evaluation
   * @returns Variant name (e.g., 'control', 'treatment', 'variant-a')
   */
  getVariant(flag: FeatureFlag, context?: FlagContext): string;

  /**
   * Get all evaluated flags for the current context
   *
   * Use this for client-side apps to send evaluated flags to the browser
   * NEVER expose all flag configurations to the client
   *
   * @param context - Context for evaluation
   * @returns Record of flag names to boolean values
   */
  getEvaluatedFlags(context: FlagContext): Record<string, boolean>;
}

// ============================================================================
// Simple Implementation
// ============================================================================

/**
 * Simple in-memory feature flag service
 *
 * Use this for development, testing, or small projects
 * For production, consider using a dedicated service (LaunchDarkly, Unleash, etc.)
 */
export class SimpleFeatureFlagService implements FeatureFlagService {
  constructor(private config: FlagsConfig) {
    this.validateConfig();
  }

  private validateConfig(): void {
    for (const [flag, config] of Object.entries(this.config)) {
      // Validate rollout percentage
      if (config.rolloutPercentage !== undefined) {
        if (config.rolloutPercentage < 0 || config.rolloutPercentage > 100) {
          throw new Error(
            `Invalid rollout percentage for ${flag}: ${config.rolloutPercentage}. Must be 0-100.`
          );
        }
      }

      // Validate enabled environments
      if (config.enabledEnvironments) {
        const validEnvs = ['dev', 'staging', 'production'];
        for (const env of config.enabledEnvironments) {
          if (!validEnvs.includes(env)) {
            throw new Error(
              `Invalid environment for ${flag}: ${env}. Must be one of: ${validEnvs.join(', ')}`
            );
          }
        }
      }
    }
  }

  isEnabled(flag: FeatureFlag, context: FlagContext = {}): boolean {
    try {
      const config = this.config[flag];

      if (!config) {
        console.warn(`Flag ${flag} not found in configuration. Defaulting to false.`);
        return false;
      }

      // Check if globally disabled
      if (!config.enabled) {
        return false;
      }

      // Check environment
      if (config.enabledEnvironments && context.environment) {
        if (!config.enabledEnvironments.includes(context.environment)) {
          return false;
        }
      }

      // Check user targeting
      if (config.allowedUsers && context.userId) {
        if (!config.allowedUsers.includes(context.userId)) {
          return false;
        }
      }

      // Check org targeting
      if (config.allowedOrgs && context.orgId) {
        if (!config.allowedOrgs.includes(context.orgId)) {
          return false;
        }
      }

      // Check rollout percentage
      if (config.rolloutPercentage !== undefined && config.rolloutPercentage < 100) {
        // Deterministic random based on user ID
        const hash = this.hashString(context.userId || 'anonymous');
        const userPercentile = hash % 100;
        return userPercentile < config.rolloutPercentage;
      }

      return true;
    } catch (error) {
      console.error(`Error evaluating flag ${flag}:`, error);
      // Fail safe: return false if evaluation fails
      return false;
    }
  }

  getVariant(flag: FeatureFlag, context: FlagContext = {}): string {
    // Simple implementation: return 'control' or 'treatment'
    // For more complex variants, use a dedicated service

    if (!this.isEnabled(flag, context)) {
      return 'control';
    }

    // Deterministic assignment based on user ID
    const hash = this.hashString(context.userId || 'anonymous');
    return hash % 2 === 0 ? 'treatment' : 'control';
  }

  getEvaluatedFlags(context: FlagContext): Record<string, boolean> {
    const evaluated: Record<string, boolean> = {};

    for (const flag of Object.values(FeatureFlag)) {
      evaluated[flag] = this.isEnabled(flag, context);
    }

    return evaluated;
  }

  /**
   * Simple string hash function for deterministic rollouts
   */
  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }
}

// ============================================================================
// Example Configuration
// ============================================================================

export const exampleConfig: FlagsConfig = {
  [FeatureFlag.NewCheckoutFlow]: {
    enabled: true,
    rolloutPercentage: 10,
    enabledEnvironments: ['dev', 'staging', 'production'],
    metadata: {
      type: 'release',
      owner: '@payments-team',
      description: 'New streamlined checkout experience',
      createdAt: '2025-01-15',
      removalDate: '2025-12-31',
    },
  },

  [FeatureFlag.AIAssistant]: {
    enabled: true,
    rolloutPercentage: 0,
    enabledEnvironments: ['dev', 'staging'],
    metadata: {
      type: 'release',
      owner: '@ai-team',
      description: 'AI-powered chat assistant',
      createdAt: '2025-01-10',
      removalDate: '2025-11-30',
    },
  },

  [FeatureFlag.ExternalAPIEnabled]: {
    enabled: true,
    enabledEnvironments: ['dev', 'staging', 'production'],
    metadata: {
      type: 'ops',
      owner: '@platform-team',
      description: 'Circuit breaker for external API calls',
    },
  },

  [FeatureFlag.AdvancedAnalytics]: {
    enabled: true,
    enabledEnvironments: ['production'],
    metadata: {
      type: 'permission',
      owner: '@analytics-team',
      description: 'Advanced analytics features for premium users',
    },
  },
};

// ============================================================================
// Usage Examples
// ============================================================================

/**
 * Example service using feature flags
 */
export class ExampleService {
  constructor(private featureFlags: FeatureFlagService) {}

  async processCheckout(cart: any, context: FlagContext): Promise<any> {
    // Use positive naming: isEnabled, not isDisabled
    if (this.featureFlags.isEnabled(FeatureFlag.NewCheckoutFlow, context)) {
      return this.newCheckoutFlow(cart);
    }

    return this.legacyCheckoutFlow(cart);
  }

  private async newCheckoutFlow(cart: any): Promise<any> {
    // New implementation
    return { version: 'v2', cart };
  }

  private async legacyCheckoutFlow(cart: any): Promise<any> {
    // Legacy implementation
    return { version: 'v1', cart };
  }

  async getAnalytics(context: FlagContext): Promise<any> {
    if (this.featureFlags.isEnabled(FeatureFlag.AdvancedAnalytics, context)) {
      return this.getAdvancedAnalytics();
    }

    return this.getBasicAnalytics();
  }

  private async getAdvancedAnalytics(): Promise<any> {
    return { type: 'advanced', features: ['predictive', 'custom-reports'] };
  }

  private async getBasicAnalytics(): Promise<any> {
    return { type: 'basic', features: ['dashboard', 'reports'] };
  }
}

// ============================================================================
// Testing Utilities
// ============================================================================

/**
 * Mock feature flag service for testing
 */
export class MockFeatureFlagService implements FeatureFlagService {
  private enabledFlags = new Map<FeatureFlag, boolean>();
  private variants = new Map<FeatureFlag, string>();

  setEnabled(flag: FeatureFlag, enabled: boolean): void {
    this.enabledFlags.set(flag, enabled);
  }

  setVariant(flag: FeatureFlag, variant: string): void {
    this.variants.set(flag, variant);
  }

  reset(): void {
    this.enabledFlags.clear();
    this.variants.clear();
  }

  isEnabled(flag: FeatureFlag, context?: FlagContext): boolean {
    return this.enabledFlags.get(flag) ?? false;
  }

  getVariant(flag: FeatureFlag, context?: FlagContext): string {
    return this.variants.get(flag) ?? 'control';
  }

  getEvaluatedFlags(context: FlagContext): Record<string, boolean> {
    const evaluated: Record<string, boolean> = {};
    for (const flag of Object.values(FeatureFlag)) {
      evaluated[flag] = this.isEnabled(flag, context);
    }
    return evaluated;
  }
}
