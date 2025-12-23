# Claude Agent SDK Usage Guide

## Overview

The Claude Agent SDK enables you to embed Claude's intelligence into your applications with skills and MCP integration.

## Two Approaches

### Approach 1: Traditional (Direct Tool Calls)

```python
from claude_agent_sdk import agent

# Explicitly call specific tools
result = await agent.call_tool(
    "mcp__task-manager__create_task",
    {"title": "Review PR", "priority": "high"}
)
```

**Characteristics**:
- Full control
- Minimal tokens
- Predictable
- No intelligence

**Use for**: Automation scripts, internal tools

### Approach 2: Agent-Driven (with Skills)

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/agent-patterns",
    setting_sources=["project"],  # Load skills
    allowed_tools=["Skill", "mcp__task-manager__*"],
    mcp_servers={"task-manager": server}
)

# Natural language - Claude decides which tools to use
async for message in query(
    prompt="Create a task to review the PR",
    options=options
):
    print(message)
```

**Characteristics**:
- Natural language
- Automatic intelligence
- Flexible
- More tokens (includes reasoning)

**Use for**: User-facing systems

## Setting Up Skills

### Step 1: Create Skill File

```
.claude/skills/task-organizer/SKILL.md
```

### Step 2: Configure SDK

```python
options = ClaudeAgentOptions(
    cwd="/project/root",
    setting_sources=["project"],  # Loads .claude/skills/
    allowed_tools=["Skill", "mcp__task-manager__*"]
)
```

### Step 3: Use Natural Language

```python
async for msg in query("Create a task for PR review", options=options):
    print(msg)
```

## MCP Server Integration

### Register Server

```python
from task_manager_mcp.server import mcp

options = ClaudeAgentOptions(
    mcp_servers={
        "task-manager": mcp  # FastMCP server instance
    }
)
```

### Access Tools

```python
# Claude automatically has access to:
# - mcp__task-manager__create_task
# - mcp__task-manager__list_tasks
# - etc.
```

## Token Efficiency

| Approach | Tokens | Use Case |
|----------|--------|----------|
| Direct tool call | 100-200 | Automation |
| With skill | 600-1000 | User interaction |

Trade-off: More tokens for natural language interface and intelligence.

## Configuration Options

```python
ClaudeAgentOptions(
    cwd="/path/to/project",           # Project root
    setting_sources=["project"],      # Load from project skills
    allowed_tools=["Skill", ...],     # Which tools to allow
    mcp_servers={...},                # MCP servers to use
    model="claude-opus-4-5",          # Which model
    timeout=30,                       # Request timeout
)
```

## Full Example

See `../sdk-examples/python/with_skill.py` and `basic_mcp.py` for complete examples.

## Debugging

### Check Skills Loaded

```python
# Verify .claude/skills/ exists and has SKILL.md files
```

### Check Tool Access

```python
# Verify mcp_servers config
# Verify allowed_tools includes MCP tools
```

### Monitor Calls

```python
# Log which tools Claude decides to call
# Verify results match expectations
```
