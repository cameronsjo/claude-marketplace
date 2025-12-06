---
description: Security audit (OWASP Top 10, secrets, vulnerabilities)
category: review
argument-hint: [file or directory]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Security Review

Comprehensive security audit covering OWASP Top 10, AI/MCP security, and secrets management.

## Usage

Review entire codebase:
```
/security-review
```

Review specific file:
```
/security-review src/auth/login.ts
```

Review directory:
```
/security-review src/api/
```

## What This Command Does

This command uses the security-review skill to conduct thorough security audits.

### Step 1: Activate security review skill

Invoke the skill for comprehensive security analysis:
```
Use the security-review skill to conduct a security audit.
```

### Step 2: Gather context

Collect information about the application:

**Questions to ask (if not obvious from code):**
1. Application type: Web app, API, MCP server, CLI tool?
2. Technology stack: Languages, frameworks, dependencies?
3. Deployment environment: Kubernetes, cloud, on-prem?
4. Authentication mechanisms: JWT, OAuth, API keys?
5. Data sensitivity: PII, credentials, financial data?

**Auto-detect from codebase:**
- Language: Check file extensions, package files
- Framework: Look for imports, config files
- Auth patterns: Search for JWT, OAuth, session code
- Secrets locations: `.env`, config files

### Step 3: Define scope

Determine what to review:

**If path provided:**
- Single file: Review that file
- Directory: Scan all files in directory
- No path: Review entire project (current directory)

**File types to scan:**
- Source code: `.js`, `.ts`, `.py`, `.go`, `.java`, `.cs`, `.rb`
- Config files: `.env`, `.yaml`, `.json`, `config.*`
- Infrastructure: `Dockerfile`, `docker-compose.yml`, `*.tf`
- Dependencies: `package.json`, `requirements.txt`, `go.mod`

### Step 4: Run OWASP Top 10 audit

Systematically check each OWASP Top 10 category:

#### A01:2021 - Broken Access Control

**Check for:**
- Missing authorization checks
- Insecure direct object references
- Missing rate limiting
- JWT tokens not invalidated on logout
- Directory listing enabled

**Search patterns:**
```python
# Authorization decorators/middleware
@require_auth, @authorize, check_permission, verify_access

# JWT handling
jwt.decode, jwt.verify, validateToken

# Rate limiting
@rate_limit, throttle, rateLimit
```

**Report:**
- Missing authorization on endpoints
- Weak or missing rate limits
- JWT handling issues

#### A02:2021 - Cryptographic Failures

**Check for:**
- Hardcoded secrets
- Weak encryption algorithms
- Insecure key storage
- Missing TLS/SSL
- Sensitive data in logs

**Search patterns:**
```python
# Hardcoded secrets
password\s*=\s*["'], api[_-]?key\s*=\s*["'], secret\s*=\s*["']

# Weak crypto
MD5, SHA1, DES, RC4

# Key management
process.env, os.environ, hardcoded keys
```

**Run secrets scanner:**
```bash
# If scripts exist
python ~/.claude/skills/security-review/scripts/find-secrets.py .
```

**Report:**
- Hardcoded credentials found
- Weak crypto algorithm usage
- Insecure key management

#### A03:2021 - Injection

**Check for:**
- SQL injection vulnerabilities
- Command injection
- NoSQL injection
- LDAP injection
- XPath injection

**Search patterns:**
```python
# SQL injection risks
raw SQL queries, string concatenation in queries
execute("SELECT * FROM users WHERE id=" + user_input)

# Command injection
subprocess.call, exec, eval, os.system
child_process.exec, shell=True

# NoSQL injection
MongoDB find/update with unvalidated input
```

**Report:**
- Unvalidated input in queries
- Dynamic code execution
- Command injection risks

#### A04:2021 - Insecure Design

**Check for:**
- Missing security requirements
- Lack of threat modeling
- Insufficient security controls
- Business logic flaws

**Analyze:**
- Authentication flow completeness
- Authorization model design
- Rate limiting strategy
- Input validation coverage

#### A05:2021 - Security Misconfiguration

**Check for:**
- Default credentials
- Unnecessary features enabled
- Detailed error messages to users
- Missing security headers
- Outdated dependencies

**Search patterns:**
```python
# Default creds
admin/admin, root/root, test/test

# Debug mode
DEBUG=True, NODE_ENV=development in production

# Verbose errors
stack traces, detailed error messages in responses
```

**Report:**
- Debug mode enabled
- Missing security headers
- Default configurations

#### A06:2021 - Vulnerable and Outdated Components

**Check dependencies:**
```bash
# Node.js
npm audit

# Python
pip-audit
# or
safety check

# Go
go list -json -m all | nancy sleuth

# Ruby
bundle audit
```

**Report:**
- CVEs in dependencies
- Outdated critical packages
- Unmaintained dependencies

#### A07:2021 - Identification and Authentication Failures

**Check for:**
- Weak password policies
- Missing MFA
- Credential stuffing protection
- Session management flaws
- Insecure password recovery

**Search patterns:**
```python
# Password handling
bcrypt, argon2, PBKDF2 (good)
plain text passwords, MD5 passwords (bad)

# Session management
session timeout, secure cookies, httpOnly flags
```

