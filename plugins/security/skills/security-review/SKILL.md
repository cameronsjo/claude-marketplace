# Security Review Skill

Conduct comprehensive security audits covering OWASP Top 10, AI/MCP security, secrets management, and secrets management.

## Objective

Identify security vulnerabilities, validate secure coding practices, and provide actionable remediation guidance.

## Security Standards

### Core Principles

- **Secure-by-default**: All systems must be secure out-of-the-box; security features enabled by default with explicit opt-outs only when necessary
- **Secure-by-design**: Build security into architecture from start; defense-in-depth, least privilege, fail-safe defaults
- Never commit secrets - use environment variables for configuration
- Validate and sanitize all input

### OWASP Top 10 Web

Validate against current OWASP Top 10:
- Injection
- Broken authentication
- Sensitive data exposure
- XXE (XML External Entities)
- Broken access control
- Security misconfiguration
- XSS (Cross-Site Scripting)
- Insecure deserialization
- Components with known vulnerabilities
- Insufficient logging & monitoring

### AI/MCP Security

For AI/LLM features and MCP servers:
- Prompt injection prevention
- Input/output validation
- Rate limiting
- PII protection
- Model access controls
- Audit logging

## Security Review Process

### 1. Initial Assessment

Gather context about the application:
- Application type (web, API, MCP server, CLI tool)
- Technology stack (languages, frameworks, dependencies)
- Deployment environment (Kubernetes, cloud, on-prem)
- Authentication/authorization mechanisms
- Data handling (PII, credentials, sensitive data)

### 2. OWASP Top 10 Web Audit

Review the codebase against OWASP Top 10 2021:

#### A01:2021 - Broken Access Control
- Verify least privilege and deny-by-default enforcement
- Check server-side access control implementation
- Review JWT token invalidation on logout
- Validate rate limiting on API endpoints
- Test directory listing and metadata file exposure
- Verify access control failure logging

**Search patterns:**
- Authorization checks: `@require`, `@authorize`, `check_permission`, `verify_access`
- JWT handling: `jwt.decode`, `jwt.verify`, `validateToken`
- Rate limiting: `rateLimit`, `throttle`, `@limit`

#### A02:2021 - Cryptographic Failures
- Verify data classification and appropriate controls
- Check TLS configuration (1.2+)
- Review encryption algorithms (no MD5/SHA1)
- Validate key management practices
- Check for hardcoded secrets
- Verify sensitive data caching disabled

**Search patterns:**
- Hardcoded secrets: Run `scripts/find-secrets.py`
- Weak crypto: `MD5`, `SHA1`, `DES`, `RC4`
- Key management: `process.env`, `os.environ`, hardcoded keys

#### A03:2021 - Injection
- Verify parameterized queries and ORMs
- Check input validation (allow-list preferred)
- Review SQL controls and LIMIT clauses
- For AI/LLM: validate prompt handling and output sanitization
- Check escape sequences in queries

**Search patterns:**
- SQL injection risks: raw queries, string concatenation
- Command injection: `exec`, `eval`, `subprocess.call` with user input
- Prompt injection: LLM input without validation

#### A04:2021 - Insecure Design
- Review threat modeling documentation
- Check secure design patterns implementation
- Verify tenant segregation in multi-tenant systems
- Validate resource consumption limits
- Review architecture documentation

**Manual review required** - check design documents and architecture diagrams.

#### A05:2021 - Security Misconfiguration
- Verify repeatable hardening process
- Check minimal platform configuration
- Review cloud storage permissions
- Verify default accounts disabled
- Check error message handling
- Validate security patch status

**Search patterns:**
- Error leakage: stack traces, detailed errors in production
- Default configs: `default_password`, `admin/admin`, `root/root`
- Debug mode: `DEBUG=true`, `NODE_ENV=development` in production

#### A06:2021 - Vulnerable and Outdated Components
- Inventory all dependencies
- Check for unused dependencies
- Run vulnerability scanners
- Verify security bulletins subscription
- Validate package sources and signatures

**Tools:**
- `npm audit` or `npm audit --json`
- `pip-audit` or `uv pip audit`
- Dependabot/Snyk alerts
- Check package.json/requirements.txt for outdated versions

#### A07:2021 - Identification and Authentication Failures
- Verify MFA implementation
- Check for default credentials
- Review password complexity requirements
- Validate rate limiting and brute force protection
- Check session management (HTTPOnly, Secure, SameSite)
- Verify session invalidation on logout

**Search patterns:**
- Session handling: `session`, `cookie`, `Set-Cookie`
- Auth implementation: custom vs established libraries
- Password handling: plaintext storage, weak hashing

#### A08:2021 - Software and Data Integrity Failures
- Verify digital signatures for software/data
- Check dependency integrity verification
- Review CI/CD pipeline security
- Validate auto-update mechanisms
- Check deserialization security

**Search patterns:**
- Deserialization: `pickle.loads`, `JSON.parse`, `yaml.load`
- CI/CD configs: `.github/workflows`, Looper configs
- Package lock files: integrity hashes present

#### A09:2021 - Security Logging and Monitoring Failures
- Verify authentication/authorization failure logging
- Check structured logging implementation
- Validate log storage security
- Review audit trail for high-value transactions
- Check monitoring and alerting setup

**Search patterns:**
- Logging: `logger`, `console.log`, `print` (ensure structured)
- Sensitive data in logs: passwords, tokens in log statements

#### A10:2021 - Server-Side Request Forgery (SSRF)
- Verify URL validation and sanitization
- Check URL schema/port/destination allow-lists
- Validate HTTP redirection handling
- Check raw response handling
- Verify network segmentation

