# MCP Client Development Guide

Complete guide for building MCP clients that connect to one or more servers, aggregate tools, and handle reconnection gracefully.

## Client Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP Client                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Transport  │  │  Transport  │  │  Transport  │         │
│  │   Manager   │  │   Manager   │  │   Manager   │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐         │
│  │   Server    │  │   Server    │  │   Server    │         │
│  │  Connection │  │  Connection │  │  Connection │         │
│  │  (stdio)    │  │  (HTTP)     │  │  (HTTP)     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Tool Aggregation Layer                     │ │
│  │  - Namespaced tools (server_name.tool_name)            │ │
│  │  - Unified tool listing                                 │ │
│  │  - Cross-server tool routing                           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Python Multi-Server Client

```python
"""
Multi-server MCP client with automatic reconnection and tool aggregation.
"""

from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum
import asyncio
import logging

from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

logger = logging.getLogger(__name__)


class TransportType(Enum):
    STDIO = "stdio"
    HTTP = "http"


class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


@dataclass
class ServerConfig:
    """Configuration for a single MCP server connection."""
    name: str
    transport: TransportType
    # For stdio transport
    command: Optional[str] = None
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    # For HTTP transport
    url: Optional[str] = None
    headers: dict[str, str] = field(default_factory=dict)
    # Connection settings
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0


@dataclass
class ServerConnection:
    """Active connection to an MCP server."""
    config: ServerConfig
    session: Optional[ClientSession] = None
    state: ConnectionState = ConnectionState.DISCONNECTED
    tools: list[dict] = field(default_factory=list)
    resources: list[dict] = field(default_factory=list)
    retry_count: int = 0
    last_error: Optional[str] = None


class MCPClient:
    """
    Multi-server MCP client with aggregated tool access.

    Example:
        client = MCPClient()
        await client.add_server(ServerConfig(
            name="filesystem",
            transport=TransportType.STDIO,
            command="npx",
            args=["@anthropic/mcp-server-filesystem", "/tmp"]
        ))
        await client.add_server(ServerConfig(
            name="github",
            transport=TransportType.HTTP,
            url="https://mcp.example.com/github/mcp"
        ))

        # List all tools across servers
        tools = await client.list_all_tools()

        # Call tool on specific server
        result = await client.call_tool("filesystem", "read_file", {"path": "/tmp/test.txt"})
    """

    def __init__(self):
        self._connections: dict[str, ServerConnection] = {}
        self._lock = asyncio.Lock()

    async def add_server(self, config: ServerConfig) -> None:
        """Add and connect to a new MCP server."""
        async with self._lock:
            if config.name in self._connections:
                raise ValueError(f"Server '{config.name}' already exists")

            conn = ServerConnection(config=config)
            self._connections[config.name] = conn

        await self._connect_server(config.name)

    async def remove_server(self, name: str) -> None:
        """Disconnect and remove a server."""
        async with self._lock:
            if name not in self._connections:
                return

            conn = self._connections[name]
            if conn.session:
                try:
                    await conn.session.close()
                except Exception as e:
                    logger.warning("Error closing session for %s: %s", name, e)

            del self._connections[name]

    async def _connect_server(self, name: str) -> None:
        """Establish connection to a server."""
        conn = self._connections.get(name)
        if not conn:
            return

        conn.state = ConnectionState.CONNECTING
        config = conn.config

        try:
            if config.transport == TransportType.STDIO:
                if not config.command:
                    raise ValueError(f"STDIO transport requires command for {name}")

                async with stdio_client(
                    command=config.command,
                    args=config.args,
                    env=config.env or None
                ) as (read, write):
                    async with ClientSession(read, write) as session:
                        await asyncio.wait_for(
                            session.initialize(),
                            timeout=config.timeout
                        )
                        conn.session = session
                        conn.state = ConnectionState.CONNECTED
                        conn.retry_count = 0

                        # Cache capabilities
                        await self._refresh_server_capabilities(name)

                        logger.info("Connected to server: %s", name)

            elif config.transport == TransportType.HTTP:
                if not config.url:
                    raise ValueError(f"HTTP transport requires URL for {name}")

                headers = {
                    "MCP-Protocol-Version": "2025-11-25",
                    **config.headers
                }

                async with streamable_http_client(
                    config.url,
                    headers=headers
                ) as (read, write):
                    async with ClientSession(read, write) as session:
                        await asyncio.wait_for(
                            session.initialize(),
                            timeout=config.timeout
                        )
                        conn.session = session
                        conn.state = ConnectionState.CONNECTED
                        conn.retry_count = 0

                        await self._refresh_server_capabilities(name)

                        logger.info("Connected to server: %s", name)

        except asyncio.TimeoutError:
            conn.state = ConnectionState.FAILED
            conn.last_error = f"Connection timeout after {config.timeout}s"
            logger.error("Timeout connecting to %s", name)
            await self._schedule_reconnect(name)

        except Exception as e:
            conn.state = ConnectionState.FAILED
            conn.last_error = str(e)
            logger.error("Failed to connect to %s: %s", name, e)
            await self._schedule_reconnect(name)

    async def _refresh_server_capabilities(self, name: str) -> None:
        """Refresh cached tools and resources for a server."""
        conn = self._connections.get(name)
        if not conn or not conn.session:
            return

        try:
            tools_result = await conn.session.list_tools()
            conn.tools = [t.model_dump() for t in tools_result.tools]

            resources_result = await conn.session.list_resources()
            conn.resources = [r.model_dump() for r in resources_result.resources]

        except Exception as e:
            logger.warning("Failed to refresh capabilities for %s: %s", name, e)

    async def _schedule_reconnect(self, name: str) -> None:
        """Schedule a reconnection attempt."""
        conn = self._connections.get(name)
        if not conn:
            return

        if conn.retry_count >= conn.config.max_retries:
            logger.error("Max retries exceeded for %s", name)
            return

        conn.retry_count += 1
        conn.state = ConnectionState.RECONNECTING
        delay = conn.config.retry_delay * (2 ** (conn.retry_count - 1))  # Exponential backoff

        logger.info("Scheduling reconnect for %s in %.1fs (attempt %d/%d)",
                   name, delay, conn.retry_count, conn.config.max_retries)

        await asyncio.sleep(delay)
        await self._connect_server(name)

    async def list_all_tools(self) -> list[dict]:
        """
        List all tools from all connected servers.

        Returns tools with namespaced names (server_name.tool_name).
        """
        all_tools = []
        for name, conn in self._connections.items():
            if conn.state != ConnectionState.CONNECTED:
                continue

            for tool in conn.tools:
                namespaced_tool = {
                    **tool,
                    "name": f"{name}.{tool['name']}",
                    "_server": name,
                    "_original_name": tool["name"]
                }
                all_tools.append(namespaced_tool)

        return all_tools

    async def call_tool(
        self,
        server: str,
        tool: str,
        arguments: dict[str, Any]
    ) -> dict:
        """
        Call a tool on a specific server.

        Args:
            server: Server name
            tool: Tool name (without namespace)
            arguments: Tool arguments

        Returns:
            Tool result with content and isError flag
        """
        conn = self._connections.get(server)
        if not conn:
            return {"isError": True, "content": [{"type": "text", "text": f"Unknown server: {server}"}]}

        if conn.state != ConnectionState.CONNECTED or not conn.session:
            return {"isError": True, "content": [{"type": "text", "text": f"Server not connected: {server}"}]}

        try:
            result = await conn.session.call_tool(tool, arguments)
            return {
                "isError": result.isError,
                "content": [c.model_dump() for c in result.content]
            }
        except Exception as e:
            logger.error("Tool call failed on %s.%s: %s", server, tool, e)
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    async def call_namespaced_tool(
        self,
        namespaced_name: str,
        arguments: dict[str, Any]
    ) -> dict:
        """
        Call a tool using its namespaced name (server.tool).

        Example:
            result = await client.call_namespaced_tool(
                "filesystem.read_file",
                {"path": "/tmp/test.txt"}
            )
        """
        if "." not in namespaced_name:
            return {"isError": True, "content": [{"type": "text", "text": f"Invalid namespaced tool: {namespaced_name}"}]}

        server, tool = namespaced_name.split(".", 1)
        return await self.call_tool(server, tool, arguments)

    def get_connection_status(self) -> dict[str, dict]:
        """Get status of all server connections."""
        return {
            name: {
                "state": conn.state.value,
                "tools_count": len(conn.tools),
                "resources_count": len(conn.resources),
                "retry_count": conn.retry_count,
                "last_error": conn.last_error
            }
            for name, conn in self._connections.items()
        }

    async def close(self) -> None:
        """Close all server connections."""
        for name in list(self._connections.keys()):
            await self.remove_server(name)
```

