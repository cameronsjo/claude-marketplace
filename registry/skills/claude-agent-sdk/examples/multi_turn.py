#!/usr/bin/env python3
"""
Claude Agent SDK - Multi-Turn Conversation Example

This example demonstrates stateful conversations using ClaudeSDKClient.
"""

import anyio
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)


async def multi_turn_conversation():
    """Demonstrate multi-turn conversation with context preservation."""
    print("=== Multi-Turn Conversation ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a helpful coding tutor. Remember what we discuss.",
        allowed_tools=["Read", "Write"],
        permission_mode="acceptEdits",
    )

    async with ClaudeSDKClient(options=options) as client:
        # First turn
        print("User: Explain what a Python decorator is.\n")
        await client.query("Explain what a Python decorator is.")

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Assistant: {block.text}\n")
            elif isinstance(message, ResultMessage):
                break

        # Second turn - Claude remembers context
        print("User: Now show me an example of one.\n")
        await client.query("Now show me an example of one.")

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Assistant: {block.text}\n")
            elif isinstance(message, ResultMessage):
                break

        # Third turn - building on previous context
        print("User: Can you create a timing decorator and save it to timing.py?\n")
        await client.query("Can you create a timing decorator and save it to timing.py?")

        async for message in client.receive_messages():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Assistant: {block.text}\n")
            elif isinstance(message, ResultMessage):
                break


async def session_management():
    """Demonstrate session persistence and forking."""
    print("\n=== Session Management ===\n")

    options = ClaudeAgentOptions(
        system_prompt="You are a project planner."
    )

    session_id = None

    # First session - establish context
    async with ClaudeSDKClient(options=options) as client:
        await client.query("Let's plan a web application. It should have user auth and a dashboard.")

        async for message in client.receive_messages():
            if hasattr(message, 'session_id'):
                session_id = message.session_id
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Planning: {block.text[:200]}...\n")
            elif isinstance(message, ResultMessage):
                break

    if session_id:
        print(f"Session ID: {session_id}\n")

        # Resume session later
        async with ClaudeSDKClient(options=options) as client:
            await client.query(
                "What were the main features we discussed?",
                resume_session=session_id
            )

            async for message in client.receive_messages():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Resumed: {block.text[:200]}...\n")
                elif isinstance(message, ResultMessage):
                    break


async def main():
    await multi_turn_conversation()
    await session_management()


if __name__ == "__main__":
    anyio.run(main)
