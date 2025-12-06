# MCP Development Skill

Build production-ready Model Context Protocol (MCP) servers with modern transports, proper tool annotations, and best practices from the latest specification.

## Overview

This skill provides comprehensive expertise for building, testing, and deploying MCP servers following the **MCP specification 2025-11-25** (one-year anniversary release) and Anthropic's tool design guidance.

## When to Use This Skill

Trigger this skill when:

- Building MCP servers (Python with FastMCP or TypeScript with official SDK)
- Building MCP clients (single or multi-server connections)
- Implementing MCP tools, resources, prompts, or tasks
- Choosing between transport mechanisms (stdio vs Streamable HTTP)
- Adding tool annotations for proper client behavior
- Optimizing token usage with Tool Search or code execution patterns
- Implementing server discovery and capability negotiation
- Building agentic workflows with Sampling (server-side LLM orchestration)
- Configuring production deployments and scaling patterns
- Debugging MCP server/client implementations

**Keywords:** MCP, fastmcp, Model Context Protocol, Streamable HTTP, tool annotations, TypeScript SDK, token optimization, sampling, tasks, multi-server, agentic

## MCP Protocol Fundamentals

### The Four Primitives

MCP defines four core primitives with different control models:

| Primitive | Controller | Purpose |
|-----------|------------|---------|
| **Tools** | Model-controlled | Actions the LLM can invoke |
| **Resources** | Application-controlled | Data the app exposes to the LLM |
| **Prompts** | User-controlled | Templates users can select |
| **Tasks** | Server-controlled | Long-running operations with progress tracking |

See `resources/tasks-primitive.md` for detailed task implementation patterns.

### Protocol Version

Always specify the protocol version in HTTP requests:

```http
MCP-Protocol-Version: 2025-11-25
```

For the latest specification, authentication patterns, and advanced features, always reference: <https://modelcontextprotocol.io/specification/2025-11-25>

### What's New in 2025-11-25

The one-year anniversary release includes major features:

- **Tasks (SEP-1686)**: New primitive for long-running operations with states (`working`, `input_required`, `completed`, `failed`, `cancelled`)
- **Sampling with Tools (SEP-1577)**: Servers can run agentic loops using client tokens
- **URL Mode Elicitation (SEP-1036)**: Secure out-of-band credential acquisition (OAuth flows, API keys)
- **Simplified Authorization (SEP-991)**: OAuth Client ID Metadata Documents replace Dynamic Client Registration
- **Extensions Framework**: Optional, composable protocol extensions for specialized capabilities
- **Standardized Tool Naming (SEP-986)**: Consistent naming format across servers

No breaking changes - fully backward compatible with 2025-06-18.

### Extended Documentation

This skill includes detailed resource guides for advanced topics:

| Resource | Topics Covered |
|----------|----------------|
| `resources/client-development.md` | Multi-server clients, reconnection, tool aggregation |
| `resources/tasks-primitive.md` | Long-running tasks, states, cancellation, input requests |
| `resources/server-discovery.md` | Well-known URLs, DNS-SD, registries, capability negotiation |
| `resources/sampling-with-tools.md` | Agentic loops, server-side LLM orchestration |
| `resources/architecture-patterns.md` | Scaling, load balancing, multi-region deployment |

---

## Transport Mechanisms

### stdio Transport (Local/CLI)

Best for local integrations and CLI tools. Client launches server as subprocess.

```python
# Python client
from mcp.client.stdio import stdio_client
from mcp import ClientSession

async def connect_stdio():
    async with stdio_client(
        command="uv",
        args=["run", "python", "server.py"]
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            return tools
```

```typescript
// TypeScript client
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({
  command: "node",
  args: ["server.js"],
});

const client = new Client({ name: "my-client", version: "1.0.0" });
await client.connect(transport);
```

**Constraints:**

- Messages delimited by newlines, MUST NOT contain embedded newlines
- Server writes only valid MCP messages to stdout
- stderr reserved for logging (UTF-8)

