---
description: Generate comprehensive tests using python-expert agent
category: testing
---

# Test Generation Mode

Launching **python-expert agent** to generate comprehensive test suites.

**What I'll do:**
1. Analyze the target module/function structure and logic
2. Identify test scenarios (happy path, edge cases, error handling)
3. Generate pytest tests with proper fixtures, mocks, and assertions
4. Run tests to verify they pass
5. Report coverage impact

**Best for:**
- Creating test suites for untested modules
- Adding edge case tests to existing suites
- Generating fixture factories and test helpers

**Usage patterns:**
- Entire module: `/test-gen path/to/module.py`
- Specific function: `/test-gen path/to/module.py::function_name`
- Multiple modules: `/test-gen path/to/dir/*.py`

---

**Target:** {{TARGET}}

Launching python-expert agent for test generation...
