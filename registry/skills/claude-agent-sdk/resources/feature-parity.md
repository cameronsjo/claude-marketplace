# Claude Code vs Claude Agent SDK: Feature Parity Guide

This document provides a comprehensive comparison between Claude Code (the CLI/web interface) and the Claude Agent SDK (programmatic API).

## Feature Comparison Matrix

### Core Capabilities

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| Text conversations | Yes | Yes | Identical capability |
| File reading | Yes | Yes | Via `Read` tool |
| File writing | Yes | Yes | Via `Write` tool |
| File editing | Yes | Yes | Via `Edit` tool |
| Shell execution | Yes | Yes | Via `Bash` tool |
| Web search | Yes | Yes | Via `WebSearch` tool |
| Web fetch | Yes | Yes | Via `WebFetch` tool |
| Pattern search (grep) | Yes | Yes | Via `Grep` tool |
| File globbing | Yes | Yes | Via `Glob` tool |
| Jupyter notebooks | Yes | Yes | Via `NotebookEdit` tool |
| Subagent spawning | Yes | Yes | Via `Task` tool |

### User Interface

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| Interactive REPL | Yes | No | SDK is programmatic only |
| Terminal UI | Yes | No | SDK runs headless |
| VS Code extension | Yes | No | IDE integration is CLI only |
| JetBrains plugin | Yes | No | IDE integration is CLI only |
| Web interface | Yes | No | Available via claude.ai |
| Streaming output | Yes | Yes | Both support streaming |

### Configuration & Customization

| Feature | Claude Code CLI | Claude Agent SDK | SDK Equivalent |
|---------|----------------|------------------|----------------|
| System prompt | CLAUDE.md | `system_prompt` option | Direct parameter |
| Settings files | settings.json | `setting_sources` option | Load via option |
| Slash commands | `/command` syntax | Load via `setting_sources` | Auto-loaded from project |
| Custom skills | .claude/skills/ | Load via `setting_sources` | Auto-loaded from project |
| Custom agents | .claude/agents/ | Load via `setting_sources` | Auto-loaded from project |
| Plugins | `/plugin` command | Not directly supported | Manual asset loading |
| Permission rules | settings.json | `allowed_tools`, `can_use_tool` | Programmatic control |
| Model selection | `/model` command | Environment variables | `ANTHROPIC_MODEL` |

### Hooks & Automation

| Feature | Claude Code CLI | Claude Agent SDK | SDK Equivalent |
|---------|----------------|------------------|----------------|
| SessionStart hook | settings.json | Not needed | Pre-execution code |
| SessionEnd hook | settings.json | Not needed | Post-execution code |
| PreToolUse hook | settings.json | `hooks` option | Programmatic hooks |
| PostToolUse hook | settings.json | `hooks` option | Programmatic hooks |
| UserPromptSubmit hook | settings.json | Not needed | Pre-query logic |
| Stop hook | settings.json | Not needed | Post-query logic |
| Custom scripts | Shell scripts | Python/TS functions | Native code |

### MCP (Model Context Protocol)

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| External MCP servers | .mcp.json | `mcp_servers` option | Both supported |
| In-process MCP | No | Yes | SDK advantage |
| Custom tools | Via MCP servers | `@tool` decorator | SDK has native support |
| Tool namespacing | `mcp__server__tool` | `mcp__server__tool` | Same convention |
| Server auto-discovery | Yes | Via `setting_sources` | Load from .mcp.json |

### Session Management

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| Session persistence | Automatic | Manual | `resume_session` option |
| Session forking | Not exposed | Yes | `fork_session` option |
| Multi-turn conversations | Yes | Yes (ClaudeSDKClient) | Stateful client required |
| Context compaction | Automatic | Automatic | Same behavior |
| Session cleanup | Automatic | Manual | Handle in application |

### Security & Permissions

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| Permission modes | 4 modes | 2 modes | acceptEdits, manual |
| Tool allowlisting | settings.json | `allowed_tools` | Array of tool names |
| Tool denylisting | settings.json | `disallowed_tools` | Array of tool names |
| Runtime filtering | No | Yes | `can_use_tool` callback |
| Sandbox mode | Yes | No | CLI-only feature |
| Enterprise policies | managed-settings.json | No | Enterprise CLI feature |

### Authentication

| Feature | Claude Code CLI | Claude Agent SDK | Notes |
|---------|----------------|------------------|-------|
| Claude.ai login | `/login` | No | CLI interactive login |
| API key auth | Environment var | Environment var | `ANTHROPIC_API_KEY` |
| Bedrock auth | Environment var | Environment var | `CLAUDE_CODE_USE_BEDROCK` |
| Vertex AI auth | Environment var | Environment var | `CLAUDE_CODE_USE_VERTEX` |
| Foundry auth | Environment var | Environment var | `CLAUDE_CODE_USE_FOUNDRY` |
| Custom auth | apiKeyHelper | apiKeyHelper | Same mechanism |

---

## Migration Guide: CLI to SDK

### 1. System Prompts

**CLI (CLAUDE.md):**
```markdown
# Project Guidelines
You are a Python expert...
```

