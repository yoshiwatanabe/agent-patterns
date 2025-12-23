#!/usr/bin/env ts-node
/**
 * Traditional approach: Direct MCP tool invocation without skills.
 *
 * This example shows how to explicitly call MCP tools programmatically
 * using the Claude Agent SDK.
 *
 * Useful for: Full control, specific tool invocation, non-agent workflows.
 */

async function demoTraditionalMCP(): Promise<void> {
  console.log("=== Traditional MCP Usage (Explicit Tool Calls) ===\n");

  console.log("Scenario: Explicitly managing tasks without agent assistance\n");

  // Pseudo-code showing the pattern:
  console.log("Example 1: Create a task");
  console.log("Code:");
  console.log(`
const taskResult = await agent.callTool(
  "mcp__task-manager__create_task",
  {
    title: "Review authentication PR",
    priority: "high",
    due_date: "2025-12-23"
  }
);
// Developer explicitly controls which tool is called
// No automatic skill invocation
// More control but requires knowing tool names
  `);

  console.log("\nExample 2: List all tasks");
  console.log("Code:");
  console.log(`
const tasksResult = await agent.callTool(
  "mcp__task-manager__list_tasks",
  { limit: 50, offset: 0 }
);
// Must explicitly specify tool and parameters
// No intelligence about what the user wants
// Useful for scripted/automated workflows
  `);

  console.log("\nExample 3: Filter high-priority tasks");
  console.log("Code:");
  console.log(`
const filteredResult = await agent.callTool(
  "mcp__task-manager__filter_tasks",
  { priority: "high", status: "pending" }
);
// Developer must know which filters exist
// Explicit control over all parameters
  `);

  console.log("\n=== Characteristics of Traditional Approach ===");
  console.log(`
✅ Pros:
  - Full control over tool invocation
  - Predictable behavior
  - Good for scripted/automated workflows
  - No overhead from model reasoning
  - Efficient for known workflows

❌ Cons:
  - Must know tool names and parameters
  - No automatic intelligence
  - Verbose code for complex workflows
  - Harder to adapt to new requirements
  - Requires documentation lookup

💡 Use Case: Traditional approach when you have:
  - Known, fixed workflows
  - Automated scheduled tasks
  - Direct integration with other systems
  - Need for precise control
  - Performance-critical operations
  `);

  console.log("\n=== Token Efficiency ===");
  console.log(`
Typical Token Usage:
  - Prompt size: Small (~100-500 tokens for tool call)
  - No context needed from model
  - No tool discovery overhead
  - Minimal context for each call

Example workflow token cost: ~200-500 tokens per operation
  `);

  console.log("\n=== When to Avoid Traditional Approach ===");
  console.log(`
❌ Don't use if you need:
  - Natural language interaction
  - Intelligent tool selection
  - Adaptive workflows based on content
  - Multi-step reasoning
  - User-friendly interface
  `);
}

async function demoVsAgentDriven(): Promise<void> {
  console.log("\n\n=== COMPARISON: Traditional vs Agent-Driven ===\n");

  console.log("Scenario: 'Help me organize my high-priority tasks for this week'\n");

  console.log("Traditional Approach:");
  console.log(`
// Developer must parse the request manually
const request = "Help me organize my high-priority tasks for this week";

// Explicit steps:
1. Call list_tasks
2. Filter results for high-priority
3. Filter results for tasks due this week
4. Format and display

// Code is prescriptive about steps
const tasks = await agent.callTool("mcp__task-manager__filter_tasks", {
  priority: "high"
});
// Then manually post-process for "this week"
  `);

  console.log("\nAgent-Driven Approach (with skill):");
  console.log(`
// Natural language, model figures out steps
const request = "Help me organize my high-priority tasks for this week";

// Claude automatically:
1. Recognizes task-organizer skill matches
2. Uses skill guidance
3. Decides which tools to call
4. Chains calls if needed
5. Provides formatted response

// Code is declarative (what you want, not how)
for await (const message of query({
  prompt: request,
  options: { ... }
})) {
  console.log(message);
}
  `);

  console.log("\nKey Differences:");
  console.log(`
┌──────────────────┬─────────────────┬────────────────────┐
│ Aspect           │ Traditional     │ Agent-Driven       │
├──────────────────┼─────────────────┼────────────────────┤
│ Control          │ Full (explicit) │ Shared (intelligent)
│ Complexity       │ Low             │ Medium             │
│ Flexibility      │ Low             │ High               │
│ Token cost       │ Very low        │ Low-Medium         │
│ User friendliness│ Poor            │ Excellent          │
│ Best for         │ Scripted tasks  │ User interaction   │
└──────────────────┴─────────────────┴────────────────────┘
  `);
}

async function main(): Promise<void> {
  await demoTraditionalMCP();
  await demoVsAgentDriven();

  console.log("\n" + "=".repeat(60));
  console.log("To see the agent-driven approach with skills, see: with_skill.ts");
  console.log("=".repeat(60));
}

main().catch(console.error);
