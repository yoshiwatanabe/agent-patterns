# MCP + Claude Skills Integration Patterns Catalog

## Overview

This comprehensive catalog documents all major patterns for integrating Model Context Protocol (MCP) servers with Claude Agent Skills. It serves as a decision-making guide for architects and developers building agent-based systems.

**Target Audience**: Advanced developers, architects, and technical leads evaluating integration patterns for custom AI applications.

**Purpose**: Enable informed architectural decisions by providing:
- Complete pattern descriptions with diagrams
- Pros/cons analysis for each pattern
- Complexity and token efficiency metrics
- Real-world use cases and scenarios
- Decision frameworks and comparison matrices

---

## Quick Pattern Selector

Choose your pattern based on your needs:

```
Do you have custom business logic/operations?
├─ Yes → Do you want automatic invocation?
│   ├─ Yes → Pattern 1: Skill-Guided MCP Tools ⭐
│   └─ No → Pattern 6: Direct MCP Usage
└─ No → Do you need structured guidance?
    ├─ Yes → Pattern 5: Skill Without Custom MCP
    └─ No → Use standard Claude Code features
```

---

---

## Pattern 1: Skill-Guided MCP Tools ⭐

**Status**: Implemented in this project | **Complexity**: Medium | **Token Efficiency**: High

### Overview

A Claude Agent skill provides guidance and instructions that help Claude automatically decide which MCP tools to use. The skill acts as an intelligent router, describing when and how to use each tool. Claude's inference layer handles tool selection, parameter extraction, and multi-step orchestration.

### Architecture Diagram

```
User Request (Natural Language)
       ↓
Claude Model
       ↓
[Skill loaded from filesystem]
  - Description matches request?
  - Available tools documented
       ↓
Claude decides which MCP tools to use
       ↓
[MCP Server Execution]
  - create_task
  - update_task
  - filter_tasks
  - etc.
       ↓
Results processed by Claude
       ↓
Formatted response to user
```

### When to Use

✅ **Ideal for**:
- Building user-facing AI applications
- Natural language interfaces
- Multi-step workflows requiring intelligence
- Systems where end users define the workflow
- Applications prioritizing ease of use
- Features that adapt to user requests

**Example scenarios**:
- Task management system with natural language
- Project planning assistants
- Customer service bots that manage tickets
- Personal productivity tools
- Document processing systems

### When NOT to Use

❌ **Avoid when**:
- You need 100% predictable tool execution
- Performance is critical (model reasoning adds latency)
- Users are technical and prefer explicit commands
- You're building internal CLI tools
- Every token matters (use direct MCP for simpler cases)

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | Medium | Requires skill design, MCP tools, and SDK configuration |
| **Token Efficiency** | High | Natural language + reasoning adds tokens, but fewer round-trips |
| **Setup Effort** | Medium | Need skill file, MCP server, SDK configuration |
| **Maintenance** | Medium | Update skill descriptions as tools change |
| **Scalability** | High | Handles complex multi-step workflows well |
| **Testability** | Medium | Need to test skill activation and tool chaining |
| **Development Speed** | High | Write skill once, works across many scenarios |
| **User Experience** | Excellent | Natural language, no memorization needed |

### Pros ✅

- **Natural Language Interface**: Users interact conversationally, no technical knowledge needed
- **Automatic Intelligence**: Claude decides which tools to use based on context
- **Flexible Workflows**: Adapts to different user requests without code changes
- **Self-Documenting**: Skill descriptions serve as documentation
- **Multi-Step Automation**: Automatically chains operations as needed
- **Scalable Design**: One skill can handle 100+ use cases
- **Easy Maintenance**: Update skill once, affects all operations
- **Minimal Client Code**: Simple SDK call, Claude handles complexity

### Cons ❌

