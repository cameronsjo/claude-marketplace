---
description: Convert PDFs, URLs, or documents into structured markdown reference docs
argument-hint: "<pdf-path|url> [output-path]"
allowed-tools: Bash, Read, Write, Edit, WebFetch
---

# Convert Document to Reference

Convert PDFs, articles, URLs, or documents into clean, structured markdown reference documentation.

## Arguments

- `$ARGUMENTS` - Path to PDF file, URL, or document. Optionally followed by output path.

## Workflow

### 1. Determine Source Type

Based on input:

- **PDF file** → Extract with `pdftotext`, read in chunks
- **URL** → Use WebFetch to retrieve content
- **GitHub repo** → Fetch README from raw.githubusercontent.com

### 2. Extract & Analyze

Identify and extract:

- **Title and version** (if applicable)
- **Core concepts** - What problem does it solve?
- **Architecture** - Components, data flow
- **Key specifications** - APIs, protocols, message types
- **Implementation guidance**
- **Code examples** - Preserve with language hints

### 3. Create Reference Document

Write to specified path or `docs/references/<document-name>.md`

**Structure:**

```markdown
---
title: "Document Title"
aliases:
  - short-name
tags:
  - domain-tag
source: "URL or citation"
created: YYYY-MM-DD
---

# Document Title

> **One-line summary** - What this document covers.

## Overview

2-3 paragraphs explaining purpose and relevance.

## [Core Sections]

Extracted content organized logically.

Use Mermaid diagrams for:
- Architecture (graph TB/LR)
- Sequences (sequenceDiagram)
- State machines (stateDiagram-v2)

Use tables for:
- Configuration options
- API endpoints
- Comparisons

## Key Takeaways

1. Main insights
2. From this document

## References

- [Source](url)
- [Related](url)
```

## PDF Processing

For large PDFs:

```bash
# Extract to text
pdftotext -layout "/path/to/doc.pdf" "/tmp/doc.txt"

# Check size
wc -l /tmp/doc.txt
```

Read in chunks (600-1000 lines per pass):
- First: Overview, TOC, intro
- Second: Core content
- Continue as needed

## Quality Checklist

- [ ] Frontmatter with title, tags, source, date
- [ ] Mermaid diagrams for architecture/flows
- [ ] Tables for structured data
- [ ] Code blocks with language hints
- [ ] Clean markdown (no platform-specific syntax)

## Examples

```
/doc-to-reference /path/to/whitepaper.pdf
/doc-to-reference https://example.com/article
/doc-to-reference https://github.com/org/repo docs/repo-overview.md
```
