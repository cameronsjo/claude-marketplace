/**
 * Claude Agent SDK - Custom Tools Example (TypeScript)
 *
 * This example demonstrates creating custom tools using in-process MCP servers.
 */

import {
  query,
  createSdkMcpServer,
  tool,
  type ClaudeAgentOptions,
  type ToolDefinition,
} from "@anthropic-ai/claude-agent-sdk";

// Define custom tools

const getCurrentTime = tool({
  name: "get_current_time",
  description: "Get the current date and time",
  inputSchema: {
    type: "object",
    properties: {},
    required: [],
  },
  execute: async () => {
    const now = new Date();
    return now.toISOString();
  },
});

const calculate = tool({
  name: "calculate",
  description: "Perform a mathematical calculation",
  inputSchema: {
    type: "object",
    properties: {
      expression: {
        type: "string",
        description: "Mathematical expression to evaluate (e.g., '2 + 2')",
      },
    },
    required: ["expression"],
  },
  execute: async (input: { expression: string }) => {
    const { expression } = input;

    // Safe evaluation - only allow numbers and basic operators
    const allowedChars = new Set("0123456789+-*/.() ".split(""));
    const isValid = [...expression].every((c) => allowedChars.has(c));

    if (!isValid) {
      return "Error: Expression contains invalid characters";
    }

    try {
      // Use Function constructor for safer eval
      const result = new Function(`return ${expression}`)();
      return `${expression} = ${result}`;
    } catch (error) {
      return `Error: ${error instanceof Error ? error.message : "Unknown error"}`;
    }
  },
});

const saveNote = tool({
  name: "save_note",
  description: "Save a note to the notes database",
  inputSchema: {
    type: "object",
    properties: {
      title: {
        type: "string",
        description: "Title of the note",
      },
      content: {
        type: "string",
        description: "Content of the note",
      },
    },
    required: ["title", "content"],
  },
  execute: async (input: { title: string; content: string }) => {
    const { title, content } = input;

    const note = {
      title,
      content,
      createdAt: new Date().toISOString(),
    };

    // In a real app, you'd save to a database
    console.log(`[Saving note: ${title}]`);

    return `Note '${title}' saved successfully`;
  },
});

const getWeather = tool({
  name: "get_weather",
  description: "Get weather information for a location",
  inputSchema: {
    type: "object",
    properties: {
      location: {
        type: "string",
        description: "City name or location",
      },
    },
    required: ["location"],
  },
  execute: async (input: { location: string }) => {
    const { location } = input;

    // Mock data - in production, call a real weather API
    const weatherData = {
      location,
      temperature: "72°F",
      condition: "Sunny",
      humidity: "45%",
    };

    return JSON.stringify(weatherData, null, 2);
  },
});

async function main(): Promise<void> {
  console.log("=== Custom Tools Example (TypeScript) ===\n");

  // Create an in-process MCP server with our custom tools
  const customServer = createSdkMcpServer({
    name: "my-tools",
    version: "1.0.0",
    tools: [getCurrentTime, calculate, saveNote, getWeather],
  });

  // Configure options with our custom tools
  const options: ClaudeAgentOptions = {
    systemPrompt: `You are a helpful assistant with access to custom tools.
Available tools:
- get_current_time: Get the current date and time
- calculate: Perform mathematical calculations
- save_note: Save notes to the database
- get_weather: Get weather for a location

Use these tools to help the user.`,
    mcpServers: [customServer],
    allowedTools: [
      "mcp__my-tools__get_current_time",
      "mcp__my-tools__calculate",
      "mcp__my-tools__save_note",
      "mcp__my-tools__get_weather",
    ],
    permissionMode: "acceptEdits",
  };

  // Test the custom tools
  const prompts = [
    "What time is it right now?",
    "Calculate 15 * 7 + 23",
    "Save a note titled 'Meeting' with content 'Team sync at 3pm'",
    "What's the weather in San Francisco?",
  ];

  for (const prompt of prompts) {
    console.log(`User: ${prompt}\n`);

    const stream = query({ prompt, options });

    for await (const message of stream) {
      if (message.type === "assistant") {
        for (const block of message.message.content) {
          if (block.type === "text") {
            console.log(`Assistant: ${block.text}`);
          } else if (block.type === "tool_use") {
            console.log(`[Tool: ${block.name}]`);
          }
        }
      } else if (message.type === "result") {
        console.log();
        break;
      }
    }

    console.log("-".repeat(40) + "\n");
  }
}

main().catch(console.error);
