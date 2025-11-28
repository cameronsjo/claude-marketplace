# API Design & Review Skill

Comprehensive API design and review based on REST best practices and enterprise API standards.

## Overview

This skill provides expert guidance for designing, reviewing, and validating RESTful APIs. It covers naming conventions, resource modeling, error handling, versioning, and OpenAPI specification compliance.

## When to Use This Skill

- Designing new REST APIs or API endpoints
- Reviewing existing API designs for compliance
- Validating OpenAPI/Swagger specifications
- Checking naming conventions (snake_case fields, kebab-case URIs)
- Ensuring proper error handling and status codes
- Reviewing resource modeling and URI design
- Validating API versioning strategy
- Generating compliant API schemas

## Core Principles

### REST Architecture
- Resource-oriented design with clear resource hierarchies
- Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Stateless client-server communication
- Consistent developer experience

### Naming Conventions
- **JSON Fields**: lower_snake_case (e.g., `email_address`, `first_name`)
- **URI Paths**: kebab-case (e.g., `/v1/identity/validate-otp`)
- **Enum Values**: CAPITALIZED_WITH_UNDERSCORES
- **Query Parameters**: snake_case (same as field names)

### Field Naming Rules
- Use American English
- No implementation details (❌ `password_hash` ✓ `password`)
- No prepositions (❌ `written_by` ✓ `author`)
- Adjectives before nouns (❌ `items_collected` ✓ `collected_items`)
- No verbs (❌ `collect_items` ✓ `collected_items`)
- Omit boolean prefixes (❌ `is_disabled` ✓ `disabled`)
- URLs use `uri` not `url` (❌ `redirect_url` ✓ `redirect_uri`)
- Quantity uses suffix `_count` (❌ `num_nodes` ✓ `node_count`)
- Time fields: `{verb}_time` format (❌ `created_time` ✓ `create_time`)
- Date fields end in `_date`, duration in `_duration`

### Resource Modeling

#### URI Structure
```
/{version}/{namespace}/{collection-resource}/{resource-id}/{sub-resource}/{sub-resource-id}
```

**Examples:**
```
/v1/identity/users
/v1/identity/users/123
/v1/identity/accounts/456/users
/v1/identity/accounts/456/users/789
```

#### Resource Operations

| HTTP Method | Operation | URI Pattern | Idempotent |
|-------------|-----------|-------------|------------|
| GET | List Resources | `GET /{collection}` | Yes |
| GET | Retrieve Resource | `GET /{collection}/{id}` | Yes |
| POST | Create Resource | `POST /{collection}` | With Idempotency-Key |
| PUT | Replace Resource | `PUT /{collection}/{id}` | Yes |
| PATCH | Partial Update | `PATCH /{collection}/{id}` | No |
| DELETE | Delete Resource | `DELETE /{collection}/{id}` | Yes |
| POST | Custom Action | `POST /{controller-resource}` | Varies |

#### Resource Hierarchy Limits
- Maximum 2 levels of nesting
- Use hierarchy only for containment relationships
- Sub-resources must match domain model hierarchy

### HTTP Status Codes

#### Success Codes
- `200 OK` - Successful GET, or successful operation with response body
- `201 Created` - Successful POST creating a resource
- `204 No Content` - Successful PUT/PATCH/DELETE with no response body
- `202 Accepted` - Long-running operation accepted
- `207 Multi-Status` - Batch operation with mixed results

#### Client Error Codes (4xx)
- `400 Bad Request` - Invalid syntax, validation errors
- `401 Unauthorized` - Authentication failure
- `403 Forbidden` - Authorization failure
- `404 Not Found` - Resource does not exist
- `409 Conflict` - Duplicate idempotent request
- `412 Precondition Failed` - If-Match/If-None-Match failure
- `413 Payload Too Large` - Request entity too large
- `415 Unsupported Media Type` - Unsupported Content-Type
- `422 Unprocessable Entity` - Semantic validation failure
- `428 Precondition Required` - Missing If-Match header
- `429 Too Many Requests` - Rate limit exceeded

