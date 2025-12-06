# CLI Development Skill

Build professional command-line interfaces with proper argument parsing, help text, error handling, and user experience.

## Overview

This skill provides expert guidance for creating production-quality CLI tools using modern patterns and best practices.

## When to Use This Skill

Trigger this skill when:
- Building CLI tools or command-line applications
- Creating developer utilities or automation scripts
- Implementing argument parsing and validation
- Designing command hierarchies (subcommands)
- Writing help text and documentation
- Adding shell completion
- Building interactive CLIs
- Creating project-specific commands
- Implementing progress bars and spinners
- Designing CLI UX and error messages

**Keywords:** CLI, command-line, argparse, click, typer, terminal, shell, commands, subcommands, argument parsing, CLI UX

## Core Principles

### CLI Design Philosophy

1. **UNIX Philosophy**: Do one thing well, compose with others
2. **Consistency**: Follow conventions (--help, --version, etc.)
3. **Discoverability**: Clear help text, examples
4. **Fail Fast**: Validate early, provide clear errors
5. **Defaults**: Sensible defaults, minimal required args
6. **Output**: Human-readable by default, machine-readable optional
7. **Colors**: Use color for clarity, not decoration
8. **Feedback**: Show progress for long operations

## Python CLI Frameworks

### Click (Most Popular)

```python
import click

@click.group()
@click.version_option()
def cli():
    """My CLI tool for managing projects"""
    pass

@cli.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='Greeting to use')
@click.option('--caps', is_flag=True, help='Capitalize output')
def greet(name: str, greeting: str, caps: bool):
    """Greet someone by name"""
    message = f"{greeting}, {name}!"
    if caps:
        message = message.upper()
    click.echo(message)

@cli.command()
@click.option('--format', type=click.Choice(['json', 'yaml', 'table']), default='table')
@click.pass_context
def list(ctx, format: str):
    """List all projects"""
    projects = get_projects()

    if format == 'json':
        click.echo(json.dumps(projects))
    elif format == 'yaml':
        click.echo(yaml.dump(projects))
    else:
        # Table format
        for project in projects:
            click.echo(f"{project['name']}: {project['status']}")

if __name__ == '__main__':
    cli()
```

### Typer (Modern, Type-Based)

```python
import typer
from typing import Optional
from enum import Enum

app = typer.Typer()

class OutputFormat(str, Enum):
    json = "json"
    yaml = "yaml"
    table = "table"

@app.command()
def greet(
    name: str,
    greeting: str = typer.Option("Hello", help="Greeting to use"),
    caps: bool = typer.Option(False, "--caps", help="Capitalize output")
):
    """Greet someone by name"""
    message = f"{greeting}, {name}!"
    if caps:
        message = message.upper()
    typer.echo(message)

@app.command()
def list(
    format: OutputFormat = typer.Option(OutputFormat.table, help="Output format")
):
    """List all projects"""
    projects = get_projects()

    if format == OutputFormat.json:
        import json
        typer.echo(json.dumps(projects))
    elif format == OutputFormat.yaml:
        import yaml
        typer.echo(yaml.dump(projects))
    else:
        for project in projects:
            typer.echo(f"{project['name']}: {project['status']}")

if __name__ == "__main__":
    app()
```

### Argparse (Standard Library)

```python
import argparse

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""

    parser = argparse.ArgumentParser(
        prog='mytool',
        description='My CLI tool for managing projects',
        epilog='For more info, visit https://example.com'
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Greet command
    greet_parser = subparsers.add_parser('greet', help='Greet someone')
    greet_parser.add_argument('name', help='Name to greet')
    greet_parser.add_argument('--greeting', default='Hello', help='Greeting to use')
    greet_parser.add_argument('--caps', action='store_true', help='Capitalize')

    # List command
    list_parser = subparsers.add_parser('list', help='List projects')
    list_parser.add_argument(
        '--format',
        choices=['json', 'yaml', 'table'],
        default='table',
        help='Output format'
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == 'greet':
        message = f"{args.greeting}, {args.name}!"
        if args.caps:
            message = message.upper()
        print(message)

    elif args.command == 'list':
        projects = get_projects()
        if args.format == 'json':
            print(json.dumps(projects))
        # ...

if __name__ == '__main__':
    main()
```

## Command Patterns

### Subcommands (Git-style)

```python
import typer

app = typer.Typer()
project_app = typer.Typer()
user_app = typer.Typer()

app.add_typer(project_app, name="project")
app.add_typer(user_app, name="user")

# mytool project create <name>
@project_app.command()
def create(name: str):
    """Create a new project"""
    typer.echo(f"Creating project: {name}")

# mytool project list
@project_app.command()
def list():
    """List all projects"""
    typer.echo("Projects:")

# mytool user add <username>
@user_app.command()
def add(username: str):
    """Add a new user"""
    typer.echo(f"Adding user: {username}")

if __name__ == "__main__":
    app()
```

