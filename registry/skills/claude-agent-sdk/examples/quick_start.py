#!/usr/bin/env python3
"""
Claude Agent SDK - Quick Start Example

This example demonstrates basic usage of the Claude Agent SDK in Python.
"""

import anyio
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)


async def simple_query():
    """Basic query without options."""
    print("=== Simple Query ===\n")

    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"\n[Completed: {message.subtype}]")


async def query_with_options():
    """Query with custom options."""
    print("\n=== Query with Options ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful Python expert. Be concise.",
        max_turns=3,
    )

    async for message in query(
        prompt="Write a function to calculate factorial",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)


async def query_with_tools():
    """Query with tool access enabled."""
    print("\n=== Query with Tools ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a file system assistant.",
        allowed_tools=["Read", "Glob", "Grep"],
        permission_mode="acceptEdits",
        cwd=".",  # Current directory
    )

    async for message in query(
        prompt="List all Python files in the current directory",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(block.text)
                elif isinstance(block, ToolUseBlock):
                    print(f"[Using tool: {block.name}]")


async def streaming_output():
    """Stream output as it arrives."""
    print("\n=== Streaming Output ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a storyteller. Write short stories."
    )

    async for message in query(
        prompt="Write a very short story about a robot (2-3 sentences)",
        options=options
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    # Print without newline for streaming effect
                    print(block.text, end="", flush=True)

    print()  # Final newline


async def main():
    """Run all examples."""
    await simple_query()
    await query_with_options()
    await query_with_tools()
    await streaming_output()


if __name__ == "__main__":
    anyio.run(main)