### Streamable HTTP Transport (Remote/Production)

**This is the current standard for remote servers.** SSE transport was deprecated in protocol version 2025-03-26 and remains deprecated in 2025-11-25.

**Why SSE was deprecated:**

- Required two endpoints (`/sse` + `/messages`) with coordination overhead
- Long-lived connections consume resources during idle
- Connection drops lose responses without recovery
- Limited bidirectionality

**Streamable HTTP advantages:**

- Single `/mcp` endpoint for all communication
- Supports both stateless and stateful servers
- Dynamic upgrade to SSE for long-running operations
- Built-in session management and event resumability
- Compatible with serverless platforms (scale to zero)

#### Server Implementation (Python)

```python
from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
from mcp.server import Server
import json

app = FastAPI()
mcp_server = Server("my-server")

# Session storage
sessions: dict[str, ServerSession] = {}

@app.post("/mcp")
async def handle_mcp(request: Request):
    """Handle all MCP messages via POST."""
    # Validate origin for DNS rebinding protection
    origin = request.headers.get("Origin")
    if origin and origin not in ALLOWED_ORIGINS:
        return Response(status_code=403)

    # Get or create session
    session_id = request.headers.get("Mcp-Session-Id")
    if session_id and session_id not in sessions:
        return Response(status_code=404)  # Session expired

    body = await request.json()

    # Check Accept header for streaming capability
    accept = request.headers.get("Accept", "")
    supports_streaming = "text/event-stream" in accept

    # Process message
    result = await mcp_server.handle_message(body, session_id)

    # For requests (not notifications), return response
    if "id" in body:
        if supports_streaming and is_long_running(body):
            # Upgrade to SSE for streaming response
            return StreamingResponse(
                stream_response(result),
                media_type="text/event-stream",
                headers={"Mcp-Session-Id": session_id} if session_id else {}
            )
        else:
            # Standard JSON response
            return Response(
                content=json.dumps(result),
                media_type="application/json",
                headers={"Mcp-Session-Id": session_id} if session_id else {}
            )

    # Notifications return 202 Accepted
    return Response(status_code=202)

@app.get("/mcp")
async def handle_mcp_stream(request: Request):
    """Optional: Server-initiated communication stream."""
    session_id = request.headers.get("Mcp-Session-Id")
    last_event_id = request.headers.get("Last-Event-ID")

    async def event_stream():
        # Resume from last event if reconnecting
        if last_event_id:
            for event in get_events_after(last_event_id):
                yield format_sse(event)

        # Stream new events
        async for event in mcp_server.events(session_id):
            yield format_sse(event)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"
    )
```

#### Server Implementation (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamable-http.js";
import express from "express";

const app = express();
const server = new Server({ name: "my-server", version: "1.0.0" });

// Configure tools, resources, prompts on server...

const transport = new StreamableHTTPServerTransport({
  sessionIdGenerator: () => crypto.randomUUID(),
  endpoint: "/mcp",
});

app.use("/mcp", transport.requestHandler());

await server.connect(transport);
app.listen(8000);
```

#### Client Implementation

```python
# Python client with fallback
from mcp.client.streamable_http import streamable_http_client
from mcp.client.sse import sse_client  # Legacy fallback

