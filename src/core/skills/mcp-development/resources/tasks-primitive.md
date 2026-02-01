# MCP Tasks Primitive Guide

The Tasks primitive (SEP-1686) provides first-class support for long-running operations in MCP 2025-11-25.

## Overview

Tasks enable:

- Tracking progress of long-running operations
- Cancellation support
- Input requests during execution
- Persistent state across reconnections

## Task States

```
┌─────────┐      start      ┌─────────┐
│ pending │────────────────▶│ working │
└─────────┘                 └────┬────┘
                                 │
           ┌─────────────────────┼─────────────────────┐
           │                     │                     │
           ▼                     ▼                     ▼
    ┌──────────────┐      ┌───────────┐      ┌────────────┐
    │input_required│      │ completed │      │   failed   │
    └──────┬───────┘      └───────────┘      └────────────┘
           │                                       ▲
           │ provide input                         │
           └───────────────▶ working ──────────────┘
                              │
                              ▼
                        ┌───────────┐
                        │ cancelled │
                        └───────────┘
```

### State Definitions

| State | Description |
|-------|-------------|
| `pending` | Task created but not started |
| `working` | Task is actively executing |
| `input_required` | Task paused, waiting for user input |
| `completed` | Task finished successfully |
| `failed` | Task encountered an error |
| `cancelled` | Task was cancelled by client |

## Server Implementation (Python)

