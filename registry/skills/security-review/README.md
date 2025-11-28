# Security Review Skill

Comprehensive security audit skill covering OWASP Top 10, AI/MCP security, secrets management, and Enterprise-specific security tooling.

## Overview

The security-review skill provides systematic security review methodology with automated tools and actionable guidance. It covers:

- **OWASP Top 10 Web (2021)** - Complete checklist and validation
- **AI/MCP Security** - Prompt injection, MCP server security, data privacy
- **Secrets Management** - Detection, `.sentinelpolicy` management, Secrets Scanner
- **CodeGate/CheckMarx - Enterprise static code scanning integration
- **Automated Scanning** - Python scripts for vulnerability detection
- **Security Test Cases** - Example test scenarios for validation

## Quick Start

### Automated Security Scan

Run a comprehensive security audit:

```bash
python scripts/security-audit.py --path /path/to/project --output security-report.json
```

### Find Hardcoded Secrets

Scan for potential secrets:

```bash
python scripts/find-secrets.py --path /path/to/project --output secrets-report.json
```

### Interactive OWASP Checklist

Walk through OWASP Top 10 checklist:

```bash
python scripts/owasp-checklist.py --output checklist-results.json
```

### Manage .sentinelpolicy

Add suppressions for Secrets Scanner:

```bash
# Add suppression key
python scripts/generate-sentinelpolicy.py --key ae4b93f9d --reason "Test fixture - mock JWT tokens"

# Audit existing .sentinelpolicy
python scripts/generate-sentinelpolicy.py --audit

# Create template
python scripts/generate-sentinelpolicy.py --template
```

## Skills Integration

Invoke from Claude Code:

```
/skill security-review
```

Or reference in your workflow:

```markdown
Please conduct a security review using the security-review skill.
```

## Tools & Scripts

### `scripts/security-audit.py`

Automated vulnerability scanner detecting:
- Hardcoded secrets (API keys, passwords, tokens)
- Weak cryptography (MD5, SHA1, DES, RC4)
- SQL injection risks
- Command injection risks
- Insecure deserialization
- Security misconfigurations
- Sensitive data in logs

**Usage:**
```bash
python scripts/security-audit.py [--path PATH] [--output report.json] [--exclude PATTERN...]
```

**Exit codes:**
- `0` - No critical/high findings
- `1` - Critical or high severity findings detected

### `scripts/find-secrets.py`

Secrets scanner using regex patterns to detect:
- AWS credentials
- API keys and tokens
- JWT tokens
- Private keys
- Database connection strings
- Service-specific tokens (Slack, GitHub, Stripe, etc.)

**Usage:**
```bash
python scripts/find-secrets.py [--path PATH] [--output report.json] [--patterns custom-patterns.json]
```

**Features:**
- High/medium/low confidence ratings
- Test fixture detection
- .sentinelpolicy integration guidance

### `scripts/generate-sentinelpolicy.py`

Secrets Scanner `.sentinelpolicy` management:

**Commands:**
```bash
# Add suppressionkey (recommended - survives refactoring)
python scripts/generate-sentinelpolicy.py --key KEY --reason "Clear explanation"

# Add safeline (breaks on line number changes)
python scripts/generate-sentinelpolicy.py --safeline FILE LINE --reason "Explanation"

# Add safefile (avoid - too broad)
python scripts/generate-sentinelpolicy.py --safefile FILE --reason "Explanation"

# Audit existing file
python scripts/generate-sentinelpolicy.py --audit

# Create template
python scripts/generate-sentinelpolicy.py --template
```

### `scripts/owasp-checklist.py`

Interactive OWASP Top 10 checklist runner:

**Usage:**
```bash
python scripts/owasp-checklist.py [--checklist custom.json] [--output results.json]
```

**Features:**
- Interactive CLI walkthrough
- Status tracking (pass/fail/skip/note)
- Generates summary report
- Highlights failed checks

## Resources

### `resources/owasp-checklist.json`

Structured OWASP Top 10 2021 checklist with:
- Check items for each category
- Test scenarios
- References to OWASP documentation
- AI/MCP security section

### `resources/secret-patterns.json`

