# MCP Development Skill

Build production-ready Model Context Protocol (MCP) servers with fastmcp, PII sanitization, and OpenTelemetry integration.

## Overview

This skill provides comprehensive expertise for building, testing, and deploying MCP servers following best practices for security, performance, and observability.

## When to Use This Skill

Trigger this skill when:

- Building MCP servers with fastmcp (Python)
- Implementing MCP tools, resources, or prompts
- Adding PII sanitization to MCP contexts
- Upgrading fastmcp dependencies safely
- Configuring Kubernetes deployments for MCP servers
- Integrating OpenTelemetry (OpenTelemetry)
- Debugging MCP server implementations
- Optimizing MCP server performance
- Creating MCP client integrations
- Validating MCP protocol compliance

**Keywords:** MCP, fastmcp, Model Context Protocol, PII sanitization, Kubernetes deployment, OpenTelemetry, tool definition, resource definition

## Core Principles

### MCP Security Standards

- **PII Protection**: Never expose PII through MCP tools/resources without sanitization
- **Input Validation**: Validate all tool inputs with JSON schemas using Pydantic
- **Rate Limiting**: Implement rate limiting for MCP endpoints
- **Audit Logging**: Log all MCP interactions with context (sanitized)
- **Least Privilege**: MCP tools should request minimum necessary permissions

### Observability Requirements

- **Structured Logging**: Use Python logging with JSON formatting
- **OpenTelemetry Tracing**: Instrument all MCP operations with spans
- **Metrics Collection**: Track tool invocation counts, latency, errors
- **Error Context**: Include sanitized context in error logs

### Protocol Best Practices

- **Tool Descriptions**: Write clear, LLM-friendly tool descriptions
- **Schema Validation**: Use Pydantic models for type safety
- **Error Handling**: Return meaningful error messages
- **Graceful Degradation**: Handle partial failures elegantly
- **Idempotency**: Design tools to be safely retryable

## FastMCP Server Patterns

### Server Initialization

```python
from fastmcp import FastMCP
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server with metadata
mcp = FastMCP(
    "server-name",
    dependencies=["dependency1>=1.0.0", "dependency2>=2.0.0"]
)

# Server lifecycle hooks
@mcp.on_startup
async def startup():
    logger.info("MCP server starting", extra={"server": "server-name"})
    # Initialize resources (DB connections, API clients, etc.)

@mcp.on_shutdown
async def shutdown():
    logger.info("MCP server shutting down")
    # Cleanup resources
```

### Tool Definition Pattern

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class ToolInput(BaseModel):
    """Well-documented input schema for LLM consumption"""

    query: str = Field(
        ...,
        description="The search query to execute",
        min_length=1,
        max_length=500
    )

    limit: int = Field(
        10,
        description="Maximum number of results to return",
        ge=1,
        le=100
    )

    @validator('query')
    def validate_query(cls, v):
        """Additional validation beyond Pydantic constraints"""
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace")
        return v.strip()

@mcp.tool()
async def search_documents(input: ToolInput) -> str:
    """
    Search through document corpus and return relevant results.

    Use this tool when the user needs to find specific information
    from the knowledge base. Returns up to {limit} results ranked
    by relevance.

    Args:
        input: Validated search parameters

    Returns:
        JSON string with search results and metadata

    Raises:
        ValueError: If search query is invalid
        RuntimeError: If search service is unavailable
    """
    from opentelemetry import trace

    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("search_documents") as span:
        # Sanitize PII from input before logging
        sanitized_query = sanitize_pii(input.query)

        span.set_attribute("query.length", len(input.query))
        span.set_attribute("query.limit", input.limit)

        logger.info(
            "Executing search",
            extra={
                "query": sanitized_query,
                "limit": input.limit
            }
        )

        try:
            # Business logic with error handling
            results = await perform_search(input.query, input.limit)

            # Sanitize PII from results
            sanitized_results = sanitize_pii(results)

            span.set_attribute("results.count", len(results))

            return sanitized_results

        except Exception as e:
            logger.error(
                "Search failed",
                exc_info=True,
                extra={"query": sanitized_query}
            )
            span.record_exception(e)
            raise RuntimeError(f"Search operation failed: {str(e)}")
