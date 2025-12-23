#!/usr/bin/env python3
"""
Modern approach: Agent-driven with automatic skill invocation.

This example shows how Claude automatically uses skills and MCP tools
when configured correctly. Natural language prompts trigger intelligent
tool selection and multi-step workflows.

Useful for: User interaction, natural language, adaptive workflows.
"""

import asyncio
import json
import os
from pathlib import Path


async def example_1_task_management():
    """Example 1: Creating and managing tasks with natural language."""
    print("\n" + "=" * 70)
    print("Example 1: Task Creation and Management")
    print("=" * 70)

    prompt = """
    Create a project called "Q4 Launch" and add these tasks:
    1. Finalize design mockups (high priority, due Dec 24)
    2. Implement backend API (high priority, due Dec 27)
    3. Frontend integration (medium priority, due Dec 29)
    4. QA and testing (high priority, due Dec 31)

    Then show me all the high-priority tasks for this project.
    """

    print("\nUser Request:")
    print(prompt)

    print("\nWhat happens with skill:")
    print("""
1. Claude detects: "task-organizer" skill matches this request
2. Skill provides guidance on available operations
3. Claude decides to:
   - Use create_project tool
   - Use create_task tool (4 times)
   - Use filter_tasks tool
4. MCP server executes each operation
5. Claude formats and returns results

Result: Project created with 4 organized tasks
""")


async def example_2_search_and_filter():
    """Example 2: Searching and filtering with natural language."""
    print("\n" + "=" * 70)
    print("Example 2: Intelligent Search and Filtering")
    print("=" * 70)

    prompt = """
    Find all overdue tasks that are high priority or blocked.
    Group them by project and show me what needs attention first.
    """

    print("\nUser Request:")
    print(prompt)

    print("\nWhat happens with skill:")
    print("""
1. Claude detects: "task-organizer" skill matches
2. Skill explains available filters and searches
3. Claude decides to:
   - Use get_overdue_tasks tool
   - Use filter_tasks for priority and status
   - Post-process results to group by project
4. Claude intelligently presents findings

Result: Prioritized list of blocked/overdue work
""")


async def example_3_analytics():
    """Example 3: Analytics and insights."""
    print("\n" + "=" * 70)
    print("Example 3: Analytics and Productivity Insights")
    print("=" * 70)

    prompt = """
    Give me a productivity summary:
    - What's my completion rate?
    - How many tasks are overdue?
    - What are my top 3 priorities this week?
    - Any projects falling behind?
    """

    print("\nUser Request:")
    print(prompt)

    print("\nWhat happens with skill:")
    print("""
1. Claude detects: "task-organizer" skill matches
2. Skill provides analytics capabilities
3. Claude decides to:
   - Use task_statistics tool
   - Use get_overdue_tasks tool
   - Use filter_tasks with priority filter
   - Use list_projects and check progress
4. Claude synthesizes data into insights

Result: Comprehensive productivity report
""")


async def example_4_multi_step_workflow():
    """Example 4: Complex multi-step workflows."""
    print("\n" + "=" * 70)
    print("Example 4: Complex Workflow Automation")
    print("=" * 70)

    prompt = """
    I'm starting a new feature project. Please:
    1. Create project "User Authentication Improvements"
    2. Create tasks for: design, implementation, testing, documentation
    3. Set authentication tasks to high priority with Dec 26 deadline
    4. Add 'security' tag to all tasks
    5. Show me the project summary
    """

    print("\nUser Request:")
    print(prompt)

    print("\nWhat happens with skill:")
    print("""
1. Claude detects: "task-organizer" skill
2. Skill provides all necessary operations
3. Claude chains multiple operations:
   - create_project (1x)
   - create_task (4x)
   - update_task (4x for priority/date)
   - add_tag (4x)
   - list_tasks (for project summary)
4. Each operation depends on previous results

Result: Complete project with organized, tagged tasks
""")


