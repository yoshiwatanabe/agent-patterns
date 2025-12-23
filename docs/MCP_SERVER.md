# MCP Server Architecture Guide

## Overview

The task-manager MCP server is built with FastMCP, providing a comprehensive task management system with 35+ tools, 5 resources, and 4 prompts.

## Architecture

### Three Core Components

#### 1. Tools (35+)

Functions that perform operations. Available for Claude to call.

**Task Tools**:
- `create_task` - Create new task with title, description, priority, due date
- `get_task` - Retrieve task by ID with tags
- `list_tasks` - List all tasks with pagination
- `update_task` - Update task fields (status, priority, etc.)
- `delete_task` - Delete a task
- `search_tasks` - Full-text search across titles/descriptions
- `filter_tasks` - Filter by status, priority, project, tags

**Project Tools**:
- `create_project` - Create new project
- `get_project` - Get project details
- `list_projects` - List all projects
- `update_project` - Update project info
- `delete_project` - Delete project
- `get_project_tasks` - Get tasks for a project

**Tag Tools**:
- `add_tag` - Add tag to task
- `remove_tag` - Remove tag from task
- `list_tags` - List all available tags

**Analytics Tools**:
- `task_statistics` - Get task counts and completion rate
- `get_overdue_tasks` - Get overdue task list

#### 2. Resources (5)

Read-only data structures. Cached and referenced via `@server:resource://path`

- `task://all` - All tasks
- `task://pending` - Pending tasks only
- `task://high-priority` - High-priority tasks
- `project://all` - All projects
- `stats://summary` - Statistics summary

#### 3. Prompts (4 Workflows)

Pre-written workflow templates that encode complex procedures.

- `daily-review` - Daily task review prompt
- `weekly-planning` - Weekly planning workflow
- `project-summary` - Project status summary
- `overdue-analysis` - Overdue task analysis

## Database Schema

### Tables

- **tasks** - Task records with status, priority, due dates
- **projects** - Project definitions
- **tags** - Tag catalog
- **task_tags** - Many-to-many relationship

### Indexes

- task status, priority, due_date
- Full-text search (FTS5) on task titles/descriptions
- Project and tag relationships

## Implementation Details

### FastMCP Decorators

```python
@mcp.tool()
async def create_task(...):
    """Tool description"""
    
@mcp.resource("task://all")
async def all_tasks_resource():
    """Resource description"""

@mcp.prompt()
async def daily_review():
    """Prompt description"""
```

### Database Access

All operations go through `DatabaseManager` class:
- Async SQLite with aiosqlite
- Connection pooling
- Error handling and logging
- Transaction management

### Error Handling

- Try/except around all operations
- Logging to stderr (important for STDIO protocol)
- JSON error messages returned to Claude
- Graceful degradation

## Running the Server

```bash
# Development
python -m task_manager_mcp.server

# Production
python -c "from task_manager_mcp.server import main; asyncio.run(main())"

# With environment
export DATABASE_PATH=tasks.db
python -m task_manager_mcp.server
```

## Integration Points

- Claude Code: Register with `claude mcp add`
- Agent SDK: Include in mcpServers config
- Custom apps: Use JSON-RPC over stdio

## Performance Considerations

- Database indexes for fast queries
- Pagination support (limit/offset)
- Full-text search with FTS5
- Async operations throughout
- Logging to stderr (not stdout)

See full implementation in `../mcp-server/src/task_manager_mcp/`
