# MCP Sampling with Tools Guide

Sampling with Tools (SEP-1577) enables servers to run agentic loops using the client's LLM tokens. This is a powerful pattern for complex multi-step operations.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         MCP Client                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    LLM (Claude, etc.)                       ││
│  └─────────────────────────────────────────────────────────────┘│
│         ▲                                                        │
│         │ sampling/createMessage                                │
│         │ (with tools array)                                    │
│         │                                                        │
│  ┌──────┴──────────────────────────────────────────────────────┐│
│  │                    MCP Server                                ││
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     ││
│  │  │   Tool A    │    │   Tool B    │    │   Tool C    │     ││
│  │  └─────────────┘    └─────────────┘    └─────────────┘     ││
│  │                                                              ││
│  │  Server orchestrates agentic loop:                          ││
│  │  1. Request LLM completion with tools                       ││
│  │  2. Execute tool calls locally                              ││
│  │  3. Feed results back to LLM                               ││
│  │  4. Repeat until task complete                              ││
│  └──────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Key Concepts

### Sampling Request with Tools

The 2025-11-25 spec adds a `tools` array to sampling requests, replacing the deprecated `includeContext`:

```python
# Server requesting sampling with tools
request = {
    "method": "sampling/createMessage",
    "params": {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "Analyze sales data and create a summary report"
                }
            }
        ],
        "systemPrompt": "You are a data analyst assistant.",
        "tools": [
            {
                "name": "query_database",
                "description": "Execute SQL query against sales database",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "create_chart",
                "description": "Generate a chart from data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "array"},
                        "chart_type": {"type": "string", "enum": ["bar", "line", "pie"]}
                    },
                    "required": ["data", "chart_type"]
                }
            }
        ],
        "maxTokens": 4096,
        "modelPreferences": {
            "hints": [{"name": "claude-sonnet-4-20250514"}],
            "intelligencePriority": 0.8,
            "speedPriority": 0.2
        }
    }
}
```

### Tool Execution Flow

```
Server                    Client                    LLM
   │                         │                        │
   │  sampling/createMessage │                        │
   │  (with tools array)     │                        │
   │────────────────────────▶│                        │
   │                         │     LLM request        │
   │                         │───────────────────────▶│
   │                         │                        │
   │                         │◀───────────────────────│
   │                         │  Response with         │
   │                         │  tool_use block        │
   │                         │                        │
   │◀────────────────────────│                        │
   │  stopReason: tool_use   │                        │
   │  tool call details      │                        │
   │                         │                        │
   │  [Server executes tool] │                        │
   │                         │                        │
   │  sampling/createMessage │                        │
   │  (with tool_result)     │                        │
   │────────────────────────▶│                        │
   │                         │───────────────────────▶│
   │                         │◀───────────────────────│
   │◀────────────────────────│  Final response       │
   │  stopReason: end_turn   │                        │
```

## Server Implementation (Python)

