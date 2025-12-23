# Claude Agent Skill Development Guide

## What is a Skill?

A Claude Agent skill is a YAML+Markdown file that describes a capability. When Claude sees a user request matching the skill's description, it automatically activates and uses available tools.

## Skill File Structure

**Location**: `.claude/skills/[skill-name]/SKILL.md`

```yaml
---
name: task-organizer              # Machine-readable name
description: "Full description..." # When to use this skill
---

# Skill Title

## Overview
What this skill does

## When to Use
- Specific scenarios
- Keywords that trigger activation

## Available Operations
- List of what can be done

## Examples
- Show how to use
```

## Key Elements

### 1. Name
- Lowercase with hyphens
- Unique identifier
- Max 64 characters

### 2. Description (Critical)
- 1-2 sentences
- Include BOTH what it does AND when to use it
- Include trigger keywords
- Max 1024 characters

**Bad**: "Helps with tasks"
**Good**: "Manage tasks and projects. Create, update, filter tasks. Use for task creation, project planning, todo lists, and productivity workflows."

### 3. Content
- Clear organization
- Step-by-step instructions
- Examples of usage
- Best practices
- Limitations

## Skill Activation

Claude activates your skill when:

1. **Description matches** - User request aligns with skill description
2. **Keywords present** - Request mentions relevant terms
3. **Context appropriate** - Situation fits documented use cases

## Best Practices

### Clear Descriptions

❌ Vague: "Manages stuff"
✅ Specific: "Manage tasks with status, priority, due dates, and tags"

### Include Keywords

Add words Claude will recognize:
- task, tasks, todo
- create, add, new
- update, modify, change
- priority, deadline, date
- project, organize

### Document Operations

List exactly what can be done:
- Create tasks
- Update status
- Filter by priority
- Search by keyword

### Provide Examples

Show concrete examples:
```
User: "Create a task for PR review"
→ Skill activates
→ Creates task with title "PR review"
```

### Limitations

Be honest about constraints:
- Can't access external systems
- Local storage only
- Single user
- Text-based interface

## Skill Design Patterns

### Pattern 1: CRUD Operations

```yaml
name: task-organizer
description: Create, read, update, delete tasks. Use for task management.
```

Covers all basic operations.

### Pattern 2: Workflow

```yaml
name: code-review-assistant
description: Guide code reviews with checklists and automation.
```

Guides a process.

### Pattern 3: Analysis

```yaml
name: data-analyzer
description: Analyze data and generate reports.
```

Performs analysis.

## Testing Skills

### Local Testing

1. Create `.claude/skills/test-skill/SKILL.md`
2. Use SDK with `setting_sources=["project"]`
3. Send requests that should activate it
4. Verify Claude mentions the skill

### What to Check

- Does skill activate? (Claude mentions it)
- Are tool calls correct?
- Does output match expectation?
- Any error handling needed?

## Common Patterns

### Task Management Skill

Activates on: "task", "todo", "create", "track", "prioritize"

### Code Review Skill

Activates on: "review", "code", "checklist", "standards"

### Data Analysis Skill

Activates on: "analyze", "data", "statistics", "report"

## Skill Organization

**Single Responsibility**: Each skill does one thing well

**Example Structure**:
- `task-organizer` - Task management
- `project-planner` - Project planning
- `analytics` - Statistics and reporting

Not: One "everything" skill

## Performance Considerations

- Skill loading is fast
- Multiple skills fine
- Clear descriptions speed up matching
- Too-generic descriptions confuse Claude

## Integration with MCP

Skill describes available tools. MCP provides them.

Example flow:
```
User: "Create a high-priority task"
     ↓
Skill activates (matches "create" + "task")
     ↓
Skill lists available operations
     ↓
Claude calls mcp__task-manager__create_task
     ↓
MCP server executes
     ↓
Result returned
```

See `../mcp-server/src/task_manager_mcp/` for tool implementation.
