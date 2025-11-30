---
description: Aggressively improve test coverage using parallel agents
category: testing
---

# Coverage Boost Mode 🚀

**Mission**: Rapidly improve test coverage using parallel agent execution and the turbo strategy.

## Strategy

1. **Analyze**: Check coverage report to identify low-coverage modules (<70%)
2. **Prioritize**: Select high-ROI targets (small-to-medium files with many missing lines)
3. **Parallelize**: Launch python-expert agents in parallel (3-5 at a time) for top targets
4. **Test & Measure**: Run tests in batches, measure coverage impact
5. **Iterate**: Repeat with next batch until target reached

## Execution Pattern

```
Iteration 1: Launch 5 agents → Create tests → Run → Measure (+2.5pp)
Iteration 2: Launch 5 agents → Create tests → Run → Measure (+2.1pp)
Iteration 3: Launch 5 agents → Create tests → Run → Measure (+1.8pp)
...continue until target reached
```

## What Gets Created

Each agent will:
- Analyze module structure and logic
- Generate comprehensive tests (happy path, edge cases, errors)
- Include proper fixtures, mocks, and assertions
- Follow project test patterns and style

## This Uses

- **Turbo Mode**: Maximum speed, aggressive parallelization
- **Metrics/Goals Strategy**: Measure → Execute → Measure cycle
- **Pattern Exploitation**: Replicate winning test approaches
- **Batch Processing**: 5-10 tests at a time, not all at once

---

**Target Coverage**: {{TARGET_COVERAGE}}%

Launching coverage analysis and agent coordination...