```python
from fastmcp import FastMCP
from dataclasses import dataclass
from typing import Optional, AsyncGenerator
from enum import Enum
import asyncio
import uuid

mcp = FastMCP("task-server")


class TaskState(Enum):
    PENDING = "pending"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskProgress:
    progress: float  # 0.0 to 1.0
    message: str
    details: Optional[dict] = None


@dataclass
class Task:
    id: str
    state: TaskState
    progress: float = 0.0
    message: str = ""
    result: Optional[dict] = None
    error: Optional[str] = None
    input_request: Optional[dict] = None


# In-memory task storage (use Redis/DB in production)
tasks: dict[str, Task] = {}
task_queues: dict[str, asyncio.Queue] = {}


@mcp.tool()
async def start_data_export(
    format: str,
    date_range: str,
    include_attachments: bool = False
) -> dict:
    """
    Start a long-running data export task.

    Returns a task ID for tracking progress.

    Args:
        format: Export format (csv, json, xlsx)
        date_range: Date range to export (e.g., "last 30 days")
        include_attachments: Include file attachments

    Returns:
        Task ID and initial status
    """
    task_id = str(uuid.uuid4())

    task = Task(
        id=task_id,
        state=TaskState.PENDING,
        message="Export queued"
    )
    tasks[task_id] = task
    task_queues[task_id] = asyncio.Queue()

    # Start background processing
    asyncio.create_task(
        _process_export(task_id, format, date_range, include_attachments)
    )

    return {
        "task_id": task_id,
        "state": task.state.value,
        "message": task.message
    }


async def _process_export(
    task_id: str,
    format: str,
    date_range: str,
    include_attachments: bool
) -> None:
    """Background task processor."""
    task = tasks[task_id]

    try:
        task.state = TaskState.WORKING
        task.message = "Starting export..."

        # Phase 1: Query data
        task.progress = 0.1
        task.message = "Querying database..."
        await asyncio.sleep(2)  # Simulate work

        # Phase 2: Check if user approval needed for large export
        record_count = 50000  # Simulated
        if record_count > 10000:
            task.state = TaskState.INPUT_REQUIRED
            task.input_request = {
                "type": "confirmation",
                "message": f"Export will include {record_count:,} records. Continue?",
                "options": ["continue", "cancel", "limit_to_10000"]
            }

            # Wait for user input
            queue = task_queues[task_id]
            user_response = await queue.get()

            if user_response == "cancel":
                task.state = TaskState.CANCELLED
                task.message = "Export cancelled by user"
                return
            elif user_response == "limit_to_10000":
                record_count = 10000

            task.state = TaskState.WORKING

        # Phase 3: Process records
        task.progress = 0.3
        task.message = f"Processing {record_count:,} records..."
        await asyncio.sleep(3)

        # Phase 4: Generate output
        task.progress = 0.7
        task.message = f"Generating {format.upper()} file..."
        await asyncio.sleep(2)

        if include_attachments:
            task.progress = 0.9
            task.message = "Packaging attachments..."
            await asyncio.sleep(1)

        # Complete
        task.state = TaskState.COMPLETED
        task.progress = 1.0
        task.message = "Export complete"
        task.result = {
            "download_url": f"https://exports.example.com/{task_id}.{format}",
            "record_count": record_count,
            "file_size_mb": 15.7,
            "expires_at": "2025-12-01T00:00:00Z"
        }

    except asyncio.CancelledError:
        task.state = TaskState.CANCELLED
        task.message = "Export cancelled"

    except Exception as e:
        task.state = TaskState.FAILED
        task.error = str(e)
        task.message = f"Export failed: {e}"


@mcp.tool()
async def get_task_status(task_id: str) -> dict:
    """
    Get the current status of a task.

    Args:
        task_id: The task ID returned from start_* methods

    Returns:
        Current task state, progress, and result if complete
    """
    task = tasks.get(task_id)
    if not task:
        return {"error": f"Task not found: {task_id}"}

    response = {
        "task_id": task_id,
        "state": task.state.value,
        "progress": task.progress,
        "message": task.message
    }

    if task.state == TaskState.COMPLETED:
        response["result"] = task.result
    elif task.state == TaskState.FAILED:
        response["error"] = task.error
    elif task.state == TaskState.INPUT_REQUIRED:
        response["input_request"] = task.input_request

    return response


@mcp.tool()
async def provide_task_input(task_id: str, input_value: str) -> dict:
    """
    Provide input to a task waiting for user response.

    Args:
        task_id: The task ID
        input_value: User's response to the input request

    Returns:
        Updated task status
    """
    task = tasks.get(task_id)
    if not task:
        return {"error": f"Task not found: {task_id}"}

    if task.state != TaskState.INPUT_REQUIRED:
        return {"error": f"Task not waiting for input (state: {task.state.value})"}

    queue = task_queues.get(task_id)
    if queue:
        await queue.put(input_value)

    # Wait briefly for state update
    await asyncio.sleep(0.1)

    return await get_task_status(task_id)


@mcp.tool()
async def cancel_task(task_id: str) -> dict:
    """
    Cancel a running task.

    Args:
        task_id: The task ID to cancel

    Returns:
        Cancellation result
    """
    task = tasks.get(task_id)
    if not task:
        return {"error": f"Task not found: {task_id}"}

    if task.state in (TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED):
        return {"error": f"Task already in terminal state: {task.state.value}"}

    task.state = TaskState.CANCELLED
    task.message = "Cancellation requested"

    return {
        "task_id": task_id,
        "state": task.state.value,
        "message": "Task cancellation requested"
    }


@mcp.tool()
async def list_tasks(
    state_filter: Optional[str] = None,
    limit: int = 20
) -> dict:
    """
    List tasks, optionally filtered by state.

    Args:
        state_filter: Filter by state (working, completed, failed, etc.)
        limit: Maximum tasks to return

    Returns:
        List of task summaries
    """
    filtered = tasks.values()

    if state_filter:
        try:
            filter_state = TaskState(state_filter)
            filtered = [t for t in filtered if t.state == filter_state]
        except ValueError:
            return {"error": f"Invalid state: {state_filter}"}

    task_list = []
    for task in list(filtered)[:limit]:
        task_list.append({
            "task_id": task.id,
            "state": task.state.value,
            "progress": task.progress,
            "message": task.message
        })

    return {
        "tasks": task_list,
        "total": len(task_list)
    }
```

## Server Implementation (TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { randomUUID } from "crypto";

type TaskState = "pending" | "working" | "input_required" | "completed" | "failed" | "cancelled";

interface Task {
  id: string;
  state: TaskState;
  progress: number;
  message: string;
  result?: Record<string, unknown>;
  error?: string;
  inputRequest?: {
    type: string;
    message: string;
    options?: string[];
  };
}

const tasks = new Map<string, Task>();
const taskInputResolvers = new Map<string, (value: string) => void>();