- **Latency**: Model reasoning adds processing time vs. direct tool calls
- **Token Cost**: More tokens than explicit tool calls (200-400 vs. 100-150 per operation)
- **Less Control**: Developer can't guarantee specific execution path
- **Skill Design**: Requires good skill descriptions and examples
- **Debugging Complexity**: Harder to trace why Claude chose a tool
- **Cost at Scale**: Many operations = significant token costs

### Token Usage Analysis

**Typical Request**: "Create a project with 5 tasks, prioritize by date, show me high-priority items"

Token breakdown:
```
Initial request + skill context:     ~250 tokens
  - User request
  - Skill description
  - Available MCP tools
  - System instructions

Claude reasoning (tool selection):   ~150 tokens
  - Analyzing request
  - Selecting which tools to call
  - Determining parameters

Tool invocations (5 calls):          ~300 tokens
  - Individual tool calls
  - Parameter specifications

MCP responses + processing:          ~200 tokens
  - Results from MCP server
  - Claude processing results
  - Formatting response

Final output:                        ~100 tokens

Total: ~1000 tokens
```

**Token efficiency tips**:
- Use concise skill descriptions (reduces context)
- Leverage MCP resources for large data sets
- Consider pagination for list operations
- Cache results when possible
- Use prompts for complex workflows

### Example Use Cases

1. **Task Management (Project Context)**
   - Request: "Create a project for website redesign with 5 tasks"
   - Skill activates: Recognizes project/task keywords
   - Tools used: create_project, create_task (5x)
   - Result: Complete organized project

2. **Productivity Analytics**
   - Request: "Show me my completion rate and top priority tasks"
   - Skill activates: Recognizes analytics request
   - Tools used: task_statistics, filter_tasks
   - Result: Personalized productivity report

3. **Intelligent Search**
   - Request: "Find all authentication-related bugs that are overdue"
   - Skill activates: Recognizes search + filtering
   - Tools used: search_tasks, filter_tasks, get_overdue_tasks
   - Result: Prioritized bug list

4. **Workflow Automation**
   - Request: "Mark all completed tasks done and calculate velocity"
   - Skill activates: Recognizes status updates
   - Tools used: list_tasks, update_task (multiple), task_statistics
   - Result: Updated system with metrics

### Implementation Complexity

**Setup**:
- Define skill file with clear descriptions
- Implement MCP tools with proper parameters
- Test skill activation with matching prompts
- Configure SDK with settingSources=["project"]

**Maintenance**:
- Update skill descriptions as tools change
- Monitor tool usage patterns
- Refine descriptions based on how Claude uses them
- Add examples for edge cases

**Testing**:
- Test skill activation with various prompts
- Verify tool chaining works correctly
- Check error handling for invalid parameters
- Test with real user scenarios

### Code Example

**Skill file** (`.claude/skills/task-organizer/SKILL.md`):
```yaml
---
name: task-organizer
description: Manage tasks and projects. Use for creating tasks, filtering by priority/status, and tracking progress.
---

# Task Organizer

Available operations:
- Create and update tasks
- Filter by priority, status, project
- Get completion statistics
- Find overdue items
```

**SDK usage**:
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["project"],  # Loads skills from filesystem
    allowed_tools=["Skill", "mcp__task-manager__*"],
    mcp_servers={"task-manager": task_server}
)

# Claude automatically invokes skill based on request
async for message in query(
    prompt="Create a task to review the PR",
    options=options
):
    print(message)
```

### Related Patterns

- **Alternative**: Pattern 6 (Direct MCP) - for predictable tool calls
- **Complementary**: Pattern 3 (MCP Resources as Context) - for large data sets
- **Prerequisite**: Pattern 4 (MCP Prompts as Workflows) - for complex operations

### Decision Checklist

Use this pattern if:
- [ ] You want natural language interfaces
- [ ] Users will ask varied requests
- [ ] Multi-step workflows are common
- [ ] Token cost is not critical
- [ ] You can design good skill descriptions

Consider alternatives if:
- [ ] You need 100% predictable execution
- [ ] Every millisecond matters (latency-sensitive)
- [ ] You're building for technical users
- [ ] Token budget is extremely limited

---

## Pattern 2: Multi-MCP Orchestration

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Integration-heavy systems

### Overview

Multiple MCP servers work together, coordinated by Claude and skills. Each MCP server handles a specific domain (database, API, files, etc.), and Claude's intelligence orchestrates interactions between them.

### Architecture Diagram

```
User Request
    ↓