**SDK:**
```python
options = ClaudeAgentOptions(
    system_prompt="You are a Python expert..."
)
```

### 2. Slash Commands

**CLI:**
```bash
/review  # Invokes .claude/commands/review.md
```

**SDK:**
```python
# Load project commands automatically
options = ClaudeAgentOptions(setting_sources=["project"])

# Or read command file directly
with open(".claude/commands/review.md") as f:
    command_prompt = f.read()
await client.query(command_prompt)
```

### 3. Skills

**CLI:** Auto-loaded from `.claude/skills/`

**SDK:**
```python
# Auto-load project skills
options = ClaudeAgentOptions(setting_sources=["project"])
```

### 4. Hooks

**CLI (settings.json):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "./validate.sh"}]
    }]
  }
}
```

**SDK:**
```python
# Implement as Python logic
async def pre_tool_hook(tool_name: str, args: dict) -> bool:
    if tool_name == "Bash":
        return validate_command(args["command"])
    return True

# Or use hooks option
options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [{
            "matcher": "Bash",
            "hooks": [{"type": "command", "command": "./validate.sh"}]
        }]
    }
)
```

### 5. Permissions

**CLI (settings.json):**
```json
{
  "permissions": {
    "allow": ["Bash(npm run:*)"],
    "deny": ["Read(.env)"]
  }
}
```

**SDK:**
```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Write", "Bash"],
    can_use_tool=lambda name: name not in ["WebFetch"]
)
```

### 6. MCP Servers

**CLI (.mcp.json):**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

**SDK:**
```python
# Load from project
options = ClaudeAgentOptions(setting_sources=["project"])

# Or create in-process
@tool("my_tool", "Description", {"arg": str})
async def my_tool(args):
    return {"content": [{"type": "text", "text": "Result"}]}

server = create_sdk_mcp_server(name="custom", tools=[my_tool])
options = ClaudeAgentOptions(mcp_servers=[server])
```

---

## SDK-Only Features

Features available in the SDK but not the CLI:

### 1. In-Process MCP Servers

```python
@tool("calculate", "Perform calculation", {"expression": str})
async def calculate(args):
    result = eval(args["expression"])  # Use safe eval in production
    return {"content": [{"type": "text", "text": str(result)}]}

server = create_sdk_mcp_server(name="math", tools=[calculate])
```

### 2. Runtime Tool Filtering

```python
def dynamic_filter(tool_name: str) -> bool:
    # Complex runtime logic
    if is_production():
        return tool_name in SAFE_TOOLS
    return True

options = ClaudeAgentOptions(can_use_tool=dynamic_filter)
```

### 3. Session Forking

```python
# Create alternative branches from a conversation point
await client.query(
    "Try approach B instead",
    resume_session=session_id,
    fork_session=True
)
```

### 4. Programmatic Multi-Agent Orchestration

```python
async def orchestrate():
    # Run specialized agents in sequence or parallel
    architect = ClaudeSDKClient(ClaudeAgentOptions(
        system_prompt="You are a software architect"
    ))

    implementer = ClaudeSDKClient(ClaudeAgentOptions(
        system_prompt="You are an implementation expert"
    ))

    # Coordinate results between agents
    design = await run_agent(architect, "Design the system")
    code = await run_agent(implementer, f"Implement: {design}")
```

---

## CLI-Only Features

Features available in CLI but not the SDK:

1. **Interactive REPL** - Real-time conversation interface
2. **IDE Integration** - VS Code and JetBrains plugins
3. **Plugin System** - `/plugin` command for marketplace
4. **Sandbox Mode** - Isolated execution environment
5. **Enterprise Policies** - managed-settings.json
6. **Interactive Login** - `/login` OAuth flow
7. **Visual Diff Review** - Interactive edit approval
8. **Auto-updater** - Automatic version updates

---

## Choosing Between CLI and SDK

### Use Claude Code CLI when:
- Working interactively on development tasks
- Need IDE integration (VS Code, JetBrains)
- Using plugins from the marketplace
- Require sandbox isolation
- Enterprise policy management needed

### Use Claude Agent SDK when:
- Building automated pipelines
- Creating custom AI-powered applications
- Need programmatic control over agent behavior
- Implementing custom tools with `@tool` decorator
- Orchestrating multi-agent systems
- Embedding Claude capabilities in services

---

## Environment Variables Reference

| Variable | CLI | SDK | Description |
|----------|-----|-----|-------------|
| `ANTHROPIC_API_KEY` | Yes | Yes | API authentication |
| `ANTHROPIC_MODEL` | Yes | Yes | Model selection |
| `CLAUDE_CODE_USE_BEDROCK` | Yes | Yes | Enable Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | Yes | Yes | Enable Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | Yes | Yes | Enable Foundry |
| `BASH_DEFAULT_TIMEOUT_MS` | Yes | Yes | Bash timeout |
| `MAX_THINKING_TOKENS` | Yes | Yes | Extended thinking |
| `CLAUDE_CONFIG_DIR` | Yes | Yes | Config directory |