#### Server Error Codes (5xx)
- `500 Internal Server Error` - Server-side error
- `503 Service Unavailable` - Service unavailable
- `504 Gateway Timeout` - External partner timeout only

### Error Handling

All error responses MUST follow RFC 9457 Problem Details format:

```json
{
  "type": "https://api.example.com/errors/invalid-request",
  "title": "Request is not well-formed, syntactically incorrect, or violates schema.",
  "status": 400,
  "detail": "Additional details about this specific occurrence",
  "instance": "/v1/resource/123",
  "trace_id": "90957fca61718",
  "errors": [
    {
      "code": "https://api.example.com/errors/missing-required-property",
      "reason": "A required field is missing.",
      "property": "/credit_card/expire_month",
      "location": "body"
    }
  ]
}
```

#### Standard Error Types
- `https://api.example.com/errors/invalid-request` - 400 Bad Request
- `https://api.example.com/errors/authentication-failure` - 401 Unauthorized
- `https://api.example.com/errors/authorization-failure` - 403 Forbidden
- `https://api.example.com/errors/resource-not-found` - 404 Not Found
- `https://api.example.com/errors/resource-conflict` - 409 Conflict
- `https://api.example.com/errors/unprocessable-entity` - 422 Unprocessable Entity
- `https://api.example.com/errors/internal-server-error` - 500 Internal Server Error

### API Versioning

- Use URI versioning: `/v{major_version}`
- Only major version in URI (e.g., `/v1`, `/v2`)
- Semantic versioning for artifacts (1.0.0)
- Minor/patch versions must be backward compatible
- Only one version in GENERALLY AVAILABLE state at a time

#### Backward Compatibility Rules
- New fields must be optional
- Cannot change existing field names or types
- Cannot make optional fields required
- Cannot change HTTP status codes
- Cannot change HTTP verbs
- Enums cannot remove values (add only)

#### Deprecation
- Add `Deprecation` header with timestamp
- Add `Sunset` header with EOL date
- Minimum 6 months deprecation period for major versions
- Document migration path before deprecating

### Common Types

Use standard types for common concepts:

- **Money**: `currency_code` (ISO 4217) + `value` (string)
- **Country**: ISO 3166-1 alpha-2 (e.g., "US")
- **Currency**: ISO 4217 (e.g., "USD")
- **Language**: BCP-47 (e.g., "en-US")
- **Phone**: E.164 format
- **Email**: Internationalized email address
- **DateTime**: RFC 3339 with UTC (e.g., "2024-01-12T00:00:00Z")
- **Date**: RFC 3339 full-date (e.g., "2024-01-12")
- **UUID**: RFC 4122 format

### JSON Schema Guidelines

#### String Types
- Always define `minLength` and `maxLength`
- Use `pattern` for validation when appropriate
- For enums, use string type with documented values
- Default maxLength: 255 unless technical reason

#### Number Types
- Avoid JSON Schema `number` type - use `string` for decimals
- Only use `integer` for 32-bit signed values (-2^31 to 2^31-1)
- Always provide `minimum` and `maximum` for integers
- Use `string` with `pattern` for large numbers or decimals

#### Arrays
- Always define `maxItems` (default: 32767)
- Define `minItems` (usually 0 or 1)
- Implement pagination for collections

#### Null Values
- APIs MUST NOT produce or consume `null` values
- Use absence of field to indicate undefined
- Never use `{"type": "null"}`

#### Additional Properties
- Do not set `additionalProperties: false`
- Validate requests/responses at runtime instead

### Pagination

Use cursor-based pagination:

**Bidirectional Navigation:**
```
?page_size=10&starting_after={id}&ending_before={id}&next_page=true
```