```python
from fastmcp import FastMCP
from dataclasses import dataclass
from typing import Optional, Any
import json

mcp = FastMCP("agentic-server")


@dataclass
class SamplingTool:
    """Tool definition for sampling requests."""
    name: str
    description: str
    input_schema: dict


# Tools available for agentic operations
SAMPLING_TOOLS = [
    SamplingTool(
        name="query_database",
        description="Execute a read-only SQL query. Returns JSON array of results.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "SQL SELECT query"
                }
            },
            "required": ["query"]
        }
    ),
    SamplingTool(
        name="create_visualization",
        description="Create a chart or graph from data.",
        input_schema={
            "type": "object",
            "properties": {
                "data": {"type": "array"},
                "chart_type": {"type": "string", "enum": ["bar", "line", "pie", "scatter"]},
                "title": {"type": "string"}
            },
            "required": ["data", "chart_type"]
        }
    ),
    SamplingTool(
        name="save_report",
        description="Save generated report to file system.",
        input_schema={
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"},
                "format": {"type": "string", "enum": ["md", "html", "pdf"]}
            },
            "required": ["filename", "content"]
        }
    )
]


async def execute_sampling_tool(name: str, arguments: dict) -> str:
    """Execute a tool during sampling and return result."""
    if name == "query_database":
        # Validate query is SELECT only
        query = arguments["query"].strip().upper()
        if not query.startswith("SELECT"):
            return json.dumps({"error": "Only SELECT queries allowed"})

        # Execute query (simplified)
        results = await db.execute(arguments["query"])
        return json.dumps(results)

    elif name == "create_visualization":
        # Generate chart
        chart_url = await charts.create(
            data=arguments["data"],
            chart_type=arguments["chart_type"],
            title=arguments.get("title", "")
        )
        return json.dumps({"chart_url": chart_url})

    elif name == "save_report":
        # Save to file system
        path = await reports.save(
            filename=arguments["filename"],
            content=arguments["content"],
            format=arguments.get("format", "md")
        )
        return json.dumps({"saved_path": path})

    return json.dumps({"error": f"Unknown tool: {name}"})


@mcp.tool()
async def analyze_and_report(
    analysis_request: str,
    output_format: str = "md"
) -> str:
    """
    Run an agentic analysis workflow using the client's LLM.

    The server orchestrates a multi-step analysis:
    1. Query relevant data
    2. Generate visualizations
    3. Create and save report

    Args:
        analysis_request: Natural language description of desired analysis
        output_format: Output format (md, html, pdf)

    Returns:
        Path to generated report
    """
    # Build initial messages
    messages = [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""Analyze the following request and create a comprehensive report.

Request: {analysis_request}

Use the available tools to:
1. Query the database for relevant data
2. Create appropriate visualizations
3. Save the final report in {output_format} format

Be thorough but efficient with queries."""
            }
        }
    ]

    # Convert tools to MCP format
    tools = [
        {
            "name": t.name,
            "description": t.description,
            "inputSchema": t.input_schema
        }
        for t in SAMPLING_TOOLS
    ]

    max_iterations = 10
    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Request sampling with tools
        response = await mcp.sample(
            messages=messages,
            system_prompt="You are a data analyst. Use the provided tools to fulfill analysis requests. Be concise and focused.",
            tools=tools,
            max_tokens=4096,
            model_preferences={
                "hints": [{"name": "claude-sonnet-4-20250514"}],
                "intelligencePriority": 0.7,
                "speedPriority": 0.3
            }
        )

        # Check stop reason
        if response.stop_reason == "end_turn":
            # LLM finished without tool call
            return extract_final_result(response.content)

        elif response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = []

            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_args = content_block.input

                    # Execute the tool
                    result = await execute_sampling_tool(tool_name, tool_args)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": result
                    })

            # Add assistant response and tool results to messages
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            messages.append({
                "role": "user",
                "content": tool_results
            })

        else:
            # Unexpected stop reason
            raise RuntimeError(f"Unexpected stop reason: {response.stop_reason}")

    raise RuntimeError("Max iterations exceeded")


def extract_final_result(content: list) -> str:
    """Extract the final result from LLM response."""
    for block in content:
        if block.type == "text":
            return block.text
    return "Analysis complete but no text response generated"
```

## Server Implementation (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

interface SamplingTool {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
}

const SAMPLING_TOOLS: SamplingTool[] = [
  {
    name: "query_database",
    description: "Execute a read-only SQL query",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string" },
      },
      required: ["query"],
    },
  },
  {
    name: "create_chart",
    description: "Generate a chart from data",
    inputSchema: {
      type: "object",
      properties: {
        data: { type: "array" },
        chartType: { type: "string", enum: ["bar", "line", "pie"] },
      },
      required: ["data", "chartType"],
    },
  },
];

