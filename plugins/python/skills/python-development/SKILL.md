# Python Best Practices Skill

Expert guidance for writing idiomatic, maintainable, and production-ready Python code following modern best practices.

## Overview

This skill provides comprehensive expertise for Python development including code style, type safety, testing, tooling, and design patterns.

## When to Use This Skill

Trigger this skill when:
- Writing Python code or scripts
- Setting up Python projects
- Implementing type hints and validation
- Using asyncio and async/await
- Applying Python design patterns
- Configuring Python tooling (ruff, mypy, pytest)
- Optimizing Python performance
- Structuring Python packages
- Following PEP standards
- Code review for Python

**Keywords:** Python, type hints, asyncio, pydantic, pytest, ruff, mypy, poetry, uv, PEP, pythonic

## Core Principles

### Pythonic Code Philosophy

**From CLAUDE.md:**
- Code should read like paragraphs with clear method/variable names
- Functional > imperative, immutable > mutable
- Async/await over callbacks
- SOLID + DRY principles
- Type safety with annotations
- Defensive programming

### The Zen of Python (PEP 20)

```python
import this

# Key principles:
# - Beautiful is better than ugly
# - Explicit is better than implicit
# - Simple is better than complex
# - Readability counts
# - Errors should never pass silently
```

## Type Safety

### Type Hints (PEP 484, 585, 604)

```python
from typing import Optional, Union, List, Dict, Any, TypeVar, Generic
from collections.abc import Sequence, Mapping

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}"

# Collections (modern syntax - Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Optional (use | None in Python 3.10+)
def find_user(user_id: int) -> User | None:
    return db.get(user_id)

# Union types (use | in Python 3.10+)
def handle_input(value: int | str) -> str:
    return str(value)

# Type aliases
UserId = int
UserData = dict[str, Any]

def get_user(user_id: UserId) -> UserData:
    ...

# Generic types
T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value

# Callable types
from collections.abc import Callable

def apply(func: Callable[[int, int], int], x: int, y: int) -> int:
    return func(x, y)
```

### Pydantic for Validation

```python
from pydantic import BaseModel, Field, validator, root_validator
from datetime import datetime

class User(BaseModel):
    """User model with validation"""

    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    tags: list[str] = Field(default_factory=list)

    @validator('email')
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v.lower()

    @validator('username')
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @root_validator
    def validate_model(cls, values: dict) -> dict:
        # Cross-field validation
        return values

    class Config:
        # Configuration
        validate_assignment = True
        arbitrary_types_allowed = False

# Usage
user = User(id=1, username="john", email="john@example.com")
print(user.json())  # JSON serialization
```

### MyPy Configuration

```ini
# mypy.ini or pyproject.toml [tool.mypy]
[mypy]
python_version = 3.10
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

# Avoid Any types
warn_return_any = true
disallow_any_unimported = false
disallow_any_expr = false  # Too strict for most projects
disallow_any_decorated = false
disallow_any_explicit = false

# Per-module options
[mypy-tests.*]
disallow_untyped_defs = false
```

## Async/Await Patterns

### Modern Asyncio

```python
import asyncio
from typing import Any
from collections.abc import Coroutine

# Basic async function
async def fetch_data(url: str) -> dict[str, Any]:
    """Fetch data from URL asynchronously"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Concurrent execution
async def fetch_all(urls: list[str]) -> list[dict[str, Any]]:
    """Fetch multiple URLs concurrently"""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

# With error handling
async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    backoff: float = 1.0
) -> dict[str, Any]:
    """Fetch with exponential backoff retry"""
    for attempt in range(max_retries):
        try:
            return await fetch_data(url)
        except aiohttp.ClientError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(backoff * (2 ** attempt))

    raise RuntimeError("Max retries exceeded")

# Async context manager
class AsyncResource:
    """Async context manager for resources"""

    async def __aenter__(self) -> "AsyncResource":
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def connect(self) -> None:
        """Connect to resource"""
        ...

    async def close(self) -> None:
        """Close resource"""
        ...

# Usage
async with AsyncResource() as resource:
    await resource.do_something()

# Async generator
async def async_range(count: int):
    """Async generator example"""
    for i in range(count):
        await asyncio.sleep(0.1)
        yield i

# Usage
async for value in async_range(10):
    print(value)

# Running async code
async def main() -> None:
    result = await fetch_data("https://api.example.com")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Async Best Practices

```python
# ✅ Good: Concurrent execution
async def process_items(items: list[int]) -> list[int]:
    tasks = [process_item(item) for item in items]
    return await asyncio.gather(*tasks)

