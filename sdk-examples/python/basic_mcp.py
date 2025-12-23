#!/usr/bin/env python3
"""
Traditional approach: Direct MCP tool invocation without skills.

This example shows how to explicitly call MCP tools programmatically.
Useful for: Full control, specific tool invocation, non-agent workflows.
"""

import asyncio
import json
from typing import Any

# Note: This is a conceptual example. The actual Claude Agent SDK
# would be used with direct tool calls. Implementation depends on
# SDK version and capabilities.


async def demo_traditional_mcp() -> None:
    """Demonstrate traditional explicit MCP tool calling."""

    print("=== Traditional MCP Usage (Explicit Tool Calls) ===\n")

    # In a real implementation, you would:
    # 1. Initialize MCP client connection to task-manager server
    # 2. Call tools explicitly by name

    print("Scenario: Explicitly managing tasks without agent assistance\n")

    # Pseudo-code showing the pattern:
    print("Example 1: Create a task")
    print("Code:")
    print("""
task_result = await mcp_client.call_tool(
    "mcp__task-manager__create_task",
    {
        "title": "Review authentication PR",
        "priority": "high",
        "due_date": "2025-12-23"
    }
)
# Developer explicitly controls which tool is called
# No automatic skill invocation
# More control but requires knowing tool names
""")

    print("\nExample 2: List all tasks")
    print("Code:")
    print("""
tasks_result = await mcp_client.call_tool(
    "mcp__task-manager__list_tasks",
    {"limit": 50, "offset": 0}
)
# Must explicitly specify tool and parameters
# No intelligence about what the user wants
# Useful for scripted/automated workflows
""")

    print("\nExample 3: Filter high-priority tasks")
    print("Code:")
    print("""
filtered_result = await mcp_client.call_tool(
    "mcp__task-manager__filter_tasks",
    {"priority": "high", "status": "pending"}
)
# Developer must know which filters exist
# Explicit control over all parameters
""")

    print("\n=== Characteristics of Traditional Approach ===")
    print("""
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
""")

    print("\n=== Token Efficiency ===")
    print("""
Typical Token Usage:
  - Prompt size: Small (~100-500 tokens for tool call)
  - No context needed from model
  - No tool discovery overhead
  - Minimal context for each call

Example workflow token cost: ~200-500 tokens per operation
""")

    print("\n=== When to Avoid Traditional Approach ===")
    print("""
❌ Don't use if you need:
  - Natural language interaction
  - Intelligent tool selection
  - Adaptive workflows based on content
  - Multi-step reasoning
  - User-friendly interface
""")


async def demo_vs_agent_driven() -> None:
    """Show comparison with agent-driven approach."""

    print("\n\n=== COMPARISON: Traditional vs Agent-Driven ===\n")

    print("Scenario: 'Help me organize my high-priority tasks for this week'\n")

    print("Traditional Approach:")
    print("""
# Developer must parse the request manually
request = "Help me organize my high-priority tasks for this week"

# Explicit steps:
1. Call list_tasks
2. Filter results for high-priority
3. Filter results for tasks due this week
4. Format and display

# Code is prescriptive about steps
tasks = await mcp.call_tool("mcp__task-manager__filter_tasks",
    {"priority": "high"})
# Then manually post-process for "this week"
""")

    print("\nAgent-Driven Approach (with skill):")
    print("""
# Natural language, model figures out steps
request = "Help me organize my high-priority tasks for this week"

# Claude automatically:
1. Recognizes task-organizer skill matches
2. Uses skill guidance
3. Decides which tools to call
4. Chains calls if needed
5. Provides formatted response

# Code is declarative (what you want, not how)
for message in await query(prompt=request, options=...):
    print(message)
""")

    print("\nKey Differences:")
    print("""
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
""")


async def main() -> None:
    """Run demonstrations."""
    await demo_traditional_mcp()
    await demo_vs_agent_driven()

    print("\n" + "=" * 60)
    print("To see the agent-driven approach with skills, see: with_skill.py")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
