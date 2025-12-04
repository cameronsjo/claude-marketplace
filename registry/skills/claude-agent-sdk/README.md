# Claude Agent SDK Skill

A comprehensive skill for building AI agents with the Claude Agent SDK in both TypeScript and Python.

## Overview

This skill provides:
- Complete API reference for both Python and TypeScript SDKs
- Feature parity comparison between Claude Code CLI and SDK
- Working code examples for common patterns
- Best practices for agent development

## Contents

- **SKILL.md** - Main skill documentation with API reference
- **resources/feature-parity.md** - Detailed comparison between CLI and SDK
- **examples/** - Working code examples:
  - `quick_start.py` - Basic Python usage
  - `multi_turn.py` - Multi-turn conversations in Python
  - `custom_tools.py` - Custom MCP tools in Python
  - `quick_start.ts` - Basic TypeScript usage
  - `custom_tools.ts` - Custom MCP tools in TypeScript

## Quick Start

### Python

```bash
pip install claude-agent-sdk
```

```python
from claude_agent_sdk import query

async for message in query(prompt="Hello, Claude!"):
    print(message)
```

### TypeScript

```bash
npm install @anthropic-ai/claude-agent-sdk
```

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({ prompt: "Hello, Claude!" })) {
    console.log(message);
}
```

## Official Resources

- [SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK GitHub](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK GitHub](https://github.com/anthropics/claude-agent-sdk-typescript)
