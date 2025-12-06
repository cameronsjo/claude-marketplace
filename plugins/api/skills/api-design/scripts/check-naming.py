#!/usr/bin/env python3
"""
API Naming Convention Checker

Validates field names, URI paths, enum values, and query parameters
against API naming conventions:
- JSON field names: snake_case
- URI paths: kebab-case
- Enum values: UPPER_SNAKE_CASE
- Query parameters: snake_case
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)


class NamingIssue:
    """Represents a naming convention issue."""

    def __init__(
        self,
        issue_type: str,
        current_name: str,
        suggested_name: str,
        location: str,
        reason: str = "",
    ):
        self.issue_type = issue_type
        self.current_name = current_name
        self.suggested_name = suggested_name
        self.location = location
        self.reason = reason

    def __str__(self) -> str:
        result = f"{self.issue_type}: {self.current_name} → {self.suggested_name}"
        result += f"\n  Location: {self.location}"
        if self.reason:
            result += f"\n  Reason: {self.reason}"
        return result


class NamingChecker:
    """Checks naming conventions in API specifications."""

    # Patterns
    SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")
    KEBAB_CASE = re.compile(r"^[a-z][a-z0-9\-]*$")
    UPPER_SNAKE_CASE = re.compile(r"^[A-Z][A-Z0-9_]*$")

    # Common prefixes to avoid
    BOOLEAN_PREFIXES = ["is_", "has_", "can_", "should_", "will_"]

    # Common suffixes
    TIME_SUFFIXES = ["_time", "_date", "_duration"]
    COUNT_SUFFIXES = ["_count", "_total", "_num"]

    def __init__(self, spec_path: Path):
        self.spec_path = spec_path
        self.spec: Dict[str, Any] = {}
        self.issues: List[NamingIssue] = []

    def load_spec(self) -> bool:
        """Load API specification from file."""
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

    def check_all(self) -> List[NamingIssue]:
        """Run all naming checks."""
        self.issues = []

        self._check_paths()
        self._check_parameters()
        self._check_schemas()

        return self.issues

    def _check_paths(self) -> None:
        """Check URI path naming conventions."""
        if "paths" not in self.spec:
            return

        for path in self.spec["paths"].keys():
            # Remove version prefix and path parameters for checking
            path_without_version = re.sub(r"^/v\d+", "", path)
            path_parts = re.sub(r"\{[^}]+\}", "", path_without_version).split("/")

            for part in path_parts:
                if not part:
                    continue

                # Check kebab-case
                if not self.KEBAB_CASE.match(part):
                    suggested = self._to_kebab_case(part)
                    if suggested != part:
                        self.issues.append(
                            NamingIssue(
                                "Path Segment",
                                part,
                                suggested,
                                path,
                                "URI paths should use kebab-case",
                            )
                        )

                # Check for underscores
                if "_" in part:
                    self.issues.append(
                        NamingIssue(
                            "Path Segment",
                            part,
                            part.replace("_", "-"),
                            path,
                            "Use hyphens instead of underscores in URI paths",
                        )
                    )

                # Check for camelCase or PascalCase
                if re.search(r"[A-Z]", part):
                    self.issues.append(
                        NamingIssue(
                            "Path Segment",
                            part,
                            part.lower(),
                            path,
                            "URI paths should be lowercase",
                        )
                    )

    def _check_parameters(self) -> None:
        """Check parameter naming conventions."""
        if "paths" not in self.spec:
            return

        for path, path_item in self.spec["paths"].items():
            # Check path parameters
            if "parameters" in path_item:
                self._check_parameter_list(path_item["parameters"], path)

            # Check operation parameters
            for method in ["get", "post", "put", "patch", "delete"]:
                if method not in path_item:
                    continue

                operation = path_item[method]
                if "parameters" in operation:
                    self._check_parameter_list(
                        operation["parameters"], f"{path} [{method.upper()}]"
                    )

    def _check_parameter_list(self, parameters: List[Dict[str, Any]], location: str) -> None:
        """Check list of parameters."""
        for param in parameters:
            if isinstance(param, dict) and "name" in param:
                param_name = param["name"]
                param_in = param.get("in", "query")

                # Query and header parameters should use snake_case
                if param_in in ["query", "header"]:
                    if not self.SNAKE_CASE.match(param_name):
                        suggested = self._to_snake_case(param_name)
                        if suggested != param_name:
                            self.issues.append(
                                NamingIssue(
                                    f"{param_in.title()} Parameter",
                                    param_name,
                                    suggested,
                                    f"{location} ({param_in})",
                                    "Query and header parameters should use snake_case",
                                )
                            )

                # Check for common naming issues
                if param_name.startswith(tuple(self.BOOLEAN_PREFIXES)):
                    prefix = next(p for p in self.BOOLEAN_PREFIXES if param_name.startswith(p))
                    suggested = param_name[len(prefix):]
                    self.issues.append(
                        NamingIssue(
                            f"{param_in.title()} Parameter",
                            param_name,
                            suggested,
                            location,
                            f"Boolean parameters should omit '{prefix}' prefix",
                        )
                    )

    def _check_schemas(self) -> None:
        """Check schema naming conventions."""
        if "components" not in self.spec or "schemas" not in self.spec["components"]:
            return

        schemas = self.spec["components"]["schemas"]

        for schema_name, schema in schemas.items():
            self._check_schema_fields(schema_name, schema, f"#/components/schemas/{schema_name}")

    def _check_schema_fields(
        self, schema_name: str, schema: Dict[str, Any], path: str
    ) -> None:
        """Check field names in schema."""
        if "properties" not in schema:
            return

        for field_name, field_schema in schema["properties"].items():
            # Check snake_case
            if not self.SNAKE_CASE.match(field_name):
                suggested = self._to_snake_case(field_name)
                if suggested != field_name:
                    self.issues.append(
                        NamingIssue(
                            "Field Name",
                            field_name,
                            suggested,
                            f"{path}/properties/{field_name}",
                            "Field names should use snake_case",
                        )
                    )

            # Check boolean prefixes
            if field_name.startswith(tuple(self.BOOLEAN_PREFIXES)):
                # Check if it's actually a boolean
                field_type = field_schema.get("type")
                if field_type == "boolean":
                    prefix = next(p for p in self.BOOLEAN_PREFIXES if field_name.startswith(p))
                    suggested = field_name[len(prefix):]
                    self.issues.append(
                        NamingIssue(
                            "Field Name",
                            field_name,
                            suggested,
                            f"{path}/properties/{field_name}",
                            f"Boolean fields should omit '{prefix}' prefix",
                        )
                    )

            # Check time field naming
            if "time" in field_name.lower() or "date" in field_name.lower():
                if field_name.endswith("_at"):
                    suggested = field_name[:-3] + "_time"
                    self.issues.append(
                        NamingIssue(
                            "Field Name",
                            field_name,
                            suggested,
                            f"{path}/properties/{field_name}",
                            "Time fields should end with '_time' not '_at'",
                        )
                    )

                # Check for past tense
                if re.search(r"(created|updated|deleted|published)_time$", field_name):
                    base = re.sub(r"d_time$", "_time", field_name)
                    self.issues.append(
                        NamingIssue(
                            "Field Name",
                            field_name,
                            base,
                            f"{path}/properties/{field_name}",
                            "Use present tense: create_time not created_time",
                        )
                    )

            # Check count naming
            if field_name.startswith("num_"):
                suggested = field_name.replace("num_", "", 1) + "_count"
                self.issues.append(
                    NamingIssue(
                        "Field Name",
                        field_name,
                        suggested,
                        f"{path}/properties/{field_name}",
                        "Use suffix '_count' instead of prefix 'num_'",
                    )
                )

            # Check for URL vs URI
            if "url" in field_name.lower() and "uri" not in field_name.lower():
                suggested = field_name.replace("url", "uri")
                self.issues.append(
                    NamingIssue(
                        "Field Name",
                        field_name,
                        suggested,
                        f"{path}/properties/{field_name}",
                        "Use 'uri' instead of 'url' (all URLs are URIs)",
                    )
                )

            # Check enum values
            if "enum" in field_schema:
                self._check_enum_values(
                    field_schema["enum"], f"{path}/properties/{field_name}"
                )

            # Recursively check nested objects
            if field_schema.get("type") == "object":
                self._check_schema_fields(
                    field_name, field_schema, f"{path}/properties/{field_name}"
                )

    def _check_enum_values(self, enum_values: List[str], path: str) -> None:
        """Check enum value naming conventions."""
        for value in enum_values:
            if not isinstance(value, str):
                continue

            # Enum values should be UPPER_SNAKE_CASE
            if not self.UPPER_SNAKE_CASE.match(value):
                suggested = self._to_upper_snake_case(value)
                if suggested != value:
                    self.issues.append(
                        NamingIssue(
                            "Enum Value",
                            value,
                            suggested,
                            path,
                            "Enum values should use UPPER_SNAKE_CASE",
                        )
                    )

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert name to snake_case."""
        # Replace hyphens and spaces with underscores
        name = name.replace("-", "_").replace(" ", "_")

        # Insert underscore before uppercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)

        return s2.lower()

    @staticmethod
    def _to_kebab_case(name: str) -> str:
        """Convert name to kebab-case."""
        # Replace underscores and spaces with hyphens
        name = name.replace("_", "-").replace(" ", "-")

        # Insert hyphen before uppercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1-\2", s1)

        return s2.lower()

    @staticmethod
    def _to_upper_snake_case(name: str) -> str:
        """Convert name to UPPER_SNAKE_CASE."""
        # Replace hyphens and spaces with underscores
        name = name.replace("-", "_").replace(" ", "_")

        # Insert underscore before uppercase letters
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)

        return s2.upper()


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check API naming conventions"
    )
    parser.add_argument("spec", type=Path, help="Path to API specification file")
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )
    parser.add_argument(
        "--type",
        choices=["all", "paths", "parameters", "fields", "enums"],
        default="all",
        help="Type of naming to check (default: all)",
    )

    args = parser.parse_args()

    if not args.spec.exists():
        print(f"Error: File not found: {args.spec}")
        return 1

    checker = NamingChecker(args.spec)

    if not checker.load_spec():
        return 1

    print(f"Checking naming conventions in {args.spec}...")

    # Run specific checks based on type
    if args.type == "all":
        issues = checker.check_all()
    elif args.type == "paths":
        checker._check_paths()
        issues = checker.issues
    elif args.type == "parameters":
        checker._check_parameters()
        issues = checker.issues
    elif args.type == "fields" or args.type == "enums":
        checker._check_schemas()
        issues = checker.issues
    else:
        issues = checker.check_all()

    if args.json:
        # Output as JSON
        result = {
            "file": str(args.spec),
            "total_issues": len(issues),
            "issues": [
                {
                    "type": i.issue_type,
                    "current": i.current_name,
                    "suggested": i.suggested_name,
                    "location": i.location,
                    "reason": i.reason,
                }
                for i in issues
            ],
        }
        print(json.dumps(result, indent=2))
    else:
        # Output human-readable format
        if not issues:
            print("✓ No naming issues found!")
            return 0

        print(f"\nFound {len(issues)} naming issue(s):\n")

        # Group by type
        by_type: Dict[str, List[NamingIssue]] = {}
        for issue in issues:
            if issue.issue_type not in by_type:
                by_type[issue.issue_type] = []
            by_type[issue.issue_type].append(issue)

        for issue_type, type_issues in by_type.items():
            print(f"\n{issue_type} ({len(type_issues)}):")
            print("=" * 80)
            for issue in type_issues:
                print(f"\n{issue}\n")

        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