**Report:**
- Weak password hashing
- Missing account lockout
- Insecure session handling

#### A08:2021 - Software and Data Integrity Failures

**Check for:**
- Unsigned packages/artifacts
- Insecure deserialization
- Missing integrity checks
- Auto-update without verification

**Search patterns:**
```python
# Deserialization
pickle.loads, eval, exec
JSON.parse on untrusted data
```

#### A09:2021 - Security Logging and Monitoring Failures

**Check for:**
- Missing audit logs
- No alerting on suspicious activity
- Sensitive data in logs
- Insufficient log retention

**Search patterns:**
```python
# Logging
logger, console.log, print statements
Check: Are auth failures logged?
Check: Are access attempts logged?
```

**Report:**
- Missing security event logs
- Sensitive data exposure in logs
- No monitoring/alerting

#### A10:2021 - Server-Side Request Forgery (SSRF)

**Check for:**
- User-controlled URLs
- Missing URL validation
- Internal service access

**Search patterns:**
```python
# HTTP requests with user input
requests.get(user_url)
fetch(user_provided_url)
axios.get(untrusted_url)
```

### Step 5: AI/MCP-specific security (if applicable)

If MCP server or AI integration detected:

**Check for:**
- Prompt injection vulnerabilities
- Missing input/output validation
- Insufficient rate limiting
- PII in prompts/logs
- Model access controls
- Audit logging

**MCP-specific:**
- Tool validation
- Resource access controls
- Permission boundaries
- Sandbox escapes

### Step 6: Generate security report

Create structured security report:

**Executive Summary:**
```markdown
# Security Audit Report

**Date:** YYYY-MM-DD
**Scope:** [files/directories reviewed]
**Critical Issues:** N
**High Severity:** N
**Medium Severity:** N
**Low Severity:** N
```

**Critical Issues (Fix Immediately):**
- Hardcoded secrets
- SQL injection vulnerabilities
- Missing authentication
- Weak cryptography

**High Severity (Fix Soon):**
- Missing authorization checks
- Command injection risks
- Insecure deserialization
- Outdated vulnerable dependencies

**Medium Severity:**
- Missing rate limiting
- Weak password policies
- Security misconfiguration
- Missing security headers

**Low Severity / Recommendations:**
- Improve logging
- Add security documentation
- Enhance monitoring

**Findings Detail:**

For each issue:
```markdown
### [CRITICAL/HIGH/MEDIUM/LOW] Issue Title

**Location:** file.py:123
**OWASP Category:** A03:2021 - Injection
**CWE:** CWE-89 (SQL Injection)

**Description:**
User input directly concatenated into SQL query without validation.

**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Impact:**
Attacker can inject SQL to access unauthorized data, modify records, or execute commands.

**Remediation:**
Use parameterized queries:
```python
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

**References:**
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
```

### Step 7: Prioritize remediation

Provide remediation roadmap:

**Phase 1 (Immediate - Critical):**
1. Remove hardcoded secrets
2. Fix SQL injection vulnerabilities
3. Add authentication to unprotected endpoints

**Phase 2 (This Sprint - High):**
1. Add authorization checks
2. Update vulnerable dependencies
3. Implement rate limiting

**Phase 3 (Next Sprint - Medium):**
1. Add security headers
2. Improve password policies
3. Enhance logging

**Phase 4 (Backlog - Low):**
1. Security documentation
2. Monitoring improvements
3. Security training

### Step 8: Provide fix examples

For common issues, provide complete fix examples:

**SQL Injection Fix:**
```python
# Before (vulnerable)
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")

# After (secure)
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

**Hardcoded Secret Fix:**
```python
# Before (vulnerable)
API_KEY = "sk-1234567890abcdef"

# After (secure)
import os
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")
```

**Command Injection Fix:**
```python
# Before (vulnerable)
os.system(f"ping {user_host}")

# After (secure)
import subprocess
subprocess.run(["ping", user_host], check=True, timeout=5)
```

## Security Scanning Tools

Recommend and run automated tools:

**Secrets Scanning:**
```bash
# trufflehog
trufflehog filesystem . --json

# gitleaks
gitleaks detect --source . --verbose
```

**Dependency Scanning:**
```bash
# Node.js
npm audit --json

# Python
pip-audit --format json
```

**SAST (if available):**
```bash
# Semgrep
semgrep --config auto .

# Bandit (Python)
bandit -r src/ -f json
```

## Output Options

**Console output:**
- Summary statistics
- Critical issues highlighted
- Remediation priorities

**Detailed report file:**
- Full markdown report
- Saved to `security-audit-report.md`
- Include code examples and references

**JSON output (for CI/CD):**
- Machine-readable format
- Severity levels
- File locations and line numbers

## Verification Checklist

After review, verify:
- [ ] All OWASP Top 10 categories checked
- [ ] Secrets scanning completed
- [ ] Dependency vulnerabilities identified
- [ ] Authentication/authorization validated
- [ ] Input validation reviewed
- [ ] Cryptography assessed
- [ ] Logging and monitoring checked
- [ ] Report generated with remediation plan

---

**Last Updated:** 2025-11-13
**Framework:** OWASP Top 10 2021
**Standards:** OWASP Security Guidelines
