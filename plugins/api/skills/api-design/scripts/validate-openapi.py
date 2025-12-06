#!/usr/bin/env python3
"""
OpenAPI Specification Validator

Validates OpenAPI specifications against API design guidelines:
- Schema structure validation
- Naming convention checks
- Required fields verification
- Error response validation
- Common type usage
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class ValidationError:
    """Represents a validation error."""

    def __init__(
        self,
        severity: str,
        category: str,
        message: str,
        path: str = "",
        suggestion: str = "",
    ):
        self.severity = severity  # ERROR, WARNING, INFO
        self.category = category
        self.message = message
        self.path = path
        self.suggestion = suggestion

    def __str__(self) -> str:
        result = f"[{self.severity}] {self.category}: {self.message}"
        if self.path:
            result += f"\n  Path: {self.path}"
        if self.suggestion:
            result += f"\n  Suggestion: {self.suggestion}"
        return result


class OpenAPIValidator:
    """Validates OpenAPI specifications against guidelines."""

    def __init__(self, spec_path: Path):
        self.spec_path = spec_path
        self.spec: Dict[str, Any] = {}
        self.errors: List[ValidationError] = []

    def load_spec(self) -> bool:
        """Load OpenAPI specification from file."""
        try:
            with open(self.spec_path, "r") as f:
                if self.spec_path.suffix in [".yaml", ".yml"]:
                    self.spec = yaml.safe_load(f)
                else:
                    self.spec = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading specification: {e}")
            return False

    def validate(self) -> List[ValidationError]:
        """Run all validations."""
        self.errors = []

        self._validate_structure()
        self._validate_versioning()
        self._validate_paths()
        self._validate_schemas()
        self._validate_responses()
        self._validate_errors()

        return self.errors

    def _validate_structure(self) -> None:
        """Validate basic OpenAPI structure."""
        # Check OpenAPI version
        if "openapi" not in self.spec:
            self.errors.append(
                ValidationError(
                    "ERROR",
                    "Structure",
                    "Missing 'openapi' field",
                    suggestion="Add 'openapi: 3.0.0' or higher",
                )
            )
        elif not self.spec["openapi"].startswith("3."):
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Structure",
                    f"OpenAPI version {self.spec['openapi']} may not be supported",
                    suggestion="Use OpenAPI 3.0 or higher",
                )
            )

        # Check required fields
        required_fields = ["info", "paths"]
        for field in required_fields:
            if field not in self.spec:
                self.errors.append(
                    ValidationError(
                        "ERROR", "Structure", f"Missing required field '{field}'"
                    )
                )

        # Check info section
        if "info" in self.spec:
            info = self.spec["info"]
            for field in ["title", "version"]:
                if field not in info:
                    self.errors.append(
                        ValidationError(
                            "ERROR", "Info", f"Missing required info field '{field}'"
                        )
                    )

    def _validate_versioning(self) -> None:
        """Validate API versioning in paths."""
        if "paths" not in self.spec:
            return

        version_pattern = re.compile(r"^/v\d+(/|$)")
        has_versioned_paths = False

        for path in self.spec["paths"].keys():
            if version_pattern.match(path):
                has_versioned_paths = True
            else:
                self.errors.append(
                    ValidationError(
                        "ERROR",
                        "Versioning",
                        f"Path does not start with version: {path}",
                        path=path,
                        suggestion="Paths should start with /v{major_version} (e.g., /v1)",
                    )
                )

        if not has_versioned_paths and self.spec["paths"]:
            self.errors.append(
                ValidationError(
                    "ERROR",
                    "Versioning",
                    "No versioned paths found",
                    suggestion="All paths should start with /v{major_version}",
                )
            )

    def _validate_paths(self) -> None:
        """Validate path naming conventions."""
        if "paths" not in self.spec:
            return

        # Pattern for kebab-case
        kebab_pattern = re.compile(r"^[a-z0-9\-\/{}]+$")

        for path in self.spec["paths"].keys():
            # Remove version prefix for checking
            path_without_version = re.sub(r"^/v\d+", "", path)

            # Check kebab-case (allowing path parameters)
            path_to_check = re.sub(r"\{[^}]+\}", "", path_without_version)
            if path_to_check and not kebab_pattern.match(path_to_check):
                self.errors.append(
                    ValidationError(
                        "ERROR",
                        "Naming",
                        f"Path does not use kebab-case: {path}",
                        path=path,
                        suggestion="Use kebab-case for URI paths (e.g., /validate-otp not /validate_otp)",
                    )
                )

            # Check for underscores
            if "_" in path_to_check:
                self.errors.append(
                    ValidationError(
                        "ERROR",
                        "Naming",
                        f"Path contains underscores: {path}",
                        path=path,
                        suggestion="Replace underscores with hyphens",
                    )
                )

            # Check nesting depth (max 2 levels after version and namespace)
            path_parts = [p for p in path_without_version.split("/") if p and not p.startswith("{")]
            if len(path_parts) > 4:  # namespace + collection + id + sub-collection
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Resource Modeling",
                        f"Path has deep nesting: {path}",
                        path=path,
                        suggestion="Limit resource hierarchy to 2 levels",
                    )
                )

    def _validate_schemas(self) -> None:
        """Validate schema definitions."""
        if "components" not in self.spec or "schemas" not in self.spec["components"]:
            return

        schemas = self.spec["components"]["schemas"]

        for schema_name, schema in schemas.items():
            self._validate_schema(schema_name, schema, f"#/components/schemas/{schema_name}")

    def _validate_schema(self, name: str, schema: Dict[str, Any], path: str) -> None:
        """Validate individual schema."""
        if "properties" in schema:
            for prop_name, prop_schema in schema["properties"].items():
                self._validate_field_name(prop_name, path)
                self._validate_field_schema(prop_name, prop_schema, f"{path}/properties/{prop_name}")

        # Check for additionalProperties: false
        if schema.get("additionalProperties") is False:
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Schema",
                    f"Schema sets additionalProperties to false: {name}",
                    path=path,
                    suggestion="Remove additionalProperties: false to allow forward compatibility",
                )
            )

    def _validate_field_name(self, field_name: str, schema_path: str) -> None:
        """Validate field name follows snake_case convention."""
        # Pattern for snake_case
        snake_case_pattern = re.compile(r"^[a-z][a-z0-9_]*$")

        if not snake_case_pattern.match(field_name):
            self.errors.append(
                ValidationError(
                    "ERROR",
                    "Naming",
                    f"Field does not use snake_case: {field_name}",
                    path=f"{schema_path}/properties/{field_name}",
                    suggestion=f"Use snake_case: {self._to_snake_case(field_name)}",
                )
            )

        # Check for common naming issues
        if field_name.startswith("is_") or field_name.startswith("has_"):
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Naming",
                    f"Boolean field uses prefix: {field_name}",
                    path=f"{schema_path}/properties/{field_name}",
                    suggestion=f"Remove prefix: {field_name.replace('is_', '').replace('has_', '')}",
                )
            )

    def _validate_field_schema(self, field_name: str, schema: Dict[str, Any], path: str) -> None:
        """Validate field schema definition."""
        field_type = schema.get("type")

        # String validation
        if field_type == "string":
            if "minLength" not in schema:
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Schema",
                        f"String field missing minLength: {field_name}",
                        path=path,
                        suggestion="Add minLength constraint",
                    )
                )
            if "maxLength" not in schema:
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Schema",
                        f"String field missing maxLength: {field_name}",
                        path=path,
                        suggestion="Add maxLength constraint (default: 255)",
                    )
                )

        # Number validation
        elif field_type == "number":
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Schema",
                    f"Field uses 'number' type: {field_name}",
                    path=path,
                    suggestion="Use 'string' for decimals or 'integer' for whole numbers",
                )
            )

        elif field_type == "integer":
            if "minimum" not in schema:
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Schema",
                        f"Integer field missing minimum: {field_name}",
                        path=path,
                        suggestion="Add minimum constraint",
                    )
                )
            if "maximum" not in schema:
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Schema",
                        f"Integer field missing maximum: {field_name}",
                        path=path,
                        suggestion="Add maximum constraint",
                    )
                )

        # Array validation
        elif field_type == "array":
            if "maxItems" not in schema:
                self.errors.append(
                    ValidationError(
                        "WARNING",
                        "Schema",
                        f"Array field missing maxItems: {field_name}",
                        path=path,
                        suggestion="Add maxItems constraint (default: 32767)",
                    )
                )

        # Null check
        if schema.get("type") == "null" or (
            isinstance(schema.get("type"), list) and "null" in schema.get("type", [])
        ):
            self.errors.append(
                ValidationError(
                    "ERROR",
                    "Schema",
                    f"Field allows null: {field_name}",
                    path=path,
                    suggestion="Remove null type - use field absence for undefined",
                )
            )

    def _validate_responses(self) -> None:
        """Validate response definitions."""
        if "paths" not in self.spec:
            return

        for path, path_item in self.spec["paths"].items():
            for method, operation in path_item.items():
                if method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]:
                    continue

                if "responses" not in operation:
                    self.errors.append(
                        ValidationError(
                            "ERROR",
                            "Responses",
                            f"Operation missing responses: {method.upper()} {path}",
                            path=f"{path}/{method}",
                        )
                    )
                    continue

                self._validate_operation_responses(method, path, operation["responses"])

    def _validate_operation_responses(
        self, method: str, path: str, responses: Dict[str, Any]
    ) -> None:
        """Validate responses for an operation."""
        # Check for success response
        success_codes = ["200", "201", "204"]
        has_success = any(code in responses for code in success_codes)

        if not has_success:
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Responses",
                    f"No success response defined: {method.upper()} {path}",
                    path=f"{path}/{method}/responses",
                    suggestion="Add 200, 201, or 204 response",
                )
            )

        # Check for error responses
        if "400" not in responses and "4XX" not in responses:
            self.errors.append(
                ValidationError(
                    "INFO",
                    "Responses",
                    f"No 400 error response defined: {method.upper()} {path}",
                    path=f"{path}/{method}/responses",
                    suggestion="Add 400 Bad Request response",
                )
            )

    def _validate_errors(self) -> None:
        """Validate error response schemas."""
        if "components" not in self.spec or "schemas" not in self.spec["components"]:
            return

        schemas = self.spec["components"]["schemas"]

        # Check for RFC 9457 compliant error schema
        has_problem_detail = False
        for schema_name in schemas.keys():
            if "error" in schema_name.lower() or "problem" in schema_name.lower():
                has_problem_detail = True
                schema = schemas[schema_name]
                self._validate_error_schema(schema_name, schema)

        if not has_problem_detail:
            self.errors.append(
                ValidationError(
                    "WARNING",
                    "Error Handling",
                    "No error schema found",
                    suggestion="Define RFC 9457 compliant problem_detail schema",
                )
            )

    def _validate_error_schema(self, name: str, schema: Dict[str, Any]) -> None:
        """Validate error schema follows RFC 9457."""
        required_fields = ["type", "title"]
        recommended_fields = ["status", "detail", "instance", "trace_id"]

        if "properties" not in schema:
            return

        properties = schema["properties"]

        # Check required fields
        for field in required_fields:
            if field not in properties:
                self.errors.append(
                    ValidationError(
                        "ERROR",
                        "Error Handling",
                        f"Error schema missing required field '{field}': {name}",
                        path=f"#/components/schemas/{name}",
                        suggestion=f"Add '{field}' field per RFC 9457",
                    )
                )

        # Check recommended fields
        for field in recommended_fields:
            if field not in properties:
                self.errors.append(
                    ValidationError(
                        "INFO",
                        "Error Handling",
                        f"Error schema missing recommended field '{field}': {name}",
                        path=f"#/components/schemas/{name}",
                    )
                )

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert name to snake_case."""
        # Insert underscore before uppercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        # Insert underscore before uppercase letters followed by lowercase
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate OpenAPI specification against API guidelines"
    )
    parser.add_argument("spec", type=Path, help="Path to OpenAPI specification file")
    parser.add_argument(
        "--severity",
        choices=["ERROR", "WARNING", "INFO"],
        default="WARNING",
        help="Minimum severity level to report (default: WARNING)",
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )

    args = parser.parse_args()

    if not args.spec.exists():
        print(f"Error: File not found: {args.spec}")
        return 1

    validator = OpenAPIValidator(args.spec)

    if not validator.load_spec():
        return 1

    print(f"Validating {args.spec}...")
    errors = validator.validate()

    # Filter by severity
    severity_order = {"ERROR": 0, "WARNING": 1, "INFO": 2}
    min_severity = severity_order[args.severity]
    filtered_errors = [
        e for e in errors if severity_order[e.severity] <= min_severity
    ]

    if args.json:
        # Output as JSON
        result = {
            "file": str(args.spec),
            "total_issues": len(filtered_errors),
            "issues": [
                {
                    "severity": e.severity,
                    "category": e.category,
                    "message": e.message,
                    "path": e.path,
                    "suggestion": e.suggestion,
                }
                for e in filtered_errors
            ],
        }
        print(json.dumps(result, indent=2))
    else:
        # Output human-readable format
        if not filtered_errors:
            print("✓ No issues found!")
            return 0

        print(f"\nFound {len(filtered_errors)} issue(s):\n")

        # Group by severity
        by_severity = {"ERROR": [], "WARNING": [], "INFO": []}
        for error in filtered_errors:
            by_severity[error.severity].append(error)

        for severity in ["ERROR", "WARNING", "INFO"]:
            if by_severity[severity]:
                print(f"\n{severity}S ({len(by_severity[severity])}):")
                print("=" * 80)
                for error in by_severity[severity]:
                    print(f"\n{error}\n")

        # Return non-zero if errors found
        return 1 if by_severity["ERROR"] else 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