async def connect_remote(base_url: str):
    try:
        # Try Streamable HTTP first (current standard)
        async with streamable_http_client(
            f"{base_url}/mcp",
            headers={"MCP-Protocol-Version": "2025-11-25"}
        ) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return session
    except Exception:
        # Fall back to legacy SSE for older servers
        async with sse_client(f"{base_url}/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return session
```

---

## Tool Annotations

Tool annotations provide metadata about behavior, helping clients show appropriate UI, warnings, and approval flows.

### The Four Behavioral Hints

| Annotation | Type | Default | Meaning |
|------------|------|---------|---------|
| `readOnlyHint` | boolean | `false` | Tool does NOT modify environment |
| `destructiveHint` | boolean | `true` | Tool MAY perform destructive updates |
| `idempotentHint` | boolean | `false` | Repeated calls with same args have no additional effect |
| `openWorldHint` | boolean | `true` | Tool interacts with external entities |

**Important:** `destructiveHint` and `idempotentHint` only matter when `readOnlyHint: false`.

### Annotation Decision Matrix

```
Is it read-only?
├── YES → readOnlyHint: true (other hints irrelevant)
└── NO → readOnlyHint: false
         ├── Does it delete/modify irreversibly? → destructiveHint: true
         ├── Can you safely retry it? → idempotentHint: true
         └── Does it touch external systems? → openWorldHint: true
```

### Examples by Category

```python
# READ-ONLY: Search/query tools
@mcp.tool(annotations={
    "readOnlyHint": True,
    "openWorldHint": False  # Internal database
})
async def search_documents(query: str) -> str:
    """Search internal document store."""
    ...

# READ-ONLY + EXTERNAL: Web search
@mcp.tool(annotations={
    "readOnlyHint": True,
    "openWorldHint": True  # External API
})
async def web_search(query: str) -> str:
    """Search the web."""
    ...

# DESTRUCTIVE: Delete operations
@mcp.tool(annotations={
    "readOnlyHint": False,
    "destructiveHint": True,
    "idempotentHint": False,  # Deleting twice = error
    "openWorldHint": False
})
async def delete_document(doc_id: str) -> str:
    """Permanently delete a document. Cannot be undone."""
    ...

# IDEMPOTENT WRITE: Upsert/PUT semantics
@mcp.tool(annotations={
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": True,  # Safe to retry
    "openWorldHint": True
})
async def update_crm_record(record_id: str, data: dict) -> str:
    """Update CRM record (creates if not exists)."""
    ...

# NON-IDEMPOTENT WRITE: Create operations
@mcp.tool(annotations={
    "readOnlyHint": False,
    "destructiveHint": False,
    "idempotentHint": False,  # Creates duplicate if retried
    "openWorldHint": False
})
async def create_document(title: str, content: str) -> str:
    """Create a new document."""
    ...
```

### TypeScript Annotations

```typescript
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "delete_file",
      description: "Permanently delete a file",
      inputSchema: {
        type: "object",
        properties: { path: { type: "string" } },
        required: ["path"],
      },
      annotations: {
        readOnlyHint: false,
        destructiveHint: true,
        idempotentHint: false,
        openWorldHint: false,
      },
    },
  ],
}));
```

---

## Tool Design Best Practices

Based on Anthropic's guidance for writing effective tools for AI agents.

### Principle 1: Thoughtful Selection Over Quantity

Build consolidated, high-impact tools instead of wrapping every API endpoint.

```python
# BAD: Too granular
# list_users, get_user, list_events, get_event, create_event,
# list_rooms, book_room, send_invite...

# GOOD: Consolidated workflow
@mcp.tool()
async def schedule_meeting(
    title: str,
    attendees: list[str],
    duration_minutes: int,
    preferred_times: list[str]
) -> str:
    """
    Schedule a meeting by finding availability and creating the event.

    Automatically:
    - Finds available time slots for all attendees
    - Creates the calendar event
    - Sends invitations
    - Reserves a conference room if needed

    Args:
        title: Meeting title
        attendees: List of email addresses
        duration_minutes: Meeting length (15, 30, 45, 60, 90, 120)
        preferred_times: Preferred time windows, e.g. ["morning", "2pm-4pm"]

    Returns:
        JSON with meeting details and calendar link
    """
```

### Principle 2: Context Efficiency

Return filtered, relevant data - not exhaustive dumps.

```python
# BAD: Returns everything (10K contacts = massive token usage)
@mcp.tool()
async def list_contacts() -> str:
    return json.dumps(await db.get_all_contacts())