**Unidirectional Navigation:**
```
?page_size=10&page_token={token}
```

**Response:**
```json
{
  "items": [...],
  "total_items": 100,
  "next_page_token": "abc123",
  "next_page": true
}
```

### Headers

#### Standard Headers
- `Content-Type: application/json; charset=utf-8`
- `Accept: application/json`
- `Authorization: Bearer {token}`
- `Idempotency-Key: {client-generated-key}` (POST/PATCH)
- `If-Match: {etag}` (PUT/PATCH/DELETE)
- `ETag: {entity-tag}` (responses)
- `Prefer: return=representation` (optional full response)
- `Deprecation: {date}` (deprecation notice)
- `Sunset: {date}` (EOL notice)

## How to Use This Skill

### 1. Design New API

```
Design a REST API for managing user accounts with the following requirements:
- CRUD operations for users
- User profile updates
- Account activation/deactivation
- List users with filtering and pagination
```

The skill will:
- Generate OpenAPI specification
- Create proper resource hierarchy
- Define request/response schemas
- Include error responses
- Add pagination support
- Ensure naming compliance

### 2. Review Existing API

```
Review this OpenAPI specification for compliance:
[paste OpenAPI spec or provide file path]
```

The skill will:
- Check naming conventions
- Validate resource modeling
- Review error handling
- Check status codes
- Verify versioning strategy
- Suggest improvements

### 3. Validate API Specification

```
Validate this API design against the guidelines:
- Check field names are snake_case
- Check URIs are kebab-case
- Verify error responses follow RFC 9457
- Check pagination implementation
```

The skill will use validation scripts to:
- Run naming convention checks
- Validate OpenAPI structure
- Check error schema compliance
- Verify common type usage

### 4. Generate API Components

```
Generate the following API components:
- Error response schemas
- Common type definitions (money, address, phone)
- Pagination response schema
- OpenAPI template for a new service
```

## Validation Scripts

The skill includes scripts for automated validation:

### validate-openapi.py
Validates OpenAPI specifications against API guidelines:
- Schema structure validation
- Naming convention checks
- Required fields verification
- Error response validation

Usage:
```bash
python scripts/validate-openapi.py path/to/openapi.yaml
```

### check-naming.py
Validates field names and URI paths:
- JSON field names (snake_case)
- URI paths (kebab-case)
- Enum values (UPPER_SNAKE_CASE)
- Query parameters (snake_case)

Usage:
```bash
python scripts/check-naming.py path/to/openapi.yaml
```

### generate-error-schema.py
Generates RFC 9457 compliant error schemas:
- Standard error response template
- Business logic error schemas
- Error catalog generation

Usage:
```bash
python scripts/generate-error-schema.py --type standard
python scripts/generate-error-schema.py --type business --code out-of-credit --title "Insufficient credit"
```

## Resources

The skill includes reference resources:

### common-types.json
Standard type definitions:
- Money (currency_code, value)
- Address (postal address components)
- Phone (E.164 format)
- Email (internationalized)
- DateTime, Date, Time
- Country, Currency, Language codes
- UUID, IP Address

### error-codes.json
Standard error codes and messages:
- HTTP status code mappings
- Error type URIs
- Standard error titles
- Fine-grained validation error codes

### openapi-template.yaml
Starter OpenAPI 3.0 template:
- Standard structure
- Common components
- Error responses
- Security schemes
- Example endpoints

## Review Checklist

When reviewing an API, check:

### Naming Conventions
- [ ] JSON fields use snake_case
- [ ] URIs use kebab-case
- [ ] Enums use UPPER_SNAKE_CASE
- [ ] No implementation details in names
- [ ] Boolean fields omit is/has prefixes
- [ ] Time fields use {verb}_time format
- [ ] Standard fields used correctly

