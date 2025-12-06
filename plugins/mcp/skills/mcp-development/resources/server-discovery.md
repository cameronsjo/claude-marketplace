# MCP Server Discovery Guide

Server discovery enables clients to find MCP servers without manual configuration. This guide covers discovery mechanisms, capability negotiation, and dynamic server listing.

## Discovery Mechanisms

### 1. Well-Known URL Discovery

Servers can advertise themselves via `.well-known` URLs:

```
https://example.com/.well-known/mcp/server-card.json
```

#### Server Card Schema

```json
{
  "$schema": "https://modelcontextprotocol.io/schemas/server-card.json",
  "name": "Example MCP Server",
  "version": "1.2.0",
  "description": "Provides document management and search capabilities",
  "vendor": {
    "name": "Example Corp",
    "url": "https://example.com",
    "support_email": "support@example.com"
  },
  "endpoints": {
    "mcp": "https://api.example.com/mcp",
    "health": "https://api.example.com/health",
    "docs": "https://docs.example.com/mcp"
  },
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": false,
    "tasks": true,
    "sampling": false
  },
  "authentication": {
    "type": "oauth2",
    "authorization_url": "https://example.com/oauth/authorize",
    "token_url": "https://example.com/oauth/token",
    "scopes": ["read", "write", "admin"]
  },
  "rate_limits": {
    "requests_per_minute": 100,
    "tokens_per_day": 1000000
  },
  "tools_summary": [
    {
      "name": "search_documents",
      "category": "search",
      "description": "Full-text search across documents"
    },
    {
      "name": "create_document",
      "category": "write",
      "description": "Create new documents"
    }
  ]
}
```

#### Server Implementation (Python)

```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import json

app = FastAPI()

SERVER_CARD = {
    "name": "Document Server",
    "version": "1.0.0",
    "description": "Document management MCP server",
    "endpoints": {
        "mcp": "/mcp",
        "health": "/health"
    },
    "capabilities": {
        "tools": True,
        "resources": True,
        "prompts": False,
        "tasks": True,
        "sampling": False
    },
    "tools_summary": [
        {"name": "search", "category": "search", "description": "Search documents"},
        {"name": "create", "category": "write", "description": "Create document"},
        {"name": "delete", "category": "write", "description": "Delete document"}
    ]
}


@app.get("/.well-known/mcp/server-card.json")
async def get_server_card():
    return JSONResponse(
        content=SERVER_CARD,
        headers={
            "Cache-Control": "public, max-age=3600",
            "Access-Control-Allow-Origin": "*"
        }
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": SERVER_CARD["version"]}
```

### 2. DNS-SD Discovery (Local Network)

For local network discovery, servers can advertise via DNS Service Discovery:

```python
import asyncio
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceBrowser
from zeroconf import ServiceStateChange

MCP_SERVICE_TYPE = "_mcp._tcp.local."


async def discover_local_servers(timeout: float = 5.0) -> list[dict]:
    """Discover MCP servers on local network via DNS-SD."""
    discovered = []

    class MCPListener:
        def add_service(self, zc, type_, name):
            info = zc.get_service_info(type_, name)
            if info:
                discovered.append({
                    "name": name.replace(f".{type_}", ""),
                    "host": info.server,
                    "port": info.port,
                    "properties": {
                        k.decode(): v.decode()
                        for k, v in info.properties.items()
                    }
                })

        def remove_service(self, zc, type_, name):
            pass

        def update_service(self, zc, type_, name):
            pass

    zeroconf = AsyncZeroconf()
    listener = MCPListener()
    browser = AsyncServiceBrowser(
        zeroconf.zeroconf,
        MCP_SERVICE_TYPE,
        listener
    )

    await asyncio.sleep(timeout)
    await browser.cancel()
    await zeroconf.async_close()

    return discovered


# Server registration
async def register_local_server(
    name: str,
    port: int,
    properties: dict[str, str]
) -> None:
    """Register MCP server for local network discovery."""
    from zeroconf import ServiceInfo
    import socket

    info = ServiceInfo(
        MCP_SERVICE_TYPE,
        f"{name}.{MCP_SERVICE_TYPE}",
        addresses=[socket.inet_aton(socket.gethostbyname(socket.gethostname()))],
        port=port,
        properties={
            "version": "2025-11-25",
            "transport": "http",
            **properties
        }
    )

    zeroconf = AsyncZeroconf()
    await zeroconf.async_register_service(info)
    return zeroconf  # Keep reference to prevent garbage collection
```

### 3. Registry-Based Discovery

For enterprise deployments, use a central registry:

