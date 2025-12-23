#!/usr/bin/env ts-node
/**
 * Modern approach: Agent-driven with automatic skill invocation.
 *
 * This example shows how Claude automatically uses skills and MCP tools
 * when configured correctly. Natural language prompts trigger intelligent
 * tool selection and multi-step workflows.
 *
 * Useful for: User interaction, natural language, adaptive workflows.
 */

async function example1TaskManagement(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Example 1: Task Creation and Management");
  console.log("=".repeat(70));

  const prompt = `
    Create a project called "Q4 Launch" and add these tasks:
    1. Finalize design mockups (high priority, due Dec 24)
    2. Implement backend API (high priority, due Dec 27)
    3. Frontend integration (medium priority, due Dec 29)
    4. QA and testing (high priority, due Dec 31)

    Then show me all the high-priority tasks for this project.
    `;

  console.log("\nUser Request:");
  console.log(prompt);

  console.log("\nWhat happens with skill:");
  console.log(`
1. Claude detects: "task-organizer" skill matches this request
2. Skill provides guidance on available operations
3. Claude decides to:
   - Use create_project tool
   - Use create_task tool (4 times)
   - Use filter_tasks tool
4. MCP server executes each operation
5. Claude formats and returns results

Result: Project created with 4 organized tasks
  `);
}

async function example2SearchAndFilter(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Example 2: Intelligent Search and Filtering");
  console.log("=".repeat(70));

  const prompt = `
    Find all overdue tasks that are high priority or blocked.
    Group them by project and show me what needs attention first.
    `;

  console.log("\nUser Request:");
  console.log(prompt);

  console.log("\nWhat happens with skill:");
  console.log(`
1. Claude detects: "task-organizer" skill matches
2. Skill explains available filters and searches
3. Claude decides to:
   - Use get_overdue_tasks tool
   - Use filter_tasks for priority and status
   - Post-process results to group by project
4. Claude intelligently presents findings

Result: Prioritized list of blocked/overdue work
  `);
}

async function example3Analytics(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Example 3: Analytics and Productivity Insights");
  console.log("=".repeat(70));

  const prompt = `
    Give me a productivity summary:
    - What's my completion rate?
    - How many tasks are overdue?
    - What are my top 3 priorities this week?
    - Any projects falling behind?
    `;

  console.log("\nUser Request:");
  console.log(prompt);

  console.log("\nWhat happens with skill:");
  console.log(`
1. Claude detects: "task-organizer" skill matches
2. Skill provides analytics capabilities
3. Claude decides to:
   - Use task_statistics tool
   - Use get_overdue_tasks tool
   - Use filter_tasks with priority filter
   - Use list_projects and check progress
4. Claude synthesizes data into insights

Result: Comprehensive productivity report
  `);
}

async function example4MultiStepWorkflow(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Example 4: Complex Workflow Automation");
  console.log("=".repeat(70));

  const prompt = `
    I'm starting a new feature project. Please:
    1. Create project "User Authentication Improvements"
    2. Create tasks for: design, implementation, testing, documentation
    3. Set authentication tasks to high priority with Dec 26 deadline
    4. Add 'security' tag to all tasks
    5. Show me the project summary
    `;

  console.log("\nUser Request:");
  console.log(prompt);

  console.log("\nWhat happens with skill:");
  console.log(`
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
  `);
}

async function showSkillConfiguration(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("How Skills Work in the Agent SDK");
  console.log("=".repeat(70));

  console.log(`
Configuration needed:

\`\`\`typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Create a task to review the PR",
  options: {
    cwd: "/path/to/agent-patterns",      // Project with .claude/skills/
    settingSources: ["project"],         // Load skills from filesystem
    allowedTools: ["Skill", "mcp__task-manager__*"],
    mcpServers: {
      "task-manager": taskManagerServer
    }
  }
})) {
  console.log(message);
}
\`\`\`

Key points:
✓ settingSources=["project"] loads .claude/skills/
✓ "Skill" in allowedTools enables skill invocation
✓ Natural language triggers skill matching
✓ MCP tools automatically available to skill
✓ Claude chains multiple tool calls as needed
  `);
}

async function showTokenEfficiency(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Token Efficiency Analysis");
  console.log("=".repeat(70));

  console.log(`
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
  `);
}

async function showAutoInvocation(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Automatic Skill Invocation");
  console.log("=".repeat(70));

  console.log(`
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
  `);
}

async function showVsWithoutSkill(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("WITH Skill vs WITHOUT Skill");
  console.log("=".repeat(70));

  console.log(`
Request: "Create a project with 5 tasks, add tags, then show me high-priority ones"

WITHOUT Skill (Manual tool calls):
────────────────────────────────────
// You must write the logic
1. call create_project
2. call create_task (5 times)
3. call add_tag (multiple times)
4. call filter_tasks with priority=high
5. Post-process and format results

Code: ~50 lines of boilerplate
Control: Complete but verbose

WITH Skill (Agent-driven):
──────────────────────────
// One natural language request
query("Create a project with 5 tasks, add tags, show high-priority ones")

Code: ~5 lines
Control: Intelligent and adaptive
  `);
}

async function main(): Promise<void> {
  console.log("\n" + "=".repeat(70));
  console.log("Agent SDK with Skills: Task Manager Examples");
  console.log("=".repeat(70));

  await example1TaskManagement();
  await example2SearchAndFilter();
  await example3Analytics();
  await example4MultiStepWorkflow();
  await showSkillConfiguration();
  await showTokenEfficiency();
  await showAutoInvocation();
  await showVsWithoutSkill();

  console.log("\n" + "=".repeat(70));
  console.log("Summary: Skills + MCP = Intelligent Task Management");
  console.log("=".repeat(70));
  console.log(`
Key Benefits:
  ✓ Natural language interface
  ✓ Automatic tool selection
  ✓ Multi-step workflows
  ✓ No boilerplate code
  ✓ Adaptive to requests
  ✓ Self-documenting (skill descriptions)

To try this yourself:
  1. Install @anthropic-ai/claude-agent-sdk
  2. Register the MCP server
  3. Use the SDK with skill configuration
  4. Write natural language prompts
  5. Claude handles the rest!
  `);
}

main().catch(console.error);