```

### Resource Definition Pattern

```python
@mcp.resource("resource://documents/{doc_id}")
async def get_document(doc_id: str) -> str:
    """
    Retrieve a document by ID from the knowledge base.

    Returns the full document content with metadata.
    Use when Claude needs to access specific document content.

    Args:
        doc_id: Unique document identifier

    Returns:
        JSON string with document content and metadata
    """
    # Validate input
    if not is_valid_doc_id(doc_id):
        raise ValueError(f"Invalid document ID format: {doc_id}")

    logger.info("Fetching document", extra={"doc_id": doc_id})

    # Fetch and sanitize
    document = await fetch_document(doc_id)

    if not document:
        raise ValueError(f"Document not found: {doc_id}")

    # Sanitize PII before returning
    sanitized_content = sanitize_pii(document.content)

    return json.dumps({
        "id": document.id,
        "title": document.title,
        "content": sanitized_content,
        "created_at": document.created_at.isoformat(),
        "updated_at": document.updated_at.isoformat()
    })
```

### Prompt Definition Pattern

```python
@mcp.prompt()
async def summarize_document(doc_id: str) -> str:
    """
    Generate a prompt for Claude to summarize a specific document.

    This prompt template helps Claude provide consistent, high-quality
    document summaries with proper structure.

    Args:
        doc_id: Document to summarize

    Returns:
        Formatted prompt for Claude
    """
    document = await fetch_document(doc_id)
    sanitized_content = sanitize_pii(document.content)

    return f"""Please provide a comprehensive summary of the following document:

Title: {document.title}
Created: {document.created_at}

Content:
{sanitized_content}

Generate a summary that includes:
1. Main topics and key points (3-5 bullet points)
2. Important conclusions or recommendations
3. Any action items or next steps mentioned

Keep the summary concise (2-3 paragraphs) but capture all essential information."""
```

## PII Sanitization Implementation

### Core Sanitization Patterns

```python
import re
from typing import Any, Dict, Union

# PII detection patterns
EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)
SSN_PATTERN = re.compile(
    r'\b\d{3}-\d{2}-\d{4}\b'
)
PHONE_PATTERN = re.compile(
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
)
CREDIT_CARD_PATTERN = re.compile(
    r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
)
# Add more patterns as needed

def sanitize_pii(text: Union[str, dict, list]) -> Union[str, dict, list]:
    """
    Remove PII from text, dictionaries, or lists recursively.

    Args:
        text: Content to sanitize

    Returns:
        Sanitized content with PII replaced by placeholders
    """
    if isinstance(text, dict):
        return sanitize_dict(text)
    elif isinstance(text, list):
        return [sanitize_pii(item) for item in text]
    elif isinstance(text, str):
        return sanitize_string(text)
    else:
        return text

def sanitize_string(text: str) -> str:
    """Sanitize PII from a string"""
    if not text:
        return text

    # Apply all sanitization patterns
    text = EMAIL_PATTERN.sub('[EMAIL]', text)
    text = SSN_PATTERN.sub('[SSN]', text)
    text = PHONE_PATTERN.sub('[PHONE]', text)
    text = CREDIT_CARD_PATTERN.sub('[CREDIT_CARD]', text)

    return text

def sanitize_dict(
    data: Dict[str, Any],
    sensitive_keys: Optional[list[str]] = None
) -> Dict[str, Any]:
    """
    Sanitize dictionary values recursively.

    Args:
        data: Dictionary to sanitize
        sensitive_keys: List of keys that should be redacted completely

    Returns:
        Sanitized dictionary
    """
    if sensitive_keys is None:
        sensitive_keys = [
            'password', 'secret', 'token', 'api_key',
            'ssn', 'social_security', 'credit_card',
            'email', 'phone', 'address'
        ]

    sanitized = {}
    for key, value in data.items():
        # Redact sensitive keys completely
        if any(sensitive in key.lower() for sensitive in sensitive_keys):
            sanitized[key] = '[REDACTED]'
        # Recursively sanitize nested structures
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value, sensitive_keys)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_pii(item) for item in value]
        elif isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        else:
            sanitized[key] = value

    return sanitized