### Resource Modeling
- [ ] Resources follow noun-based naming
- [ ] URI hierarchy matches domain model
- [ ] Maximum 2 levels of nesting
- [ ] Collection resources are plural
- [ ] Singleton resources use singular nouns
- [ ] Custom actions use verb-based naming

### HTTP Methods & Status Codes
- [ ] Correct HTTP methods for operations
- [ ] Appropriate status codes used
- [ ] Idempotent operations identified
- [ ] Content-Type headers correct
- [ ] Conditional requests supported (ETag)

### Error Handling
- [ ] RFC 9457 format for all errors
- [ ] Standard error types used
- [ ] trace_id included in all errors
- [ ] Validation errors include field location
- [ ] Business errors use 422 status
- [ ] Error catalog documented

### Versioning
- [ ] URI versioning implemented
- [ ] Semantic versioning for artifacts
- [ ] Backward compatibility maintained
- [ ] Deprecation headers for old versions
- [ ] Migration path documented

### Data Types & Validation
- [ ] String fields have min/max length
- [ ] Numbers use appropriate types
- [ ] Arrays have item limits
- [ ] No null values produced/consumed
- [ ] Common types used for standard concepts
- [ ] Date/time in RFC 3339 format

### Pagination
- [ ] Cursor-based pagination implemented
- [ ] page_size parameter supported
- [ ] Maximum page size enforced
- [ ] total_items included when possible
- [ ] next_page indicator provided

### Documentation
- [ ] OpenAPI 3.0 specification
- [ ] All endpoints documented
- [ ] Request/response examples
- [ ] Error responses documented
- [ ] Authentication/authorization described
- [ ] Common types referenced

## Example API Review

When you ask to review an API, the skill will:

1. **Parse the API specification** (OpenAPI/Swagger)
2. **Check naming conventions**:
   - Scan all field names for snake_case compliance
   - Verify URI paths use kebab-case
   - Check enum values are UPPER_SNAKE_CASE

3. **Validate resource modeling**:
   - Verify resource hierarchy depth
   - Check HTTP methods match operations
   - Validate URI patterns

4. **Review error handling**:
   - Check RFC 9457 compliance
   - Verify standard error types used
   - Validate error response structure

5. **Check data types**:
   - Verify string constraints
   - Check number type usage
   - Validate common type usage

6. **Validate versioning**:
   - Check URI versioning
   - Review backward compatibility
   - Verify deprecation strategy

7. **Generate report**:
   - List compliance issues
   - Provide specific recommendations
   - Include code examples
   - Suggest fixes

## Integration with Development Workflow

This skill integrates with:

- **API Design**: Generate compliant OpenAPI specs
- **Code Review**: Validate API implementations
- **Documentation**: Generate API documentation
- **Testing**: Validate API responses
- **CI/CD**: Automated compliance checks

## Reference Documentation

For detailed guidelines, see:
- `~/.claude/docs/api-guidelines/naming-conventions.md`
- `~/.claude/docs/api-guidelines/resource-modeling.md`
- `~/.claude/docs/api-guidelines/error-handling.md`
- `~/.claude/docs/api-guidelines/http-methods-headers-status-codes.md`
- `~/.claude/docs/api-guidelines/api-versioning.md`
- `~/.claude/docs/api-guidelines/common-types.md`
- `~/.claude/docs/api-guidelines/json-types.md`

## Best Practices

1. **Design-First**: Create OpenAPI spec before implementation
2. **Use Common Types**: Reuse standard definitions for consistency
3. **Document Everything**: Include examples and descriptions
4. **Version Carefully**: Plan for evolution, maintain compatibility
5. **Test Thoroughly**: Validate against spec, test error cases
6. **Monitor Usage**: Track API usage, deprecation metrics
7. **Iterate Based on Feedback**: Improve based on consumer needs
8. **Security First**: Implement authentication, authorization, rate limiting
9. **Performance Matters**: Design for scale, implement pagination
10. **Developer Experience**: Make APIs intuitive, consistent, well-documented