const server = new Server(
  { name: "task-server", version: "1.0.0" },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "start_data_export",
      description: "Start a long-running data export task",
      inputSchema: {
        type: "object",
        properties: {
          format: { type: "string", enum: ["csv", "json", "xlsx"] },
          dateRange: { type: "string" },
          includeAttachments: { type: "boolean", default: false },
        },
        required: ["format", "dateRange"],
      },
    },
    {
      name: "get_task_status",
      description: "Get current status of a task",
      inputSchema: {
        type: "object",
        properties: {
          taskId: { type: "string" },
        },
        required: ["taskId"],
      },
    },
    {
      name: "provide_task_input",
      description: "Provide input to a task waiting for user response",
      inputSchema: {
        type: "object",
        properties: {
          taskId: { type: "string" },
          inputValue: { type: "string" },
        },
        required: ["taskId", "inputValue"],
      },
    },
    {
      name: "cancel_task",
      description: "Cancel a running task",
      inputSchema: {
        type: "object",
        properties: {
          taskId: { type: "string" },
        },
        required: ["taskId"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "start_data_export": {
      const taskId = randomUUID();
      const task: Task = {
        id: taskId,
        state: "pending",
        progress: 0,
        message: "Export queued",
      };
      tasks.set(taskId, task);

      // Start background processing
      processExport(taskId, args as { format: string; dateRange: string; includeAttachments?: boolean });

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ taskId, state: task.state, message: task.message }),
          },
        ],
      };
    }

    case "get_task_status": {
      const task = tasks.get(args.taskId as string);
      if (!task) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: "Task not found" }) }],
          isError: true,
        };
      }

      const response: Record<string, unknown> = {
        taskId: task.id,
        state: task.state,
        progress: task.progress,
        message: task.message,
      };

      if (task.state === "completed") response.result = task.result;
      if (task.state === "failed") response.error = task.error;
      if (task.state === "input_required") response.inputRequest = task.inputRequest;

      return { content: [{ type: "text", text: JSON.stringify(response) }] };
    }

    case "provide_task_input": {
      const task = tasks.get(args.taskId as string);
      if (!task) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: "Task not found" }) }],
          isError: true,
        };
      }

      if (task.state !== "input_required") {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: "Task not waiting for input" }) }],
          isError: true,
        };
      }

      const resolver = taskInputResolvers.get(args.taskId as string);
      if (resolver) {
        resolver(args.inputValue as string);
        taskInputResolvers.delete(args.taskId as string);
      }

      return { content: [{ type: "text", text: JSON.stringify({ status: "input_provided" }) }] };
    }

    case "cancel_task": {
      const task = tasks.get(args.taskId as string);
      if (!task) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: "Task not found" }) }],
          isError: true,
        };
      }

      if (["completed", "failed", "cancelled"].includes(task.state)) {
        return {
          content: [{ type: "text", text: JSON.stringify({ error: "Task already in terminal state" }) }],
          isError: true,
        };
      }

      task.state = "cancelled";
      task.message = "Cancelled by user";

      return { content: [{ type: "text", text: JSON.stringify({ taskId: task.id, state: task.state }) }] };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