# ❌ Bad: Sequential execution
async def process_items_bad(items: list[int]) -> list[int]:
    results = []
    for item in items:
        result = await process_item(item)  # Wastes time
        results.append(result)
    return results

# ✅ Good: Proper error handling
async def safe_fetch(url: str) -> dict[str, Any] | None:
    try:
        return await fetch_data(url)
    except asyncio.TimeoutError:
        logger.warning("Timeout fetching %s", url)
        return None
    except Exception as e:
        logger.error("Error fetching %s: %s", url, e)
        return None

# ✅ Good: Resource cleanup
async def process_with_cleanup():
    connection = await create_connection()
    try:
        return await connection.execute(query)
    finally:
        await connection.close()
```

## Code Style and Standards

### Naming Conventions (From CLAUDE.md)

```python
# ✅ Positive names (avoid negatives)
is_enabled = True      # Good
is_visible = True      # Good
is_active = True       # Good

is_disabled = False    # Bad - double negative: if not is_disabled
is_hidden = False      # Bad
is_inactive = False    # Bad

# ✅ Descriptive names without abbreviations
def calculate_total_price(items: list[Item]) -> Decimal:  # Good
    ...

def calc_tot(items):  # Bad - abbreviated
    ...

# ✅ Accurate, neutral, inclusive terminology
allow_list = ["item1", "item2"]  # Good
block_list = ["spam"]            # Good

whitelist = []  # Bad (unless describing colors)
blacklist = []  # Bad

primary_database = "main"    # Good
secondary_database = "replica"  # Good

master_db = ""  # Bad
slave_db = ""   # Bad
```

### Ruff Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py310"

select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "DTZ", # flake8-datetimez
    "T10", # flake8-debugger
    "ICN", # flake8-import-conventions
    "PIE", # flake8-pie
    "PT",  # flake8-pytest-style
    "RSE", # flake8-raise
    "RET", # flake8-return
    "SIM", # flake8-simplify
    "TID", # flake8-tidy-imports
    "ARG", # flake8-unused-arguments
    "PTH", # flake8-use-pathlib
    "ERA", # eradicate
    "PL",  # pylint
    "RUF", # ruff-specific
]

ignore = [
    "E501",  # Line too long (handled by formatter)
    "PLR0913",  # Too many arguments
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests

[tool.ruff.isort]
known-first-party = ["myproject"]

[tool.ruff.mccabe]
max-complexity = 10
```

### Black Configuration

```toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

## Error Handling

### Defensive Programming (From CLAUDE.md)

```python
from datetime import datetime, date
from decimal import Decimal

# ✅ Type check datetimes
def format_date(value: datetime | date | str) -> str:
    """Format date defensively"""
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    elif isinstance(value, date):
        value = datetime.combine(value, datetime.min.time())

    if not isinstance(value, datetime):
        raise TypeError(f"Expected datetime, got {type(value)}")

    return value.strftime("%Y-%m-%d")

# ✅ Validate inputs
def divide(a: float, b: float) -> float:
    """Divide with validation"""
    if b == 0:
        raise ValueError("Cannot divide by zero")

    if not isinstance(a, (int, float)):
        raise TypeError(f"Expected number for a, got {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Expected number for b, got {type(b)}")

    return a / b

# ✅ Fail fast with clear errors
def process_user(user_id: int) -> User:
    """Process user with fail-fast approach"""
    if user_id <= 0:
        raise ValueError(f"Invalid user_id: {user_id}. Must be positive.")

    user = get_user(user_id)

    if user is None:
        raise ValueError(f"User not found: {user_id}")

    if not user.is_active:
        raise ValueError(f"User is inactive: {user_id}")

    return user