Comprehensive secret detection patterns:
- 30+ pattern definitions
- Confidence levels
- Severity ratings
- Remediation guidance
- Service-specific patterns

### `resources/security-test-cases.md`

Example security test scenarios for:
- OWASP Top 10 categories
- AI/MCP security
- Enterprise-specific tooling
- Security headers
- Authentication/authorization

## Documentation

### Skill Definition

`skill.md` - Complete security review methodology including:
- OWASP Top 10 audit process
- AI/MCP security considerations
- Secrets Scanner integration
- CodeGate/CheckMarx workflow
- Security audit report templates
- Remediation tracking

### Security Documentation

Reference documentation:
- `~/.claude/docs/security/owasp-top-10.md`
- `~/.claude/docs/security/codegate-checkmarx.md`
- `~/.claude/docs/secrets-scanner-guide.md`

## Workflow Examples

### Complete Security Audit

```bash
# 1. Run automated scans
python scripts/security-audit.py --path . --output security-report.json
python scripts/find-secrets.py --path . --output secrets-report.json

# 2. Review reports
cat security-report.json | jq '.summary'
cat secrets-report.json | jq '.summary'

# 3. Interactive OWASP checklist
python scripts/owasp-checklist.py --output checklist-results.json

# 4. Handle secrets findings
# For test fixtures: Add to .sentinelpolicy
python scripts/generate-sentinelpolicy.py --key SUPPRESSION_KEY --reason "Test fixture - mock JWT"

# For real secrets: Rotate immediately and move to environment variables

# 5. Generate audit report
# Use findings to create comprehensive security audit report
```

### CI/CD Integration

```yaml
# .github/workflows/security.yml (example for external repos)
name: Security Audit
on: [pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Security Audit
        run: python .claude/skills/security-review/scripts/security-audit.py

      - name: Find Secrets
        run: python .claude/skills/security-review/scripts/find-secrets.py

      - name: Dependency Audit
        run: |
          npm audit --audit-level=high
          pip-audit
```

### Secrets Scanner Response

```bash
# 1. Review notification
# Copy suppression key from email/notification

# 2. Verify it's a false positive
# Check if it's test fixture, not real secret

# 3. Add to .sentinelpolicy
python scripts/generate-sentinelpolicy.py \
  --key ae4b93f9d \
  --reason "Test fixture - mock JWT tokens in conftest.py for auth testing"

# 4. Audit .sentinelpolicy
python scripts/generate-sentinelpolicy.py --audit

# 5. Commit and push
git add .sentinelpolicy
git commit -m "chore: add secrets scanner suppression for test fixtures"
git push
```

## Best Practices

### Security Review Approach

1. **Automated first** - Run automated tools to catch low-hanging fruit
2. **Manual review** - Deep dive into business logic and architecture
3. **Threat modeling** - Think like an attacker
4. **Document everything** - Create clear, actionable findings
5. **Prioritize** - Critical and High findings first
6. **Verify fixes** - Re-scan after remediation

### Secrets Management

**Valid reasons to suppress:**
- ✅ Test fixtures and mock data
- ✅ Example data in documentation/docstrings
- ✅ Dummy tokens for unit tests
- ✅ Redacted values used in test validation

**NEVER suppress:**
- ❌ Real API keys
- ❌ Actual passwords
- ❌ Production credentials
- ❌ Service account tokens

### Tool Selection

- **suppressionkey** - Recommended for test fixtures (survives refactoring)
- **safeline** - Specific lines (breaks on line number changes)
- **safefile** - Avoid unless absolutely necessary (too broad)

## Exit Codes

All scripts follow consistent exit code patterns:

- `0` - Success, no issues found
- `1` - Issues detected (critical/high findings, secrets requiring review)

Use in CI/CD pipelines to fail builds on security issues.

## Requirements

- Python 3.8+
- No external dependencies (uses Python standard library only)
- Optional: jq for JSON processing in examples

## Support

For questions or issues:
- Review documentation in `~/.claude/docs/security/`
- Check OWASP references: https://owasp.org/Top10/
- Enterprise Security Portal

## License

Part of Cameron's Claude Code configuration.
