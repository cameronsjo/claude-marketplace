#!/usr/bin/env python3
"""
Claude Agent SDK - Custom Tools Example

This example demonstrates creating custom tools using in-process MCP servers.
"""

import anyio
import json
from datetime import datetime
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)


# Define custom tools using the @tool decorator
@tool(
    name="get_current_time",
    description="Get the current date and time",
    input_schema={}
)
async def get_current_time(args):
    """Return the current time."""
    now = datetime.now()
    return {
        "content": [{
            "type": "text",
            "text": now.strftime("%Y-%m-%d %H:%M:%S")
        }]
    }


@tool(
    name="calculate",
    description="Perform a mathematical calculation",
    input_schema={
        "expression": {
            "type": "string",
            "description": "Mathematical expression to evaluate (e.g., '2 + 2')"
        }
    }
)
async def calculate(args):
    """Safely evaluate a mathematical expression."""
    expression = args.get("expression", "")

    # Safe evaluation - only allow numbers and basic operators
    allowed_chars = set("0123456789+-*/.() ")
    if not all(c in allowed_chars for c in expression):
        return {
            "content": [{
                "type": "text",
                "text": "Error: Expression contains invalid characters"
            }]
        }

    try:
        result = eval(expression)  # Safe due to character filtering
        return {
            "content": [{
                "type": "text",
                "text": f"{expression} = {result}"
            }]
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error: {str(e)}"
            }]
        }


@tool(
    name="save_note",
    description="Save a note to the notes database",
    input_schema={
        "title": {
            "type": "string",
            "description": "Title of the note"
        },
        "content": {
            "type": "string",
            "description": "Content of the note"
        }
    }
)
async def save_note(args):
    """Save a note to a JSON file."""
    title = args.get("title", "Untitled")
    content = args.get("content", "")

    note = {
        "title": title,
        "content": content,
        "created_at": datetime.now().isoformat()
    }

    # In a real app, you'd save to a database
    print(f"[Saving note: {title}]")

    return {
        "content": [{
            "type": "text",
            "text": f"Note '{title}' saved successfully"
        }]
    }


@tool(
    name="get_weather",
    description="Get weather information for a location",
    input_schema={
        "location": {
            "type": "string",
            "description": "City name or location"
        }
    }
)
async def get_weather(args):
    """Mock weather service - replace with real API call."""
    location = args.get("location", "Unknown")

    # Mock data - in production, call a real weather API
    weather_data = {
        "location": location,
        "temperature": "72°F",
        "condition": "Sunny",
        "humidity": "45%"
    }

    return {
        "content": [{
            "type": "text",
            "text": json.dumps(weather_data, indent=2)
        }]
    }


async def main():
    """Run custom tools example."""
    print("=== Custom Tools Example ===\n")

    # Create an in-process MCP server with our custom tools
    custom_server = create_sdk_mcp_server(
        name="my-tools",
        version="1.0.0",
        tools=[get_current_time, calculate, save_note, get_weather]
    )

    # Configure options with our custom tools
    options = ClaudeAgentOptions(
        system_prompt="""You are a helpful assistant with access to custom tools.
Available tools:
- get_current_time: Get the current date and time
- calculate: Perform mathematical calculations
- save_note: Save notes to the database
- get_weather: Get weather for a location

Use these tools to help the user.""",
        mcp_servers=[custom_server],
        allowed_tools=[
            "mcp__my-tools__get_current_time",
            "mcp__my-tools__calculate",
            "mcp__my-tools__save_note",
            "mcp__my-tools__get_weather",
        ],
        permission_mode="acceptEdits"
    )

    # Test the custom tools
    prompts = [
        "What time is it right now?",
        "Calculate 15 * 7 + 23",
        "Save a note titled 'Meeting' with content 'Team sync at 3pm'",
        "What's the weather in San Francisco?",
    ]

    for prompt in prompts:
        print(f"User: {prompt}\n")

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Assistant: {block.text}")
                    elif isinstance(block, ToolUseBlock):
                        print(f"[Tool: {block.name}]")
            elif isinstance(message, ResultMessage):
                print()
                break

        print("-" * 40 + "\n")


if __name__ == "__main__":
    anyio.run(main)
