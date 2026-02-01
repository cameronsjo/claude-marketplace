#!/usr/bin/env python3
"""
Security audit script for automated vulnerability detection.

Scans codebase for common security issues:
- Hardcoded secrets
- Weak cryptography
- SQL injection risks
- Command injection risks
- Insecure deserialization
- Security misconfigurations
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    """Security finding data structure."""

    severity: str  # critical, high, medium, low, info
    category: str  # OWASP category or security domain
    title: str
    description: str
    file_path: str
    line_number: int
    line_content: str
    remediation: str
    references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert finding to dictionary."""
        return {
            "severity": self.severity,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "location": {
                "file": self.file_path,
                "line": self.line_number,
                "content": self.line_content.strip(),
            },
            "remediation": self.remediation,
            "references": self.references,
        }


class SecurityAuditor:
    """Automated security vulnerability scanner."""

    def __init__(self, base_path: Path, exclude_patterns: list[str] | None = None):
        self.base_path = base_path
        self.exclude_patterns = exclude_patterns or [
            r"node_modules/",
            r"\.git/",
            r"venv/",
            r"\.venv/",
            r"__pycache__/",
            r"dist/",
            r"build/",
            r"\.pytest_cache/",
            r"test_.*\.py$",
            r".*_test\.py$",
            r".*\.test\.(ts|js)$",
            r".*\.spec\.(ts|js)$",
        ]
        self.findings: list[Finding] = []

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from scanning."""
        path_str = str(path)
        return any(re.search(pattern, path_str) for pattern in self.exclude_patterns)

    def scan_file(self, file_path: Path) -> None:
        """Scan a single file for security issues."""
        if self.should_exclude(file_path):
            return

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            for line_num, line in enumerate(lines, start=1):
                self._check_hardcoded_secrets(file_path, line_num, line)
                self._check_weak_crypto(file_path, line_num, line)
                self._check_sql_injection(file_path, line_num, line)
                self._check_command_injection(file_path, line_num, line)
                self._check_insecure_deserialization(file_path, line_num, line)
                self._check_debug_mode(file_path, line_num, line)
                self._check_sensitive_data_logging(file_path, line_num, line)

        except (UnicodeDecodeError, PermissionError):
            # Skip binary files and files without read permission
            pass

    def _check_hardcoded_secrets(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for hardcoded secrets."""
        # API keys
        if re.search(r'["\']?[Aa][Pp][Ii]_?[Kk][Ee][Yy]["\']?\s*[:=]\s*["\'][^"\']{20,}["\']', line):
            if not self._is_test_fixture(line):
                self.findings.append(
                    Finding(
                        severity="critical",
                        category="A02:2021 - Cryptographic Failures",
                        title="Hardcoded API Key",
                        description="Potential hardcoded API key detected",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Use environment variables or secret management (Akeyless)",
                        references=["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
                    )
                )

        # Passwords
        if re.search(r'["\']?[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]["\']?\s*[:=]\s*["\'][^"\']+["\']', line):
            if not self._is_test_fixture(line) and "os.environ" not in line and "process.env" not in line:
                self.findings.append(
                    Finding(
                        severity="critical",
                        category="A02:2021 - Cryptographic Failures",
                        title="Hardcoded Password",
                        description="Potential hardcoded password detected",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Use environment variables or secret management",
                        references=["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
                    )
                )

        # AWS credentials
        if re.search(r"AKIA[0-9A-Z]{16}", line):
            self.findings.append(
                Finding(
                    severity="critical",
                    category="A02:2021 - Cryptographic Failures",
                    title="AWS Access Key",
                    description="AWS access key detected",
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=line,
                    remediation="Rotate key immediately, use environment variables",
                    references=["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
                )
            )

    def _check_weak_crypto(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for weak cryptographic algorithms."""
        weak_algos = ["MD5", "SHA1", "DES", "RC4", "ECB"]
        for algo in weak_algos:
            if re.search(rf"\b{algo}\b", line, re.IGNORECASE):
                # Check if it's actually being used for crypto (not just in comments)
                if not line.strip().startswith("#") and not line.strip().startswith("//"):
                    self.findings.append(
                        Finding(
                            severity="high",
                            category="A02:2021 - Cryptographic Failures",
                            title=f"Weak Cryptographic Algorithm: {algo}",
                            description=f"{algo} is cryptographically weak and should not be used",
                            file_path=str(file_path),
                            line_number=line_num,
                            line_content=line,
                            remediation=f"Replace {algo} with SHA-256 or stronger (e.g., SHA-3, bcrypt for passwords)",
                            references=["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
                        )
                    )

    def _check_sql_injection(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for SQL injection vulnerabilities."""
        # String concatenation in SQL queries
        if re.search(r'(execute|query|cursor\.execute)\s*\([^)]*[+]|f["\'].*SELECT.*FROM', line):
            if "?" not in line and "%s" not in line:  # Not parameterized
                self.findings.append(
                    Finding(
                        severity="critical",
                        category="A03:2021 - Injection",
                        title="SQL Injection Risk",
                        description="SQL query constructed with string concatenation",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Use parameterized queries or ORMs",
                        references=["https://owasp.org/Top10/A03_2021-Injection/"],
                    )
                )

    def _check_command_injection(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for command injection vulnerabilities."""
        dangerous_funcs = [
            r"subprocess\.call\(",
            r"subprocess\.run\(",
            r"os\.system\(",
            r"exec\(",
            r"eval\(",
            r"child_process\.exec\(",
        ]

        for func_pattern in dangerous_funcs:
            if re.search(func_pattern, line):
                # Check if user input might be involved
                if any(keyword in line for keyword in ["input", "request", "req.", "user", "param"]):
                    self.findings.append(
                        Finding(
                            severity="critical",
                            category="A03:2021 - Injection",
                            title="Command Injection Risk",
                            description="Command execution with potential user input",
                            file_path=str(file_path),
                            line_number=line_num,
                            line_content=line,
                            remediation="Validate and sanitize input, use safe alternatives (subprocess with list args)",
                            references=["https://owasp.org/Top10/A03_2021-Injection/"],
                        )
                    )

    def _check_insecure_deserialization(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for insecure deserialization."""
        insecure_patterns = [
            r"pickle\.loads?\(",
            r"yaml\.load\(",  # Should be yaml.safe_load
            r"JSON\.parse\(",  # Check context for untrusted input
        ]

        for pattern in insecure_patterns:
            if re.search(pattern, line):
                # yaml.safe_load is okay
                if "yaml.safe_load" in line:
                    continue

                self.findings.append(
                    Finding(
                        severity="high",
                        category="A08:2021 - Software and Data Integrity Failures",
                        title="Insecure Deserialization",
                        description="Deserialization of untrusted data detected",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Use safe alternatives (yaml.safe_load, validate before deserializing)",
                        references=["https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/"],
                    )
                )

    def _check_debug_mode(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for debug mode enabled."""
        if re.search(r'DEBUG\s*=\s*True|NODE_ENV\s*=\s*["\']development["\']', line):
            if "config" in str(file_path).lower() or "settings" in str(file_path).lower():
                self.findings.append(
                    Finding(
                        severity="medium",
                        category="A05:2021 - Security Misconfiguration",
                        title="Debug Mode Enabled",
                        description="Debug mode may be enabled in production",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Use environment variables, ensure DEBUG=False in production",
                        references=["https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"],
                    )
                )

    def _check_sensitive_data_logging(self, file_path: Path, line_num: int, line: str) -> None:
        """Check for sensitive data in logging statements."""
        if re.search(r'(logger\.|console\.log|print)\(.*', line):
            sensitive_keywords = ["password", "token", "secret", "api_key", "apiKey", "credential"]
            if any(keyword in line.lower() for keyword in sensitive_keywords):
                self.findings.append(
                    Finding(
                        severity="medium",
                        category="A09:2021 - Security Logging and Monitoring Failures",
                        title="Sensitive Data in Logs",
                        description="Potential sensitive data logged",
                        file_path=str(file_path),
                        line_number=line_num,
                        line_content=line,
                        remediation="Redact sensitive data before logging",
                        references=["https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/"],
                    )
                )

    def _is_test_fixture(self, line: str) -> bool:
        """Check if line appears to be test fixture data."""
        test_indicators = ["mock", "test", "fixture", "dummy", "example", "MOCK", "TEST"]
        return any(indicator in line for indicator in test_indicators)

    def scan_directory(self) -> None:
        """Scan all files in directory recursively."""
        for file_path in self.base_path.rglob("*"):
            if file_path.is_file():
                self.scan_file(file_path)

    def generate_report(self) -> dict[str, Any]:
        """Generate security audit report."""
        findings_by_severity = {
            "critical": [f for f in self.findings if f.severity == "critical"],
            "high": [f for f in self.findings if f.severity == "high"],
            "medium": [f for f in self.findings if f.severity == "medium"],
            "low": [f for f in self.findings if f.severity == "low"],
            "info": [f for f in self.findings if f.severity == "info"],
        }

        return {
            "summary": {
                "total_findings": len(self.findings),
                "critical": len(findings_by_severity["critical"]),
                "high": len(findings_by_severity["high"]),
                "medium": len(findings_by_severity["medium"]),
                "low": len(findings_by_severity["low"]),
                "info": len(findings_by_severity["info"]),
            },
            "findings": [f.to_dict() for f in self.findings],
        }

    def print_report(self) -> None:
        """Print human-readable report to console."""
        report = self.generate_report()
        summary = report["summary"]

        print("\n" + "=" * 80)
        print("SECURITY AUDIT REPORT")
        print("=" * 80)
        print(f"\nTotal Findings: {summary['total_findings']}")
        print(f"  Critical: {summary['critical']}")
        print(f"  High:     {summary['high']}")
        print(f"  Medium:   {summary['medium']}")
        print(f"  Low:      {summary['low']}")
        print(f"  Info:     {summary['info']}")

        if self.findings:
            print("\n" + "-" * 80)
            print("FINDINGS")
            print("-" * 80)

            for finding in sorted(self.findings, key=lambda f: ["critical", "high", "medium", "low", "info"].index(f.severity)):
                print(f"\n[{finding.severity.upper()}] {finding.title}")
                print(f"Category: {finding.category}")
                print(f"Location: {finding.file_path}:{finding.line_number}")
                print(f"Code:     {finding.line_content.strip()}")
                print(f"Fix:      {finding.remediation}")

        print("\n" + "=" * 80)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Automated security audit scanner")
    parser.add_argument("--path", type=Path, default=Path.cwd(), help="Path to scan (default: current directory)")
    parser.add_argument("--output", type=Path, help="Output JSON report to file")
    parser.add_argument("--exclude", nargs="+", help="Additional patterns to exclude")

    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: Path does not exist: {args.path}", file=sys.stderr)
        return 1

    auditor = SecurityAuditor(args.path, exclude_patterns=args.exclude)
    print(f"Scanning {args.path}...")
    auditor.scan_directory()

    auditor.print_report()

    if args.output:
        report = auditor.generate_report()
        args.output.write_text(json.dumps(report, indent=2))
        print(f"\nJSON report written to: {args.output}")

    # Return non-zero exit code if critical or high findings
    summary = auditor.generate_report()["summary"]
    if summary["critical"] > 0 or summary["high"] > 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
