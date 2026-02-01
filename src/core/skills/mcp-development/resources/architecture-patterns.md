# MCP Architecture Patterns Guide

Comprehensive guide for designing and deploying MCP-based systems at scale, including session management, load balancing, and multi-region deployments.

## Architecture Decision Framework

```
┌──────────────────────────────────────────────────────────────────┐
│                    Architecture Selection                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Single Server           Multi-Server              Gateway        │
│  ┌─────┐                ┌─────┐ ┌─────┐         ┌─────────┐     │
│  │ MCP │                │ MCP │ │ MCP │         │ Gateway │     │
│  │ Srv │                │ Srv │ │ Srv │         └────┬────┘     │
│  └──┬──┘                └──┬──┘ └──┬──┘              │          │
│     │                      │       │           ┌─────┴─────┐    │
│     │                      └───┬───┘           │           │    │
│  ┌──▼──┐                   ┌──▼──┐          ┌─▼─┐       ┌─▼─┐  │
│  │Client│                  │Client│         │MCP│       │MCP│  │
│  └─────┘                   └─────┘          │Srv│       │Srv│  │
│                                              └───┘       └───┘  │
│  Use when:                Use when:          Use when:          │
│  - Simple use case        - Multiple domains - Load balancing   │
│  - Single domain          - Tool namespacing - Auth gateway     │
│  - Direct access          - Fault isolation  - Rate limiting    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Pattern 1: Single Client, Single Server

Simplest pattern - direct connection between one client and one server.

```python
# Simple direct connection
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession


