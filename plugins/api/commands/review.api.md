---
description: Review API design for REST best practices and OpenAPI compliance
category: review
argument-hint: [file or endpoint]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Claude Command: API Review

Comprehensive API design review covering REST best practices, naming conventions, resource modeling, and OpenAPI/Swagger specification compliance.

## Usage

Review OpenAPI/Swagger spec:
```
/api-review openapi.yaml
```

Review specific endpoint implementation:
```
/api-review src/api/users.ts
```

Review all API files in directory:
```
/api-review src/api/
```

## What This Command Does

This command uses the api-design skill to conduct thorough API design reviews.

### Step 1: Activate API design skill

Invoke the skill for comprehensive API review capabilities:
```
Use the api-design skill to help review this API.
```

### Step 2: Identify scope

Determine what to review:

**If file path provided:**
- Check if it's OpenAPI/Swagger spec (`.yaml`, `.yml`, `.json`)
- Check if it's API implementation code
- Check if it's a directory (glob for API files)

**If no path provided:**
- Ask: "What should I review? (OpenAPI spec, endpoint file, or directory)"
- Look for common locations: `openapi.yaml`, `swagger.json`, `src/api/`, `api/`

### Step 3: Load and analyze content

**For OpenAPI/Swagger specs:**
1. Read the spec file
2. Parse YAML/JSON structure
3. Extract paths, schemas, responses

**For implementation files:**
1. Read the API route/controller files
2. Extract endpoint definitions
3. Identify request/response structures

**For directories:**
1. Glob for API-related files (`**/*api*.{ts,js,py}`, `**/routes/**`, `**/controllers/**`)
2. Read and aggregate endpoints

### Step 4: Run comprehensive review

Review against API design standards:

#### 1. Naming Conventions

**JSON Fields (snake_case):**
- ✅ `email_address`, `first_name`, `user_id`
- ❌ `emailAddress`, `firstName`, `userId`

**URI Paths (kebab-case):**
- ✅ `/v1/identity/validate-otp`
- ❌ `/v1/identity/validateOtp`, `/v1/identity/validate_otp`

**Field Naming Rules:**
- No implementation details: `password` not `password_hash`
- No prepositions: `author` not `written_by`
- Adjectives before nouns: `collected_items` not `items_collected`
- No verbs: `collected_items` not `collect_items`
- No boolean prefixes: `disabled` not `is_disabled`
- URLs use `uri`: `redirect_uri` not `redirect_url`
- Quantity uses `_count`: `node_count` not `num_nodes`
- Time fields: `create_time` not `created_time`

#### 2. Resource Modeling

**URI Structure:**
```
/{version}/{namespace}/{collection}/{id}/{sub-collection}/{sub-id}
```

Examples:
- ✅ `/v1/users/123/orders/456`
- ❌ `/v1/getUserOrders?userId=123&orderId=456`

**HTTP Methods:**
- GET - Read/list resources
- POST - Create resources
- PUT - Replace resource
- PATCH - Update resource fields
- DELETE - Remove resource

**Collection vs Singular:**
- Collections: `/users`, `/orders` (plural)
- Single resource: `/users/123`, `/profile` (singular)

#### 3. Status Codes

Verify proper HTTP status code usage:

**2xx Success:**
- 200 OK - GET/PUT/PATCH success
- 201 Created - POST success (include Location header)
- 204 No Content - DELETE success

**4xx Client Errors:**
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid auth
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource doesn't exist
- 409 Conflict - Resource conflict
- 422 Unprocessable Entity - Validation errors

**5xx Server Errors:**
- 500 Internal Server Error - Unexpected error
- 503 Service Unavailable - Temporary unavailability

#### 4. Error Response Format

Validate error responses follow standard structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email_address",
        "message": "Invalid email format"
      }
    ]
  }
}
```

#### 5. Versioning

Check versioning strategy:
- URI versioning: `/v1/users`, `/v2/users`
- Version in path, not query string
- Major versions only (v1, v2, not v1.1)

#### 6. Pagination

For collection endpoints:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_count": 150,
    "total_pages": 8
  }
}
```

**Query parameters:**
- `page` (1-indexed)
- `page_size` or `limit`
- `offset` (alternative to page)