```python
from dataclasses import dataclass
from typing import Optional
import httpx


@dataclass
class ServerRegistration:
    name: str
    endpoint: str
    version: str
    capabilities: list[str]
    tags: list[str]
    health_endpoint: Optional[str] = None


class MCPRegistry:
    """Central registry for MCP server discovery."""

    def __init__(self, registry_url: str):
        self.registry_url = registry_url
        self.client = httpx.AsyncClient()

    async def register_server(self, server: ServerRegistration) -> str:
        """Register a server with the registry."""
        response = await self.client.post(
            f"{self.registry_url}/servers",
            json={
                "name": server.name,
                "endpoint": server.endpoint,
                "version": server.version,
                "capabilities": server.capabilities,
                "tags": server.tags,
                "health_endpoint": server.health_endpoint
            }
        )
        response.raise_for_status()
        return response.json()["server_id"]

    async def discover_servers(
        self,
        capabilities: Optional[list[str]] = None,
        tags: Optional[list[str]] = None
    ) -> list[dict]:
        """Discover servers matching criteria."""
        params = {}
        if capabilities:
            params["capabilities"] = ",".join(capabilities)
        if tags:
            params["tags"] = ",".join(tags)

        response = await self.client.get(
            f"{self.registry_url}/servers",
            params=params
        )
        response.raise_for_status()
        return response.json()["servers"]

    async def get_server(self, server_id: str) -> dict:
        """Get details for a specific server."""
        response = await self.client.get(
            f"{self.registry_url}/servers/{server_id}"
        )
        response.raise_for_status()
        return response.json()

    async def heartbeat(self, server_id: str) -> None:
        """Send heartbeat to keep registration active."""
        await self.client.post(
            f"{self.registry_url}/servers/{server_id}/heartbeat"
        )


# Registry server implementation
from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import uuid

registry_app = FastAPI()
servers: dict[str, dict] = {}
HEARTBEAT_TIMEOUT = timedelta(minutes=5)


@registry_app.post("/servers")
async def register(data: dict) -> dict:
    server_id = str(uuid.uuid4())
    servers[server_id] = {
        **data,
        "id": server_id,
        "registered_at": datetime.utcnow().isoformat(),
        "last_heartbeat": datetime.utcnow()
    }
    return {"server_id": server_id}


@registry_app.get("/servers")
async def list_servers(
    capabilities: Optional[str] = None,
    tags: Optional[str] = None
) -> dict:
    # Filter out stale servers
    now = datetime.utcnow()
    active = {
        k: v for k, v in servers.items()
        if now - v["last_heartbeat"] < HEARTBEAT_TIMEOUT
    }

    result = list(active.values())

    if capabilities:
        required = set(capabilities.split(","))
        result = [s for s in result if required <= set(s.get("capabilities", []))]

    if tags:
        required = set(tags.split(","))
        result = [s for s in result if required & set(s.get("tags", []))]

    return {"servers": result}


@registry_app.post("/servers/{server_id}/heartbeat")
async def heartbeat(server_id: str):
    if server_id not in servers:
        raise HTTPException(404, "Server not found")
    servers[server_id]["last_heartbeat"] = datetime.utcnow()
    return {"status": "ok"}
```

## Capability Negotiation

During connection initialization, clients and servers negotiate capabilities:

### Server Capability Declaration

```python
from mcp.server import Server
from mcp.types import ServerCapabilities, ToolCapabilities

server = Server("my-server")

# Declare server capabilities
capabilities = ServerCapabilities(
    tools=ToolCapabilities(
        list_changed=True  # Server will notify when tools change
    ),
    resources=ResourceCapabilities(
        list_changed=True,
        subscribe=True  # Server supports resource subscriptions
    ),
    prompts=PromptCapabilities(
        list_changed=True
    ),
    experimental={
        "tasks": {
            "supported": True,
            "max_concurrent": 10
        }
    }
)

@server.initialize_handler
async def handle_initialize(params):
    return {
        "protocolVersion": "2025-11-25",
        "serverInfo": {
            "name": "my-server",
            "version": "1.0.0"
        },
        "capabilities": capabilities.model_dump()
    }
```

### Client Capability Requirements

```python
from mcp import ClientSession

async def connect_with_requirements(
    read_stream,
    write_stream,
    required_capabilities: list[str]
) -> ClientSession:
    """Connect to server, verifying required capabilities."""

    async with ClientSession(read_stream, write_stream) as session:
        init_result = await session.initialize()

        server_caps = init_result.capabilities
        missing = []

        for cap in required_capabilities:
            if cap == "tools" and not server_caps.tools:
                missing.append(cap)
            elif cap == "resources" and not server_caps.resources:
                missing.append(cap)
            elif cap == "prompts" and not server_caps.prompts:
                missing.append(cap)
            elif cap == "tasks" and not server_caps.experimental.get("tasks"):
                missing.append(cap)
            elif cap == "sampling" and not server_caps.sampling:
                missing.append(cap)

        if missing:
            raise RuntimeError(f"Server missing required capabilities: {missing}")

        return session
```

