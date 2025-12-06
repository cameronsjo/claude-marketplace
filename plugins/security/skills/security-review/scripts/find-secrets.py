#!/usr/bin/env python3
"""
Find potential hardcoded secrets in codebase.

Uses regex patterns to detect:
- API keys
- Passwords
- Tokens
- Private keys
- Connection strings
- AWS credentials
- JWT tokens
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SecretMatch:
    """Detected secret match."""

    pattern_name: str
    file_path: str
    line_number: int
    line_content: str
    matched_text: str
    confidence: str  # high, medium, low
    is_likely_test: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "pattern": self.pattern_name,
            "file": self.file_path,
            "line": self.line_number,
            "content": self.line_content.strip(),
            "matched": self.matched_text,
            "confidence": self.confidence,
            "likely_test_fixture": self.is_likely_test,
        }


class SecretScanner:
    """Scanner for hardcoded secrets."""

    def __init__(self, patterns_file: Path | None = None):
        self.patterns = self._load_patterns(patterns_file)
        self.matches: list[SecretMatch] = []
        self.exclude_patterns = [
            r"node_modules/",
            r"\.git/",
            r"venv/",
            r"\.venv/",
            r"__pycache__/",
            r"dist/",
            r"build/",
            r"\.pytest_cache/",
        ]

    def _load_patterns(self, patterns_file: Path | None) -> dict[str, dict[str, Any]]:
        """Load secret detection patterns."""
        if patterns_file and patterns_file.exists():
            return json.loads(patterns_file.read_text())

        # Default patterns
        return {
            "aws_access_key": {
                "pattern": r"AKIA[0-9A-Z]{16}",
                "confidence": "high",
                "description": "AWS Access Key ID",
            },
            "aws_secret_key": {
                "pattern": r"aws_secret_access_key\s*=\s*['\"]?([A-Za-z0-9/+=]{40})['\"]?",
                "confidence": "high",
                "description": "AWS Secret Access Key",
            },
            "generic_api_key": {
                "pattern": r'["\']?[Aa][Pp][Ii]_?[Kk][Ee][Yy]["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                "confidence": "medium",
                "description": "Generic API Key",
            },
            "password_assignment": {
                "pattern": r'["\']?[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                "confidence": "medium",
                "description": "Password Assignment",
            },
            "bearer_token": {
                "pattern": r'[Bb]earer\s+([A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+)',
                "confidence": "high",
                "description": "Bearer Token (JWT)",
            },
            "jwt_token": {
                "pattern": r"eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+",
                "confidence": "high",
                "description": "JWT Token",
            },
            "private_key": {
                "pattern": r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
                "confidence": "high",
                "description": "Private Key",
            },
            "connection_string": {
                "pattern": r'(mongodb|mysql|postgresql|mssql)://[^:]+:[^@]+@',
                "confidence": "high",
                "description": "Database Connection String",
            },
            "slack_token": {
                "pattern": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
                "confidence": "high",
                "description": "Slack Token",
            },
            "github_token": {
                "pattern": r"gh[pousr]_[A-Za-z0-9]{36}",
                "confidence": "high",
                "description": "GitHub Token",
            },
            "generic_secret": {
                "pattern": r'["\']?[Ss][Ee][Cc][Rr][Ee][Tt]["\']?\s*[:=]\s*["\']([^"\']{10,})["\']',
                "confidence": "medium",
                "description": "Generic Secret",
            },
            "authorization_header": {
                "pattern": r'[Aa]uthorization["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
                "confidence": "medium",
                "description": "Authorization Header",
            },
            "basic_auth": {
                "pattern": r"Basic\s+[A-Za-z0-9+/]+=*",
                "confidence": "high",
                "description": "Basic Auth Credentials",
            },
        }

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        path_str = str(path)
        return any(re.search(pattern, path_str) for pattern in self.exclude_patterns)

    def is_likely_test_fixture(self, file_path: Path, line: str) -> bool:
        """Check if this is likely a test fixture."""
        # Check file path
        test_indicators_path = ["test", "tests", "spec", "mock", "fixture", "example"]
        if any(indicator in str(file_path).lower() for indicator in test_indicators_path):
            return True

        # Check line content
        test_indicators_line = ["mock", "test", "fixture", "dummy", "example", "MOCK", "TEST", "FIXTURE"]
        if any(indicator in line for indicator in test_indicators_line):
            return True

        # Check for common test patterns
        if re.search(r"(def test_|it\(|describe\(|@pytest)", line):
            return True

        return False

    def scan_file(self, file_path: Path) -> None:
        """Scan a file for secrets."""
        if self.should_exclude(file_path):
            return

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            for line_num, line in enumerate(lines, start=1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith("#") or stripped.startswith("//"):
                    continue

                for pattern_name, pattern_info in self.patterns.items():
                    matches = re.finditer(pattern_info["pattern"], line)
                    for match in matches:
                        matched_text = match.group(0)

                        # Skip if it looks like environment variable
                        if "os.environ" in line or "process.env" in line:
                            continue

                        # Skip if it's a placeholder
                        if any(
                            placeholder in matched_text.lower()
                            for placeholder in ["your-", "example", "placeholder", "<", ">", "xxx", "***"]
                        ):
                            continue

                        is_test = self.is_likely_test_fixture(file_path, line)

                        self.matches.append(
                            SecretMatch(
                                pattern_name=pattern_name,
                                file_path=str(file_path),
                                line_number=line_num,
                                line_content=line,
                                matched_text=matched_text[:50] + "..." if len(matched_text) > 50 else matched_text,
                                confidence=pattern_info["confidence"],
                                is_likely_test=is_test,
                            )
                        )

        except (UnicodeDecodeError, PermissionError):
            pass

    def scan_directory(self, path: Path) -> None:
        """Scan directory recursively."""
        for file_path in path.rglob("*"):
            if file_path.is_file():
                self.scan_file(file_path)

    def generate_report(self) -> dict[str, Any]:
        """Generate secrets scan report."""
        high_confidence = [m for m in self.matches if m.confidence == "high" and not m.is_likely_test]
        test_fixtures = [m for m in self.matches if m.is_likely_test]

        return {
            "summary": {
                "total_matches": len(self.matches),
                "high_confidence": len(high_confidence),
                "likely_test_fixtures": len(test_fixtures),
                "requires_review": len(high_confidence),
            },
            "findings": [m.to_dict() for m in self.matches],
        }

    def print_report(self) -> None:
        """Print human-readable report."""
        report = self.generate_report()
        summary = report["summary"]

        print("\n" + "=" * 80)
        print("SECRETS SCANNER REPORT")
        print("=" * 80)
        print(f"\nTotal Matches:          {summary['total_matches']}")
        print(f"High Confidence:        {summary['high_confidence']}")
        print(f"Likely Test Fixtures:   {summary['likely_test_fixtures']}")
        print(f"Requires Review:        {summary['requires_review']}")

        # Group by confidence and test status
        high_conf_real = [m for m in self.matches if m.confidence == "high" and not m.is_likely_test]
        test_fixtures = [m for m in self.matches if m.is_likely_test]
        other_matches = [m for m in self.matches if m.confidence != "high" and not m.is_likely_test]

        if high_conf_real:
            print("\n" + "-" * 80)
            print("HIGH CONFIDENCE - REQUIRES IMMEDIATE REVIEW")
            print("-" * 80)
            for match in high_conf_real:
                print(f"\n[{match.pattern_name}] {match.file_path}:{match.line_number}")
                print(f"  {match.line_content.strip()}")
                print(f"  Matched: {match.matched_text}")

        if test_fixtures:
            print("\n" + "-" * 80)
            print("LIKELY TEST FIXTURES - Review for .sentinelpolicy")
            print("-" * 80)
            for match in test_fixtures[:10]:  # Show first 10
                print(f"\n[{match.pattern_name}] {match.file_path}:{match.line_number}")
                print(f"  {match.line_content.strip()}")

            if len(test_fixtures) > 10:
                print(f"\n... and {len(test_fixtures) - 10} more test fixtures")

        if other_matches:
            print("\n" + "-" * 80)
            print("OTHER MATCHES - Review as needed")
            print("-" * 80)
            for match in other_matches[:5]:  # Show first 5
                print(f"\n[{match.pattern_name}] {match.file_path}:{match.line_number}")
                print(f"  {match.line_content.strip()}")

            if len(other_matches) > 5:
                print(f"\n... and {len(other_matches) - 5} more matches")

        print("\n" + "=" * 80)
        print("\nNEXT STEPS:")
        if high_conf_real:
            print("  1. Review high confidence findings immediately")
            print("  2. Rotate any real secrets found")
            print("  3. Move secrets to environment variables or Akeyless")
        if test_fixtures:
            print("  4. Add test fixtures to .sentinelpolicy with clear comments")
        print("\n" + "=" * 80)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scan for hardcoded secrets")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Path to scan")
    parser.add_argument("--output", type=Path, help="Output JSON report to file")
    parser.add_argument("--patterns", type=Path, help="Custom patterns JSON file")

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    scanner = SecretScanner(patterns_file=args.patterns)
    print(f"Scanning {args.path} for secrets...")
    scanner.scan_directory(args.path)

    scanner.print_report()

    if args.output:
        report = scanner.generate_report()
        args.output.write_text(json.dumps(report, indent=2))
        print(f"\nJSON report written to: {args.output}")

    # Return non-zero if high confidence matches found
    summary = scanner.generate_report()["summary"]
    if summary["requires_review"] > 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