async function executeSamplingTool(
  name: string,
  args: Record<string, unknown>
): Promise<string> {
  switch (name) {
    case "query_database":
      const results = await executeQuery(args.query as string);
      return JSON.stringify(results);

    case "create_chart":
      const chartUrl = await createChart(args.data as unknown[], args.chartType as string);
      return JSON.stringify({ chartUrl });

    default:
      return JSON.stringify({ error: `Unknown tool: ${name}` });
  }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "analyze_data") {
    const { analysisRequest } = request.params.arguments as { analysisRequest: string };

    const messages: Array<{ role: string; content: unknown }> = [
      {
        role: "user",
        content: {
          type: "text",
          text: `Analyze: ${analysisRequest}`,
        },
      },
    ];

    const tools = SAMPLING_TOOLS.map((t) => ({
      name: t.name,
      description: t.description,
      inputSchema: t.inputSchema,
    }));

    let iterations = 0;
    const maxIterations = 10;

    while (iterations < maxIterations) {
      iterations++;

      // Request sampling
      const response = await server.request(
        {
          method: "sampling/createMessage",
          params: {
            messages,
            tools,
            maxTokens: 4096,
            systemPrompt: "You are a data analyst.",
          },
        },
        CreateMessageResultSchema
      );

      if (response.stopReason === "end_turn") {
        // Extract final text
        const textContent = response.content.find((c) => c.type === "text");
        return {
          content: [{ type: "text", text: textContent?.text ?? "Complete" }],
        };
      }

      if (response.stopReason === "tool_use") {
        const toolResults = [];

        for (const block of response.content) {
          if (block.type === "tool_use") {
            const result = await executeSamplingTool(block.name, block.input as Record<string, unknown>);
            toolResults.push({
              type: "tool_result",
              tool_use_id: block.id,
              content: result,
            });
          }
        }

        // Add to conversation
        messages.push({ role: "assistant", content: response.content });
        messages.push({ role: "user", content: toolResults });
      }
    }

    throw new Error("Max iterations exceeded");
  }

  throw new Error(`Unknown tool: ${request.params.name}`);
});
```

## Client Implementation

The client must handle sampling requests from servers:

```python
from mcp import ClientSession
from mcp.types import SamplingMessage, CreateMessageRequest
import anthropic


class SamplingEnabledClient:
    """MCP client that supports sampling requests from servers."""

    def __init__(self, anthropic_client: anthropic.Anthropic):
        self.anthropic = anthropic_client
        self.session: Optional[ClientSession] = None

    async def connect(self, read_stream, write_stream):
        self.session = ClientSession(read_stream, write_stream)

        # Register sampling handler
        self.session.set_sampling_handler(self._handle_sampling)

        await self.session.initialize()

    async def _handle_sampling(
        self,
        request: CreateMessageRequest
    ) -> CreateMessageResult:
        """Handle sampling requests from the server."""

        # Convert MCP messages to Anthropic format
        messages = self._convert_messages(request.messages)

        # Convert MCP tools to Anthropic format
        tools = None
        if request.tools:
            tools = [
                {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "input_schema": t["inputSchema"]
                }
                for t in request.tools
            ]

        # Call Anthropic API
        response = self.anthropic.messages.create(
            model=self._select_model(request.model_preferences),
            max_tokens=request.max_tokens,
            system=request.system_prompt or "",
            messages=messages,
            tools=tools
        )

        # Convert response back to MCP format
        return self._convert_response(response)

    def _select_model(self, preferences: Optional[dict]) -> str:
        """Select model based on preferences."""
        if not preferences:
            return "claude-sonnet-4-20250514"

        # Check hints first
        if preferences.get("hints"):
            for hint in preferences["hints"]:
                if hint.get("name"):
                    return hint["name"]

        # Fall back to priority-based selection
        intelligence = preferences.get("intelligencePriority", 0.5)
        if intelligence > 0.8:
            return "claude-sonnet-4-20250514"
        elif intelligence > 0.5:
            return "claude-sonnet-4-20250514"
        else:
            return "claude-3-5-haiku-20241022"

    def _convert_messages(self, mcp_messages: list) -> list:
        """Convert MCP message format to Anthropic format."""
        messages = []
        for msg in mcp_messages:
            content = msg["content"]
            if isinstance(content, dict):
                if content["type"] == "text":
                    messages.append({
                        "role": msg["role"],
                        "content": content["text"]
                    })
            elif isinstance(content, list):
                # Handle tool results
                messages.append({
                    "role": msg["role"],
                    "content": content
                })
        return messages

    def _convert_response(self, response) -> dict:
        """Convert Anthropic response to MCP format."""
        content = []
        for block in response.content:
            if block.type == "text":
                content.append({
                    "type": "text",
                    "text": block.text
                })
            elif block.type == "tool_use":
                content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })

        return {
            "content": content,
            "stopReason": response.stop_reason,
            "model": response.model
        }
```

## Parallel Tool Execution

For efficiency, execute independent tool calls in parallel:

```python
import asyncio


async def execute_tool_calls_parallel(
    tool_calls: list[dict]
) -> list[dict]:
    """Execute multiple tool calls in parallel."""

    async def execute_one(call: dict) -> dict:
        try:
            result = await execute_sampling_tool(
                call["name"],
                call["input"]
            )
            return {
                "type": "tool_result",
                "tool_use_id": call["id"],
                "content": result
            }
        except Exception as e:
            return {
                "type": "tool_result",
                "tool_use_id": call["id"],
                "content": json.dumps({"error": str(e)}),
                "is_error": True
            }

    results = await asyncio.gather(
        *[execute_one(call) for call in tool_calls]
    )

    return list(results)