# GOOD: Search-first with format control
@mcp.tool()
async def search_contacts(
    query: str,
    response_format: Literal["detailed", "concise"] = "concise"
) -> str:
    """
    Search contacts by name, email, or company.

    Use 'detailed' format when you need IDs for follow-up operations.
    Use 'concise' format (default) to minimize token usage.
    """
    results = await db.search_contacts(query, limit=20)

    if response_format == "concise":
        return json.dumps([
            {"name": c.name, "email": c.email}
            for c in results
        ])
    else:
        return json.dumps([c.to_dict() for c in results])
```

### Principle 3: LLM-Friendly Descriptions

Write descriptions as if explaining to a new team member.

```python
@mcp.tool()
async def query_sales_data(
    query: str,
    date_range: Optional[str] = None
) -> str:
    """
    Query the sales database using natural language.

    The query is translated to SQL internally. You can ask:
    - "Total revenue last quarter"
    - "Top 10 customers by order value"
    - "Products with declining sales"

    Date range format: "YYYY-MM-DD to YYYY-MM-DD" or relative like
    "last 30 days", "this quarter", "YTD"

    Returns JSON with columns and rows. Large results paginated
    (max 100 rows per response).

    Note: Only SELECT queries are supported. Aggregations and
    JOINs work but may be slower for complex queries.
    """
```

### Principle 4: Meaningful Field Names

Return semantically meaningful names, not raw IDs.

```python
# BAD: Low-level identifiers
{
    "uuid": "a1b2c3d4",
    "256px_image_url": "...",
    "mime_type": "image/jpeg"
}

# GOOD: Meaningful names
{
    "name": "Product Photo",
    "image_url": "...",
    "file_type": "jpeg"
}
```

### Principle 5: Actionable Error Messages

```python
# BAD
raise ValueError("Invalid input")

# GOOD
raise ValueError(
    f"Invalid date format '{date_str}'. "
    f"Expected YYYY-MM-DD (e.g., '2025-01-15') or relative format "
    f"(e.g., 'last 30 days', 'this quarter'). "
    f"Try: search_sales(date_range='last 30 days')"
)
```

---

## Token Optimization Patterns

### Tool Search Tool (Defer Loading)

Instead of loading all tool definitions upfront (55K+ tokens), use progressive discovery.

```python
# Mark tools for deferred loading
tools = [
    {
        "name": "search_documents",
        "description": "Search internal documents",
        "defer_loading": False,  # Critical - always available
    },
    {
        "name": "export_to_pdf",
        "description": "Export document to PDF format",
        "defer_loading": True,   # Discovered on-demand
    },
    # ... hundreds more deferred tools
]
```

**Anthropic's benchmarks:**

- Opus 4: 49% → 74% accuracy
- Opus 4.5: 79.5% → 88.1% accuracy
- Token usage: 77K → 8.7K (85% reduction)

### Code Execution Pattern

Transform discrete tool calls into programmatic access. See the **mcp-tools-as-code** skill for detailed implementation.

**Before (150K tokens):**

```
Tool call: gdrive.getDocument → Process 50K transcript
Tool call: summarize → Process transcript again
Tool call: salesforce.update → Process summary
```

**After (2K tokens):**

```typescript
const transcript = (await gdrive.getDocument({ id })).content;
const summary = extractKeyPoints(transcript); // Runs in sandbox
await salesforce.updateRecord({ data: { notes: summary } });
// Transcript never leaves sandbox
```

**98.7% token reduction** for multi-step workflows.

---

## Security Requirements

### Origin Validation (Required)

From the spec: *"Servers MUST validate the Origin header on all incoming connections to prevent DNS rebinding attacks."*

```python
ALLOWED_ORIGINS = {
    "http://localhost:3000",
    "https://app.example.com",
    "vscode-webview://",  # VS Code extensions
}

@app.middleware("http")
async def validate_origin(request: Request, call_next):
    origin = request.headers.get("Origin")
    if origin and origin not in ALLOWED_ORIGINS:
        logger.warning("Rejected request from origin: %s", origin)
        return Response(status_code=403, content="Invalid origin")
    return await call_next(request)
```

### Session Security

```python
import secrets

