# MCP Development Skill - Test Prompts

Test prompts to verify this skill triggers correctly.

## Should Trigger Skill ✅

### Test 1: Direct MCP Request
```
Create an MCP server with a tool for searching documents
```
**Expected:** Skill loads, provides fastmcp patterns

### Test 2: PII Sanitization
```
Add PII sanitization to this MCP tool that processes user data
```
**Expected:** Skill loads, provides sanitization patterns

### Test 3: KITT Deployment
```
Generate KITT configuration for deploying an MCP server to WCNP
```
**Expected:** Skill loads (may also load wcnp-kitt-k8s skill)

### Test 4: FastMCP Upgrade
```
How do I safely upgrade fastmcp from 2.10 to 2.13?
```
**Expected:** Skill loads, provides upgrade guidance

### Test 5: Tool Definition
```
Help me define an MCP tool with proper input validation
```
**Expected:** Skill loads, provides Pydantic patterns

### Test 6: Universal Tracing
```
Add OpenTelemetry tracing to my MCP server
```
**Expected:** Skill loads, provides Universal Tracing integration

### Test 7: Resource Definition
```
Create an MCP resource that returns document content
```
**Expected:** Skill loads, provides resource patterns

### Test 8: Testing Strategy
```
How should I test MCP tools for PII sanitization?
```
**Expected:** Skill loads, provides testing patterns

## Should NOT Trigger Skill ❌

### Test 9: General Python
```
Write a Python script to parse JSON files
```
**Expected:** Python skill may load, but NOT mcp-development

### Test 10: API Development
```
Design a REST API for user management
```
**Expected:** api-design skill loads, NOT mcp-development

### Test 11: General Deployment
```
How do I deploy a Node.js application to Kubernetes?
```
**Expected:** wcnp-kitt-k8s may load, but NOT mcp-development specifically

## Edge Cases

### Test 12: Model Context Protocol (Full Name)
```
I need to implement the Model Context Protocol for my application
```
**Expected:** Should trigger skill (tests full name recognition)

### Test 13: Anthropic MCP
```
Build an Anthropic MCP server for database queries
```
**Expected:** Should trigger skill (tests vendor association)

### Test 14: Protocol Implementation
```
Implement MCP protocol with custom transport layer
```
**Expected:** Should trigger skill (advanced use case)