# ✅ Explicit errors, no silent failures
def load_config(path: str) -> dict[str, Any]:
    """Load configuration, fail explicitly on error"""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file not found: {path}\n"
            f"Create it with: cp config.example.json {path}"
        )
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON in configuration file: {path}\n"
            f"Error at line {e.lineno}: {e.msg}"
        )
```

### Exception Hierarchies

```python
# Custom exceptions
class ApplicationError(Exception):
    """Base exception for application"""
    pass

class ValidationError(ApplicationError):
    """Validation failed"""
    pass

class NotFoundError(ApplicationError):
    """Resource not found"""
    pass

class AuthenticationError(ApplicationError):
    """Authentication failed"""
    pass

# Usage
def get_user(user_id: int) -> User:
    if user_id <= 0:
        raise ValidationError(f"Invalid user_id: {user_id}")

    user = db.query(User).get(user_id)
    if not user:
        raise NotFoundError(f"User not found: {user_id}")

    return user
```

## Logging Best Practices (From CLAUDE.md)

### Lazy Logging

```python
import logging

logger = logging.getLogger(__name__)

# ✅ Good: Lazy evaluation (only formats if logging level active)
logger.debug("Processing user %s with data %s", user_id, data)

# ❌ Bad: Eager evaluation (always creates string)
logger.debug(f"Processing user {user_id} with data {data}")

