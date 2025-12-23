# Agent Patterns: MCP + Claude Skills Integration

A comprehensive learning project demonstrating patterns for integrating Model Context Protocol (MCP) servers with Claude Agent skills.

## 🎯 Purpose

Learn and understand different architectural patterns for combining MCP servers with Claude Agent skills. This project serves as both a reference implementation and a decision-making guide for building agent-based systems.

## 📚 Primary Deliverable

**[PATTERNS_CATALOG.md](docs/PATTERNS_CATALOG.md)** - Comprehensive reference guide with 14+ integration patterns, each with:
- Architecture diagrams
- Pros/cons analysis
- Complexity and token efficiency ratings
- Real-world use cases
- Decision frameworks
- Implementation guidance

## 🏗️ Project Structure

```
agent-patterns/
├── README.md                          # This file
├── .gitignore
│
├── mcp-server/                        # FastMCP Server Implementation
│   ├── pyproject.toml                 # Python project config
│   ├── src/task_manager_mcp/
│   │   ├── __init__.py
│   │   ├── server.py                  # MCP server with 35+ tools
│   │   ├── database.py                # SQLite operations
│   │   └── schema.sql                 # Database schema
│   └── tests/
│       └── test_server.py
│
├── .claude/
│   └── skills/
│       └── task-organizer/
│           └── SKILL.md               # Claude Agent skill definition
│
├── sdk-examples/
│   ├── python/
│   │   ├── requirements.txt
│   │   ├── basic_mcp.py              # Direct tool calling
│   │   └── with_skill.py             # Agent-driven with skills
│   └── typescript/
│       ├── package.json
│       ├── basic_mcp.ts              # Direct tool calling
│       └── with_skill.ts             # Agent-driven with skills
│
└── docs/
    ├── PATTERNS_CATALOG.md            # ⭐ Primary reference (2000+ lines)
    ├── MCP_SERVER.md                  # Server architecture guide
    ├── SKILL_GUIDE.md                 # Skill development guide
    ├── SDK_USAGE.md                   # SDK integration examples
    ├── EXAMPLES.md                    # Real-world scenarios
    └── EXTENDING.md                   # How to extend the system
```

## 🚀 Quick Start

### 1. Install MCP Server

```bash
cd mcp-server
pip install -e .
```

### 2. Register with Claude Code

```bash
claude mcp add --transport stdio task-manager \
  -- python -m task_manager_mcp.server
```

### 3. Test in Claude Code CLI

```bash
claude
> Create a task to review the authentication PR
> Show me all high-priority tasks
> What's my task completion rate?
```

### 4. Run SDK Examples

**Python:**
```bash
cd sdk-examples/python
pip install -r requirements.txt
python with_skill.py      # Agent-driven approach
python basic_mcp.py       # Direct approach
```

**TypeScript:**
```bash
cd sdk-examples/typescript
npm install
npx tsx with_skill.ts     # Agent-driven approach
npx tsx basic_mcp.ts      # Direct approach
```

## 📖 Learning Path

### For Architects & Decision Makers
1. Start with [PATTERNS_CATALOG.md](docs/PATTERNS_CATALOG.md)
2. Review decision frameworks and rankings
3. Study comparison matrices

### For Developers Building MCP Servers
1. Read [MCP_SERVER.md](docs/MCP_SERVER.md)
2. Review `mcp-server/src/task_manager_mcp/server.py`
3. Explore database schema and operations
4. See [EXAMPLES.md](docs/EXAMPLES.md)

### For Developers Building Skills
1. Read [SKILL_GUIDE.md](docs/SKILL_GUIDE.md)
2. Review `.claude/skills/task-organizer/SKILL.md`
3. Understand skill activation patterns
4. Practice skill descriptions

### For SDK Integration
1. Read [SDK_USAGE.md](docs/SDK_USAGE.md)
2. Review both `with_skill.py` and `basic_mcp.py`
3. Understand skill configuration
4. See token efficiency trade-offs

### For Extension
1. Read [EXTENDING.md](docs/EXTENDING.md)
2. Add new tools to server
3. Add new skills to guide tool use
4. Implement new patterns

## 🎓 Key Learnings

### Pattern 1: Skill-Guided MCP Tools ⭐

The primary pattern demonstrated in this project:

```python
# User makes natural language request
"Create a project with high-priority tasks"

# Claude automatically:
# 1. Detects task-organizer skill matches
# 2. Reads skill guidance
# 3. Decides which MCP tools to use
# 4. Chains operations as needed
# 5. Returns formatted results
```

**Use when**: Building user-facing systems with natural language interfaces

**Token cost**: ~600-1000 per operation (includes model reasoning)

### Pattern 6: Direct MCP Usage

Traditional approach for automation:

```python
# Explicitly call specific tool
await mcp.call_tool(
    "mcp__task-manager__filter_tasks",
    {"priority": "high"}
)
```

**Use when**: Building automated scripts with known workflows