[Orchestration Skill]
    ↓
┌─────────────────────────────────────┐
│   Claude (Intelligence)             │
│  - Decides which servers to use     │
│  - Coordinates data flow            │
│  - Handles cross-domain logic       │
└──────┬──────────────────────────────┘
       ↓
   Parallel/Sequential Calls
  /        |         \
 ↓         ↓          ↓
[DB MCP] [API MCP] [File MCP]
 ↓         ↓          ↓
 DB      External    File
Results  Data        Results
```

### When to Use

✅ **Ideal for**:
- Systems with multiple data sources
- Complex integrations (database + API + files)
- Workflows spanning multiple domains
- Enterprise systems with specialized services
- Data processing pipelines

**Example**: Backup system using DB MCP + Storage MCP + Notification MCP

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Very High |
| **Token Efficiency** | Medium |
| **Setup Effort** | High |
| **Maintainability** | Medium |
| **Scalability** | Excellent |
| **Reliability** | Medium (depends on all servers) |

### Pros ✅

- Separation of concerns (each MCP handles one domain)
- Reusable across multiple applications
- Specialized servers optimized per domain
- Parallel execution possible
- Easy to add new servers

### Cons ❌

- Complex debugging (multiple servers)
- Dependency management (all servers must be up)
- Higher token costs (coordinate across servers)
- Network/latency considerations
- Eventual consistency issues possible

### Token Usage Analysis

```
Orchestration request:           ~200 tokens
Multi-server coordination:       ~500 tokens
Database operations:            ~150 tokens
External API calls:             ~200 tokens
Result synthesis:               ~100 tokens

Total: ~1150 tokens
(vs. single MCP: ~600 tokens)

Cost: ~2x single MCP
```

### Example Use Cases

1. **Data Pipeline**: Extract from DB → Transform with API → Store in Files
2. **Backup System**: Database MCP (backup) → Cloud MCP (upload) → Notify MCP (alert)
3. **Report Generation**: Data MCP (query) → Analysis MCP (compute) → Export MCP (output)

### Implementation Complexity

- Moderate to High
- Need to manage dependencies between servers
- Ensure data consistency across calls
- Handle partial failures gracefully

---

## Pattern 3: MCP Resources as Context

**Complexity**: Low | **Token Efficiency**: Medium | **Recommended for**: Knowledge-driven systems

### Overview

MCP servers expose read-only resources (documentation, schemas, standards) that provide context to Claude. These resources are loaded as part of the conversation context, helping Claude make better decisions without needing to fetch data dynamically.

### Architecture Diagram

```
User Request
    ↓
Load MCP Resources (read-only)
    ↓
@docs:resource://coding-standards
@db:resource://schema
    ↓
Claude (enriched context)
    ↓
Educated Decision Making
    ↓
Tool invocation (if needed)
```

### When to Use

✅ **Ideal for**:
- Knowledge bases (documentation, standards, guidelines)
- Schema/specification files
- Configuration references
- Code generation with style guides
- Compliance/regulatory requirements

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Low |
| **Token Efficiency** | Medium |
| **Setup Effort** | Low |
| **Performance** | Excellent |
| **Cacheability** | High |

### Pros ✅

- Simple to implement
- Read-only (no side effects)
- Highly cacheable
- Reduces model hallucination
- Self-documenting via resources

### Cons ❌

- Resource size affects tokens
- No dynamic computation
- Must pre-compute all resources
- Stale resources possible

### Token Usage

```
Resource loading:    ~200 tokens (cached)
Context enrichment:  ~100 tokens
Model reasoning:     ~150 tokens
Tool usage:          ~100 tokens

