#!/usr/bin/env python3
"""
Generate and manage .sentinelpolicy entries for Secrets Scanner.

Helps create properly formatted suppression entries with clear comments.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional


class SentinelPolicyManager:
    """Manage .sentinelpolicy file."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.policy_file = repo_root / ".sentinelpolicy"

    def add_suppressionkey(self, key: str, reason: str) -> None:
        """Add a suppressionkey entry."""
        if not reason or len(reason.strip()) < 10:
            print("Error: Reason must be at least 10 characters and explain WHY this is safe", file=sys.stderr)
            sys.exit(1)

        entry = f"suppressionkey={key};{reason}\n"

        # Check if already exists
        if self.policy_file.exists():
            content = self.policy_file.read_text()
            if f"suppressionkey={key}" in content:
                print(f"Warning: Suppression key {key} already exists in .sentinelpolicy")
                response = input("Update comment? (y/n): ")
                if response.lower() != "y":
                    return

                # Update existing entry
                lines = content.split("\n")
                new_lines = []
                for line in lines:
                    if line.startswith(f"suppressionkey={key}"):
                        new_lines.append(entry.rstrip())
                    else:
                        new_lines.append(line)
                content = "\n".join(new_lines)
                self.policy_file.write_text(content)
                print(f"Updated suppression key {key}")
                return

        # Append new entry
        with self.policy_file.open("a") as f:
            if self.policy_file.stat().st_size > 0:
                f.write("\n")
            f.write(entry)

        print(f"Added suppression key {key} to .sentinelpolicy")

    def add_safeline(self, filename: str, line_number: int, reason: str) -> None:
        """Add a safeline entry."""
        if not reason or len(reason.strip()) < 10:
            print("Error: Reason must be at least 10 characters and explain WHY this is safe", file=sys.stderr)
            sys.exit(1)

        entry = f"safeline={filename};{line_number};{reason}\n"

        with self.policy_file.open("a") as f:
            if self.policy_file.stat().st_size > 0:
                f.write("\n")
            f.write(entry)

        print(f"Added safeline for {filename}:{line_number} to .sentinelpolicy")
        print("Warning: Safeline entries break when line numbers change. Consider using suppressionkey instead.")

    def add_safefile(self, filename: str, reason: str) -> None:
        """Add a safefile entry."""
        if not reason or len(reason.strip()) < 10:
            print("Error: Reason must be at least 10 characters and explain WHY this is safe", file=sys.stderr)
            sys.exit(1)

        print("Warning: Safefile suppresses the ENTIRE file. Are you sure?")
        response = input("Continue? (y/n): ")
        if response.lower() != "y":
            return

        entry = f"safefile={filename};{reason}\n"

        with self.policy_file.open("a") as f:
            if self.policy_file.stat().st_size > 0:
                f.write("\n")
            f.write(entry)

        print(f"Added safefile for {filename} to .sentinelpolicy")

    def audit(self) -> None:
        """Audit existing .sentinelpolicy entries."""
        if not self.policy_file.exists():
            print("No .sentinelpolicy file found in repository root")
            return

        content = self.policy_file.read_text()
        lines = content.split("\n")

        print("\n" + "=" * 80)
        print("SENTINEL POLICY AUDIT")
        print("=" * 80)

        issues = []
        valid_entries = []

        for line_num, line in enumerate(lines, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Check format
            if line.startswith("suppressionkey="):
                parts = line.split(";", 1)
                if len(parts) < 2:
                    issues.append(f"Line {line_num}: Missing comment")
                elif len(parts[1].strip()) < 10:
                    issues.append(f"Line {line_num}: Comment too short (< 10 chars)")
                else:
                    valid_entries.append(("suppressionkey", parts[0], parts[1]))

            elif line.startswith("safeline="):
                parts = line.split(";", 2)
                if len(parts) < 3:
                    issues.append(f"Line {line_num}: Invalid safeline format")
                elif len(parts[2].strip()) < 10:
                    issues.append(f"Line {line_num}: Comment too short (< 10 chars)")
                else:
                    valid_entries.append(("safeline", f"{parts[0]};{parts[1]}", parts[2]))

            elif line.startswith("safefile="):
                parts = line.split(";", 1)
                if len(parts) < 2:
                    issues.append(f"Line {line_num}: Missing comment")
                elif len(parts[1].strip()) < 10:
                    issues.append(f"Line {line_num}: Comment too short (< 10 chars)")
                else:
                    valid_entries.append(("safefile", parts[0], parts[1]))

            else:
                issues.append(f"Line {line_num}: Unknown format: {line}")

        print(f"\nTotal Entries: {len(valid_entries)}")
        print(f"Issues Found:  {len(issues)}")

        if valid_entries:
            print("\n" + "-" * 80)
            print("VALID ENTRIES")
            print("-" * 80)
            for entry_type, key, comment in valid_entries:
                print(f"\n[{entry_type}]")
                print(f"  Key:     {key}")
                print(f"  Comment: {comment}")

        if issues:
            print("\n" + "-" * 80)
            print("ISSUES")
            print("-" * 80)
            for issue in issues:
                print(f"  {issue}")

        print("\n" + "=" * 80)

    def create_template(self) -> None:
        """Create a template .sentinelpolicy file."""
        if self.policy_file.exists():
            print("Error: .sentinelpolicy already exists", file=sys.stderr)
            sys.exit(1)

        template = """# .sentinelpolicy - Secrets Scanner Configuration
#
# Format:
#   suppressionkey=KEY;Clear explanation of why this is safe
#   safeline=filename;line_number;Clear explanation
#   safefile=filename;Clear explanation (avoid - too broad)
#
# Guidelines:
#   - Always add clear comments explaining WHY the suppression is safe
#   - Use suppressionkey for test fixtures (survives refactoring)
#   - Use safeline for specific lines (breaks on line number changes)
#   - Avoid safefile unless absolutely necessary
#   - NEVER suppress real secrets
#
# Valid reasons to suppress:
#   ✅ Test fixtures and mock data
#   ✅ Example data in documentation/docstrings
#   ✅ Dummy tokens for unit tests
#   ✅ Redacted values used in test validation
#
# NEVER suppress:
#   ❌ Real API keys
#   ❌ Actual passwords
#   ❌ Production credentials
#   ❌ Service account tokens

# Example suppressions (delete these and add your own):
# suppressionkey=ae4b93f9d;Test fixture - token.json mock JWT tokens for testing
# suppressionkey=b1764b91c;Documentation example in structured_logger.py docstring
"""

        self.policy_file.write_text(template)
        print(f"Created template .sentinelpolicy at {self.policy_file}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Manage .sentinelpolicy for Secrets Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add suppressionkey from secrets scanner notification
  python generate-sentinelpolicy.py --key ae4b93f9d --reason "Test fixture - mock JWT tokens"

  # Add safeline for specific line
  python generate-sentinelpolicy.py --safeline config.py 42 --reason "This is a username, not a secret"

  # Audit existing .sentinelpolicy
  python generate-sentinelpolicy.py --audit

  # Create template .sentinelpolicy
  python generate-sentinelpolicy.py --template
""",
    )

    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root (default: current directory)")
    parser.add_argument("--key", type=str, help="Suppression key from secrets scanner notification")
    parser.add_argument("--reason", type=str, help="Clear explanation of why this is safe")
    parser.add_argument("--safeline", nargs=2, metavar=("FILE", "LINE"), help="Add safeline entry")
    parser.add_argument("--safefile", type=str, help="Add safefile entry (use with caution)")
    parser.add_argument("--audit", action="store_true", help="Audit existing .sentinelpolicy")
    parser.add_argument("--template", action="store_true", help="Create template .sentinelpolicy")

    args = parser.parse_args()

    manager = SentinelPolicyManager(args.repo_root)

    if args.template:
        manager.create_template()
        return 0

    if args.audit:
        manager.audit()
        return 0

    if args.key and args.reason:
        manager.add_suppressionkey(args.key, args.reason)
        return 0

    if args.safeline and args.reason:
        filename, line_number = args.safeline
        manager.add_safeline(filename, int(line_number), args.reason)
        return 0

    if args.safefile and args.reason:
        manager.add_safefile(args.safefile, args.reason)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