```

## Security Considerations

### Token Budget Management

```python
class TokenBudgetManager:
    """Manage token budget for sampling operations."""

    def __init__(self, max_tokens_per_request: int = 100000):
        self.max_tokens = max_tokens_per_request
        self.used_tokens = 0

    def can_sample(self, estimated_tokens: int) -> bool:
        return self.used_tokens + estimated_tokens <= self.max_tokens

    def record_usage(self, tokens: int):
        self.used_tokens += tokens

    def reset(self):
        self.used_tokens = 0


# Usage in agentic loop
budget = TokenBudgetManager(max_tokens_per_request=50000)

while iteration < max_iterations:
    estimated = estimate_tokens(messages, tools)

    if not budget.can_sample(estimated):
        raise RuntimeError("Token budget exceeded")

    response = await mcp.sample(...)
    budget.record_usage(response.usage.total_tokens)
```

### Tool Allowlisting

```python
class SecureSamplingServer:
    """Server with tool allowlisting for sampling."""

    # Tools safe for server-side execution
    ALLOWED_TOOLS = {
        "query_database",
        "create_chart",
        "save_report"
    }

    async def validate_tool_request(
        self,
        tool_name: str,
        arguments: dict
    ) -> bool:
        if tool_name not in self.ALLOWED_TOOLS:
            return False

        # Tool-specific validation
        if tool_name == "query_database":
            query = arguments.get("query", "").upper()
            # Only allow SELECT
            if not query.strip().startswith("SELECT"):
                return False
            # Block dangerous keywords
            dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE"]
            if any(kw in query for kw in dangerous):
                return False

        return True
```

### Rate Limiting

```python
from datetime import datetime, timedelta
from collections import defaultdict


class SamplingRateLimiter:
    """Rate limit sampling requests per client."""

    def __init__(
        self,
        requests_per_minute: int = 10,
        tokens_per_hour: int = 100000
    ):
        self.rpm_limit = requests_per_minute
        self.tph_limit = tokens_per_hour
        self.request_times: dict[str, list[datetime]] = defaultdict(list)
        self.token_usage: dict[str, list[tuple[datetime, int]]] = defaultdict(list)

    def check_rate_limit(self, client_id: str, estimated_tokens: int) -> bool:
        now = datetime.utcnow()

        # Check requests per minute
        recent_requests = [
            t for t in self.request_times[client_id]
            if now - t < timedelta(minutes=1)
        ]
        if len(recent_requests) >= self.rpm_limit:
            return False

        # Check tokens per hour
        recent_tokens = sum(
            tokens for t, tokens in self.token_usage[client_id]
            if now - t < timedelta(hours=1)
        )
        if recent_tokens + estimated_tokens > self.tph_limit:
            return False

        return True

    def record_request(self, client_id: str, tokens_used: int):
        now = datetime.utcnow()
        self.request_times[client_id].append(now)
        self.token_usage[client_id].append((now, tokens_used))

        # Cleanup old entries
        cutoff = now - timedelta(hours=1)
        self.request_times[client_id] = [
            t for t in self.request_times[client_id] if t > cutoff
        ]
        self.token_usage[client_id] = [
            (t, tokens) for t, tokens in self.token_usage[client_id] if t > cutoff
        ]
```

## Best Practices

### Agentic Loop Design

1. **Set iteration limits** - Prevent infinite loops
2. **Track token usage** - Don't exceed budgets
3. **Log each iteration** - Debug complex flows
4. **Handle partial failures** - One tool error shouldn't crash loop

### Tool Selection

1. **Minimal tool set** - Only include tools needed for the task
2. **Clear descriptions** - Help LLM choose correct tools
3. **Validate inputs** - Check tool arguments before execution
4. **Structured outputs** - Return JSON for reliable parsing

### Error Handling

1. **Distinguish error types** - Tool errors vs. LLM errors vs. protocol errors
2. **Provide context** - Include error details in tool_result
3. **Allow recovery** - LLM can often work around tool failures
4. **Set stop conditions** - Exit gracefully when task cannot complete

## Related

- **Tasks Primitive**: See `resources/tasks-primitive.md` for long-running task patterns
- **Client Development**: See `resources/client-development.md` for client implementation