Total: ~550 tokens
Efficiency: High (resources cached)
```

### Example Use Cases

1. **Code Generation**: Load style guide resources → Generate code matching standards
2. **Documentation Assistant**: Load API specs → Answer questions with accurate details
3. **Compliance Checker**: Load regulations → Review documents for compliance

---

## Pattern 4: MCP Prompts as Workflows

**Complexity**: Medium | **Token Efficiency**: High | **Recommended for**: Complex operations

### Overview

MCP servers expose prompts (pre-written, structured workflows) that encode complex, multi-step procedures. Skills trigger these prompts to execute complete workflows without needing to orchestrate individual steps.

### Architecture Diagram

```
User Request ("Weekly review")
    ↓
Skill Activation
    ↓
MCP Prompt Execution
    ↓
┌─────────────────────────┐
│ Workflow (built-in):     │
│ 1. Get statistics       │
│ 2. Identify bottlenecks │
│ 3. Format report        │
│ 4. Generate summary     │
└─────────────────────────┘
    ↓
Complete Report
```

### When to Use

✅ **Ideal for**:
- Recurring complex workflows
- Best practice procedures
- Multi-step processes with fixed patterns
- Domain-specific workflows
- Audit/compliance routines

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Medium |
| **Token Efficiency** | High |
| **Consistency** | Excellent |
| **Flexibility** | Low |

### Pros ✅

- Encodes domain expertise
- Highly consistent results
- Efficient execution
- Easy to understand

### Cons ❌

- Less flexible than building steps dynamically
- Requires predicting workflows

---

## Pattern 5: Skill Without Custom MCP

**Complexity**: Low | **Token Efficiency**: Very High | **Recommended for**: Lean systems

### Overview

Skills provide guidance and instructions without needing custom MCP servers. Skills use built-in Claude Code tools (Read, Write, Bash, Edit, etc.) to guide Claude through workflows.

### Architecture Diagram

```
User Request
    ↓
[Skill Loaded]
  (Describes best practices and approaches)
    ↓
Claude Uses Built-in Tools
  /      |       \
Read   Write    Edit
(and other standard tools)
    ↓
Results Achieved
```

### When to Use

✅ **Ideal for**:
- File-based operations
- Code generation/modification
- Developer assistance tools
- Documentation generation
- Project scaffolding

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Low |
| **Token Efficiency** | Very High |
| **Setup Effort** | Minimal |
| **Performance** | Excellent |
| **Scope** | Limited to file operations |

### Pros ✅

- No MCP server needed
- Very low token overhead
- Simple to implement
- Works out of the box
- Leverages standard tools

### Cons ❌

- Limited to file operations
- Can't access external systems
- No custom business logic

### Token Usage

```
Skill guidance:    ~100 tokens
Tool instructions: ~50 tokens
Built-in tools:    ~150 tokens

Total: ~300 tokens
(Lowest overhead of any pattern)
```

### Example: Test-Driven Development Skill

```yaml
---
name: tdd-guide
description: Follow test-driven development practices using standard tools.
---

# TDD Workflow

1. Write failing test
   - Use Write tool to create test file

2. Run test
   - Use Bash to execute tests

3. Implement feature
   - Use Edit tool to modify code

4. Run tests again
   - Bash to verify all pass
```

---

## Pattern 6: Direct MCP Usage (No Skill)

**Complexity**: Low | **Token Efficiency**: Very High | **Recommended for**: Automation/scripts

### Overview

Directly call MCP tools without a skill layer. Developer controls which tools are called, when they're called, and with what parameters. No model reasoning overhead.

### Architecture Diagram

```
Program/Script
    ↓
[Direct Tool Calls]
    ↓
MCP Server
    ↓