### Interactive Prompts

```python
import typer

@app.command()
def init():
    """Initialize a new project interactively"""

    # Simple prompt
    name = typer.prompt("Project name")

    # With default
    language = typer.prompt("Language", default="Python")

    # Hidden (passwords)
    api_key = typer.prompt("API key", hide_input=True)

    # Confirmation
    if typer.confirm("Create project with these settings?"):
        create_project(name, language, api_key)
        typer.echo("✓ Project created")
    else:
        typer.echo("Cancelled")
```

### Progress Bars

```python
import typer
from rich.progress import track
import time

@app.command()
def process():
    """Process items with progress"""

    items = range(100)

    # Simple progress bar
    with typer.progressbar(items, label="Processing") as progress:
        for item in progress:
            time.sleep(0.1)

    # Rich progress bar
    for item in track(items, description="Processing..."):
        time.sleep(0.1)
```

## Output Formatting

### Colors and Styling

```python
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@app.command()
def status():
    """Show status with colors"""

    # Typer colored output
    typer.secho("✓ Success", fg=typer.colors.GREEN, bold=True)
    typer.secho("⚠ Warning", fg=typer.colors.YELLOW)
    typer.secho("✗ Error", fg=typer.colors.RED, bold=True)

    # Rich console
    console.print("[green]✓[/green] Success")
    console.print("[yellow]⚠[/yellow] Warning")
    console.print("[red]✗[/red] Error")

@app.command()
def list():
    """List with table"""

    table = Table(title="Projects")
    table.add_column("Name", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Updated", style="green")

    table.add_row("Project A", "Active", "2024-01-01")
    table.add_row("Project B", "Paused", "2024-01-02")

    console.print(table)

@app.command()
def info():
    """Show info in panel"""

    panel = Panel(
        "[bold]Project Information[/bold]\n\nName: My Project\nStatus: Active",
        title="Info",
        border_style="blue"
    )
    console.print(panel)
```

### JSON/YAML Output

```python
import json
import yaml
from typing import Any

def output(data: Any, format: str):
    """Output data in specified format"""

    if format == 'json':
        print(json.dumps(data, indent=2))
    elif format == 'yaml':
        print(yaml.dump(data, default_flow_style=False))
    elif format == 'table':
        # Rich table
        table = create_table(data)
        console.print(table)
    else:
        # Human-readable
        for key, value in data.items():
            print(f"{key}: {value}")
```

## Error Handling

### User-Friendly Errors

```python
import typer
from typing import NoReturn

def error(message: str, exit_code: int = 1) -> NoReturn:
    """Display error and exit"""
    typer.secho(f"✗ Error: {message}", fg=typer.colors.RED, err=True)
    raise typer.Exit(exit_code)

def warn(message: str):
    """Display warning"""
    typer.secho(f"⚠ Warning: {message}", fg=typer.colors.YELLOW, err=True)

@app.command()
def deploy(project: str):
    """Deploy a project"""

    if not project_exists(project):
        error(f"Project '{project}' not found. Run 'mytool project list' to see available projects.")

    if not has_permissions(project):
        error("You don't have permission to deploy this project.", exit_code=13)

    try:
        perform_deployment(project)
        typer.secho("✓ Deployment successful", fg=typer.colors.GREEN)
    except DeploymentError as e:
        error(f"Deployment failed: {e}\n\nTry:\n  mytool logs {project}\n  mytool status {project}")
```

### Validation

```python
from pathlib import Path

def validate_file_exists(value: Path) -> Path:
    """Validate file exists"""
    if not value.exists():
        raise typer.BadParameter(f"File not found: {value}")
    return value

def validate_positive_int(value: int) -> int:
    """Validate positive integer"""
    if value <= 0:
        raise typer.BadParameter("Must be a positive integer")
    return value

@app.command()
def process(
    input_file: Path = typer.Argument(..., callback=validate_file_exists),
    count: int = typer.Option(1, callback=validate_positive_int)
):
    """Process input file"""
    typer.echo(f"Processing {input_file} {count} times")
```

## Configuration

### Config Files

```python
import typer
from pathlib import Path
import yaml

CONFIG_DIR = Path.home() / ".config" / "mytool"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

def load_config() -> dict:
    """Load configuration"""
    if not CONFIG_FILE.exists():
        return {}

    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f) or {}

def save_config(config: dict):
    """Save configuration"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

@app.command()
def config(
    key: str = typer.Argument(None),
    value: str = typer.Argument(None)
):
    """Get or set configuration"""

    config = load_config()

    if key is None:
        # Show all config
        for k, v in config.items():
            typer.echo(f"{k} = {v}")
    elif value is None:
        # Get specific key
        if key in config:
            typer.echo(config[key])
        else:
            error(f"Configuration key '{key}' not found")
    else:
        # Set key
        config[key] = value
        save_config(config)
        typer.secho(f"✓ Set {key} = {value}", fg=typer.colors.GREEN)
```

