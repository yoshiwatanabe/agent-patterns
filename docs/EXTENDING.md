# Extending the System

This guide shows how to add new features to the agent-patterns project.

## Adding New MCP Tools

### Step 1: Add to database.py

Implement the operation in `DatabaseManager`:

```python
async def your_operation(self, param1: str) -> dict:
    """Your operation description."""
    try:
        # Your implementation
        result = ...
        return result
    except Exception as e:
        logger.error(f"Error: {e}")
        raise
```

### Step 2: Add to server.py

Create a tool with the decorator:

```python
@mcp.tool()
async def your_tool(param1: str) -> str:
    """Tool description for Claude."""
    try:
        result = await db_manager.your_operation(param1)
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"
```

### Step 3: Update Skill

Add to `.claude/skills/task-organizer/SKILL.md`:

```markdown
- **Your Operation**: Description of what it does
```

### Step 4: Test

```python
# Test directly
result = await db_manager.your_operation("test")

# Test via MCP
result = await mcp.call_tool("mcp__task-manager__your_tool", ...)

# Test via skill
# "Natural language request using your new feature"
```

---

## Adding New Resources

### Step 1: Implement in server.py

```python
@mcp.resource("task://your-resource")
async def your_resource() -> str:
    """Resource description."""
    try:
        data = await db_manager.get_data()
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"
```

### Step 2: Document in Skill

```markdown
## Resources Available

- `task://your-resource` - Description
```

### Step 3: Use in Skill

Reference resources in skill descriptions.

---

## Adding New Prompts

### Step 1: Implement in server.py

```python
@mcp.prompt()
async def your_workflow() -> str:
    """Prompt description."""
    data = await db_manager.get_data()
    
    prompt = f"""# Your Workflow

Description of what to do.

Data: {data}
"""
    return prompt
```

### Step 2: Reference in Skill

```markdown
## Workflows

- Use `/mcp__task-manager__your_workflow` for your workflow
```

---

## Creating New Skills

### Step 1: Create Directory

```bash
mkdir .claude/skills/new-skill
```

### Step 2: Create SKILL.md

```yaml
---
name: new-skill
description: "What it does and when to use it"
---

# New Skill

## Overview
Description

## When to Use
- Scenario 1
- Scenario 2

## Available Operations
- Operation 1
- Operation 2
```

### Step 3: Test with SDK

```python
options = ClaudeAgentOptions(
    setting_sources=["project"],
    allowed_tools=["Skill"],
)

async for msg in query("Request that should activate new skill", options):
    print(msg)
```

---

## Extending Database Schema

### Step 1: Backup Current Data

```bash
cp tasks.db tasks.db.backup
```

### Step 2: Add Migration

Update `schema.sql`:

```sql
-- Add new table
CREATE TABLE IF NOT EXISTS new_table (
    id INTEGER PRIMARY KEY,
    ...
);

-- Add new index
CREATE INDEX idx_new ON new_table(...);
```

### Step 3: Reinitialize

Database will auto-create schema on next run.

### Step 4: Add Operations

Add methods to `DatabaseManager` for new table operations.

---

## Adding New Patterns

### Step 1: Document in PATTERNS_CATALOG.md

Add new pattern section with:
- Overview
- Diagram
- When to use
- Characteristics
- Pros/cons
- Examples

### Step 2: Create Example

Add reference implementation:
- MCP server example
- Skill example
- SDK integration example

### Step 3: Add to Comparison

Update comparison matrix and decision tree.

---

## Performance Optimization

### Add Indexes

For frequent queries:

```sql
CREATE INDEX idx_name ON table(column);
```

### Implement Caching

For read-heavy operations:

```python
self.cache = {}
self.cache_ttl = 300  # 5 minutes

# Get with cache
if key in self.cache:
    timestamp = self.cache[key][1]
    if time.time() - timestamp < self.cache_ttl:
        return self.cache[key][0]
```

### Pagination

For large result sets:

```python
async def list_items(self, limit: int = 50, offset: int = 0):
    # Use LIMIT and OFFSET in query
```

---

## Testing

### Unit Tests

```python
# tests/test_operations.py
import pytest

@pytest.mark.asyncio
async def test_your_operation():
    db = DatabaseManager()
    await db.initialize()
    
    result = await db.your_operation("test")
    
    assert result is not None
    assert result["field"] == "expected"
    
    await db.close()
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_tool_via_mcp():
    # Test tool invocation through MCP
    result = await mcp.invoke_tool("your_tool", {...})
    # Assertions
```

### Manual Testing

```bash
# Start server
python -m task_manager_mcp.server

# In another terminal
curl -X POST http://localhost:9999/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "your_tool", "params": {...}}'
```

---

## Documentation Updates

When adding features:

1. Update relevant doc in `docs/`
2. Add examples to `EXAMPLES.md`
3. Update `PATTERNS_CATALOG.md` if pattern-related
4. Update `README.md` if major feature
5. Add to this EXTENDING.md

---

## Common Extension Examples

### Add Priority Levels

**Database**: Add priority validation
**Tool**: create_task accepts priority param
**Skill**: Document priority options
**Example**: "Create high-priority task"

### Add Recurring Tasks

**Database**: Add recurrence field
**Operations**: Generate recurring instances
**Tool**: create_recurring_task
**Skill**: Document recurrence syntax

### Add Tags Hierarchy

**Database**: Add parent_tag_id
**Operations**: Support hierarchical queries
**Tool**: get_tags_tree
**Skill**: Document tag organization

### Add Time Tracking

**Database**: Add time_spent field
**Operations**: Track cumulative time
**Tool**: log_time_spent
**Analytics**: Report by time tracked

---

## Troubleshooting Extensions

### Problem: Skill Not Activating

- Check skill description includes keywords
- Verify `.claude/skills/` directory structure
- Check SKILL.md format (YAML frontmatter)
- Test with SDK using `setting_sources=["project"]`

### Problem: MCP Tool Not Working

- Check tool appears in `server.py`
- Verify decorator `@mcp.tool()`
- Check tool name format: `mcp__server__tool`
- Verify function signature matches

### Problem: Database Migration Issues

- Backup data first
- Schema is auto-applied on next run
- Check migrations are additive (don't modify existing)
- Test in development first

---

## Best Practices

### Code Quality
- Follow existing patterns
- Add type hints
- Include docstrings
- Handle errors gracefully

### Testing
- Write tests for new operations
- Test both success and failure paths
- Test via MCP and skill layers

### Documentation
- Document new features
- Add examples
- Update decision matrices
- Keep this file updated

### Performance
- Consider indexes for new queries
- Use pagination for large results
- Implement caching where appropriate
- Monitor response times

---

For more information, see the main documentation files:
- [PATTERNS_CATALOG.md](PATTERNS_CATALOG.md) - Pattern reference
- [MCP_SERVER.md](MCP_SERVER.md) - Server architecture
- [SKILL_GUIDE.md](SKILL_GUIDE.md) - Skill development
- [EXAMPLES.md](EXAMPLES.md) - Real-world examples
