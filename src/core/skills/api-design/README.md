# API Design & Review Skill

Comprehensive API design and review skill based on REST best practices and enterprise API standards.

## Directory Structure

```
api-design/
├── skill.md                      # Main skill instructions
├── README.md                     # This file
├── scripts/                      # Validation and generation scripts
│   ├── validate-openapi.py       # OpenAPI specification validator
│   ├── check-naming.py           # Naming convention checker
│   └── generate-error-schema.py  # Error schema generator
└── resources/                    # Reference resources
    ├── common-types.json         # Standard type definitions
    ├── error-codes.json          # Standard error codes
    └── openapi-template.yaml     # OpenAPI template
```

## Usage

### Invoke the Skill

In Claude Code, you can invoke this skill using the Skill tool:

```
Use the api-design skill to review this OpenAPI specification:
[paste spec or provide path]
```

Or invoke directly:

```
/skill api-design
```

### Using Scripts Directly

#### 1. Validate OpenAPI Specification

```bash
python scripts/validate-openapi.py path/to/openapi.yaml
```

Options:
- `--severity ERROR|WARNING|INFO` - Minimum severity to report (default: WARNING)
- `--json` - Output results as JSON

Example:
```bash
python scripts/validate-openapi.py api.yaml --severity ERROR
```

#### 2. Check Naming Conventions

```bash
python scripts/check-naming.py path/to/openapi.yaml
```

Options:
- `--type all|paths|parameters|fields|enums` - Type of naming to check (default: all)
- `--json` - Output results as JSON

Example:
```bash
python scripts/check-naming.py api.yaml --type fields
```

#### 3. Generate Error Schemas

Generate standard error schemas:
```bash
python scripts/generate-error-schema.py --type standard -o error-schemas.json
```

Generate business error schema:
```bash
python scripts/generate-error-schema.py --type business \
  --code out-of-credit \
  --title "You do not have enough credit" \
  -o out-of-credit-error.json
```

Generate error responses:
```bash
python scripts/generate-error-schema.py --type responses -o error-responses.json
```

Generate error catalog:
```bash
python scripts/generate-error-schema.py --type catalog \
  --api-name "Users API" \
  --base-path "/v1/users" \
  -o error-catalog.json
```

## Resources

### common-types.json

Standard type definitions for common concepts:
- Money (currency + value)
- Address (postal address)
- Phone Number (E.164)
- Email Address
- DateTime, Date, Time
- Country, Currency, Language codes
- UUID, IP Address
- Person Name
- Pagination Response
- JSON Patch
- HATEOAS Link

Usage in OpenAPI:
```yaml
properties:
  amount:
    $ref: './resources/common-types.json#/components/schemas/Money'
  email:
    $ref: './resources/common-types.json#/components/schemas/EmailAddress'
```

### error-codes.json

Standard error codes and validation error codes:
- HTTP status code mappings
- RFC 9457 error types
- Validation error codes
- Business error examples
- Standard field definitions

### openapi-template.yaml

Complete OpenAPI 3.0 template with:
- Standard structure
- Common components (schemas, responses, parameters)
- Error responses (RFC 9457 compliant)
- Security schemes
- Example CRUD endpoints
- Pagination support
- HATEOAS links

## Dependencies

Scripts require:
- Python 3.7+
- PyYAML: `pip install pyyaml`

## Key Guidelines

### Naming Conventions
- **JSON Fields**: snake_case
- **URI Paths**: kebab-case
- **Enums**: UPPER_SNAKE_CASE

### Resource Modeling
- URI pattern: `/{version}/{namespace}/{collection}/{id}`
- Maximum 2 levels of nesting
- RESTful operations (GET, POST, PUT, PATCH, DELETE)

### Error Handling
- RFC 9457 Problem Details format
- Standard error types with URIs
- Validation errors with field locations
- trace_id for correlation

### Versioning
- URI versioning (/v1, /v2)
- Semantic versioning for artifacts
- Backward compatibility requirements
- Deprecation strategy

### Data Types
- String: always define minLength and maxLength
- Numbers: use integer (32-bit) or string
- Arrays: define maxItems
- No null values
- Common types for standard concepts

## Examples

### Example 1: Validate API Spec

```bash
python scripts/validate-openapi.py my-api.yaml
```

Output:
```
Validating my-api.yaml...

Found 3 issue(s):

ERRORS (1):
================================================================================

[ERROR] Naming: Field does not use snake_case: userId
  Path: #/components/schemas/User/properties/userId
  Suggestion: Use snake_case: user_id


WARNINGS (2):
================================================================================

[WARNING] Schema: String field missing maxLength: email
  Path: #/components/schemas/User/properties/email
  Suggestion: Add maxLength constraint (default: 255)
```

### Example 2: Check Naming Only

```bash
python scripts/check-naming.py my-api.yaml --type fields
```

Output:
```
Checking naming conventions in my-api.yaml...

Found 2 naming issue(s):

Field Name (2):
================================================================================

Field Name: userId → user_id
  Location: #/components/schemas/User/properties/userId
  Reason: Field names should use snake_case

Field Name: isActive → active
  Location: #/components/schemas/User/properties/isActive
  Reason: Boolean fields should omit 'is_' prefix
```

### Example 3: Generate Error Schema

```bash
python scripts/generate-error-schema.py --type standard
```

Output:
```json
{
  "components": {
    "schemas": {
      "ProblemDetail": {
        "type": "object",
        "required": ["type", "title", "trace_id"],
        "properties": {
          "type": {
            "type": "string",
            "format": "uri"
          },
          ...
        }
      }
    }
  }
}
```

## Integration

This skill integrates with:
- **API Design**: Generate compliant specs
- **Code Review**: Validate implementations
- **Documentation**: Generate API docs
- **CI/CD**: Automated compliance checks
- **Testing**: Validate API responses

## Reference Documentation

Detailed guidelines available at:
- `~/.claude/docs/api-guidelines/`

Key documents:
- `naming-conventions.md`
- `resource-modeling.md`
- `error-handling.md`
- `http-methods-headers-status-codes.md`
- `api-versioning.md`
- `common-types.md`
- `json-types.md`

## Contributing

When updating this skill:
1. Update `skill.md` with new guidelines
2. Add validation rules to scripts
3. Update resource files with new types
4. Add examples to this README
5. Test all scripts with sample specs

## License

Proprietary - Internal use only