async function processExport(
  taskId: string,
  params: { format: string; dateRange: string; includeAttachments?: boolean }
): Promise<void> {
  const task = tasks.get(taskId)!;

  try {
    task.state = "working";
    task.message = "Starting export...";

    // Simulate phases
    task.progress = 0.1;
    task.message = "Querying database...";
    await sleep(2000);

    // Check for large export
    const recordCount = 50000;
    if (recordCount > 10000) {
      task.state = "input_required";
      task.inputRequest = {
        type: "confirmation",
        message: `Export will include ${recordCount.toLocaleString()} records. Continue?`,
        options: ["continue", "cancel", "limit_to_10000"],
      };

      // Wait for user input
      const userResponse = await new Promise<string>((resolve) => {
        taskInputResolvers.set(taskId, resolve);
      });

      if (userResponse === "cancel") {
        task.state = "cancelled";
        task.message = "Export cancelled by user";
        return;
      }

      task.state = "working";
    }

    // Continue processing
    task.progress = 0.5;
    task.message = "Processing records...";
    await sleep(3000);

    task.progress = 0.9;
    task.message = `Generating ${params.format.toUpperCase()} file...`;
    await sleep(2000);

    // Complete
    task.state = "completed";
    task.progress = 1.0;
    task.message = "Export complete";
    task.result = {
      downloadUrl: `https://exports.example.com/${taskId}.${params.format}`,
      recordCount,
      fileSizeMb: 15.7,
    };
  } catch (error) {
    task.state = "failed";
    task.error = error instanceof Error ? error.message : String(error);
    task.message = `Export failed: ${task.error}`;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

## Client Usage Patterns

### Polling Pattern

```python
async def wait_for_task(
    client: MCPClient,
    server: str,
    task_id: str,
    poll_interval: float = 2.0,
    timeout: float = 300.0
) -> dict:
    """Poll a task until completion or timeout."""
    start = asyncio.get_event_loop().time()

    while True:
        result = await client.call_tool(server, "get_task_status", {"task_id": task_id})
        status = json.loads(result["content"][0]["text"])

        if status.get("error"):
            raise RuntimeError(status["error"])

        state = status["state"]

        if state == "completed":
            return status["result"]

        if state == "failed":
            raise RuntimeError(status.get("error", "Task failed"))

        if state == "cancelled":
            raise RuntimeError("Task was cancelled")

        if state == "input_required":
            # Handle input request (could prompt user or make decision)
            input_req = status["input_request"]
            print(f"Task requires input: {input_req['message']}")
            # For automated handling:
            user_input = "continue"  # Or prompt user
            await client.call_tool(server, "provide_task_input", {
                "task_id": task_id,
                "input_value": user_input
            })

        elapsed = asyncio.get_event_loop().time() - start
        if elapsed > timeout:
            raise TimeoutError(f"Task {task_id} timed out after {timeout}s")

        # Log progress
        print(f"Task {task_id}: {status['progress']*100:.0f}% - {status['message']}")

        await asyncio.sleep(poll_interval)
```

### SSE Streaming Pattern

For real-time updates via Server-Sent Events:

```python
async def stream_task_updates(
    base_url: str,
    task_id: str
) -> AsyncGenerator[dict, None]:
    """Stream task updates via SSE."""
    import httpx

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "GET",
            f"{base_url}/mcp",
            headers={
                "Accept": "text/event-stream",
                "Mcp-Session-Id": session_id,
                "MCP-Protocol-Version": "2025-11-25"
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])
                    if data.get("task_id") == task_id:
                        yield data
                        if data["state"] in ("completed", "failed", "cancelled"):
                            return
```

## Best Practices

### Task Design

1. **Return task ID immediately** - Don't block on long operations
2. **Provide meaningful progress** - Update progress and message regularly
3. **Design idempotent cancellation** - Handle cancel requests gracefully
4. **Clean up resources** - Remove completed tasks after TTL

### Input Requests

1. **Be specific** - Clearly describe what input is needed and why
2. **Provide options** - When possible, give predefined choices
3. **Handle timeouts** - Don't wait forever for user input
4. **Validate input** - Check responses before continuing

### State Persistence

For production, persist task state to survive restarts:

```python
# Redis-based task storage
import redis.asyncio as redis

class RedisTaskStore:
    def __init__(self, url: str):
        self.client = redis.from_url(url)

    async def save_task(self, task: Task) -> None:
        await self.client.hset(
            f"task:{task.id}",
            mapping={
                "state": task.state.value,
                "progress": task.progress,
                "message": task.message,
                "result": json.dumps(task.result) if task.result else "",
                "error": task.error or ""
            }
        )
        await self.client.expire(f"task:{task.id}", 86400)  # 24h TTL

    async def get_task(self, task_id: str) -> Optional[Task]:
        data = await self.client.hgetall(f"task:{task_id}")
        if not data:
            return None
        return Task(
            id=task_id,
            state=TaskState(data[b"state"].decode()),
            progress=float(data[b"progress"]),
            message=data[b"message"].decode(),
            result=json.loads(data[b"result"]) if data[b"result"] else None,
            error=data[b"error"].decode() or None
        )
```

## Related

- **Sampling with Tools**: See `resources/sampling-with-tools.md` for agentic loops
- **Architecture Patterns**: See `resources/architecture-patterns.md` for task distribution
