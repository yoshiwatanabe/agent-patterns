# Real-World Usage Examples

## Example 1: Daily Standup Assistant

**Goal**: Provide team status using task completion data

**Request**:
```
"Give me a daily standup report with completion metrics and blockers"
```

**What Happens**:
1. Skill activates (recognizes daily/report/metrics)
2. Claude calls `task_statistics` → gets completion rate
3. Claude calls `get_overdue_tasks` → finds blockers
4. Claude calls `list_projects` → project progress
5. Claude synthesizes into readable report

**Result**: Formatted standup report ready to share

**Token Cost**: ~800 tokens

---

## Example 2: Sprint Planning

**Goal**: Plan upcoming sprint with organized tasks

**Request**:
```
"Create sprint for Q1 launch: design (5 tasks), development (8 tasks), 
testing (3 tasks). Set all to high priority, due date Jan 31."
```

**What Happens**:
1. Skill activates
2. Claude creates project "Q1 Launch"
3. Claude creates 16 tasks total
4. Claude updates all to high priority with due date
5. Claude organizes by tags (design/dev/testing)

**Result**: Organized sprint ready to execute

**Token Cost**: ~1200 tokens

---

## Example 3: Search-Based Triage

**Goal**: Find and organize specific work items

**Request**:
```
"Find all authentication-related tasks that are high priority or blocked.
Group by project and show what needs immediate attention."
```

**What Happens**:
1. Skill activates
2. Claude calls `search_tasks` with "authentication"
3. Claude calls `filter_tasks` for high priority
4. Claude calls `get_overdue_tasks`
5. Claude organizes results by project

**Result**: Prioritized task list for immediate action

**Token Cost**: ~900 tokens

---

## Example 4: Productivity Analytics

**Goal**: Understand team productivity trends

**Request**:
```
"What's our completion rate? How many tasks are overdue?
What are our top 3 focus areas this week?"
```

**What Happens**:
1. Skill activates
2. Claude calls `task_statistics` → completion rate, totals
3. Claude calls `get_overdue_tasks` → overdue count
4. Claude calls `filter_tasks` with various filters
5. Claude synthesizes into insights

**Result**: Comprehensive productivity report

**Token Cost**: ~1000 tokens

---

## Example 5: Automated Cleanup

**Goal**: Close completed work and cleanup database

**Request**: Via automated script
```python
# Traditional approach - direct tool calls
closed_tasks = await get_completed_tasks()
for task in closed_tasks:
    await mcp.call_tool("mcp__task-manager__delete_task", 
                       {"task_id": task.id})
```

**What Happens**:
1. Script directly calls `list_tasks` with status filter
2. Script directly calls `delete_task` for each
3. No Claude reasoning involved
4. Fast, predictable execution

**Token Cost**: ~200 tokens

---

## Example 6: Code Review Workflow

**Goal**: Track code review tasks as part of development workflow

**Request**:
```
"Create a project 'Authentication Refactor' with tasks:
- Code review (high priority, due tomorrow)
- Unit tests (high priority, due tomorrow)  
- Integration tests (medium, due in 2 days)
- Documentation (medium, due in 3 days)

Tag all with 'security' and 'review'."
```

**What Happens**:
1. Skill activates
2. Create project
3. Create 4 tasks with specific priorities/dates
4. Add tags to all

**Result**: Organized code review workflow

**Token Cost**: ~1100 tokens

---

## Example 7: Status Updates via Skill

**Goal**: Keep team informed of progress

**Request**:
```
"Mark the authentication PR review as complete and 
update the refactor project status."
```

**What Happens**:
1. Skill activates
2. Claude finds relevant task
3. Claude calls `update_task` with status=completed
4. Claude retrieves project progress

**Result**: Updated team tracking

**Token Cost**: ~600 tokens

---

## Example 8: Performance Optimization

**Goal**: Identify and track performance work

**Request**:
```
"Find all performance-related tasks, prioritize by 
impact, and create a quarterly roadmap."
```

**What Happens**:
1. Search for "performance"
2. Filter by status and priority
3. Analyze and organize results

**Result**: Performance roadmap

**Token Cost**: ~950 tokens

---

## Comparison: Skill vs Direct Calls

### With Skill (Natural Language)

```python
async for msg in query("Show me high-priority tasks due this week", 
                       options=options):
    print(msg)
# Result: Formatted list, ~800 tokens
```

### Without Skill (Direct Calls)

```python
tasks = await mcp.call_tool("mcp__task-manager__filter_tasks",
                            {"priority": "high"})
# Result: Raw JSON, ~150 tokens
```

**Trade-off**: More tokens for natural language and intelligence

---

## Best Practices

### 1. Use Skills for User-Facing

```python
# ✅ Good - natural language for users
"Help me organize my high-priority tasks"
```

### 2. Use Direct Calls for Automation

```python
# ✅ Good - explicit calls for scripts
await mcp.call_tool("mcp__task-manager__filter_tasks", ...)
```

### 3. Meaningful Requests

```python
# ✅ Good - clear intent
"Create a project for Q1 with weekly milestones"

# ❌ Bad - vague
"Do something with tasks"
```

### 4. Include Context

```python
# ✅ Good - provides context
"Create high-priority tasks for authentication review due tomorrow"

# ❌ Bad - missing details
"Create tasks"
```

---

## Common Patterns

### Pattern 1: Triage and Organize

Request: "Find [criteria], organize by [dimension]"
Tokens: ~900

### Pattern 2: Create and Configure

Request: "Create [project] with [tasks], [configuration]"
Tokens: ~1000-1200

### Pattern 3: Analyze and Report

Request: "Give me [metric], [breakdown]"
Tokens: ~1000

### Pattern 4: Update and Clean

Request: "Mark [items] as [status], [cleanup]"
Tokens: ~700

---

See the SDK examples in `../sdk-examples/` for executable code.