def generate_session_id() -> str:
    """Generate cryptographically secure session ID."""
    return secrets.token_urlsafe(32)  # 256 bits of entropy
```

### Input Validation

Always validate at the tool level:

```python
from pydantic import BaseModel, Field, validator
import re

class FileOperationInput(BaseModel):
    path: str = Field(..., description="File path to operate on")

    @validator('path')
    def validate_path(cls, v):
        # Prevent path traversal
        if '..' in v or v.startswith('/'):
            raise ValueError("Invalid path: no traversal or absolute paths")
        # Allowlist directories
        if not v.startswith(('documents/', 'exports/')):
            raise ValueError("Path must be in documents/ or exports/")
        return v
```

### Authentication

For OAuth 2.1, PKCE, session management, and other auth patterns, reference the latest MCP specification: <https://modelcontextprotocol.io/specification/2025-11-25>

The 2025-11-25 release simplifies auth with OAuth Client ID Metadata Documents (SEP-991) replacing Dynamic Client Registration.

---

## FastMCP Server Patterns (Python)

### Server Initialization

```python
from fastmcp import FastMCP
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "my-server",
    dependencies=["httpx>=0.25.0", "pydantic>=2.0.0"]
)

@mcp.on_startup
async def startup():
    logger.info("MCP server starting")
    # Initialize DB connections, API clients, etc.

@mcp.on_shutdown
async def shutdown():
    logger.info("MCP server shutting down")
    # Cleanup resources
```

### Tool with Full Patterns

```python
from pydantic import BaseModel, Field
from typing import Literal

class SearchInput(BaseModel):
    """Search parameters with validation."""
    query: str = Field(
        ...,
        description="Search query",
        min_length=1,
        max_length=500
    )
    limit: int = Field(
        10,
        description="Max results (1-100)",
        ge=1,
        le=100
    )
    format: Literal["detailed", "concise"] = Field(
        "concise",
        description="Response format"
    )

@mcp.tool(annotations={
    "readOnlyHint": True,
    "openWorldHint": False
})
async def search_documents(input: SearchInput) -> str:
    """
    Search internal document store.

    Use 'detailed' format when you need document IDs for
    follow-up operations like get_document or update_document.
    """
    from opentelemetry import trace
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("search_documents") as span:
        span.set_attribute("query.length", len(input.query))
        span.set_attribute("limit", input.limit)

        try:
            results = await perform_search(input.query, input.limit)

            if input.format == "concise":
                output = [{"title": r.title, "snippet": r.snippet[:200]}
                          for r in results]
            else:
                output = [r.to_dict() for r in results]

            span.set_attribute("results.count", len(results))
            return json.dumps(output)

        except Exception as e:
            span.record_exception(e)
            raise RuntimeError(f"Search failed: {e}")
```

### Resource Pattern

```python
@mcp.resource("documents/{doc_id}")
async def get_document(doc_id: str) -> str:
    """
    Retrieve document by ID.

    Returns full document content with metadata.
    """
    if not re.match(r'^[a-zA-Z0-9_-]+$', doc_id):
        raise ValueError(f"Invalid document ID format: {doc_id}")

    document = await fetch_document(doc_id)
    if not document:
        raise ValueError(f"Document not found: {doc_id}")

    return json.dumps({
        "id": document.id,
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at.isoformat(),
    })
```

---

## Client Development

Building MCP clients that connect to servers. For comprehensive patterns including multi-server aggregation and reconnection, see `resources/client-development.md`.

### Basic Client Connection

```python
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession

async def connect_to_server(url: str):
    """Connect to an MCP server via Streamable HTTP."""
    async with streamable_http_client(
        url,
        headers={"MCP-Protocol-Version": "2025-11-25"}
    ) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool(
                "search_documents",
                {"query": "quarterly report"}
            )
            return result