**Token cost**: ~100-200 per operation (minimal overhead)

## 🏢 Project Features

### MCP Server (35+ Tools)

**Task Operations**:
- create_task, get_task, update_task, delete_task, list_tasks
- search_tasks (full-text), filter_tasks

**Project Operations**:
- create_project, get_project, list_projects, update_project, delete_project
- get_project_tasks

**Tag Management**:
- add_tag, remove_tag, list_tags

**Analytics**:
- task_statistics, get_overdue_tasks

### Claude Agent Skill

- Task creation and management
- Project planning
- Tag-based organization
- Automatic invocation on relevant requests
- Comprehensive operation guidance

### Resources (5)

- `task://all` - All tasks
- `task://pending` - Pending tasks
- `task://high-priority` - High-priority tasks
- `project://all` - All projects
- `stats://summary` - Task statistics

### Prompts (4 Workflows)

- daily-review - Daily task review
- weekly-planning - Weekly planning
- project-summary - Project summaries
- overdue-analysis - Overdue task analysis

## 📊 Pattern Summary

| Pattern | Complexity | Token Efficiency | Best For |
|---------|------------|------------------|----------|
| 1. Skill-Guided MCP | Medium | High | User-facing systems |
| 2. Multi-MCP Orchestration | Very High | Medium | Complex integrations |
| 3. MCP Resources as Context | Low | Medium | Knowledge systems |
| 4. MCP Prompts as Workflows | Medium | High | Complex procedures |
| 5. Skill Without Custom MCP | Low | Very High | File operations |
| 6. Direct MCP Usage | Very Low | Very High | Automation scripts |
| 7. Stateful Conversation | High | Medium | Multi-turn sessions |
| 8. Data Pipeline | High | Medium | ETL processes |
| 9. Hybrid Local + Remote | Very High | Low | Mixed infrastructure |
| 10. Security/Authorization | Very High | Medium | Regulated systems |
| 11. Hierarchical Skills | Medium | High | Large systems |
| 12. Event-Driven MCP | Very High | Low | Reactive systems |
| 13. Chain-of-Thought | High | Medium | Complex reasoning |
| 14. Caching + Resources | Medium | Very High | Read-heavy systems |

See [PATTERNS_CATALOG.md](docs/PATTERNS_CATALOG.md) for detailed analysis.

## 🔧 Technology Stack

- **MCP Server**: Python + FastMCP + aiosqlite
- **Database**: SQLite with FTS5 full-text search
- **Skills**: YAML + Markdown format
- **SDK**: Claude Agent SDK (Python & TypeScript examples)
- **Query**: Async operations throughout

## 📦 Dependencies

**MCP Server**:
- mcp >= 1.1.2
- aiosqlite >= 0.20.0

**SDK Examples**:
- anthropic >= 0.28.0 (Python)
- @anthropic-ai/claude-agent-sdk (TypeScript)

## 🧪 Testing

```bash
# Run server tests
cd mcp-server
pytest tests/

# Test with Claude Code
claude mcp list                    # Verify registration
# Then test commands in Claude Code CLI
```

## 🎓 Success Criteria

After studying this project, you should be able to:

✅ Identify which pattern fits your use case
✅ Understand trade-offs between patterns
✅ Implement Pattern 1 (Skill-Guided MCP)
✅ Implement Pattern 6 (Direct MCP)
✅ Design effective skill descriptions
✅ Build MCP tools with proper structure
✅ Configure SDK with skills and MCP servers
✅ Optimize token usage
✅ Make informed architectural decisions

## 📚 Documentation

- **[PATTERNS_CATALOG.md](docs/PATTERNS_CATALOG.md)** (2000+ lines) - Complete patterns reference
- **[MCP_SERVER.md](docs/MCP_SERVER.md)** - MCP server architecture and APIs
- **[SKILL_GUIDE.md](docs/SKILL_GUIDE.md)** - Skill design and best practices
- **[SDK_USAGE.md](docs/SDK_USAGE.md)** - SDK integration examples
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Real-world usage scenarios
- **[EXTENDING.md](docs/EXTENDING.md)** - How to extend with new features

## 🤝 Contributing

This is an educational project. To extend it:

1. Add new patterns to PATTERNS_CATALOG.md
2. Implement additional tools in the MCP server
3. Create new skills for different domains
4. Add more examples and use cases

## 📝 License

MIT License - Feel free to use and modify for learning purposes.

## 🙋 Questions?

Refer to the comprehensive documentation in the `docs/` directory. Each file has detailed examples and explanations.

## 🎯 Next Steps

1. **Read**: Start with [PATTERNS_CATALOG.md](docs/PATTERNS_CATALOG.md)
2. **Run**: Test the server and SDK examples
3. **Understand**: Study the skill and MCP server code
4. **Apply**: Implement patterns in your own projects
5. **Extend**: Add new tools, skills, and patterns

---

**Happy learning! 🚀**
