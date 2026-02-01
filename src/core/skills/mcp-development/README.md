# MCP Development Skill

Build production-ready Model Context Protocol servers with fastmcp, comprehensive PII sanitization, and platform integration.

## Overview

This skill provides expert guidance for:
- FastMCP server development (Python)
- PII sanitization implementation and testing
- Tool/resource/prompt definitions
- KITT deployment configuration
- Universal Tracing (OpenTelemetry) integration
- Performance optimization
- Security best practices

## Quick Start

Claude will automatically invoke this skill when you:
- Mention MCP, fastmcp, or Model Context Protocol
- Ask about building MCP servers or tools
- Need PII sanitization patterns
- Want to deploy MCP servers to WCNP/KITT
- Need MCP testing strategies

## What's Included

- **SKILL.md**: Comprehensive MCP development patterns and best practices
- **resources/**: Templates, schemas, and configuration files
- **scripts/**: Validation, testing, and generation tools

## Key Features

### Security-First Development
- Comprehensive PII sanitization (22+ test patterns)
- Input validation with Pydantic
- Rate limiting patterns
- Audit logging best practices

### Production-Ready Patterns
- Server lifecycle management
- Health check implementations
- Graceful shutdown handling
- Error handling and retry logic

### Platform Integration
- KITT deployment configuration
- Universal Tracing setup
- Akeyless secrets integration
- WCNP best practices

### Performance Optimization
- Connection pooling
- Caching strategies
- Async/await patterns
- Resource management

## Related Skills

- `wcnp-kitt-k8s` - WCNP deployment and KITT configuration
- `security-review` - OWASP compliance and vulnerability scanning
- `python-development` - Python best practices and type safety

## Usage Examples

```
# Building a new MCP server
"Create an MCP server with tools for document search and retrieval"

# Adding PII sanitization
"Add PII sanitization to this MCP tool"

# Deploying to WCNP
"Generate KITT configuration for this MCP server"

# Testing
"Create comprehensive tests for MCP tool PII sanitization"
```

## Documentation

See `SKILL.md` for complete documentation including:
- FastMCP patterns and lifecycle
- PII sanitization implementation
- Testing strategies
- KITT deployment
- Universal Tracing integration
- Troubleshooting guide