## TypeScript Multi-Server Client

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamable-http.js";

type TransportType = "stdio" | "http";

interface ServerConfig {
  name: string;
  transport: TransportType;
  // For stdio
  command?: string;
  args?: string[];
  env?: Record<string, string>;
  // For HTTP
  url?: string;
  headers?: Record<string, string>;
  // Connection settings
  timeout?: number;
  maxRetries?: number;
  retryDelay?: number;
}

interface ServerConnection {
  config: ServerConfig;
  client: Client | null;
  tools: Array<{ name: string; description?: string; inputSchema: unknown }>;
  state: "disconnected" | "connecting" | "connected" | "reconnecting" | "failed";
  retryCount: number;
  lastError?: string;
}

export class MCPClient {
  private connections = new Map<string, ServerConnection>();

  async addServer(config: ServerConfig): Promise<void> {
    if (this.connections.has(config.name)) {
      throw new Error(`Server '${config.name}' already exists`);
    }

    const conn: ServerConnection = {
      config,
      client: null,
      tools: [],
      state: "disconnected",
      retryCount: 0,
    };

    this.connections.set(config.name, conn);
    await this.connectServer(config.name);
  }

  private async connectServer(name: string): Promise<void> {
    const conn = this.connections.get(name);
    if (!conn) return;

    conn.state = "connecting";
    const { config } = conn;
    const timeout = config.timeout ?? 30000;

    try {
      const client = new Client({ name: "multi-server-client", version: "1.0.0" });

      if (config.transport === "stdio") {
        if (!config.command) {
          throw new Error(`STDIO transport requires command for ${name}`);
        }

        const transport = new StdioClientTransport({
          command: config.command,
          args: config.args,
          env: config.env,
        });

        await Promise.race([
          client.connect(transport),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error("Connection timeout")), timeout)
          ),
        ]);
      } else if (config.transport === "http") {
        if (!config.url) {
          throw new Error(`HTTP transport requires URL for ${name}`);
        }

        const transport = new StreamableHTTPClientTransport(new URL(config.url), {
          requestInit: {
            headers: {
              "MCP-Protocol-Version": "2025-11-25",
              ...config.headers,
            },
          },
        });

        await Promise.race([
          client.connect(transport),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error("Connection timeout")), timeout)
          ),
        ]);
      }

      conn.client = client;
      conn.state = "connected";
      conn.retryCount = 0;

      // Cache tools
      const { tools } = await client.listTools();
      conn.tools = tools;

      console.log(`Connected to server: ${name}`);
    } catch (error) {
      conn.state = "failed";
      conn.lastError = error instanceof Error ? error.message : String(error);
      console.error(`Failed to connect to ${name}:`, error);
      await this.scheduleReconnect(name);
    }
  }

  private async scheduleReconnect(name: string): Promise<void> {
    const conn = this.connections.get(name);
    if (!conn) return;

    const maxRetries = conn.config.maxRetries ?? 3;
    if (conn.retryCount >= maxRetries) {
      console.error(`Max retries exceeded for ${name}`);
      return;
    }

    conn.retryCount++;
    conn.state = "reconnecting";
    const baseDelay = conn.config.retryDelay ?? 1000;
    const delay = baseDelay * Math.pow(2, conn.retryCount - 1);

    console.log(`Reconnecting to ${name} in ${delay}ms (attempt ${conn.retryCount}/${maxRetries})`);

    await new Promise((resolve) => setTimeout(resolve, delay));
    await this.connectServer(name);
  }

  async listAllTools(): Promise<
    Array<{
      name: string;
      description?: string;
      inputSchema: unknown;
      _server: string;
      _originalName: string;
    }>
  > {
    const allTools = [];

    for (const [name, conn] of this.connections) {
      if (conn.state !== "connected") continue;

      for (const tool of conn.tools) {
        allTools.push({
          ...tool,
          name: `${name}.${tool.name}`,
          _server: name,
          _originalName: tool.name,
        });
      }
    }

    return allTools;
  }

  async callTool(
    server: string,
    tool: string,
    args: Record<string, unknown>
  ): Promise<{ isError: boolean; content: Array<{ type: string; text?: string }> }> {
    const conn = this.connections.get(server);
    if (!conn) {
      return { isError: true, content: [{ type: "text", text: `Unknown server: ${server}` }] };
    }

    if (conn.state !== "connected" || !conn.client) {
      return { isError: true, content: [{ type: "text", text: `Server not connected: ${server}` }] };
    }

    try {
      const result = await conn.client.callTool({ name: tool, arguments: args });
      return {
        isError: result.isError ?? false,
        content: result.content as Array<{ type: string; text?: string }>,
      };
    } catch (error) {
      return {
        isError: true,
        content: [{ type: "text", text: error instanceof Error ? error.message : String(error) }],
      };
    }
  }

  async callNamespacedTool(
    namespacedName: string,
    args: Record<string, unknown>
  ): Promise<{ isError: boolean; content: Array<{ type: string; text?: string }> }> {
    const dotIndex = namespacedName.indexOf(".");
    if (dotIndex === -1) {
      return { isError: true, content: [{ type: "text", text: `Invalid namespaced tool: ${namespacedName}` }] };
    }

    const server = namespacedName.slice(0, dotIndex);
    const tool = namespacedName.slice(dotIndex + 1);
    return this.callTool(server, tool, args);
  }

  getConnectionStatus(): Record<
    string,
    { state: string; toolsCount: number; retryCount: number; lastError?: string }
  > {
    const status: Record<string, { state: string; toolsCount: number; retryCount: number; lastError?: string }> = {};

    for (const [name, conn] of this.connections) {
      status[name] = {
        state: conn.state,
        toolsCount: conn.tools.length,
        retryCount: conn.retryCount,
        lastError: conn.lastError,
      };
    }

    return status;
  }

  async close(): Promise<void> {
    for (const [name, conn] of this.connections) {
      if (conn.client) {
        try {
          await conn.client.close();
        } catch (error) {
          console.warn(`Error closing ${name}:`, error);
        }
      }
    }
    this.connections.clear();
  }
}
```

## Connection Lifecycle

```
┌───────────────┐
│  DISCONNECTED │
└───────┬───────┘
        │ add_server()
        ▼
