/**
 * Claude Agent SDK - Quick Start Example (TypeScript)
 *
 * This example demonstrates basic usage of the Claude Agent SDK in TypeScript.
 */

import {
  query,
  type ClaudeAgentOptions,
  type Message,
} from "@anthropic-ai/claude-agent-sdk";

/**
 * Basic query without options.
 */
async function simpleQuery(): Promise<void> {
  console.log("=== Simple Query ===\n");

  const stream = query({ prompt: "What is 2 + 2?" });

  for await (const message of stream) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if (block.type === "text") {
          console.log(block.text);
        }
      }
    } else if (message.type === "result") {
      console.log(`\n[Completed: ${message.subtype}]`);
    }
  }
}

/**
 * Query with custom options.
 */
async function queryWithOptions(): Promise<void> {
  console.log("\n=== Query with Options ===\n");

  const options: ClaudeAgentOptions = {
    systemPrompt: "You are a helpful TypeScript expert. Be concise.",
    maxTurns: 3,
  };

  const stream = query({
    prompt: "Write a function to calculate factorial",
    options,
  });

  for await (const message of stream) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if (block.type === "text") {
          console.log(block.text);
        }
      }
    }
  }
}

/**
 * Query with tool access enabled.
 */
async function queryWithTools(): Promise<void> {
  console.log("\n=== Query with Tools ===\n");

  const options: ClaudeAgentOptions = {
    systemPrompt: "You are a file system assistant.",
    allowedTools: ["Read", "Glob", "Grep"],
    permissionMode: "acceptEdits",
    cwd: ".", // Current directory
  };

  const stream = query({
    prompt: "List all TypeScript files in the current directory",
    options,
  });

  for await (const message of stream) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if (block.type === "text") {
          console.log(block.text);
        } else if (block.type === "tool_use") {
          console.log(`[Using tool: ${block.name}]`);
        }
      }
    }
  }
}

/**
 * Stream output as it arrives.
 */
async function streamingOutput(): Promise<void> {
  console.log("\n=== Streaming Output ===\n");

  const options: ClaudeAgentOptions = {
    systemPrompt: "You are a storyteller. Write short stories.",
  };

  const stream = query({
    prompt: "Write a very short story about a robot (2-3 sentences)",
    options,
  });

  for await (const message of stream) {
    if (message.type === "assistant") {
      for (const block of message.message.content) {
        if (block.type === "text") {
          // Write without newline for streaming effect
          process.stdout.write(block.text);
        }
      }
    }
  }

  console.log(); // Final newline
}

/**
 * Run all examples.
 */
async function main(): Promise<void> {
  try {
    await simpleQuery();
    await queryWithOptions();
    await queryWithTools();
    await streamingOutput();
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