### Environment Variables

```python
import os
import typer

@app.command()
def deploy(
    api_key: str = typer.Option(
        None,
        envvar="API_KEY",
        help="API key (or set API_KEY env var)"
    )
):
    """Deploy with API key from env or option"""

    if not api_key:
        error("API key required. Set --api-key or API_KEY environment variable.")

    perform_deployment(api_key)
```

## Shell Completion

### Bash Completion

```python
import typer

app = typer.Typer()

@app.command()
def completion(shell: str = typer.Argument("bash")):
    """Generate shell completion script"""

    if shell == "bash":
        script = """
_mytool_completion() {
    local IFS=$'\\n'
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \\
                   COMP_CWORD=$COMP_CWORD \\
                   _MYTOOL_COMPLETE=complete $1 ) )
    return 0
}

complete -F _mytool_completion -o default mytool
"""
        typer.echo(script)
    else:
        typer.echo(f"Shell '{shell}' not supported")
```

## Testing CLIs

### Click Testing

```python
from click.testing import CliRunner
import pytest

@pytest.fixture
def runner():
    return CliRunner()

def test_greet_command(runner):
    """Test greet command"""
    result = runner.invoke(cli, ['greet', 'John'])

    assert result.exit_code == 0
    assert 'Hello, John!' in result.output

def test_greet_with_caps(runner):
    """Test greet with caps flag"""
    result = runner.invoke(cli, ['greet', 'John', '--caps'])

    assert result.exit_code == 0
    assert 'HELLO, JOHN!' in result.output

def test_invalid_command(runner):
    """Test invalid command"""
    result = runner.invoke(cli, ['invalid'])

    assert result.exit_code != 0
    assert 'Error' in result.output
```

### Typer Testing

```python
from typer.testing import CliRunner
import pytest

runner = CliRunner()

def test_command():
    """Test CLI command"""
    result = runner.invoke(app, ["greet", "World"])

    assert result.exit_code == 0
    assert "Hello, World!" in result.stdout
```

## Advanced Patterns

### Plugin System

```python
import importlib
import pkgutil

def discover_plugins(package_name: str):
    """Discover and load plugins"""

    package = importlib.import_module(package_name)
    plugins = []

    for _, name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package_name}.{name}")

        if hasattr(module, 'register'):
            plugins.append(module)

    return plugins

# Load plugins
for plugin in discover_plugins('mytool.plugins'):
    plugin.register(app)
```

### Middleware/Hooks

```python
import typer
from functools import wraps

def require_auth(func):
    """Decorator to require authentication"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            error("Authentication required. Run 'mytool login' first.")
        return func(*args, **kwargs)
    return wrapper

@app.command()
@require_auth
def deploy(project: str):
    """Deploy project (requires auth)"""
    perform_deployment(project)
```

## Node.js CLI (Commander.js)

```javascript
#!/usr/bin/env node
const { program } = require('commander');
const chalk = require('chalk');

program
  .name('mytool')
  .description('My CLI tool for managing projects')
  .version('1.0.0');

program
  .command('greet <name>')
  .description('Greet someone by name')
  .option('--greeting <greeting>', 'greeting to use', 'Hello')
  .option('--caps', 'capitalize output')
  .action((name, options) => {
    let message = `${options.greeting}, ${name}!`;
    if (options.caps) {
      message = message.toUpperCase();
    }
    console.log(message);
  });

program
  .command('list')
  .description('List all projects')
  .option('-f, --format <format>', 'output format', 'table')
  .action((options) => {
    const projects = getProjects();

    if (options.format === 'json') {
      console.log(JSON.stringify(projects, null, 2));
    } else {
      projects.forEach(p => {
        console.log(`${p.name}: ${p.status}`);
      });
    }
  });

program.parse();
```

## Resources

### Templates
- `resources/click-template.py` - Click CLI template
- `resources/typer-template.py` - Typer CLI template
- `resources/commander-template.js` - Commander.js template
- `resources/argparse-template.py` - Argparse template

### Scripts
- `scripts/generate-cli.py` - Generate CLI boilerplate
- `scripts/test-cli-ux.py` - CLI UX testing tool

## Related Skills

- **developer-experience**: CLI for development workflows
- **python-development**: Python CLI best practices

## Best Practices Summary

1. **Follow Conventions**: --help, --version, exit codes
2. **Clear Help Text**: Examples, descriptions
3. **Sensible Defaults**: Minimize required arguments
4. **Early Validation**: Fail fast with clear errors
5. **Progress Feedback**: Show progress for long operations
6. **Colors Thoughtfully**: Enhance clarity, not decoration
7. **Output Formats**: Human and machine-readable options
8. **Testing**: Automated CLI testing
9. **Completion**: Shell completion support
10. **Documentation**: README with examples