#### 7. Filtering and Sorting

**Query parameters:**
- Filters: `?status=active&role=admin`
- Sorting: `?sort=create_time` or `?sort=-create_time` (desc)
- Field selection: `?fields=id,name,email_address`

#### 8. Authentication & Authorization

Check security headers:
- `Authorization: Bearer {token}` for JWT
- `X-API-Key: {key}` for API keys
- No credentials in query strings

#### 9. CORS Headers

Validate CORS configuration:
```
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
```

#### 10. OpenAPI Spec Compliance

If OpenAPI spec provided:
- Validate schema structure
- Check required vs optional fields
- Verify example values
- Check `operationId` uniqueness
- Validate `$ref` references
- Check security schemes defined

### Step 5: Generate review report

Create structured report with:

**Executive Summary:**
- Overall compliance score
- Critical issues count
- Warnings count
- Best practices followed/missed

**Critical Issues (Must Fix):**
- Incorrect status codes
- Missing authentication
- Injection vulnerabilities
- Broken pagination

**Warnings (Should Fix):**
- Naming convention violations
- Missing error details
- Inconsistent versioning
- Poor resource modeling

**Recommendations:**
- Suggested improvements
- Best practices to adopt
- Examples of proper implementation

**Compliant Patterns (Good Examples):**
- Highlight what's done well
- Use as reference for fixes

### Step 6: Provide fix guidance

For each issue, provide:

1. **What's wrong:** Specific violation
2. **Why it matters:** Impact on API consumers
3. **How to fix:** Code example
4. **Reference:** Link to best practice doc

**Example Fix:**

❌ **Before:**
```typescript
GET /api/getUserById?userId=123
Response: { userId: 123, firstName: "John" }
```

✅ **After:**
```typescript
GET /api/v1/users/123
Response: {
  user_id: 123,
  first_name: "John"
}
```

**Changes:**
- Use resource-oriented URI (`/users/123`)
- Add version prefix (`/v1`)
- Use snake_case for fields (`user_id`, `first_name`)

### Step 7: Optional OpenAPI generation

If reviewing implementation code without OpenAPI spec:
- Offer to generate OpenAPI spec from code
- Extract schemas from request/response types
- Generate compliant endpoint definitions

## Review Checklist

Run through these checks:

**Naming:**
- [ ] JSON fields use snake_case
- [ ] URIs use kebab-case
- [ ] No implementation details in field names
- [ ] Boolean fields have no prefix
- [ ] Time fields use `{verb}_time` format

**REST:**
- [ ] Resource-oriented URIs (not RPC-style)
- [ ] Proper HTTP methods (GET/POST/PUT/PATCH/DELETE)
- [ ] Collection resources are plural
- [ ] Versioning in URI path

**Responses:**
- [ ] Proper status codes (2xx/4xx/5xx)
- [ ] Consistent error format
- [ ] Pagination for collections
- [ ] Standard response structure

**Security:**
- [ ] Authentication required
- [ ] Authorization checks present
- [ ] No credentials in URLs
- [ ] CORS properly configured
- [ ] Input validation on all fields

**OpenAPI:**
- [ ] Schema definitions present
- [ ] Request/response examples included
- [ ] Security schemes defined
- [ ] All endpoints documented

## Common Issues & Fixes

### Issue: Inconsistent field naming
```
❌ { userId: 1, email: "..." }
✅ { user_id: 1, email_address: "..." }
```

### Issue: RPC-style URIs
```
❌ POST /api/createUser
✅ POST /api/v1/users
```

### Issue: Wrong status codes
```
❌ 200 for resource not found
✅ 404 for resource not found
```

### Issue: Missing error details
```
❌ { error: "Bad request" }
✅ {
  error: {
    code: "VALIDATION_ERROR",
    message: "Invalid request",
    details: [{ field: "email_address", message: "Required" }]
  }
}
```

## Output Format

**Console output:**
- Summary statistics
- Critical issues highlighted
- Warning count

**Optional report file:**
- Detailed markdown report
- Saved to `api-review-report.md`
- Include fix examples and references

---

**Last Updated:** 2025-11-13
**Based on:** REST Best Practices