Results
```

### When to Use

✅ **Ideal for**:
- Automated scripts/cron jobs
- Known, fixed workflows
- Internal tools for developers
- Performance-critical operations
- Testing/integration scenarios

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Very Low |
| **Token Efficiency** | Excellent |
| **Setup Effort** | Low |
| **Performance** | Excellent |
| **Flexibility** | Low |

### Pros ✅

- Maximum control
- Minimal token usage
- Very fast (no model reasoning)
- Deterministic behavior
- Easy to debug

### Cons ❌

- Must know tool names/parameters
- No intelligence
- Verbose for complex workflows
- Requires code changes for variations

### Token Usage

```
Tool specification:  ~50 tokens
Parameters:         ~30 tokens
Execution:          ~20 tokens

Total: ~100 tokens
(Minimal overhead)
```

### Code Example

```python
# Traditional programming - no AI reasoning
result = await mcp.call_tool(
    "mcp__task-manager__filter_tasks",
    {"priority": "high", "status": "pending"}
)
# Explicit, predictable, efficient
```

---

## Pattern 7: Stateful Conversation MCP

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Long conversations

### Overview

MCP server maintains state across conversation turns. Useful for multi-turn interactions where context needs to persist (conversations, debugging sessions, iterative refinement).

### Architecture Diagram

```
Turn 1: User request
    ↓
MCP stores context/state
    ↓
Turn 2: Follow-up request
    ↓
MCP retrieves and updates state
    ↓
Turn 3+: Continue with preserved context
```

### When to Use

✅ **Ideal for**:
- Multi-turn debugging sessions
- Iterative design/refinement
- Conversations with memory
- Problem-solving workflows
- Code review sessions

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | High |
| **Token Efficiency** | Medium |
| **Consistency** | Medium (state sync needed) |
| **Context Preservation** | Excellent |

### Pros ✅

- Persistent context across turns
- Better user experience
- Reduces token for context (some in server state)
- Enables complex workflows

### Cons ❌

- State management complexity
- Synchronization issues possible
- More storage needed
- Cleanup required

---

## Pattern 8: Data Pipeline Pattern

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: ETL/data processing

### Overview

Sequential orchestration of multiple MCP servers to form a data pipeline. Data flows through transformations across different servers.

### Architecture Diagram

```
Input Data
    ↓
[Extract MCP]
    ↓
[Transform MCP]
    ↓
[Load MCP]
    ↓
Output Data
```

### When to Use

✅ **Ideal for**:
- Data migration
- ETL processes
- Report generation
- Data analysis pipelines
- Batch processing

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | High |
| **Token Efficiency** | Medium |
| **Scalability** | High |
| **Performance** | Good (sequential) |

### Token Usage: ~1500 tokens per pipeline execution

---

## Pattern 9: Hybrid Local + Remote MCP

**Complexity**: High | **Token Efficiency**: Low | **Recommended for**: Mixed infrastructure

### Overview

Combine local STDIO MCP servers with remote HTTP MCP servers in same application.

### When to Use

✅ **Ideal for**:
- Local data + cloud services
- On-premise + SaaS integrations
- Development + production systems
- Hybrid infrastructure

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | High |
| **Latency** | Medium (remote adds latency) |
| **Reliability** | Medium (dependencies on both) |
| **Setup** | High |

---

## Pattern 10: Security/Authorization Pattern

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Regulated systems

### Overview

MCP servers enforce security policies and authorization checks before executing operations.

### When to Use

✅ **Ideal for**:
- Healthcare systems (HIPAA)
- Financial systems (SOX)
- Government systems (compliance)
- Sensitive data operations
- Multi-tenant systems

### Characteristics

| Aspect | Rating |
|--------|--------|
| **Complexity** | Very High |
| **Security** | Excellent |
| **Overhead** | Medium (auth checks) |

### Security Considerations

- Validate user permissions at MCP level
- Encrypt sensitive data
- Audit all operations
- Rate limit sensitive operations
- Use skills to enforce policies

---

## Pattern 11: Hierarchical Skills

**Complexity**: Medium | **Token Efficiency**: High | **Recommended for**: Large systems

### Overview

Parent skills delegate to child skills. Useful for organizing complex systems with sub-domains.

### Architecture Diagram

```
User Request (complex)
    ↓
