#!/usr/bin/env python3
"""
Error Schema Generator

Generates RFC 9457 compliant error schemas and error catalogs:
- Standard error response templates
- Business logic error schemas
- Error catalog generation
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional


def generate_standard_error_schema() -> Dict[str, Any]:
    """Generate RFC 9457 compliant problem detail schema."""
    return {
        "type": "object",
        "title": "Problem Detail",
        "description": "RFC 9457 compliant error response",
        "required": ["type", "title", "trace_id"],
        "properties": {
            "type": {
                "type": "string",
                "format": "uri",
                "description": "URI reference identifying the problem type",
                "example": "https://api.example.com/errors/invalid-request",
            },
            "title": {
                "type": "string",
                "description": "Short, human-readable summary of the problem type",
                "example": "Request is not well-formed, syntactically incorrect, or violates schema.",
            },
            "status": {
                "type": "integer",
                "minimum": 400,
                "maximum": 599,
                "description": "HTTP status code for this occurrence of the problem",
                "example": 400,
            },
            "detail": {
                "type": "string",
                "description": "Human-readable explanation specific to this occurrence",
                "example": "The credit_card.expire_month field is required",
            },
            "instance": {
                "type": "string",
                "format": "uri-reference",
                "description": "URI reference identifying the specific occurrence",
                "example": "/v1/checkout/orders/123",
            },
            "trace_id": {
                "type": "string",
                "description": "Correlation and tracing identifier",
                "example": "90957fca61718",
            },
            "errors": {
                "type": "array",
                "description": "Array of detailed validation errors (for 400 Bad Request)",
                "items": {"$ref": "#/components/schemas/ValidationError"},
            },
        },
    }


def generate_validation_error_schema() -> Dict[str, Any]:
    """Generate validation error detail schema."""
    return {
        "type": "object",
        "title": "Validation Error",
        "description": "Detailed validation error information",
        "required": ["code", "reason", "property", "location"],
        "properties": {
            "code": {
                "type": "string",
                "format": "uri",
                "description": "URI identifying the specific error code",
                "example": "https://api.example.com/errors/missing-required-property",
            },
            "reason": {
                "type": "string",
                "description": "Human-readable explanation of the error",
                "example": "A required field is missing.",
            },
            "property": {
                "type": "string",
                "description": "JSON Pointer to the field in error",
                "example": "/credit_card/expire_month",
            },
            "location": {
                "type": "string",
                "enum": ["body", "query", "path", "header"],
                "description": "Location of the field in the request",
                "example": "body",
            },
        },
    }


def generate_business_error_schema(
    error_code: str, title: str, additional_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Generate business logic error schema."""
    schema = {
        "allOf": [
            {"$ref": "#/components/schemas/ProblemDetail"},
            {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "format": "uri",
                        "enum": [f"https://api.example.com/errors/{error_code}"],
                        "example": f"https://api.example.com/errors/{error_code}",
                    },
                    "title": {
                        "type": "string",
                        "enum": [title],
                        "example": title,
                    },
                },
            },
        ],
    }

    # Add additional fields if specified
    if additional_fields:
        additional_props = {
            field: {
                "type": "string",
                "description": f"Additional context for {field}",
            }
            for field in additional_fields
        }
        schema["allOf"].append({"type": "object", "properties": additional_props})

    return schema


