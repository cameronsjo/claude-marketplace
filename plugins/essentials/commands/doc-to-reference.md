---
description: Convert PDFs, URLs, or documents into Obsidian-compatible reference documentation
argument-hint: "<pdf-path|url|document-description>"
allowed-tools: Bash, Read, Write, Edit, WebFetch
disable-model-invocation: true
---

# Process Document into Reference Library

Convert PDFs, URLs, or documents into Obsidian-compatible reference documentation for the zen security library.

## Arguments

- `$ARGUMENTS` - Path to PDF file, URL, or document description

## Workflow

### 1. Determine Source Type

Based on `$ARGUMENTS`:

- **PDF file path** → Use `pdftotext` to extract, then read in chunks (600-1000 lines)
- **URL** → Use WebFetch to retrieve content
- **GitHub repo URL** → Fetch README and relevant specs from raw.githubusercontent.com

### 2. Analyze Content

Identify document type and extract:

- **Title and version**
- **Core concepts** (what problem does it solve?)
- **Architecture** (components, data flow)
- **Key specifications** (message types, APIs, protocols)
- **Security considerations**
- **Implementation guidance**
- **Code examples** (preserve with language hints)

### 3. Create Reference Document

Write to: `docs/references/<document-name>.md`

**Required structure:**

```markdown
---
title: "Document Title"
aliases:
  - short-name
  - alternative-name
tags:
  - relevant-tag
  - domain-tag
source: "URL or citation"
spec_version: "X.Y" (if applicable)
created: YYYY-MM-DD
status: active
---

# Document Title

> **One-line summary** - What this document covers.

---

## Overview

2-3 paragraphs explaining the document's purpose and relevance.

---

## [Core Sections]

Use Mermaid diagrams for:
- Architecture (graph TB/LR)
- Sequences (sequenceDiagram)
- State machines (stateDiagram-v2)

Use GFM tables for:
- Configuration options
- API endpoints
- Error codes
- Comparisons

---

## zen Platform Relevance

How does this relate to the zen platform?
- Integration points with existing components
- Applicability to Apple/Banana agents, MCP servers
- Considerations or limitations

---

## Related Documents

- [[related-doc-1]] - Brief description
- [[related-doc-2]] - Brief description

---

## References

- [Source Link](url)
- [Related Spec](url)

---

## Key Takeaways

1. Numbered list
2. Of main insights
3. From this document
```

### 4. Update INDEX

Add entry to `docs/references/00-INDEX.md`:

1. Find appropriate section (Security, Identity, Protocols, Implementation, etc.)
2. Add wiki-link with brief description and tags
3. Update Statistics section if needed
4. Add to "Recent Additions" section

### 5. Verify Obsidian Compatibility

Ensure document uses:

- GFM-compatible tables (not Obsidian-only)
- Mermaid diagrams (renders in both GitHub and Obsidian)
- Wiki links for internal references (`[[doc-name]]`)
- Standard markdown for external links (`[text](url)`)
- Frontmatter with proper YAML types

## PDF Processing Strategy

For large PDFs that exceed read limits:

```bash
# Extract to text
pdftotext -layout "/path/to/document.pdf" "/tmp/document.txt"

# Check size
wc -l /tmp/document.txt
```

Then read in chunks:

- First pass: Lines 1-800 (overview, TOC, intro)
- Second pass: Lines 800-1600 (core content)
- Continue as needed...

## Quality Checklist

Before completing:

- [ ] Frontmatter complete with title, tags, source, created date
- [ ] Mermaid diagrams for any architecture/flow descriptions
- [ ] Tables for structured data (not prose lists)
- [ ] zen Platform Relevance section addresses applicability
- [ ] Related Documents section links to existing refs
- [ ] INDEX updated with new entry
- [ ] No Obsidian-only syntax that breaks GitHub rendering

## Example Invocations

```
/doc-to-reference /path/to/security-spec.pdf
/doc-to-reference https://github.com/org/repo
/doc-to-reference https://example.com/whitepaper.html
```

## Target Location

All reference docs go to:
`~/projects/example/docs/references/`

## Scope Filter

**IN SCOPE** for zen security library:

- MCP security, attacks, defenses
- Zero-trust, identity, authentication
- Agent architecture, multi-agent patterns
- Protocol specifications (A2A, MCP, OAuth)
- Kubernetes security, deployment patterns
- Post-quantum cryptography

**OUT OF SCOPE** (suggest alternative location):

- Business/market research
- General adoption trends
- Large-scale infrastructure economics (zen is laptop-scale)
- Legacy modernization (zen is greenfield)

If document is out of scope, suggest moving to `~/Projects/industry-research/` instead.
