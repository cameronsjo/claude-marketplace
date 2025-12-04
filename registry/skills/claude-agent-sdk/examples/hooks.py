#!/usr/bin/env python3
"""
Claude Agent SDK - Hooks Example

This example demonstrates using hooks with Claude Code SDK.
Based on official Anthropic SDK examples from:
https://github.com/anthropics/claude-agent-sdk-python/blob/main/examples/hooks.py

Hooks are Python functions that the Claude Code application invokes at
specific points of the Claude agent loop. They enable deterministic
processing and automated feedback.
"""

import asyncio
import logging
from typing import Any

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    ResultMessage,
    TextBlock,
)
from claude_agent_sdk.types import (
    HookContext,
    HookInput,
    HookJSONOutput,
    HookMatcher,
    Message,
)

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def display_message(msg: Message) -> None:
    """Standardized message display function."""
    if isinstance(msg, AssistantMessage):
        for block in msg.content:
            if isinstance(block, TextBlock):
                print(f"Claude: {block.text}")
    elif isinstance(msg, ResultMessage):
        print("Result ended")


# ============================================================================
# Hook Callback Functions
# ============================================================================

async def check_bash_command(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """
    PreToolUse hook that blocks certain bash commands.

    This hook examines bash commands before execution and can deny
    commands that match blocked patterns.
    """
    tool_name = input_data["tool_name"]
    tool_input = input_data["tool_input"]

    if tool_name != "Bash":
        return {}

    command = tool_input.get("command", "")
    block_patterns = ["rm -rf", "sudo", "curl | bash"]

    for pattern in block_patterns:
        if pattern in command:
            logger.warning(f"Blocked command: {command}")
            return {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Command contains blocked pattern: {pattern}",
                }
            }

    return {}


async def add_custom_instructions(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """
    UserPromptSubmit hook that adds custom context.

    This hook runs when the user submits a prompt and can inject
    additional context into the conversation.
    """
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "Remember: Always explain your reasoning step by step.",
        }
    }


async def review_tool_output(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """
    PostToolUse hook that reviews tool output.

    This hook runs after a tool completes and can provide
    additional context or warnings based on the output.
    """
    tool_response = input_data.get("tool_response", "")

    if "error" in str(tool_response).lower():
        return {
            "systemMessage": "⚠️ The command produced an error",
            "reason": "Tool execution failed",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "Consider trying a different approach.",
            }
        }

    return {}


async def strict_approval_hook(
    input_data: HookInput,
    tool_use_id: str | None,
    context: HookContext
) -> HookJSONOutput:
    """
    PreToolUse hook demonstrating permissionDecision control.

    This hook explicitly allows or denies tool execution based
    on security policies.
    """
    tool_name = input_data.get("tool_name")
    tool_input = input_data.get("tool_input", {})

    # Block Write operations to specific files
    if tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        if "important" in file_path.lower() or ".env" in file_path:
            logger.warning(f"Blocked Write to: {file_path}")
            return {
                "reason": "Security policy blocks writes to sensitive files",
                "systemMessage": "🚫 Write operation blocked by security policy",
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Security policy blocks writes to sensitive files",
                },
            }

    # Allow everything else
    return {
        "reason": "Tool use approved",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Tool passed security checks",
        },
    }


# ============================================================================
# Examples
# ============================================================================

async def example_pretooluse() -> None:
    """Demonstrate PreToolUse hook that blocks dangerous commands."""
    print("=== PreToolUse Example ===")
    print("This example shows how PreToolUse can block dangerous bash commands.\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Bash"],
        hooks={
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[check_bash_command]),
            ],
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        # Test 1: Dangerous command (will be blocked)
        print("Test 1: Trying 'rm -rf /' (should be blocked)...")
        await client.query("Run: echo test && rm -rf /")

        async for msg in client.receive_response():
            display_message(msg)

        print("\n" + "=" * 50 + "\n")

        # Test 2: Safe command (should work)
        print("Test 2: Trying 'echo hello' (should work)...")
        await client.query("Run: echo 'Hello from hooks!'")

        async for msg in client.receive_response():
            display_message(msg)


async def example_userpromptsubmit() -> None:
    """Demonstrate UserPromptSubmit hook that adds context."""
    print("\n=== UserPromptSubmit Example ===")
    print("This example shows how to inject context via UserPromptSubmit.\n")

    options = ClaudeAgentOptions(
        hooks={
            "UserPromptSubmit": [
                HookMatcher(matcher=None, hooks=[add_custom_instructions]),
            ],
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("What is 2 + 2?")

        async for msg in client.receive_response():
            display_message(msg)


async def example_posttooluse() -> None:
    """Demonstrate PostToolUse hook that reviews output."""
    print("\n=== PostToolUse Example ===")
    print("This example shows how PostToolUse can review tool output.\n")

    options = ClaudeAgentOptions(
        allowed_tools=["Bash"],
        hooks={
            "PostToolUse": [
                HookMatcher(matcher="Bash", hooks=[review_tool_output]),
            ],
        }
    )

    async with ClaudeSDKClient(options=options) as client:
        print("Running a command that will produce an error...")
        await client.query("Run: ls /nonexistent_directory_12345")

        async for msg in client.receive_response():
            display_message(msg)


async def main():
    """Run all hook examples."""
    print("=" * 60)
    print("Claude Agent SDK - Hooks Examples")
    print("=" * 60)

    await example_pretooluse()
    await example_userpromptsubmit()
    await example_posttooluse()


if __name__ == "__main__":
    asyncio.run(main())