**Search patterns:**
- HTTP requests with user input: `fetch`, `axios`, `requests.get`
- URL construction: user-controlled URLs

### 3. AI/MCP Security Audit

For applications using AI/LLM or implementing MCP servers:

#### Prompt Injection Prevention
- Validate user input sanitization before LLM
- Check instruction/data separation patterns
- Verify output validation and filtering
- Review monitoring for jailbreak attempts

**Search patterns:**
- LLM calls: `openai`, `anthropic`, `completion`, `generate`
- User input to prompts: direct concatenation without validation

#### MCP Server Security
- Verify MCP client authentication
- Check tool parameter validation
- Validate resource URI handling
- Review rate limiting per client
- Check audit logging for tool invocations
- Verify least privilege for tool capabilities
- Validate sampling request data handling

**Search patterns:**
- MCP server implementation: `@mcp/server`, tool handlers
- Authentication: connection validation
- Tool parameters: validation logic

#### Data Privacy
- Verify PII handling and consent
- Check data anonymization/pseudonymization
- Validate data retention policies
- Review audit trail for data sent to models

**Search patterns:**
- PII detection: email, SSN, phone, address patterns
- External API calls: data sent to LLM providers


- Review latest CodeGate scan results
- Prioritize Critical, High, Medium findings (build blockers)
- Validate false positive marking with clear comments
- Document non-exploitable findings properly

**Note:** CodeGate findings cannot be downgraded, only marked as "Non Exploitable" with explanation.

## Automated Tools

### Security Audit Script

Run comprehensive security checks:
```bash
python scripts/security-audit.py [--path PATH] [--output report.json]
```

Checks:
- Hardcoded secrets detection
- Weak cryptography patterns
- SQL injection risks
- Command injection risks
- Insecure deserialization
- Security misconfigurations
- Vulnerable dependencies

### OWASP Checklist Runner

Interactive checklist for manual review:
```bash
python scripts/owasp-checklist.py
```

Walks through OWASP Top 10 with file-specific guidance.

### Secrets Scanner

Find potential secrets:
```bash
python scripts/find-secrets.py [--path PATH] [--output findings.json]
```

### Sentinel Policy Generator

Generate `.sentinelpolicy` entries:
```bash
python scripts/generate-sentinelpolicy.py --key SUPPRESSION_KEY --reason "Explanation"
```

## Deliverables

### Security Audit Report

Create a comprehensive report:

```markdown
# Security Audit Report - [Project Name]

**Date:** YYYY-MM-DD
**Auditor:** [Name]
**Scope:** [Description]

## Executive Summary

[High-level overview of findings]

## Critical Findings

### Finding 1: [Title]
- **Severity:** Critical/High/Medium/Low
- **Category:** [OWASP Category]
- **Location:** [File:Line]
- **Description:** [What was found]
- **Impact:** [Security impact]
- **Remediation:** [How to fix]
- **References:** [Links to docs/standards]

## OWASP Top 10 Checklist

- [x] A01: Broken Access Control - PASS
- [ ] A02: Cryptographic Failures - 2 findings
- ...

## AI/MCP Security (if applicable)

[Findings specific to AI/MCP]

## Secrets Management

[Review of .sentinelpolicy, findings from secrets scanner]

## Recommendations

1. [Priority recommendation]
2. [Next recommendation]
...

## Conclusion

[Overall security posture assessment]
```

### Remediation Tracking

For each finding, create GitHub issues:
```markdown
## Security: [Title]

**Severity:** Critical/High/Medium/Low
**Category:** [OWASP Category]

**Description:**
[Detailed explanation]

**Impact:**
[Security implications]

**Remediation:**
```python
# Before (vulnerable)
query = f"SELECT * FROM users WHERE id = {user_id}"

# After (secure)
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

**References:**
- OWASP Top 10: [Link]
- CWE: [Link]

**Labels:** security, [severity]
```

## Best Practices

### Review Approach

1. **Automated first:** Run automated tools to catch low-hanging fruit
2. **Manual review:** Deep dive into business logic and architecture
3. **Threat modeling:** Think like an attacker
4. **Document everything:** Create clear, actionable findings
5. **Prioritize:** Critical and High findings first
6. **Verify fixes:** Re-scan after remediation

### Communication

- Be clear and specific about vulnerabilities
- Provide context and impact assessment
- Offer concrete remediation guidance with code examples
- Link to authoritative references (OWASP, CWE)
- Avoid security theater - focus on real risks

### False Positives

- Validate before reporting
- Understand the context (test vs production code)
- Document why something is safe
- Use proper suppression mechanisms

## Resources

### Documentation
- `~/.claude/docs/security/owasp-top-10.md`
- `~/.claude/docs/security/codegate-checkmarx.md`
- `Security scanning documentation`

### Tools
- `scripts/security-audit.py` - Automated security scanning
- `scripts/find-secrets.py` - Secrets detection
- `scripts/generate-sentinelpolicy.py` - Sentinel policy management
- `scripts/owasp-checklist.py` - Interactive checklist

### External References
- OWASP Top 10 2021: https://owasp.org/Top10/
- OWASP AI Security: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- CWE Top 25: https://cwe.mitre.org/top25/
- OWASP: https://owasp.org/

## Usage

Invoke this skill when:
- Conducting security code reviews
- Auditing new or existing applications
- Responding to security scan findings
- Creating `.sentinelpolicy` suppressions
- Validating secure coding practices
- Preparing for security assessments
- Investigating potential vulnerabilities

The skill provides systematic security review methodology with automated tools and actionable guidance.