[Parent Skill]
    ↓
    /    |    \
   ↓     ↓     ↓
[Child] [Child] [Child]
Skill1  Skill2  Skill3
```

### When to Use

✅ **Ideal for**:
- Large applications (100+ operations)
- Multi-domain systems
- Team-based development
- Modular architectures

---

## Pattern 12: Event-Driven MCP

**Complexity**: Very High | **Token Efficiency**: Low | **Recommended for**: Reactive systems

### Overview

MCP servers monitor events/webhooks and trigger Claude actions based on events.

### When to Use

✅ **Ideal for**:
- CI/CD automation
- Real-time monitoring
- Webhook-based workflows
- Reactive systems
- Event processing

---

## Pattern 13: Chain-of-Thought with MCP

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Complex reasoning

### Overview

Break complex problem-solving into steps, using different MCP tools at each step.

### Architecture Diagram

```
Complex Problem
    ↓
[Analyze Phase] (Analysis MCP)
    ↓
[Design Phase] (Design MCP)
    ↓
[Implement Phase] (Implementation MCP)
    ↓
[Verify Phase] (Validation MCP)
    ↓
Solution
```

### When to Use

✅ **Ideal for**:
- Complex problem solving
- Architecture design
- Multi-phase projects
- Scientific computing
- Research applications

### Token Usage: ~2000+ tokens (reasoning overhead)

---

## Pattern 14: Caching + MCP Resources

**Complexity**: Medium | **Token Efficiency**: Very High | **Recommended for**: Read-heavy systems

### Overview

Cache MCP resources and results to reduce repeated token usage.

### When to Use

✅ **Ideal for**:
- Reference data (rarely changes)
- Large resource files
- High-traffic systems
- Cost-sensitive applications

### Caching Strategy

```
Request 1: Load @schema → 200 tokens
Request 2: Cached @schema → 0 tokens
Request 3: Cached @schema → 0 tokens