```

### PII Sanitization Checklist

Critical for all MCP implementations:

- [ ] Sanitize before logging (never log raw PII)
- [ ] Sanitize before external API calls
- [ ] Sanitize before caching or storage
- [ ] Sanitize in error messages and exceptions
- [ ] Sanitize in tool return values
- [ ] Sanitize in resource content
- [ ] Test with PII patterns (emails, SSNs, credit cards, phones)
- [ ] Implement field-level redaction for sensitive keys
- [ ] Use regex patterns for common PII types
- [ ] Validate sanitization with comprehensive test suite (22+ tests)
- [ ] Handle nested data structures (dicts, lists)
- [ ] Document PII handling in tool descriptions

## MCP Client Integration

### Stdio Transport (Recommended)

```python
from mcp.client.stdio import stdio_client
from mcp import ClientSession

async def connect_to_mcp_server():
    """Connect to MCP server via stdio transport"""

    async with stdio_client(
        command="uv",
        args=["run", "python", "server.py"]
    ) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            logger.info("Connected to MCP server")

            # List available tools
            tools = await session.list_tools()
            logger.info(f"Available tools: {[t.name for t in tools]}")

            # Call a tool
            result = await session.call_tool(
                "search_documents",
                {
                    "query": "machine learning",
                    "limit": 5
                }
            )

            return result
```

### SSE Transport (Server-Sent Events)

```python
from mcp.client.sse import sse_client
from mcp import ClientSession

async def connect_via_sse():
    """Connect to MCP server via SSE transport"""

    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Use session...
            tools = await session.list_tools()
            return tools
```

## Kubernetes Deployment

### Kubernetes Deployment Configuration

For deploying MCP servers to Kubernetes:

**See Related Skill:** Reference the `kubernetes-deployment` skill for complete Kubernetes deployment patterns.

```yaml
# kubernetes.yml for MCP server deployment
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
  namespace: your-namespace
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 8000
      targetPort: 8000
  selector:
    app: mcp-server

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
        - name: mcp-server
          image: registry.example.com/your-team/mcp-server:latest
          ports:
            - containerPort: 8000
          env:
            - name: LOG_LEVEL
              value: "INFO"
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://universal-tracing:4318"
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

### OpenTelemetry Integration

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name: str):
    """
    Configure OpenTelemetry.

    Args:
        service_name: Name of the MCP server for trace identification
    """
    resource = Resource.create({"service.name": service_name})

    tracer_provider = TracerProvider(resource=resource)

    # Configure OTLP exporter for OpenTelemetry
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://universal-tracing:4318/v1/traces"
    )

    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)

    trace.set_tracer_provider(tracer_provider)

    logger.info(f"OpenTelemetry configured for {service_name}")

# Use in MCP server
tracer = trace.get_tracer(__name__)

@mcp.tool()
async def traced_tool(input: ToolInput) -> str:
    """Tool with OpenTelemetry tracing"""

    with tracer.start_as_current_span("tool_execution") as span:
        # Add attributes (sanitized)
        span.set_attribute("input.param", sanitize_pii(str(input)))
        span.set_attribute("tool.name", "traced_tool")

        try:
            result = await process(input)
            span.set_attribute("result.length", len(result))
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise
```

## Testing Strategies

### Unit Testing with pytest

```python
import pytest
from fastmcp.testing import MCPTestClient

@pytest.fixture
async def test_client():
    """Fixture providing MCP test client"""
    client = MCPTestClient(mcp)
    await client.connect()
    yield client
    await client.disconnect()

# Test tool execution
async def test_search_documents_success(test_client):
    """Test successful search operation"""
    result = await test_client.call_tool(
        "search_documents",
        {"query": "test query", "limit": 10}
    )

    assert result.success
    assert "results" in result.content

# Test input validation
async def test_search_documents_invalid_input(test_client):
    """Test search with invalid input"""
    with pytest.raises(ValueError, match="Query cannot be empty"):
        await test_client.call_tool(
            "search_documents",
            {"query": "   ", "limit": 10}
        )

# Test PII sanitization
async def test_pii_sanitization(test_client):
    """Test that PII is properly sanitized"""
    result = await test_client.call_tool(
        "search_documents",
        {"query": "email test@example.com phone 555-123-4567", "limit": 5}
    )

    # PII should be redacted in result
    assert "[EMAIL]" in result.content
    assert "[PHONE]" in result.content
    assert "test@example.com" not in result.content
    assert "555-123-4567" not in result.content

# Test error handling
async def test_tool_error_handling(test_client):
    """Test proper error handling and messaging"""
    with pytest.raises(RuntimeError, match="Search operation failed"):
        await test_client.call_tool(
            "search_documents",
            {"query": "trigger_error", "limit": 10}
        )