def generate_error_responses() -> Dict[str, Any]:
    """Generate standard error response definitions."""
    return {
        "400BadRequest": {
            "description": "Bad Request - Request is not well-formed, syntactically incorrect, or violates schema",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/invalid-request",
                        "title": "Request is not well-formed, syntactically incorrect, or violates schema.",
                        "status": 400,
                        "trace_id": "90957fca61718",
                        "errors": [
                            {
                                "code": "https://api.example.com/errors/missing-required-property",
                                "reason": "A required field is missing.",
                                "property": "/email_address",
                                "location": "body",
                            }
                        ],
                    },
                }
            },
        },
        "401Unauthorized": {
            "description": "Unauthorized - Authentication failed",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/authentication-failure",
                        "title": "Authentication failed due to invalid credentials.",
                        "status": 401,
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
        "403Forbidden": {
            "description": "Forbidden - Authorization failed due to insufficient permissions",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/authorization-failure",
                        "title": "Authorization failed due to insufficient permissions.",
                        "status": 403,
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
        "404NotFound": {
            "description": "Not Found - The specified resource does not exist",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/resource-not-found",
                        "title": "The specified resource does not exist.",
                        "status": 404,
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
        "409Conflict": {
            "description": "Conflict - Request conflicts with current state",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/resource-conflict",
                        "title": "The server has detected a conflict while processing this request.",
                        "status": 409,
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
        "422UnprocessableEntity": {
            "description": "Unprocessable Entity - Request failed semantic validation",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/unprocessable-entity",
                        "title": "The request cannot be processed due to semantic errors.",
                        "status": 422,
                        "detail": "Cannot void a payment that has already been captured",
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
        "500InternalServerError": {
            "description": "Internal Server Error - An unexpected error occurred",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/ProblemDetail"},
                    "example": {
                        "type": "https://api.example.com/errors/internal-server-error",
                        "title": "An internal server error has occurred.",
                        "status": 500,
                        "trace_id": "90957fca61718",
                    },
                }
            },
        },
    }


def generate_error_catalog(
    api_name: str, base_path: str, operations: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate error catalog for an API."""
    return {
        "language": "en-US",
        "basePath": base_path,
        "title": api_name,
        "description": f"All errors in {api_name} API",
        "operations": operations,
    }


def generate_error_catalog_operation(
    operation_id: str, errors: List[Dict[str, str]]
) -> Dict[str, Any]:
    """Generate error catalog operation entry."""
    return {"operationId": operation_id, "errors": errors}


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate RFC 9457 compliant error schemas"
    )
    parser.add_argument(
        "--type",
        choices=["standard", "business", "responses", "catalog"],
        required=True,
        help="Type of error schema to generate",
    )
    parser.add_argument(
        "--code", help="Error code for business errors (e.g., out-of-credit)"
    )
    parser.add_argument("--title", help="Error title for business errors")
    parser.add_argument(
        "--fields",
        help="Comma-separated list of additional fields for business errors",
    )
    parser.add_argument(
        "--api-name", help="API name for error catalog"
    )
    parser.add_argument(
        "--base-path", help="Base path for error catalog"
    )
    parser.add_argument(
        "--output", "-o", type=argparse.FileType("w"), default=sys.stdout,
        help="Output file (default: stdout)"
    )

    args = parser.parse_args()

    result = None

    if args.type == "standard":
        # Generate standard error schemas
        result = {
            "components": {
                "schemas": {
                    "ProblemDetail": generate_standard_error_schema(),
                    "ValidationError": generate_validation_error_schema(),
                }
            }
        }

    elif args.type == "business":
        # Generate business error schema
        if not args.code or not args.title:
            print("Error: --code and --title are required for business errors")
            return 1

        additional_fields = None
        if args.fields:
            additional_fields = [f.strip() for f in args.fields.split(",")]

        result = {
            "components": {
                "schemas": {
                    f"{args.code.replace('-', '_').title()}Error": generate_business_error_schema(
                        args.code, args.title, additional_fields
                    )
                }
            }
        }

    elif args.type == "responses":
        # Generate error response definitions
        result = {"components": {"responses": generate_error_responses()}}

    elif args.type == "catalog":
        # Generate error catalog template
        if not args.api_name or not args.base_path:
            print("Error: --api-name and --base-path are required for catalog")
            return 1

        # Example operations
        operations = [
            generate_error_catalog_operation(
                "resource.create",
                [
                    {
                        "type": "https://api.example.com/errors/out-of-credit",
                        "title": "You do not have enough credit.",
                    },
                    {
                        "type": "https://api.example.com/errors/amount-mismatch",
                        "title": "Amount calculation mismatch.",
                    },
                ],
            )
        ]

        result = generate_error_catalog(args.api_name, args.base_path, operations)

    if result:
        json.dump(result, args.output, indent=2)
        args.output.write("\n")
        if args.output != sys.stdout:
            print(f"Generated error schema written to {args.output.name}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