## Dynamic Tool Discovery

### Handling listChanged Notifications

When servers modify their tool set dynamically:

```python
from mcp import ClientSession

class DynamicToolClient:
    def __init__(self):
        self.tools: dict[str, dict] = {}
        self.session: Optional[ClientSession] = None

    async def connect(self, read_stream, write_stream):
        self.session = ClientSession(read_stream, write_stream)
        await self.session.initialize()

        # Check if server supports list_changed
        caps = self.session.server_capabilities
        if caps.tools and caps.tools.list_changed:
            # Subscribe to tool changes
            self.session.on_notification(
                "notifications/tools/list_changed",
                self._on_tools_changed
            )

        # Initial tool fetch
        await self._refresh_tools()

    async def _refresh_tools(self):
        """Fetch and cache current tools."""
        result = await self.session.list_tools()
        self.tools = {t.name: t.model_dump() for t in result.tools}
        logger.info("Tools refreshed: %d tools available", len(self.tools))

    async def _on_tools_changed(self):
        """Handle tools/list_changed notification."""
        logger.info("Tools changed notification received")
        await self._refresh_tools()

    def get_tool(self, name: str) -> Optional[dict]:
        return self.tools.get(name)

    def list_tools(self) -> list[dict]:
        return list(self.tools.values())
```

### Server-Side Dynamic Tools

```python
from fastmcp import FastMCP
import asyncio

mcp = FastMCP("dynamic-server")

# Track registered tools
registered_tools: set[str] = set()


async def register_plugin_tools(plugin_name: str, tools: list[dict]):
    """Dynamically register tools from a plugin."""
    for tool_def in tools:
        tool_name = f"{plugin_name}_{tool_def['name']}"

        @mcp.tool(name=tool_name)
        async def dynamic_tool(**kwargs):
            # Route to plugin handler
            return await plugin_handlers[plugin_name](tool_def['name'], kwargs)

        registered_tools.add(tool_name)

    # Notify clients of tool change
    await mcp.notify_tools_changed()


async def unregister_plugin_tools(plugin_name: str):
    """Remove tools from a plugin."""
    prefix = f"{plugin_name}_"
    to_remove = [t for t in registered_tools if t.startswith(prefix)]

    for tool_name in to_remove:
        mcp.remove_tool(tool_name)
        registered_tools.discard(tool_name)

    await mcp.notify_tools_changed()
```

## Multi-Environment Discovery

For applications spanning dev/staging/prod:

```python
from enum import Enum
from typing import Optional
import os


class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentAwareDiscovery:
    """Discover servers based on current environment."""

    def __init__(self):
        self.env = Environment(os.getenv("MCP_ENV", "development"))
        self.base_urls = {
            Environment.DEVELOPMENT: "http://localhost:8000",
            Environment.STAGING: "https://staging.mcp.example.com",
            Environment.PRODUCTION: "https://mcp.example.com"
        }

    def get_server_url(self, server_name: str) -> str:
        """Get server URL for current environment."""
        base = self.base_urls[self.env]
        return f"{base}/{server_name}/mcp"

    async def discover_servers(self) -> list[dict]:
        """Discover all servers for current environment."""
        base = self.base_urls[self.env]

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base}/.well-known/mcp/servers.json")
            if response.status_code == 200:
                return response.json()["servers"]
            return []

    def get_config_for_env(self, server_name: str) -> dict:
        """Get environment-specific server configuration."""
        configs = {
            Environment.DEVELOPMENT: {
                "timeout": 60,
                "retry_count": 1,
                "verify_ssl": False
            },
            Environment.STAGING: {
                "timeout": 30,
                "retry_count": 2,
                "verify_ssl": True
            },
            Environment.PRODUCTION: {
                "timeout": 10,
                "retry_count": 3,
                "verify_ssl": True
            }
        }
        return configs[self.env]
```

## Best Practices

### Discovery

1. **Cache server cards** - Use appropriate TTL (1-24 hours)
2. **Health check before use** - Verify server is responding
3. **Handle discovery failures gracefully** - Fall back to cached data
4. **Support multiple discovery methods** - Well-known, registry, manual config

### Capability Negotiation

1. **Fail fast on missing capabilities** - Check at connection time
2. **Support capability fallbacks** - Use alternatives when possible
3. **Version compatibility** - Check protocol version before capability check
4. **Log negotiation results** - Debug capability mismatches

### Dynamic Tools

1. **Subscribe to changes** - Don't poll for tool list
2. **Cache tool definitions** - Minimize list_tools calls
3. **Handle races** - Tool may disappear between list and call
4. **Namespace plugins** - Prevent tool name collisions

## Related

- **Client Development**: See `resources/client-development.md` for full client implementation
- **Architecture Patterns**: See `resources/architecture-patterns.md` for multi-server deployments