```

### Multi-Server Client Architecture

```
┌─────────────────────────────────────────┐
│              MCP Client                  │
│  ┌───────────────────────────────────┐  │
│  │      Tool Aggregation Layer       │  │
│  │  server_a.tool_1                  │  │
│  │  server_b.tool_2                  │  │
│  └───────────────────────────────────┘  │
│         │                   │           │
│    ┌────▼────┐         ┌────▼────┐     │
│    │Server A │         │Server B │     │
│    └─────────┘         └─────────┘     │
└─────────────────────────────────────────┘
```

Key patterns:

- **Namespaced tools**: Prefix tool names with server name to prevent collisions
- **Independent connections**: Each server connection managed separately
- **Reconnection with backoff**: Exponential backoff on connection failures
- **Capability caching**: Cache tool lists, refresh on `listChanged` notification

---

## TypeScript SDK Patterns

### Server Setup

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-server", version: "1.0.0" },
  { capabilities: { tools: { listChanged: true } } }
);

// List tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "search_documents",
      description: "Search internal document store",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "Search query" },
          limit: { type: "number", default: 10 },
        },
        required: ["query"],
      },
      annotations: {
        readOnlyHint: true,
        openWorldHint: false,
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "search_documents":
      const results = await searchDocuments(args.query, args.limit);
      return {
        content: [{ type: "text", text: JSON.stringify(results) }],
      };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});
```

### Error Handling

Two-layer error model:

```typescript
// Protocol errors (unknown tool, invalid args)
throw new McpError(
  ErrorCode.InvalidParams,
  `Unknown tool: ${name}`
);

// Tool execution errors (return in result)
return {
  content: [{ type: "text", text: "API rate limited" }],
  isError: true,
};
```

---

## PII Sanitization

Critical for all MCP implementations. See `resources/pii-patterns.json` for comprehensive patterns.

```python
import re
from typing import Any, Union

PATTERNS = {
    'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
    'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
}

SENSITIVE_KEYS = {'password', 'secret', 'token', 'api_key', 'ssn', 'credit_card'}

def sanitize(data: Any) -> Any:
    """Recursively sanitize PII from any data structure."""
    if isinstance(data, dict):
        return {
            k: '[REDACTED]' if any(s in k.lower() for s in SENSITIVE_KEYS)
            else sanitize(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [sanitize(item) for item in data]
    elif isinstance(data, str):
        result = data
        for name, pattern in PATTERNS.items():
            result = pattern.sub(f'[{name.upper()}]', result)
        return result
    return data
```

### Sanitization Checklist

- [ ] Before logging
- [ ] Before external API calls
- [ ] Before caching
- [ ] In error messages
- [ ] In tool return values
- [ ] In resource content

---

## Observability

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name: str):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
    provider.add_span_processor(BatchSpanProcessor(exporter))

    trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
```

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

@mcp.tool()
async def my_tool(input: ToolInput) -> str:
    logger.info(
        "tool_invoked",
        tool="my_tool",
        input_length=len(str(input)),
        # Never log raw PII
        query_sanitized=sanitize(input.query)
    )
```

---

## Sampling with Tools (Agentic Loops)

Sampling with Tools (SEP-1577) enables servers to run agentic loops using the client's LLM. The server orchestrates multi-step workflows while the client provides token budget.

For full implementation details, see `resources/sampling-with-tools.md`.

### Basic Flow

```
Server                    Client                    LLM
   │  sampling/createMessage │                        │
   │  (with tools array)     │                        │
   │────────────────────────▶│───────────────────────▶│
   │                         │◀───────────────────────│
   │◀────────────────────────│  tool_use response     │
   │  [Execute tool locally] │                        │
   │  sampling/createMessage │                        │
   │  (with tool_result)     │                        │
   │────────────────────────▶│───────────────────────▶│
```

### Example: Server-Side Agentic Tool

```python
@mcp.tool()
async def analyze_and_report(request: str) -> str:
    """Run multi-step analysis using client's LLM."""

    tools = [
        {"name": "query_database", "description": "Execute SQL query", ...},
        {"name": "create_chart", "description": "Generate visualization", ...}
    ]

    messages = [{"role": "user", "content": {"type": "text", "text": request}}]

    while True:
        response = await mcp.sample(
            messages=messages,
            tools=tools,
            max_tokens=4096
        )

        if response.stop_reason == "end_turn":
            return extract_result(response)

        if response.stop_reason == "tool_use":
            # Execute tools locally, add results to messages
            tool_results = await execute_tools(response.content)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
```