```

### PII Sanitization Test Suite

```python
import pytest
from sanitization import sanitize_pii, sanitize_string, sanitize_dict

# Email sanitization tests
def test_sanitize_email():
    assert sanitize_string("Contact: test@example.com") == "Contact: [EMAIL]"

def test_sanitize_multiple_emails():
    text = "Emails: a@test.com and b@test.com"
    assert sanitize_string(text) == "Emails: [EMAIL] and [EMAIL]"

# SSN sanitization tests
def test_sanitize_ssn():
    assert sanitize_string("SSN: 123-45-6789") == "SSN: [SSN]"

# Phone sanitization tests
def test_sanitize_phone():
    assert sanitize_string("Call 555-123-4567") == "Call [PHONE]"
    assert sanitize_string("Call 5551234567") == "Call [PHONE]"

# Credit card sanitization tests
def test_sanitize_credit_card():
    text = "Card: 1234-5678-9012-3456"
    assert sanitize_string(text) == "Card: [CREDIT_CARD]"

# Dictionary sanitization tests
def test_sanitize_dict_sensitive_keys():
    data = {"password": "secret123", "username": "john"}
    result = sanitize_dict(data)
    assert result["password"] == "[REDACTED]"
    assert result["username"] == "john"

def test_sanitize_nested_dict():
    data = {
        "user": {
            "email": "test@example.com",
            "name": "John Doe"
        }
    }
    result = sanitize_dict(data)
    assert result["user"]["email"] == "[REDACTED]"
    assert result["user"]["name"] == "John Doe"

# Edge case tests
def test_sanitize_empty_string():
    assert sanitize_string("") == ""
    assert sanitize_string(None) is None

def test_sanitize_no_pii():
    text = "This is clean text with no PII"
    assert sanitize_string(text) == text

def test_sanitize_mixed_pii():
    text = "Contact test@example.com or 555-1234 SSN: 123-45-6789"
    result = sanitize_string(text)
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "[SSN]" in result
    assert "test@example.com" not in result

# List sanitization tests
def test_sanitize_list():
    data = ["email: test@example.com", "phone: 555-1234"]
    result = sanitize_pii(data)
    assert "[EMAIL]" in result[0]
    assert "[PHONE]" in result[1]

# 22+ tests total covering all PII types and edge cases
```

## Performance Optimization

### Connection Pooling

```python
from aiohttp import ClientSession
from typing import Optional

class OptimizedMCPServer:
    """MCP server with connection pooling"""

    def __init__(self):
        self._session: Optional[ClientSession] = None
        self._cache = {}

    async def get_session(self) -> ClientSession:
        """Get or create HTTP session"""
        if self._session is None or self._session.closed:
            self._session = ClientSession(
                timeout=ClientTimeout(total=30),
                connector=TCPConnector(limit=100)
            )
        return self._session

    async def cleanup(self):
        """Cleanup resources"""
        if self._session and not self._session.closed:
            await self._session.close()

# Use in server lifecycle
server = OptimizedMCPServer()

@mcp.on_shutdown
async def shutdown():
    await server.cleanup()
```

### Caching Strategy

```python
from functools import lru_cache
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

# Sync cache for deterministic lookups
@lru_cache(maxsize=128)
def get_config(key: str) -> str:
    """Cache configuration values"""
    return load_config(key)

# Async cache with TTL
@cached(
    ttl=300,  # 5 minute cache
    cache=Cache.MEMORY,
    serializer=JsonSerializer()
)
async def fetch_expensive_data(id: str) -> dict:
    """Cache expensive operations"""
    return await perform_expensive_operation(id)

# Cache invalidation
async def invalidate_cache(id: str):
    """Invalidate specific cache entry"""
    cache = Cache(Cache.MEMORY)
    await cache.delete(f"fetch_expensive_data_{id}")
```

## FastMCP Dependency Management

### Safe Upgrade Process

1. **Research Changes**: Review fastmcp changelog and breaking changes
2. **Version Constraints**: Use appropriate version ranges
3. **Test Thoroughly**: Run comprehensive test suite
4. **Verify Protocol**: Check MCP protocol compatibility
5. **Update Documentation**: Document any API changes

### pyproject.toml Configuration

```toml
[project]
name = "mcp-server"
version = "0.1.0"
description = "Production MCP server"
requires-python = ">=3.10"

