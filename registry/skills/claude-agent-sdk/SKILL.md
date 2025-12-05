---
name: claude-agent-sdk
description: Comprehensive guide for building AI agents with the Claude Agent SDK in TypeScript and Python, including feature parity with Claude Code CLI.
---

# Claude Agent SDK Development Guide

## Overview

The **Claude Agent SDK** is a programmatic library that enables developers to build AI agents with Claude Code's capabilities. It provides the same agent harness that powers Claude Code itself, allowing you to create autonomous agents that can understand codebases, edit files, run commands, and execute complex workflows.

## When to Use This Skill

- Building programmatic AI agents with Claude capabilities
- Creating CLI tools or backend services powered by Claude
- Integrating Claude Code functionality into applications
- Developing custom tools with MCP (Model Context Protocol)
- Understanding feature parity between Claude Code CLI and SDK

---

## Installation

### Python

```bash
pip install claude-agent-sdk
```

**Requirements:** Python 3.10+

### TypeScript/Node.js

```bash
npm install @anthropic-ai/claude-agent-sdk
```

**Requirements:** Node.js 18+

---

## Authentication

Set your API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Alternative Providers

```bash
# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1

# Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
```

---

## Core API Reference

### Python SDK

#### `query()` Function

Simple async interface for stateless queries:

```python
import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful coding assistant",
        allowed_tools=["Read", "Write", "Bash"],
        permission_mode="acceptEdits",
        cwd="/path/to/project"
    )

    async for message in query(prompt="Create a hello world script", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)

anyio.run(main)
```

#### `ClaudeSDKClient` Class

Bidirectional, stateful client for multi-turn conversations:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a code reviewer",
        allowed_tools=["Read", "Grep", "Bash"],
        permission_mode="acceptEdits"
    )

    async with ClaudeSDKClient(options=options) as client:
        # First turn
        await client.query("Review the auth module")
        async for message in client.receive_messages():
            if message.type == "result":
                break

        # Second turn - context preserved
        await client.query("Now check for security issues")
        async for message in client.receive_messages():
            if message.type == "result":
                break