async def show_skill_configuration():
    """Show how skills are configured in the SDK."""
    print("\n" + "=" * 70)
    print("How Skills Work in the Agent SDK")
    print("=" * 70)

    print("""
Configuration needed:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/agent-patterns",        # Project with .claude/skills/
    setting_sources=["project"],          # Load skills from filesystem
    allowed_tools=["Skill", "mcp__task-manager__*"],
    mcp_servers={
        "task-manager": task_manager_server
    }
)

# Claude automatically invokes skills
async for message in query(
    prompt="Create a task to review the PR",
    options=options
):
    print(message)
```

Key points:
✓ settingSources=["project"] loads .claude/skills/
✓ "Skill" in allowedTools enables skill invocation
✓ Natural language triggers skill matching
✓ MCP tools automatically available to skill
✓ Claude chains multiple tool calls as needed
""")


async def show_token_efficiency():
    """Show token efficiency of skill-based approach."""
    print("\n" + "=" * 70)
    print("Token Efficiency Analysis")
    print("=" * 70)

    print("""
Request: "Create a high-priority task for PR review with Dec 23 deadline"

Token Usage Breakdown:

1. Initial Prompt: ~200 tokens
   - User request
   - Skill description loaded
   - MCP tools available

2. Tool Call: ~100 tokens
   - Claude decides: use create_task
   - Parameters filled

3. Tool Result: ~50 tokens
   - Response from MCP server
   - Task confirmation

4. Formatting: ~50 tokens
   - Claude presents result

Total: ~400 tokens

Efficiency vs traditional:
- Traditional: ~200 tokens (direct tool call, no reasoning)
- With skill: ~400 tokens (includes model reasoning)
- Trade-off: +200 tokens for natural language + intelligence

For complex workflows, skill approach saves tokens by:
- Reducing multi-step prompting
- Automatic tool chaining
- Single-turn completion of complex tasks
""")


async def show_auto_invocation():
    """Show how skill auto-invocation works."""
    print("\n" + "=" * 70)
    print("Automatic Skill Invocation")
    print("=" * 70)

    print("""
The task-organizer skill activates when you mention:
  ✓ "Create a task..."
  ✓ "Add a task..."
  ✓ "Show my tasks"
  ✓ "Mark task complete"
  ✓ "Create a project..."
  ✓ "Organize my work"
  ✓ "What tasks are overdue?"
  ✓ "What's my completion rate?"
  ✓ "Filter tasks by..."
  ✓ And many more variations!

The skill describes when to use it:
"Manage tasks, projects, and tags using a SQLite-backed task management
system. Use for task creation, project planning, todo lists, task tracking,
and productivity workflows."

Claude matches your request against this description and automatically
enables the skill if it's relevant.

NO explicit activation needed:
❌ Don't do: /skill task-organizer create_task ...
✅ Just say: Create a task to review the PR
""")


async def show_vs_without_skill():
    """Contrast with approach without skills."""
    print("\n" + "=" * 70)
    print("WITH Skill vs WITHOUT Skill")
    print("=" * 70)

    print("""
Request: "Create a project with 5 tasks, add tags, then show me high-priority ones"

WITHOUT Skill (Manual tool calls):
────────────────────────────────────
# You must write the logic
1. call create_project
2. call create_task (5 times)
3. call add_tag (multiple times)
4. call filter_tasks with priority=high
5. Post-process and format results

Code: ~50 lines of boilerplate
Control: Complete but verbose

WITH Skill (Agent-driven):
──────────────────────────
# One natural language request
query("Create a project with 5 tasks, add tags, show high-priority ones")

Code: ~5 lines
Control: Intelligent and adaptive
""")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 70)
    print("Agent SDK with Skills: Task Manager Examples")
    print("=" * 70)

    await example_1_task_management()
    await example_2_search_and_filter()
    await example_3_analytics()
    await example_4_multi_step_workflow()
    await show_skill_configuration()
    await show_token_efficiency()
    await show_auto_invocation()
    await show_vs_without_skill()

    print("\n" + "=" * 70)
    print("Summary: Skills + MCP = Intelligent Task Management")
    print("=" * 70)
    print("""
Key Benefits:
  ✓ Natural language interface
  ✓ Automatic tool selection
  ✓ Multi-step workflows
  ✓ No boilerplate code
  ✓ Adaptive to requests
  ✓ Self-documenting (skill descriptions)

To try this yourself:
  1. Install claude-agent-sdk
  2. Register the MCP server
  3. Use the SDK with skill configuration
  4. Write natural language prompts
  5. Claude handles the rest!
""")


if __name__ == "__main__":
    asyncio.run(main())