# ✅ Good: Structured logging with extra
logger.info(
    "User login successful",
    extra={
        "user_id": user_id,
        "ip_address": request.remote_addr,
        "user_agent": request.headers.get("User-Agent")
    }
)
```

### Logging Configuration

```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    },
    "loggers": {
        "": {  # Root logger
            "level": "INFO",
            "handlers": ["console", "file"]
        },
        "myapp": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## Testing with Pytest

### Test Organization

```python
# tests/test_user.py
import pytest
from myapp.models import User
from myapp.services import UserService

# ✅ Atomic, self-contained tests
def test_create_user():
    """Test user creation"""
    user = User(username="john", email="john@example.com")
    assert user.username == "john"
    assert user.email == "john@example.com"

# ✅ Use fixtures for reusable setup
@pytest.fixture
def user_service():
    """User service fixture"""
    return UserService(db=MockDatabase())

@pytest.fixture
def sample_user():
    """Sample user fixture"""
    return User(id=1, username="john", email="john@example.com")

# ✅ Parameterize for multiple test cases
@pytest.mark.parametrize("username,expected", [
    ("john", True),
    ("j", False),  # Too short
    ("", False),   # Empty
    ("a" * 100, False),  # Too long
])
def test_validate_username(username: str, expected: bool):
    """Test username validation"""
    result = validate_username(username)
    assert result == expected

# ✅ Async tests (NO @pytest.mark.asyncio needed with asyncio_mode = "auto")
async def test_async_fetch_user(user_service):
    """Test async user fetch"""
    user = await user_service.get_user(1)
    assert user.id == 1

# ✅ Exception testing
def test_invalid_user_id():
    """Test that invalid user_id raises ValueError"""
    with pytest.raises(ValueError, match="Invalid user_id"):
        get_user(-1)

# ✅ Use markers for test categories
@pytest.mark.slow
def test_expensive_operation():
    """Test that takes a long time"""
    ...

@pytest.mark.integration
async def test_database_integration():
    """Integration test with real database"""
    ...
```

### Pytest Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"  # No @pytest.mark.asyncio needed
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=myapp",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

## Project Structure

### Modern Python Project

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── __main__.py       # Entry point: python -m myproject
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── unit/
│   │   └── test_user.py
│   └── integration/
│       └── test_api.py
├── docs/
│   └── README.md
├── pyproject.toml            # Project configuration
├── README.md
└── .python-version           # Python version for pyenv
```

### pyproject.toml (Complete)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "myproject"
version = "0.1.0"
description = "My Python project"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "pydantic>=2.0.0",
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.7.0",
    "ruff>=0.1.6",
    "black>=23.11.0",
]

[project.scripts]
myproject = "myproject.__main__:main"

[tool.hatch.build.targets.wheel]
packages = ["src/myproject"]

# Ruff configuration
[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "W", "F", "I", "N", "B", "A", "C4"]

# Black configuration
[tool.black]
line-length = 88
target-version = ['py310']

# MyPy configuration
[tool.mypy]
python_version = "3.10"
strict = true

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
```

## Design Patterns

### Factory Pattern

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    async def connect(self) -> None:
        ...

    @abstractmethod
    async def query(self, sql: str) -> list[dict]:
        ...

class PostgresDatabase(Database):
    async def connect(self) -> None:
        # PostgreSQL connection
        ...

    async def query(self, sql: str) -> list[dict]:
        # Execute query
        ...

class DatabaseFactory:
    @staticmethod
    def create(db_type: str) -> Database:
        if db_type == "postgres":
            return PostgresDatabase()
        elif db_type == "mysql":
            return MySQLDatabase()
        else:
            raise ValueError(f"Unknown database type: {db_type}")

# Usage
db = DatabaseFactory.create("postgres")
await db.connect()
```

### Context Manager

```python
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def file_handler(filename: str):
    """Context manager for file handling"""
    f = open(filename, 'w')
    try:
        yield f
    finally:
        f.close()

# Usage
with file_handler('test.txt') as f:
    f.write('Hello')

@asynccontextmanager
async def async_resource():
    """Async context manager"""
    resource = await acquire_resource()
    try:
        yield resource
    finally:
        await release_resource(resource)

# Usage
async with async_resource() as resource:
    await resource.do_something()
```

## Performance Optimization

### Avoid Common Pitfalls

```python
# ✅ Good: Use list comprehension
squares = [x**2 for x in range(1000)]

# ❌ Bad: Append in loop
squares = []
for x in range(1000):
    squares.append(x**2)

# ✅ Good: Use dict.get() with default
value = config.get('key', default_value)

# ❌ Bad: Check with hasattr
if hasattr(config, 'key'):
    value = config.key
else:
    value = default_value

# ✅ Good: Use sets for membership testing
valid_ids = {1, 2, 3, 4, 5}
if user_id in valid_ids:  # O(1)
    ...

# ❌ Bad: Use lists for membership
valid_ids = [1, 2, 3, 4, 5]
if user_id in valid_ids:  # O(n)
    ...

# ✅ Good: Use generators for large data
def process_large_file(filename: str):
    with open(filename) as f:
        for line in f:  # Generator, memory efficient
            yield process_line(line)

# ❌ Bad: Load everything into memory
def process_large_file_bad(filename: str):
    with open(filename) as f:
        lines = f.readlines()  # Loads entire file
        return [process_line(line) for line in lines]
```

## Resources

### Templates
- `resources/pyproject-template.toml` - Modern Python project config
- `resources/ruff-config.toml` - Ruff linter configuration
- `resources/mypy-config.ini` - MyPy type checker config
- `resources/pytest-template.py` - Pytest test templates

### Scripts
- `scripts/setup-python-project.py` - Initialize new Python project
- `scripts/analyze-type-coverage.py` - Check type hint coverage
- `scripts/profile-performance.py` - Profile Python code

## Related Skills

- **mcp-development**: Python MCP servers with fastmcp
- **developer-experience**: Python DX improvements
- **api-design**: Python API development

## Best Practices Summary (From CLAUDE.md)

1. **Type Hints Always**: Add type annotations, minimize `Any`
2. **No Magic Strings/Numbers**: Use constants and enums
3. **Avoid hasattr()**: Use `getattr()` with default or try/except
4. **Lazy Logging**: Use `logger.debug("val=%s", val)` not f-strings
5. **Defensive Programming**: Validate inputs, fail fast
6. **Positive Naming**: `is_enabled` not `is_disabled`
7. **Tooling**: ruff, black, isort, mypy, pylance, pyright
8. **Async/Await**: Modern asyncio patterns
9. **Testing**: pytest with asyncio_mode="auto"
10. **Package Manager**: uv for speed, pip as fallback