async def simple_client(server_url: str):
    async with streamable_http_client(f"{server_url}/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            # Use tools...
```

**When to use:**

- Prototyping and development
- Single-purpose applications
- Direct tool access without orchestration

**Limitations:**

- No fault tolerance
- Single point of failure
- No tool aggregation

## Pattern 2: Multi-Server Aggregation

Single client connecting to multiple servers with tool aggregation.

```
┌─────────────────────────────────────────┐
│              MCP Client                  │
│  ┌───────────────────────────────────┐  │
│  │      Tool Aggregation Layer       │  │
│  │  filesystem.read_file             │  │
│  │  github.create_issue              │  │
│  │  slack.post_message               │  │
│  └───────────────────────────────────┘  │
│         │           │           │        │
│    ┌────▼────┐ ┌────▼────┐ ┌────▼────┐  │
│    │Filesystem│ │ GitHub  │ │  Slack  │  │
│    │ Server   │ │ Server  │ │ Server  │  │
│    └─────────┘ └─────────┘ └─────────┘  │
└─────────────────────────────────────────┘
```

See `resources/client-development.md` for full implementation.

**When to use:**

- Composing tools from multiple domains
- Building AI agents with diverse capabilities
- Each server maintained independently

**Key considerations:**

- Tool namespacing to prevent collisions
- Independent failure handling per server
- Capability aggregation

## Pattern 3: Gateway/Proxy

Central gateway that routes requests to appropriate backend servers.

```
                   ┌─────────────┐
                   │   Clients   │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │   Gateway   │
                   │  - Auth     │
                   │  - Routing  │
                   │  - Caching  │
                   └──────┬──────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
    │Server A │      │Server B │      │Server C │
    │(CRM)    │      │(Docs)   │      │(Calendar)│
    └─────────┘      └─────────┘      └─────────┘
```

```python
from fastapi import FastAPI, Request, Response
import httpx
from typing import Optional
import json

app = FastAPI()


# Server registry
SERVERS = {
    "crm": "http://crm-server:8000/mcp",
    "docs": "http://docs-server:8000/mcp",
    "calendar": "http://calendar-server:8000/mcp"
}


# Tool to server mapping (built at startup)
tool_routes: dict[str, str] = {}


async def build_tool_routes():
    """Discover all tools and build routing table."""
    async with httpx.AsyncClient() as client:
        for server_name, url in SERVERS.items():
            try:
                # List tools from each server
                response = await client.post(
                    url,
                    json={
                        "jsonrpc": "2.0",
                        "method": "tools/list",
                        "id": 1
                    }
                )
                result = response.json()
                for tool in result.get("result", {}).get("tools", []):
                    tool_routes[tool["name"]] = server_name
            except Exception as e:
                print(f"Failed to fetch tools from {server_name}: {e}")


@app.on_event("startup")
async def startup():
    await build_tool_routes()


@app.post("/mcp")
async def gateway(request: Request):
    body = await request.json()
    method = body.get("method", "")

    # Aggregate tool listing
    if method == "tools/list":
        return await aggregate_tools()

    # Route tool calls
    if method == "tools/call":
        tool_name = body.get("params", {}).get("name")
        server_name = tool_routes.get(tool_name)
        if not server_name:
            return {"jsonrpc": "2.0", "id": body.get("id"), "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}
        return await forward_to_server(server_name, body)

    # Forward other requests to primary server
    return await forward_to_server("crm", body)


async def aggregate_tools():
    """Aggregate tools from all servers."""
    all_tools = []
    async with httpx.AsyncClient() as client:
        for server_name, url in SERVERS.items():
            response = await client.post(
                url,
                json={"jsonrpc": "2.0", "method": "tools/list", "id": 1}
            )
            result = response.json()
            tools = result.get("result", {}).get("tools", [])
            # Optionally namespace tools
            for tool in tools:
                tool["_server"] = server_name
            all_tools.extend(tools)

    return {"jsonrpc": "2.0", "id": 1, "result": {"tools": all_tools}}


async def forward_to_server(server_name: str, body: dict):
    """Forward request to backend server."""
    url = SERVERS[server_name]
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=body)
        return response.json()
```

**When to use:**

- Centralized authentication
- Rate limiting across servers
- Tool discovery and routing
- Caching common responses

## Pattern 4: Load-Balanced Servers

Horizontal scaling with multiple server instances behind a load balancer.

```
              ┌─────────────┐
              │   Client    │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │Load Balancer│
              │  (nginx/k8s)│
              └──────┬──────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│Server │        │Server │        │Server │
│  #1   │        │  #2   │        │  #3   │
└───┬───┘        └───┬───┘        └───┬───┘
    │                │                │
    └────────────────┼────────────────┘
                     │
              ┌──────▼──────┐
              │Shared State │
              │   (Redis)   │
              └─────────────┘
```

### Session Affinity Configuration

```yaml
# Kubernetes ingress with session affinity
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mcp-server
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "MCP_SESSION"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "3600"
spec:
  rules:
    - host: mcp.example.com
      http:
        paths:
          - path: /mcp
            pathType: Prefix
            backend:
              service:
                name: mcp-server
                port:
                  number: 8000
```

### Shared Session Store

```python
import redis.asyncio as redis
from dataclasses import dataclass
from typing import Optional
import json
import secrets


@dataclass
class SessionData:
    session_id: str
    user_id: str
    capabilities: dict
    created_at: str
    last_activity: str
    metadata: dict


class RedisSessionStore:
    """Redis-backed session store for distributed MCP servers."""

    def __init__(self, redis_url: str, ttl_seconds: int = 3600):
        self.client = redis.from_url(redis_url)
        self.ttl = ttl_seconds

    async def create_session(
        self,
        user_id: str,
        capabilities: dict,
        metadata: Optional[dict] = None
    ) -> str:
        """Create new session and return session ID."""
        session_id = secrets.token_urlsafe(32)
        now = datetime.utcnow().isoformat()

        session = SessionData(
            session_id=session_id,
            user_id=user_id,
            capabilities=capabilities,
            created_at=now,
            last_activity=now,
            metadata=metadata or {}
        )

        await self.client.setex(
            f"mcp:session:{session_id}",
            self.ttl,
            json.dumps(session.__dict__)
        )

        return session_id

    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Retrieve session by ID."""
        data = await self.client.get(f"mcp:session:{session_id}")
        if not data:
            return None

        session_dict = json.loads(data)
        return SessionData(**session_dict)

    async def update_activity(self, session_id: str) -> None:
        """Update last activity timestamp."""
        session = await self.get_session(session_id)
        if session:
            session.last_activity = datetime.utcnow().isoformat()
            await self.client.setex(
                f"mcp:session:{session_id}",
                self.ttl,
                json.dumps(session.__dict__)
            )

    async def delete_session(self, session_id: str) -> None:
        """Delete a session."""
        await self.client.delete(f"mcp:session:{session_id}")

    async def get_active_sessions(self, user_id: str) -> list[str]:
        """Get all active sessions for a user."""
        pattern = "mcp:session:*"
        sessions = []

        async for key in self.client.scan_iter(match=pattern):
            data = await self.client.get(key)
            if data:
                session = json.loads(data)
                if session.get("user_id") == user_id:
                    sessions.append(session["session_id"])

        return sessions
```

## Pattern 5: Serverless/Edge

Deploy MCP servers as serverless functions for automatic scaling.

```
              ┌─────────────┐
              │   Client    │
              └──────┬──────┘
                     │
              ┌──────▼──────┐
              │  API Gateway│
              │(AWS/Vercel) │
              └──────┬──────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐        ┌───▼───┐        ┌───▼───┐
│Lambda │        │Lambda │        │Lambda │
│  fn   │        │  fn   │        │  fn   │
└───────┘        └───────┘        └───────┘
```

### AWS Lambda Handler

```python
import json
from mangum import Mangum
from fastapi import FastAPI
from mcp.server import Server

app = FastAPI()
mcp_server = Server("serverless-mcp")

# Configure MCP server tools...

@app.post("/mcp")
async def handle_mcp(request: dict):
    # Process MCP request
    response = await mcp_server.handle_request(request)
    return response


# Lambda handler
handler = Mangum(app)
```

### Vercel Edge Function

```typescript
// api/mcp.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({ name: "edge-mcp", version: "1.0.0" });

// Configure tools...

export const config = {
  runtime: "edge",
};

export default async function handler(req: Request) {
  if (req.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  const body = await req.json();
  const response = await server.handleRequest(body);

  return new Response(JSON.stringify(response), {
    headers: { "Content-Type": "application/json" },
  });
}
```

**When to use:**

- Stateless tools (no session required)
- Infrequent usage patterns
- Cost optimization for variable load
- Global edge deployment

**Limitations:**

- Cold start latency
- No persistent connections
- Limited execution time
- Stateless by default

## Pattern 6: Multi-Region Deployment

Geo-distributed servers for low latency and high availability.

```
                    ┌─────────────┐
                    │   Client    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  GeoDNS/    │
                    │  Anycast    │
                    └──────┬──────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
┌───▼───┐              ┌───▼───┐              ┌───▼───┐
│US-East│              │EU-West│              │AP-East│
│Region │              │Region │              │Region │
└───┬───┘              └───┬───┘              └───┬───┘
    │                      │                      │
    └──────────────────────┼──────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  Global DB  │
                    │(CockroachDB)│
                    └─────────────┘
```

### Region-Aware Client

```python
import httpx
from typing import Optional


class MultiRegionClient:
    """MCP client with multi-region failover."""

    def __init__(self, regions: dict[str, str]):
        """
        Args:
            regions: Map of region name to endpoint URL
                     {"us-east": "https://us.mcp.example.com/mcp", ...}
        """
        self.regions = regions
        self.primary_region: Optional[str] = None
        self.latencies: dict[str, float] = {}

    async def discover_fastest_region(self) -> str:
        """Measure latency to each region and select fastest."""
        import time

        async with httpx.AsyncClient() as client:
            for region, url in self.regions.items():
                try:
                    start = time.monotonic()
                    await client.get(url.replace("/mcp", "/health"), timeout=5.0)
                    latency = time.monotonic() - start
                    self.latencies[region] = latency
                except Exception:
                    self.latencies[region] = float("inf")

        # Select region with lowest latency
        self.primary_region = min(self.latencies, key=self.latencies.get)
        return self.primary_region

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict,
        max_retries: int = 2
    ) -> dict:
        """Call tool with region failover."""
        if not self.primary_region:
            await self.discover_fastest_region()

        # Sort regions by latency
        sorted_regions = sorted(
            self.regions.keys(),
            key=lambda r: self.latencies.get(r, float("inf"))
        )

        last_error = None
        for region in sorted_regions[:max_retries + 1]:
            try:
                url = self.regions[region]
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        url,
                        json={
                            "jsonrpc": "2.0",
                            "method": "tools/call",
                            "params": {"name": tool_name, "arguments": arguments},
                            "id": 1
                        },
                        timeout=30.0
                    )
                    return response.json()
            except Exception as e:
                last_error = e
                # Mark region as slow
                self.latencies[region] = float("inf")

        raise RuntimeError(f"All regions failed: {last_error}")
```

## Session Persistence Strategies

### Strategy 1: In-Memory (Single Instance)

```python
# Simple in-memory store - development only
sessions: dict[str, dict] = {}
```

### Strategy 2: Redis (Distributed)

See Redis session store implementation above.

### Strategy 3: Database (Persistent)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, JSON, DateTime
from datetime import datetime

Base = declarative_base()


class MCPSession(Base):
    __tablename__ = "mcp_sessions"

    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(64), index=True)
    capabilities: Mapped[dict] = mapped_column(JSON)
    metadata: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, index=True)


class DatabaseSessionStore:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)

    async def create_session(
        self,
        user_id: str,
        capabilities: dict,
        ttl_seconds: int = 3600
    ) -> str:
        session_id = secrets.token_urlsafe(32)
        now = datetime.utcnow()

        async with AsyncSession(self.engine) as db:
            session = MCPSession(
                session_id=session_id,
                user_id=user_id,
                capabilities=capabilities,
                created_at=now,
                last_activity=now,
                expires_at=now + timedelta(seconds=ttl_seconds)
            )
            db.add(session)
            await db.commit()

        return session_id
```

### Strategy 4: Hybrid (Redis + Database)

```python
class HybridSessionStore:
    """Redis for hot data, database for persistence."""

    def __init__(self, redis_url: str, database_url: str):
        self.redis = RedisSessionStore(redis_url)
        self.db = DatabaseSessionStore(database_url)

    async def get_session(self, session_id: str) -> Optional[SessionData]:
        # Try Redis first (fast path)
        session = await self.redis.get_session(session_id)
        if session:
            return session

        # Fall back to database
        session = await self.db.get_session(session_id)
        if session:
            # Repopulate Redis cache
            await self.redis.save_session(session)
            return session

        return None

    async def create_session(self, **kwargs) -> str:
        # Create in both stores
        session_id = await self.db.create_session(**kwargs)
        await self.redis.create_session(session_id, **kwargs)
        return session_id
```

## Deployment Checklist

### Pre-Deployment

- [ ] Choose architecture pattern based on requirements
- [ ] Plan session persistence strategy
- [ ] Configure health checks
- [ ] Set up monitoring and alerting
- [ ] Plan capacity and scaling rules

### Security

- [ ] Origin validation configured
- [ ] TLS/HTTPS enabled
- [ ] Authentication implemented
- [ ] Rate limiting configured
- [ ] Input validation on all tools

### Observability

- [ ] Structured logging enabled
- [ ] OpenTelemetry tracing configured
- [ ] Metrics collection set up
- [ ] Alerting rules defined

### Resilience

- [ ] Health checks implemented
- [ ] Graceful shutdown handling
- [ ] Connection retry logic
- [ ] Circuit breakers for external services
- [ ] Backup/recovery procedures

## Best Practices

### Scaling

1. **Start simple** - Single server until you need more
2. **Scale horizontally** - Add instances, not bigger machines
3. **Use session affinity** - Minimize cross-instance coordination
4. **Cache aggressively** - Tool definitions, auth tokens, etc.

### Reliability

1. **Health checks** - `/health` endpoint for load balancers
2. **Graceful degradation** - Handle partial failures
3. **Circuit breakers** - Prevent cascade failures
4. **Timeouts everywhere** - Don't hang on slow dependencies

### Performance

1. **Connection pooling** - Reuse HTTP/DB connections
2. **Async everything** - Non-blocking I/O
3. **Batch operations** - Reduce round trips
4. **Edge caching** - Static responses at CDN

## Related

- **Client Development**: See `resources/client-development.md`
- **Server Development**: See main SKILL.md
- **Tasks Primitive**: See `resources/tasks-primitive.md`