Savings: 400 tokens after first request
```

---

---

## Pattern Comparison Matrix

| Pattern | Complexity | Token Efficiency | Best For | Learning Curve |
|---------|------------|------------------|----------|-----------------|
| 1. Skill-Guided MCP | Medium | High | User-facing systems | Medium |
| 2. Multi-MCP Orchestration | Very High | Medium | Complex integrations | High |
| 3. MCP Resources as Context | Low | Medium | Knowledge systems | Low |
| 4. MCP Prompts as Workflows | Medium | High | Complex procedures | Medium |
| 5. Skill Without Custom MCP | Low | Very High | File operations | Low |
| 6. Direct MCP Usage | Very Low | Very High | Automation scripts | Very Low |
| 7. Stateful Conversation | High | Medium | Multi-turn sessions | High |
| 8. Data Pipeline | High | Medium | ETL processes | High |
| 9. Hybrid Local + Remote | Very High | Low | Mixed infrastructure | Very High |
| 10. Security/Authorization | Very High | Medium | Regulated systems | Very High |
| 11. Hierarchical Skills | Medium | High | Large systems | Medium |
| 12. Event-Driven MCP | Very High | Low | Reactive systems | Very High |
| 13. Chain-of-Thought | High | Medium | Complex reasoning | High |
| 14. Caching + Resources | Medium | Very High | Read-heavy systems | Medium |

---

## Decision Framework

### Question 1: Who are your users?

- **End users** → Use Pattern 1 (Skill-Guided MCP)
- **Developers** → Use Pattern 6 (Direct MCP)
- **Mix** → Use Pattern 11 (Hierarchical Skills)

### Question 2: How many MCP servers?

- **One** → Use Pattern 1, 3, 4, or 5
- **Few (2-3)** → Use Pattern 2 (Multi-MCP)
- **Many (5+)** → Use Pattern 11 (Hierarchical)

### Question 3: What's your priority?

- **Natural language interface** → Pattern 1
- **Maximum speed** → Pattern 6
- **Token efficiency** → Pattern 5 or 14
- **Complex workflows** → Pattern 13
- **Real-time events** → Pattern 12

### Question 4: What constraints?

- **Regulatory/security** → Pattern 10
- **Stateful conversations** → Pattern 7
- **Data transformation** → Pattern 8
- **Hybrid infrastructure** → Pattern 9

---

## Token Efficiency Ranking

From most to least efficient:

```
1. Pattern 6 (Direct MCP)           ~100-200 tokens
2. Pattern 5 (Skill no Custom MCP)  ~300-500 tokens
3. Pattern 4 (Prompts as Workflows) ~400-600 tokens
4. Pattern 1 (Skill-Guided MCP)     ~600-1000 tokens
5. Pattern 3 (Resources as Context) ~500-800 tokens
6. Pattern 14 (Caching)             ~300-500 tokens (after cache)
7. Pattern 2 (Multi-MCP)            ~1000-1500 tokens
8. Pattern 7 (Stateful)             ~700-1200 tokens
9. Pattern 8 (Data Pipeline)        ~1200-1800 tokens
10. Pattern 13 (Chain-of-Thought)   ~1500-2500 tokens
```

---

## Complexity Ranking

From simplest to most complex:

```
1. Pattern 6 (Direct MCP)
2. Pattern 5 (Skill no Custom MCP)
3. Pattern 3 (Resources as Context)
4. Pattern 4 (Prompts as Workflows)
5. Pattern 1 (Skill-Guided MCP)
6. Pattern 14 (Caching + Resources)
7. Pattern 11 (Hierarchical Skills)
8. Pattern 7 (Stateful Conversation)
9. Pattern 8 (Data Pipeline)
10. Pattern 2 (Multi-MCP Orchestration)
11. Pattern 13 (Chain-of-Thought)
12. Pattern 9 (Hybrid Local + Remote)
13. Pattern 12 (Event-Driven)
14. Pattern 10 (Security/Authorization)
```

---

## Architectural Decision Tree

```
START: "I need to build a system with MCP and Skills"
  │
  ├─ Will end users interact with it directly?
  │  │
  │  ├─ Yes → Use Pattern 1 (Skill-Guided MCP) ⭐
  │  │   └─ Provides natural language interface
  │  │
  │  └─ No → Is it a developer tool?
  │      │
  │      ├─ Yes, known workflows → Pattern 6 (Direct MCP)
  │      │   └─ Maximum efficiency
  │      │
  │      └─ Yes, varied tasks → Pattern 11 (Hierarchical)
  │          └─ Organize sub-domains
  │
  ├─ Do you need custom business logic?
  │  │
  │  ├─ No → Can you use built-in tools?
  │  │   │
  │  │   ├─ Yes → Pattern 5 (Skill without Custom MCP)
  │  │   │   └─ Minimal complexity
  │  │   │
  │  │   └─ No → Pattern 3 (Resources as Context)
  │  │       └─ Use knowledge resources
  │  │
  │  └─ Yes → Multiple servers needed?
  │      │
  │      ├─ No → Pattern 1 (Skill-Guided)
  │      │   └─ Single server, intelligent routing
  │      │
  │      └─ Yes → Orchestration complexity?
  │          │
  │          ├─ Sequential → Pattern 8 (Data Pipeline)
  │          │   └─ ETL-style processing
  │          │
  │          └─ Parallel → Pattern 2 (Multi-MCP)
  │              └─ Coordinate multiple servers
  │
  └─ Special requirements?
     │
     ├─ Regulatory compliance → Pattern 10
     ├─ Real-time events → Pattern 12
     ├─ Complex reasoning → Pattern 13
     ├─ Multi-turn sessions → Pattern 7
     ├─ Read-heavy operations → Pattern 14 (Caching)
     └─ Mixed infrastructure → Pattern 9
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)

