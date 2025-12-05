#!/usr/bin/env python3
"""
Claude Agent SDK - Custom Tools Example

This example demonstrates creating custom tools using in-process MCP servers.
Based on official Anthropic SDK examples from:
https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/mcp_calculator.py
"""

import asyncio
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    create_sdk_mcp_server,
    tool,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
)


# Define calculator tools using the @tool decorator
# Format: @tool(name, description, {param: type})

@tool("add", "Add two numbers", {"a": float, "b": float})
async def add_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """Add two numbers together."""
    result = args["a"] + args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} + {args['b']} = {result}"}]
    }


@tool("subtract", "Subtract one number from another", {"a": float, "b": float})
async def subtract_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """Subtract b from a."""
    result = args["a"] - args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} - {args['b']} = {result}"}]
    }


@tool("multiply", "Multiply two numbers", {"a": float, "b": float})
async def multiply_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """Multiply two numbers."""
    result = args["a"] * args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} × {args['b']} = {result}"}]
    }


@tool("divide", "Divide one number by another", {"a": float, "b": float})
async def divide_numbers(args: dict[str, Any]) -> dict[str, Any]:
    """Divide a by b."""
    if args["b"] == 0:
        return {
            "content": [
                {"type": "text", "text": "Error: Division by zero is not allowed"}
            ],
            "is_error": True,
        }

    result = args["a"] / args["b"]
    return {
        "content": [{"type": "text", "text": f"{args['a']} ÷ {args['b']} = {result}"}]
    }


@tool("sqrt", "Calculate square root", {"n": float})
async def square_root(args: dict[str, Any]) -> dict[str, Any]:
    """Calculate the square root of a number."""
    n = args["n"]
    if n < 0:
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error: Cannot calculate square root of negative number {n}",
                }
            ],
            "is_error": True,
        }

    import math
    result = math.sqrt(n)
    return {"content": [{"type": "text", "text": f"√{n} = {result}"}]}


def display_message(msg):
    """Display message content in a clean format."""
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(f"Claude: {block.text}")
            elif isinstance(block, ToolUseBlock):
                print(f"Using tool: {block.name}")
                if block.input:
                    print(f"  Input: {block.input}")
    elif isinstance(msg, ResultMessage):
        print("Result ended")
        if msg.total_cost_usd:
            print(f"Cost: ${msg.total_cost_usd:.6f}")


async def main():
    """Run example calculations using the SDK MCP server with streaming client."""
    print("=== Calculator MCP Server Example ===\n")

    # Create the calculator server with all tools
    calculator = create_sdk_mcp_server(
        name="calculator",
        version="2.0.0",
        tools=[
            add_numbers,
            subtract_numbers,
            multiply_numbers,
            divide_numbers,
            square_root,
        ],
    )

    # Configure Claude to use the calculator server
    # Note: mcp_servers is a dict mapping server names to server instances
    # Tools are namespaced as mcp__{server_name}__{tool_name}
    options = ClaudeAgentOptions(
        mcp_servers={"calc": calculator},
        allowed_tools=[
            "mcp__calc__add",
            "mcp__calc__subtract",
            "mcp__calc__multiply",
            "mcp__calc__divide",
            "mcp__calc__sqrt",
        ],
    )

    # Example prompts to demonstrate calculator usage
    prompts = [
        "List your tools",
        "Calculate 15 + 27",
        "What is 100 divided by 7?",
        "Calculate the square root of 144",
        "Calculate (12 + 8) * 3 - 10",
    ]

    for prompt in prompts:
        print(f"\n{'=' * 50}")
        print(f"Prompt: {prompt}")
        print(f"{'=' * 50}")

        async with ClaudeSDKClient(options=options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                display_message(message)


if __name__ == "__main__":
    asyncio.run(main())
