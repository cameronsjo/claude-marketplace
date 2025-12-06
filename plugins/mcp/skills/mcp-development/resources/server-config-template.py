"""
MCP Server Configuration Template

Complete production-ready MCP server with:
- FastMCP initialization
- PII sanitization
- OpenTelemetry tracing
- Health checks
- Error handling
"""

import logging
import os
from typing import Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenTelemetry
def setup_tracing(service_name: str = "mcp-server"):
    """Configure Universal Tracing (OpenTelemetry)"""
    resource = Resource.create({"service.name": service_name})
    tracer_provider = TracerProvider(resource=resource)

    otlp_endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://localhost:4318/v1/traces"
    )
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

    span_processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    logger.info(f"Tracing configured for {service_name}")

# Initialize MCP server
mcp = FastMCP(
    "example-mcp-server",
    dependencies=["fastmcp>=2.13.0"]
)

tracer = trace.get_tracer(__name__)

# Server lifecycle hooks
@mcp.on_startup
async def startup():
    """Initialize resources on server startup"""
    logger.info("MCP server starting")
    setup_tracing("example-mcp-server")
    # Initialize DB connections, API clients, etc.

@mcp.on_shutdown
async def shutdown():
    """Cleanup resources on server shutdown"""
    logger.info("MCP server shutting down")
    # Close DB connections, cleanup resources, etc.

# PII Sanitization
import re

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')

def sanitize_pii(text: str) -> str:
    """Remove PII from text"""
    if not text:
        return text
    text = EMAIL_PATTERN.sub('[EMAIL]', text)
    text = SSN_PATTERN.sub('[SSN]', text)
    text = PHONE_PATTERN.sub('[PHONE]', text)
    return text

# Tool definition
class ExampleToolInput(BaseModel):
    """Input schema for example tool"""
    query: str = Field(
        ...,
        description="The query to process",
        min_length=1,
        max_length=500
    )
    limit: int = Field(
        10,
        description="Maximum results to return",
        ge=1,
        le=100
    )

@mcp.tool()
async def example_tool(input: ExampleToolInput) -> str:
    """
    Example MCP tool with proper patterns.

    This tool demonstrates:
    - Pydantic validation
    - PII sanitization
    - OpenTelemetry tracing
    - Structured logging
    - Error handling
    """
    with tracer.start_as_current_span("example_tool") as span:
        # Sanitize input before logging
        sanitized_query = sanitize_pii(input.query)

        span.set_attribute("query.length", len(input.query))
        span.set_attribute("limit", input.limit)

        logger.info(
            "Processing request",
            extra={"query": sanitized_query, "limit": input.limit}
        )

        try:
            # Business logic here
            result = f"Processed: {sanitized_query}"

            span.set_attribute("success", True)
            return result

        except Exception as e:
            logger.error("Tool execution failed", exc_info=True)
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise

# Resource definition
@mcp.resource("resource://example/{resource_id}")
async def get_resource(resource_id: str) -> str:
    """
    Example MCP resource.

    Returns content for the specified resource ID.
    """
    logger.info("Fetching resource", extra={"resource_id": resource_id})

    # Validate input
    if not resource_id or not resource_id.isalnum():
        raise ValueError(f"Invalid resource ID: {resource_id}")

    # Fetch and sanitize content
    content = f"Resource content for {resource_id}"
    return sanitize_pii(content)

# Prompt definition
@mcp.prompt()
async def example_prompt(topic: str) -> str:
    """
    Generate a prompt template for a specific topic.
    """
    return f"""Please analyze the following topic and provide insights:

Topic: {topic}

Provide:
1. Key concepts and themes
2. Important considerations
3. Actionable recommendations

Keep your analysis concise but comprehensive."""

# Health check (if using FastAPI alongside)
# from fastapi import FastAPI
#
# app = FastAPI()
#
# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}
#
# @app.get("/ready")
# async def readiness_check():
#     return {"status": "ready"}

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