┌───────────────┐
│  CONNECTING   │
└───────┬───────┘
        │
   ┌────┴────┐
   │         │
   ▼         ▼
┌───────┐  ┌───────┐
│CONNECT│  │ FAILED│◄────────────┐
│  ED   │  └───┬───┘             │
└───┬───┘      │                 │
    │          │ retry < max     │
    │          ▼                 │
    │    ┌───────────┐           │
    │    │RECONNECT- │───────────┘
    │    │   ING     │    failure
    │    └─────┬─────┘
    │          │ success
    │          ▼
    └──────────►┌───────────────┐
               │   CONNECTED   │
               └───────────────┘
```

## Handling listChanged Notifications

Servers can notify clients when their capabilities change:

```python
class MCPClient:
    async def _setup_notifications(self, name: str) -> None:
        """Set up notification handlers for a server."""
        conn = self._connections.get(name)
        if not conn or not conn.session:
            return

        # Handle tools/list_changed
        @conn.session.on_notification("notifications/tools/list_changed")
        async def on_tools_changed():
            logger.info("Tools changed on %s, refreshing...", name)
            await self._refresh_server_capabilities(name)

        # Handle resources/list_changed
        @conn.session.on_notification("notifications/resources/list_changed")
        async def on_resources_changed():
            logger.info("Resources changed on %s, refreshing...", name)
            await self._refresh_server_capabilities(name)
```

## Best Practices

### Connection Management

1. **Use exponential backoff** for reconnection attempts
2. **Cache capabilities** to avoid repeated list calls
3. **Handle partial availability** - don't fail if one server is down
4. **Namespace tools** to prevent collisions across servers

### Error Handling

1. **Distinguish connection errors from tool errors** - connection issues should trigger reconnect, tool errors should be returned to caller
2. **Log comprehensively** - server name, tool name, arguments (sanitized), timing
3. **Set reasonable timeouts** - balance responsiveness with reliability

### Security

1. **Validate server configs** before connecting
2. **Use TLS** for HTTP connections in production
3. **Don't expose raw errors** to end users - log details, return generic messages

## Related

- **Server Development**: See main SKILL.md for building servers
- **Tasks Primitive**: See `resources/tasks-primitive.md` for long-running operations
- **Architecture Patterns**: See `resources/architecture-patterns.md` for deployment strategies