dependencies = [
    "fastmcp>=2.13.0,<3.0.0",  # Pin to major version
    "pydantic>=2.0.0,<3.0.0",
    "opentelemetry-api>=1.20.0",
    "opentelemetry-sdk>=1.20.0",
    "opentelemetry-exporter-otlp>=1.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.10"
strict = true
```

## Common Patterns and Solutions

### Health Check Endpoint

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """Kubernetes liveness probe"""
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    # Check dependencies (DB, external services)
    try:
        await check_dependencies()
        return {"status": "ready"}
    except Exception as e:
        logger.error("Readiness check failed", exc_info=True)
        raise HTTPException(status_code=503, detail="Not ready")
```

### Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Simple in-memory rate limiter"""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)

        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter(requests_per_minute=100)

@mcp.tool()
async def rate_limited_tool(input: ToolInput) -> str:
    """Tool with rate limiting"""
    client_id = get_client_id()  # From MCP session

    if not rate_limiter.is_allowed(client_id):
        raise ValueError("Rate limit exceeded. Try again later.")

    return await process(input)
```

## Troubleshooting Guide

### Common Issues

**Issue: PII leakage in logs**

- **Symptom**: PII appears in log files or monitoring dashboards
- **Solution**: Ensure `sanitize_pii()` is called before all logging statements
- **Prevention**: Add tests that verify logs contain no PII patterns

**Issue: fastmcp upgrade breaks protocol**

- **Symptom**: Clients can't connect after fastmcp upgrade
- **Solution**: Check fastmcp changelog for breaking changes, test with real clients
- **Prevention**: Pin major version, test upgrades in dev environment first

**Issue: Slow MCP tool execution**

- **Symptom**: Tools take >5 seconds to respond
- **Solution**: Implement connection pooling, caching, and async patterns
- **Prevention**: Add performance tests, monitor latency metrics

**Issue: JSON schema validation failures**

- **Symptom**: Pydantic raises validation errors for valid inputs
- **Solution**: Review Pydantic model definitions, ensure validators are correct
- **Prevention**: Comprehensive input validation tests

**Issue: Memory leaks in long-running servers**

- **Symptom**: Memory usage grows over time
- **Solution**: Ensure cleanup in shutdown hooks, check for circular references
- **Prevention**: Profile memory usage, implement resource limits

## Resources

### Templates

- `resources/tool-schema-template.json` - JSON schema for tool definitions
- `resources/resource-schema-template.json` - JSON schema for resource definitions
- `resources/pii-patterns.json` - Comprehensive PII detection patterns
- `resources/server-config-template.py` - Complete server configuration example

### Scripts

- `scripts/validate-mcp-server.py` - Validate MCP server implementation
- `scripts/test-pii-sanitization.py` - Comprehensive PII test runner
- `scripts/generate-mcp-tool.py` - Generate new tool scaffolding
- `scripts/benchmark-server.py` - Performance benchmarking tool

### Documentation References

- FastMCP Documentation: <https://github.com/jlowin/fastmcp>
- MCP Protocol Spec: <https://modelcontextprotocol.io>
- Kubernetes Skill: `~/.claude/skills/kubernetes-deployment/`
- Security Standards: `~/.claude/docs/security/owasp-top-10.md`
- CLAUDE.md Security Section: PII protection, input validation

## Related Skills

- **kubernetes-deployment**: Kubernetes deployment and secrets management
- **security-review**: OWASP compliance, vulnerability scanning
- **api-design**: REST API patterns, OpenAPI specifications
- **python-development**: Python best practices, type hints, async patterns

## Best Practices Summary

1. **Security First**: Sanitize PII, validate inputs, implement rate limiting
2. **Observable by Default**: Structured logging, OpenTelemetry tracing, metrics
3. **Type Safety**: Use Pydantic models, mypy type checking
4. **Comprehensive Testing**: 22+ PII tests, integration tests, performance tests
5. **Resource Management**: Connection pooling, graceful shutdown, cleanup
6. **Error Handling**: Meaningful errors, proper exception types, retry logic
7. **Documentation**: Clear tool descriptions, examples, troubleshooting guides
8. **Performance**: Caching, async/await, connection pooling
9. **Protocol Compliance**: Follow MCP specification, test with real clients
10. **Production Ready**: Health checks, monitoring, rate limiting, Kubernetes deployment
