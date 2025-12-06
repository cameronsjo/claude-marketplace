#!/usr/bin/env python3
"""
Test PII sanitization implementation.

Runs comprehensive test suite to verify PII patterns are properly sanitized.
Requires pytest.

Usage:
    python scripts/test-pii-sanitization.py
    python scripts/test-pii-sanitization.py --verbose
    python scripts/test-pii-sanitization.py --pattern email
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# Load PII patterns
PATTERNS_FILE = Path(__file__).parent.parent / "resources" / "pii-patterns.json"

def load_patterns() -> Dict:
    """Load PII patterns from JSON file"""
    with open(PATTERNS_FILE) as f:
        return json.load(f)

def sanitize_string(text: str, patterns: Dict) -> str:
    """Sanitize text using provided patterns"""
    if not text:
        return text

    for pattern_name, pattern_config in patterns["patterns"].items():
        regex = re.compile(pattern_config["regex"])
        text = regex.sub(pattern_config["replacement"], text)

    return text

def run_test_cases(patterns: Dict, verbose: bool = False) -> tuple[int, int]:
    """
    Run all test cases from patterns file.

    Returns:
        tuple: (passed_count, total_count)
    """
    test_cases = patterns.get("test_cases", [])
    passed = 0
    total = len(test_cases)

    print(f"\nRunning {total} test cases...")
    print("=" * 60)

    for i, test_case in enumerate(test_cases, 1):
        input_text = test_case["input"]
        expected = test_case["expected"]
        actual = sanitize_string(input_text, patterns)

        passed_test = actual == expected

        if verbose or not passed_test:
            print(f"\nTest {i}:")
            print(f"  Input:    {input_text}")
            print(f"  Expected: {expected}")
            print(f"  Actual:   {actual}")
            print(f"  Status:   {'✓ PASS' if passed_test else '✗ FAIL'}")

        if passed_test:
            passed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")

    return passed, total

def test_specific_pattern(pattern_name: str, patterns: Dict) -> bool:
    """Test a specific PII pattern with its examples"""
    if pattern_name not in patterns["patterns"]:
        print(f"Error: Pattern '{pattern_name}' not found")
        return False

    pattern_config = patterns["patterns"][pattern_name]
    regex = re.compile(pattern_config["regex"])
    replacement = pattern_config["replacement"]

    print(f"\nTesting pattern: {pattern_name}")
    print(f"Description: {pattern_config['description']}")
    print(f"Regex: {pattern_config['regex']}")
    print("=" * 60)

    all_passed = True
    for example in pattern_config.get("examples", []):
        sanitized = regex.sub(replacement, example)
        passed = replacement in sanitized and example not in sanitized

        print(f"\nExample: {example}")
        print(f"Result:  {sanitized}")
        print(f"Status:  {'✓ PASS' if passed else '✗ FAIL'}")

        if not passed:
            all_passed = False

    return all_passed

def main():
    parser = argparse.ArgumentParser(
        description="Test PII sanitization implementation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all test results, not just failures"
    )
    parser.add_argument(
        "--pattern", "-p",
        type=str,
        help="Test specific pattern only (e.g., 'email', 'ssn')"
    )

    args = parser.parse_args()

    # Load patterns
    try:
        patterns = load_patterns()
    except FileNotFoundError:
        print(f"Error: Could not find patterns file: {PATTERNS_FILE}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in patterns file: {e}")
        return 1

    # Run tests
    if args.pattern:
        success = test_specific_pattern(args.pattern, patterns)
        return 0 if success else 1
    else:
        passed, total = run_test_cases(patterns, args.verbose)
        return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