Key considerations:

- **Token budgets**: Track and limit token usage per request
- **Iteration limits**: Prevent infinite agentic loops
- **Tool allowlisting**: Only expose safe tools for server-side execution
- **Parallel execution**: Execute independent tool calls concurrently

---

## Architecture Patterns

For production deployments, see `resources/architecture-patterns.md` for complete patterns.

### Pattern Overview

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| Single server | Development, simple apps | Low |
| Multi-server aggregation | Tool composition | Medium |
| Gateway/proxy | Auth, routing, caching | Medium |
| Load-balanced | High availability | High |
| Serverless | Variable load, cost optimization | Medium |
| Multi-region | Global low latency | High |

### Session Persistence Options

| Strategy | Latency | Durability | Scaling |
|----------|---------|------------|---------|
| In-memory | ~1ms | None | Single instance |
| Redis | ~5ms | Configurable | Horizontal |
| Database | ~20ms | High | Horizontal |
| Hybrid | ~5ms | High | Horizontal |

### Deployment Checklist

- [ ] Origin validation enabled
- [ ] Health check endpoint (`/health`)
- [ ] Session persistence configured
- [ ] Rate limiting in place
- [ ] OpenTelemetry tracing
- [ ] Graceful shutdown handling

---

## Testing

### MCP Test Client

```python
import pytest
from fastmcp.testing import MCPTestClient

@pytest.fixture
async def client():
    client = MCPTestClient(mcp)
    await client.connect()
    yield client
    await client.disconnect()

async def test_search_returns_results(client):
    result = await client.call_tool(
        "search_documents",
        {"query": "test", "limit": 5}
    )
    assert not result.isError
    data = json.loads(result.content[0].text)
    assert len(data) <= 5

async def test_invalid_input_returns_error(client):
    result = await client.call_tool(
        "search_documents",
        {"query": "", "limit": 5}  # Empty query
    )
    assert result.isError
```

---

## Resources

### Official Documentation

- **MCP Specification**: <https://modelcontextprotocol.io/specification/2025-11-25>
- **TypeScript SDK**: <https://github.com/modelcontextprotocol/typescript-sdk>
- **Python SDK**: <https://github.com/modelcontextprotocol/python-sdk>
- **FastMCP**: <https://github.com/jlowin/fastmcp>

### Anthropic Engineering

- [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)
- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

### Related Skills

- **mcp-tools-as-code**: Convert MCP servers to typed TypeScript APIs
- **api-design**: REST API patterns, OpenAPI specifications
- **security-review**: OWASP compliance, vulnerability scanning

## Best Practices Summary

### Server Development

1. **Use Streamable HTTP** for remote servers (SSE is deprecated)
2. **Add tool annotations** - `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`
3. **Design consolidated tools** - workflows over granular endpoints
4. **Optimize for tokens** - search-first, response formats, defer loading
5. **Validate origins** - prevent DNS rebinding attacks
6. **Sanitize PII** - before logging, caching, returning
7. **Write LLM-friendly descriptions** - explain like to a new team member
8. **Return actionable errors** - include examples and suggestions

### Client Development

9. **Namespace tools** - prevent collisions across multi-server setups
10. **Implement reconnection** - exponential backoff with max retries
11. **Handle listChanged** - subscribe to capability update notifications
12. **Cache tool definitions** - minimize list_tools calls

### Production Deployment

13. **Instrument with OpenTelemetry** - traces, metrics, structured logs
14. **Implement health checks** - `/health` endpoint for load balancers
15. **Plan session persistence** - Redis or database for distributed setups
16. **Reference the spec** - <https://modelcontextprotocol.io/specification/2025-11-25>