```

### TypeScript SDK

#### `query()` Function

```typescript
import { query, type ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

async function main() {
    const options: ClaudeAgentOptions = {
        systemPrompt: "You are a TypeScript expert",
        allowedTools: ["Read", "Write", "Bash"],
        permissionMode: "acceptEdits",
        cwd: "/path/to/project"
    };

    const stream = query({ prompt: "Create an Express server", options });

    for await (const message of stream) {
        if (message.type === "assistant") {
            for (const block of message.message.content) {
                if (block.type === "text") {
                    console.log(block.text);
                }
            }
        }
    }
}
```

#### `ClaudeSDKClient` Class

```typescript
import { ClaudeSDKClient, type ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

async function main() {
    const options: ClaudeAgentOptions = {
        systemPrompt: "You are a full-stack developer",
        allowedTools: ["Read", "Write", "Bash", "Grep"],
        permissionMode: "acceptEdits"
    };

    const client = new ClaudeSDKClient(options);
    await client.connect();

    try {
        await client.query("Create a REST API endpoint");
        for await (const msg of client.receiveMessages()) {
            if (msg.type === "result") break;
            console.log(msg);
        }
    } finally {
        await client.disconnect();
    }
}
```

---

## ClaudeAgentOptions Reference

### Python Options

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    # System prompt for the agent
    system_prompt="You are a helpful assistant",

    # Tool access control
    allowed_tools=["Read", "Write", "Bash", "Grep", "Glob"],

    # Permission mode: "acceptEdits" auto-accepts file changes
    permission_mode="acceptEdits",

    # Working directory
    cwd="/path/to/project",

    # Maximum conversation turns
    max_turns=10,

    # Session management
    resume_session="session-id",  # Resume existing session
    fork_session=True,            # Fork from session

    # Load project settings (.claude/settings.json, CLAUDE.md, etc.)
    setting_sources=["project", "local"],

    # MCP servers for custom tools
    mcp_servers=[mcp_server_instance],

    # Custom tool filtering
    can_use_tool=lambda name: name != "Bash",

    # Hooks for workflow automation
    hooks={
        "PreToolUse": [hook_config],
        "PostToolUse": [hook_config]
    },

    # Custom CLI path (optional)
    cli_path="/custom/path/to/claude"
)
```

### TypeScript Options

```typescript
interface ClaudeAgentOptions {
    systemPrompt?: string;
    allowedTools?: string[];
    disallowedTools?: string[];
    permissionMode?: "acceptEdits" | "manual";
    cwd?: string;
    maxTurns?: number;
    resumeSession?: string;
    forkSession?: boolean;
    settingSources?: string[];
    mcpServers?: MCP[];
    canUseTool?: (toolName: string) => boolean;
}
```

---

## Available Tools

The SDK provides access to Claude Code's built-in tools:

| Tool | Description | Permission |
|------|-------------|------------|
| `Read` | Read file contents | No |
| `Write` | Create/overwrite files | Yes |
| `Edit` | Make targeted edits | Yes |
| `Bash` | Execute shell commands | Yes |
| `Grep` | Search file contents | No |
| `Glob` | Pattern-based file matching | No |
| `WebFetch` | Fetch web content | Yes |
| `WebSearch` | Search the web | Yes |
| `Task` | Run sub-agents | No |
| `NotebookEdit` | Modify Jupyter notebooks | Yes |

---

## Custom Tools with MCP

### Python In-Process MCP Server

```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions

@tool("get_weather", "Get weather for a location", {"location": str})
async def get_weather(args):
    location = args["location"]
    # Your implementation here
    return {"content": [{"type": "text", "text": f"Sunny in {location}, 72°F"}]}

@tool("save_note", "Save a note", {"title": str, "content": str})
async def save_note(args):
    # Your implementation
    return {"content": [{"type": "text", "text": f"Note '{args['title']}' saved"}]}

# Create MCP server
server = create_sdk_mcp_server(
    name="my-tools",
    version="1.0.0",
    tools=[get_weather, save_note]
)

# Use in options
options = ClaudeAgentOptions(
    allowed_tools=[
        "Read", "Write",
        "mcp__my-tools__get_weather",
        "mcp__my-tools__save_note"
    ],
    mcp_servers=[server]
)
```

### TypeScript Custom Tools

```typescript
import { createSdkMcpServer, tool, type ClaudeAgentOptions } from '@anthropic-ai/claude-agent-sdk';

const weatherTool = tool({
    name: "get_weather",
    description: "Get weather for a location",
    inputSchema: {
        type: "object",
        properties: {
            location: { type: "string", description: "City name" }
        },
        required: ["location"]
    },
    execute: async (input: { location: string }) => {
        return `Weather in ${input.location}: Sunny, 72°F`;
    }
});

const mcp = createSdkMcpServer({
    name: "my-tools",
    tools: [weatherTool]
});

const options: ClaudeAgentOptions = {
    mcpServers: [mcp],
    allowedTools: ["Read", "Write", "mcp__my-tools__get_weather"]
};
```

### External MCP Servers

Configure in `.mcp.json`:

```json
{
    "mcpServers": {
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {
                "GITHUB_TOKEN": "${GITHUB_TOKEN}"
            }
        },
        "postgres": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": {
                "POSTGRES_URL": "${DATABASE_URL}"
            }
        }
    }
}
```

---

## Session Management

### Resuming Sessions

```python
# Get session ID from first interaction
async with ClaudeSDKClient() as client:
    await client.query("Start a project")
    session_id = await client.get_session_id()

# Later: resume the session
async with ClaudeSDKClient() as client:
    await client.query(
        "Continue where we left off",
        resume_session=session_id
    )
```

### Forking Sessions

```python
# Create a branch from existing conversation
async with ClaudeSDKClient() as client:
    await client.query(
        "Try an alternative approach",
        resume_session=session_id,
        fork_session=True  # Creates new branch
    )
```

---

## Message Types

### Python

```python
from claude_agent_sdk import (
    AssistantMessage,
    UserMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock
)

async for message in query(prompt="Hello"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                print("Text:", block.text)
            elif isinstance(block, ToolUseBlock):
                print("Tool:", block.name)
    elif isinstance(message, ResultMessage):
        print("Done:", message.subtype)
```

### TypeScript

```typescript
for await (const message of stream) {
    switch (message.type) {
        case "assistant":
            for (const block of message.message.content) {
                if (block.type === "text") {
                    console.log("Text:", block.text);
                } else if (block.type === "tool_use") {
                    console.log("Tool:", block.name);
                }
            }
            break;
        case "result":
            console.log("Done:", message.subtype);
            break;
    }
}
```

---

## Error Handling

### Python

```python
from claude_agent_sdk import (
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
    CLIConnectionError
)

try:
    async for message in query(prompt="Hello"):
        print(message)
except CLINotFoundError:
    print("Claude CLI not installed")
except ProcessError as e:
    print(f"Process failed: {e}")
except CLIJSONDecodeError:
    print("Failed to parse response")
except CLIConnectionError:
    print("Connection failed")
```

---

## Loading Project Configuration

To load `.claude/settings.json`, `CLAUDE.md`, skills, and commands from your project:

### Python

```python
options = ClaudeAgentOptions(
    setting_sources=["project", "local"]
)
```

### TypeScript

```typescript
const options: ClaudeAgentOptions = {
    settingSources: ["project", "local"]
};
```

This automatically loads:
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local overrides
- `CLAUDE.md` or `.claude/CLAUDE.md` - Project context
- `.claude/skills/` - Custom skills
- `.claude/agents/` - Custom subagents
- `.claude/commands/` - Custom slash commands

---

## Feature Parity: Claude Code CLI vs SDK

See [resources/feature-parity.md](./resources/feature-parity.md) for the complete comparison table.

### Quick Reference

| Feature | Claude Code CLI | SDK |
|---------|----------------|-----|
| Interactive REPL | Yes | No |
| Slash Commands | `/command` | Load via `settingSources` |
| Skills | Auto-loaded | Load via `settingSources` |
| Subagents | Auto-loaded | Load via `settingSources` |
| Hooks | settings.json | `hooks` option |
| MCP Servers | .mcp.json | `mcpServers` option |
| Plugins | `/plugin` command | Not directly supported |
| Permissions | `/permissions` | `allowedTools`, `canUseTool` |
| Sessions | Automatic | `resumeSession`, `forkSession` |
| IDE Integration | VS Code, JetBrains | Programmatic only |

---

## Best Practices

### 1. Use Appropriate Permission Modes

```python
# For automated pipelines - auto-accept edits
options = ClaudeAgentOptions(permission_mode="acceptEdits")

# For interactive apps - manual approval
options = ClaudeAgentOptions(permission_mode="manual")
```

### 2. Limit Tool Access

```python
# Only grant necessary tools
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep"],  # Read-only access
)
```

### 3. Set Working Directory

```python
options = ClaudeAgentOptions(
    cwd="/path/to/project"  # Constrain file operations
)
```

### 4. Use Custom Tool Filtering

```python
def filter_tools(tool_name: str) -> bool:
    dangerous = ["Bash", "Write"]
    return tool_name not in dangerous

options = ClaudeAgentOptions(can_use_tool=filter_tools)
```

### 5. Handle Streaming Properly

```python
async for message in query(prompt="Task"):
    if isinstance(message, AssistantMessage):
        for block in message.content:
            if isinstance(block, TextBlock):
                # Stream output as it arrives
                print(block.text, end="", flush=True)
```

---

## Complete Examples

See the [examples/](./examples/) directory for:
- `quick_start.py` - Basic usage
- `streaming_mode.py` - Streaming responses
- `mcp_calculator.py` - Custom MCP tools
- `multi_agent.py` - Multi-agent coordination
- `quick_start.ts` - TypeScript basics

---

## Resources

### Official Documentation
- [SDK Overview](https://docs.claude.com/en/api/agent-sdk/overview)
- [Python SDK Reference](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python)
- [TypeScript SDK Reference](https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-typescript)

### GitHub Repositories
- [Python SDK](https://github.com/anthropics/claude-agent-sdk-python)
- [TypeScript SDK](https://github.com/anthropics/claude-agent-sdk-typescript)

### Claude Code Documentation
- [Settings Reference](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Hooks Guide](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Plugins Guide](https://docs.anthropic.com/en/docs/claude-code/plugins)
