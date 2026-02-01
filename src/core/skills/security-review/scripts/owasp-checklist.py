#!/usr/bin/env python3
"""
Interactive OWASP Top 10 checklist runner.

Walks through OWASP Top 10 2021 checklist with file-specific guidance.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class OWASPChecker:
    """Interactive OWASP Top 10 checklist."""

    def __init__(self, checklist_file: Path):
        self.checklist = self._load_checklist(checklist_file)
        self.results: dict[str, list[dict[str, Any]]] = {}

    def _load_checklist(self, checklist_file: Path) -> dict[str, Any]:
        """Load OWASP checklist from JSON."""
        if checklist_file.exists():
            return json.loads(checklist_file.read_text())

        # Default checklist
        return {
            "A01:2021": {
                "name": "Broken Access Control",
                "checks": [
                    "Enforce least privilege and deny-by-default",
                    "Implement access control checks on server-side",
                    "Invalidate JWT tokens on logout",
                    "Rate-limit API and controller access",
                    "Disable directory listing, ensure metadata files not accessible",
                    "Log access control failures, alert on suspicious patterns",
                ],
            },
            "A02:2021": {
                "name": "Cryptographic Failures",
                "checks": [
                    "Classify data (PII, credentials) and apply controls",
                    "Encrypt data at rest and in transit (TLS 1.2+)",
                    "Use strong encryption algorithms (AES-256, no MD5/SHA1)",
                    "Proper key management (rotate, store securely)",
                    "Disable caching for sensitive data responses",
                ],
            },
            "A03:2021": {
                "name": "Injection",
                "checks": [
                    "Use parameterized queries, ORMs, or prepared statements",
                    "Validate and sanitize all user input (allow-list preferred)",
                    "Use LIMIT and SQL controls to prevent mass disclosure",
                    "For AI/LLM: validate prompts, sanitize inputs/outputs",
                    "Escape special characters in queries and commands",
                ],
            },
            "A04:2021": {
                "name": "Insecure Design",
                "checks": [
                    "Threat modeling during design phase",
                    "Secure design patterns (defense-in-depth, fail-safe defaults)",
                    "Segregate tenants robustly in multi-tenant systems",
                    "Limit resource consumption per user/tenant",
                    "Review architecture with security expert",
                ],
            },
            "A05:2021": {
                "name": "Security Misconfiguration",
                "checks": [
                    "Repeatable hardening process (IaC, automated config)",
                    "Minimal platform (remove unused features)",
                    "Review cloud storage permissions",
                    "Disable default accounts and passwords",
                    "Error messages don't leak sensitive information",
                    "Keep security patches up-to-date",
                ],
            },
            "A06:2021": {
                "name": "Vulnerable and Outdated Components",
                "checks": [
                    "Inventory all components (packages, libraries)",
                    "Remove unused dependencies and features",
                    "Monitor for vulnerabilities (Dependabot, npm audit)",
                    "Subscribe to security bulletins",
                    "Obtain components from official sources",
                    "Prefer signed packages",
                ],
            },
            "A07:2021": {
                "name": "Identification and Authentication Failures",
                "checks": [
                    "Implement MFA where possible",
                    "No default credentials shipped",
                    "Weak password checks (block common passwords)",
                    "Brute force and credential stuffing protections",
                    "Secure session management (HTTPOnly, Secure, SameSite)",
                    "Invalidate sessions on logout",
                    "Use established auth libraries (OAuth 2.1, OpenID Connect)",
                ],
            },
            "A08:2021": {
                "name": "Software and Data Integrity Failures",
                "checks": [
                    "Use digital signatures to verify integrity",
                    "Verify dependencies from trusted repos",
                    "Review CI/CD pipeline security",
                    "Implement auto-update with integrity verification",
                    "Validate data before deserialization",
                ],
            },
            "A09:2021": {
                "name": "Security Logging and Monitoring Failures",
                "checks": [
                    "Log authentication, authorization failures",
                    "Structured logging with context",
                    "Logs stored securely, protected from tampering",
                    "High-value transactions have audit trail",
                    "Effective monitoring and alerting",
                    "Incident response plan in place",
                ],
            },
            "A10:2021": {
                "name": "Server-Side Request Forgery (SSRF)",
                "checks": [
                    "Sanitize and validate all client-supplied URL data",
                    "Enforce URL schema, port, destination with allow-list",
                    "Disable HTTP redirections",
                    "Don't send raw responses to clients",
                    "Network segmentation to reduce impact",
                ],
            },
        }

    def run_interactive(self) -> None:
        """Run interactive checklist."""
        print("\n" + "=" * 80)
        print("OWASP TOP 10 2021 - INTERACTIVE SECURITY CHECKLIST")
        print("=" * 80)
        print("\nFor each check, mark as:")
        print("  ✅ [p]ass - Implemented correctly")
        print("  ❌ [f]ail - Not implemented or vulnerable")
        print("  ⏭️  [s]kip - Not applicable")
        print("  ℹ️  [n]ote - Add note/finding")
        print()

        for category_id, category_data in self.checklist.items():
            print("\n" + "=" * 80)
            print(f"{category_id} - {category_data['name']}")
            print("=" * 80)

            category_results = []

            for check in category_data["checks"]:
                print(f"\n❓ {check}")
                response = input("   Status [p/f/s/n]: ").strip().lower()

                result = {"check": check, "status": response}

                if response == "n":
                    note = input("   Note: ").strip()
                    result["note"] = note
                    result["status"] = "fail"  # Notes indicate issues
                elif response == "f":
                    note = input("   Details (optional): ").strip()
                    if note:
                        result["note"] = note

                category_results.append(result)

            self.results[category_id] = category_results

    def generate_report(self) -> dict[str, Any]:
        """Generate checklist report."""
        summary = {"pass": 0, "fail": 0, "skip": 0}

        for category_results in self.results.values():
            for result in category_results:
                status = result["status"]
                if status in ["p", "pass"]:
                    summary["pass"] += 1
                elif status in ["f", "fail"]:
                    summary["fail"] += 1
                elif status in ["s", "skip"]:
                    summary["skip"] += 1

        return {"summary": summary, "results": self.results}

    def print_report(self) -> None:
        """Print summary report."""
        report = self.generate_report()
        summary = report["summary"]

        print("\n" + "=" * 80)
        print("OWASP CHECKLIST SUMMARY")
        print("=" * 80)
        print(f"\n✅ Passed: {summary['pass']}")
        print(f"❌ Failed: {summary['fail']}")
        print(f"⏭️  Skipped: {summary['skip']}")

        # Show failures
        failures = []
        for category_id, category_results in self.results.items():
            category_name = self.checklist[category_id]["name"]
            for result in category_results:
                if result["status"] in ["f", "fail"]:
                    failures.append({"category": f"{category_id} - {category_name}", "check": result["check"], "note": result.get("note", "")})

        if failures:
            print("\n" + "-" * 80)
            print("FAILED CHECKS - REQUIRES ATTENTION")
            print("-" * 80)
            for failure in failures:
                print(f"\n[{failure['category']}]")
                print(f"  {failure['check']}")
                if failure["note"]:
                    print(f"  Note: {failure['note']}")

        print("\n" + "=" * 80)

    def save_report(self, output_path: Path) -> None:
        """Save report to JSON file."""
        report = self.generate_report()
        output_path.write_text(json.dumps(report, indent=2))
        print(f"\nReport saved to: {output_path}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Interactive OWASP Top 10 checklist")
    parser.add_argument("--checklist", type=Path, help="Custom checklist JSON file")
    parser.add_argument("--output", type=Path, help="Output report to JSON file")

    args = parser.parse_args()

    # Find checklist file
    checklist_file = args.checklist
    if not checklist_file:
        # Look for resources/owasp-checklist.json
        script_dir = Path(__file__).parent
        resources_dir = script_dir.parent / "resources"
        checklist_file = resources_dir / "owasp-checklist.json"

    checker = OWASPChecker(checklist_file)
    checker.run_interactive()
    checker.print_report()

    if args.output:
        checker.save_report(args.output)

    # Return non-zero if failures
    report = checker.generate_report()
    if report["summary"]["fail"] > 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