Start with simplest patterns:
1. **Pattern 6** (Direct MCP) - Get comfortable with tool calls
2. **Pattern 5** (Skill without Custom MCP) - Add skill layer
3. **Pattern 3** (Resources as Context) - Provide knowledge

### Phase 2: Intelligence (Weeks 3-4)

Add automatic intelligence:
1. **Pattern 1** (Skill-Guided MCP) - Natural language routing
2. **Pattern 4** (Prompts as Workflows) - Encode complex procedures

### Phase 3: Scale (Weeks 5-8)

Handle complexity:
1. **Pattern 2** (Multi-MCP) - Coordinate multiple servers
2. **Pattern 11** (Hierarchical) - Organize large systems
3. **Pattern 8** (Data Pipeline) - Process data flows

### Phase 4: Advanced (Weeks 9+)

Specialized patterns:
1. **Pattern 7** (Stateful) - Persistent conversations
2. **Pattern 13** (Chain-of-Thought) - Complex reasoning
3. **Pattern 10** (Security) - Compliance and authorization

---

## Common Pitfalls and Solutions

### Pitfall 1: Overcomplicating Pattern Selection

❌ **Wrong**: "We might need 10 MCP servers someday, so build Pattern 2 now"

✅ **Right**: Start with Pattern 1, refactor to Pattern 2 only when you have actual multiple servers

**Lesson**: Don't over-engineer. Start simple, scale as needed.

### Pitfall 2: Ignoring Token Costs

❌ **Wrong**: Using Pattern 13 (2000+ tokens) for simple operations

✅ **Right**: Use Pattern 6 (100 tokens) for known workflows

**Lesson**: Match pattern complexity to problem complexity. Simplest solution wins.

### Pitfall 3: Poor Skill Descriptions

❌ **Wrong**: "Manages stuff" (vague, Claude won't activate)

✅ **Right**: "Manage tasks and projects. Create, update, filter, and track tasks. Use for task creation, project planning, and productivity." (specific, triggers correctly)

**Lesson**: Skill descriptions are critical. Invest time in good writing.

### Pitfall 4: Missing Error Handling

❌ **Wrong**: Assume all MCP calls succeed

✅ **Right**: Implement fallbacks, retries, and clear error messages

**Lesson**: Real systems fail. Handle failures gracefully.

### Pitfall 5: Ignoring Performance

❌ **Wrong**: Serializing everything, loading all resources

✅ **Right**: Parallelize where possible, cache resources, paginate results

**Lesson**: Performance matters. Monitor and optimize.

---

## Metrics and Monitoring

### Key Metrics to Track

```
Pattern Usage Metrics:
- Which patterns are used most?
- Skill activation rate
- Tool invocation frequency
- Average tokens per request

Performance Metrics:
- Response latency (P50, P95, P99)
- Error rate per pattern
- MCP server availability
- Cache hit rate

Cost Metrics:
- Tokens per user session
- Cost per operation
- Cost trends over time
```

### Optimization Checklist

- [ ] Monitor skill activation patterns
- [ ] Identify underutilized patterns
- [ ] Measure token usage by pattern
- [ ] Track error rates and causes
- [ ] Monitor MCP server performance
- [ ] Measure user satisfaction
- [ ] Identify refactoring opportunities

---

## Conclusion

The pattern you choose should match your specific requirements:

- **User-facing**: Pattern 1 (Skill-Guided MCP)
- **Automation**: Pattern 6 (Direct MCP)
- **Knowledge-driven**: Pattern 3 (Resources as Context)
- **Complex workflows**: Pattern 13 (Chain-of-Thought)
- **Large systems**: Pattern 11 (Hierarchical Skills)

Start simple. Scale as needed. Measure and optimize continuously.

Remember: **The best pattern is the simplest one that solves your problem.**

---

## Further Reading

- See `MCP_SERVER.md` for MCP implementation details
- See `SKILL_GUIDE.md` for skill development best practices
- See `SDK_USAGE.md` for integration examples
- See `EXAMPLES.md` for real-world code samples
