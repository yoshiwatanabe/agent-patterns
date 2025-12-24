# MCP + Claude Skills Integration Patterns Catalog

## Overview

This catalog focuses specifically on **Skills-centric integration patterns** - patterns where Claude Agent Skills actively orchestrate and coordinate MCP servers to accomplish complex workflows.

**Target Audience**: Developers building intelligent agent systems, particularly those learning how to leverage Skills effectively with MCP.

**Focus**: Learn how Skills work and how to adapt MCP and additional Skills effectively

**Purpose**:
- Understand how Skills drive MCP orchestration
- Learn pattern progression from simple to complex
- See real examples of Skill-MCP integration
- Build skills-focused agent systems

**Note**: For patterns that don't center on Skills orchestration (e.g., direct MCP calls, resource context enrichment), see [PATTERNS_REFERENCE.md](PATTERNS_REFERENCE.md).

---

## Quick Pattern Selector

Choose your pattern based on your Skill needs:

```
How should your Skill orchestrate MCP?
│
├─ Skill routes to ONE MCP server based on context
│  └─ Pattern 1: Skill-Guided MCP Tools ⭐ START HERE
│
├─ Skill coordinates MULTIPLE MCP servers
│  ├─ In parallel/mixed? → Pattern 2: Multi-MCP Orchestration
│  └─ Sequential? → Pattern 8: Data Pipeline
│
├─ Skill needs to handle MULTI-TURN conversations
│  └─ Pattern 7: Stateful Conversation MCP
│
├─ Skill should TRIGGER pre-built workflows
│  └─ Pattern 4: MCP Prompts as Workflows
│
├─ Skill coordinates MULTIPLE SKILLS
│  └─ Pattern 11: Hierarchical Skills
│
└─ Skill needs COMPLEX REASONING across steps
   └─ Pattern 13: Chain-of-Thought with MCP
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

## Skills-Centric Pattern Comparison Matrix

| Pattern | Complexity | Token Efficiency | Skill's Role | Learning Curve |
|---------|------------|------------------|-------------|-----------------|
| 1. Skill-Guided MCP Tools | Medium | High | Routes to ONE MCP based on context | Medium |
| 2. Multi-MCP Orchestration | Very High | Medium | Coordinates MULTIPLE MCP servers | High |
| 4. MCP Prompts as Workflows | Medium | High | Triggers pre-built MCP workflows | Medium |
| 7. Stateful Conversation | High | Medium | Manages state across conversation turns | High |
| 8. Data Pipeline | High | Medium | Orchestrates sequential data flow | High |
| 11. Hierarchical Skills | Medium | High | Delegates to child skills | Medium |
| 13. Chain-of-Thought | High | Medium | Guides multi-step reasoning | High |

---

## Skills-Centric Decision Framework

### Question 1: How many MCP servers should your Skill coordinate?

- **One MCP server** → Pattern 1: Skill-Guided MCP Tools
  - Skill intelligently routes requests to single MCP
  - Best for: Task management, single-domain operations

- **Two or more MCP servers** → Pattern 2: Multi-MCP Orchestration
  - Skill orchestrates calls across multiple MCPs
  - Best for: Complex workflows needing data from multiple sources

### Question 2: What type of data flow does your Skill need?

- **Real-time responses** → Pattern 1 or 2
  - Skill makes individual tool calls for each request

- **Sequential/pipeline** → Pattern 8: Data Pipeline
  - Skill orchestrates data flowing through multiple transformations
  - Best for: ETL, report generation, data processing

- **Pre-built workflows** → Pattern 4: MCP Prompts as Workflows
  - Skill triggers complete workflows encoded in MCP
  - Best for: Complex procedures with fixed steps

### Question 3: Does your Skill need to handle conversation context?

- **Single-turn requests** → Pattern 1, 2, 4, or 8
  - Each request is independent

- **Multi-turn conversations** → Pattern 7: Stateful Conversation
  - Skill maintains state across conversation turns
  - Best for: Iterative design, debugging, refinement

### Question 4: How complex is your skill system?

- **Single Skill** → Pattern 1, 2, 4, 7, 8, or 13
  - One skill handles orchestration

- **Multiple coordinated Skills** → Pattern 11: Hierarchical Skills
  - Parent skill delegates to child skills
  - Best for: Large systems, team development, modular architecture

### Question 5: Does your Skill need complex reasoning?

- **Straightforward logic** → Pattern 1, 2, 4, 8
  - Direct orchestration without multi-step reasoning

- **Multi-step problem solving** → Pattern 13: Chain-of-Thought
  - Skill guides reasoning across multiple analysis/design/implement phases
  - Best for: Architecture design, complex problem solving

---

## Skills-Centric Token Efficiency Ranking

From most to least efficient:

```
1. Pattern 4 (Prompts as Workflows)  ~400-600 tokens
2. Pattern 1 (Skill-Guided MCP)      ~600-1000 tokens
3. Pattern 11 (Hierarchical Skills)  ~600-1000 tokens
4. Pattern 7 (Stateful Conversation) ~700-1200 tokens
5. Pattern 8 (Data Pipeline)         ~1200-1800 tokens
6. Pattern 2 (Multi-MCP)             ~1000-1500 tokens
7. Pattern 13 (Chain-of-Thought)     ~1500-2500 tokens
```

---

## Skills-Centric Complexity Ranking

From simplest to most complex:

```
1. Pattern 1 (Skill-Guided MCP) - Single MCP, intelligent routing
2. Pattern 4 (Prompts as Workflows) - Trigger pre-built workflows
3. Pattern 11 (Hierarchical Skills) - Delegate to child skills
4. Pattern 7 (Stateful Conversation) - Manage conversation state
5. Pattern 8 (Data Pipeline) - Orchestrate sequential data flow
6. Pattern 2 (Multi-MCP Orchestration) - Coordinate multiple MCPs
7. Pattern 13 (Chain-of-Thought) - Guide multi-step reasoning
```

---

## Skills-Centric Architectural Decision Tree

```
START: "I need a Skill to orchestrate MCP servers"
  │
  ├─ How many MCP servers?
  │  │
  │  ├─ One → Pattern 1: Skill-Guided MCP Tools ⭐ START HERE
  │  │   └─ Skill intelligently routes to single MCP
  │  │   └─ Examples: Task manager, single-domain operations
  │  │
  │  └─ Multiple → How should data flow?
  │      │
  │      ├─ Parallel/mixed calls → Pattern 2: Multi-MCP Orchestration
  │      │   └─ Skill coordinates across servers
  │      │   └─ Examples: Business logic + analytics, order + shipping
  │      │
  │      ├─ Sequential pipeline → Pattern 8: Data Pipeline
  │      │   └─ Skill orchestrates data transformations
  │      │   └─ Examples: ETL, report generation, data processing
  │      │
  │      └─ Pre-built workflows → Pattern 4: MCP Prompts as Workflows
  │          └─ Skill triggers complete MCP workflows
  │          └─ Examples: Complex procedures, best practices
  │
  ├─ Does your Skill need complex structure?
  │  │
  │  ├─ No, single skill → Continue with patterns above
  │  │
  │  └─ Yes, multiple skills → Pattern 11: Hierarchical Skills
  │      └─ Parent skill delegates to child skills
  │      └─ Examples: Large systems, team development
  │
  ├─ Does your Skill handle conversations?
  │  │
  │  ├─ Single-turn requests → Use pattern selected above
  │  │
  │  └─ Multi-turn interactions → Pattern 7: Stateful Conversation
  │      └─ Skill maintains state across turns
  │      └─ Examples: Iterative design, debugging sessions
  │
  └─ Does your Skill need complex reasoning?
     │
     ├─ Straightforward logic → Use pattern selected above
     │
     └─ Multi-step problem solving → Pattern 13: Chain-of-Thought
         └─ Skill guides reasoning phases (analyze → design → implement → verify)
         └─ Examples: Architecture design, complex problem solving
```

---

## Skills-Centric Implementation Roadmap

### Phase 1: Foundations (Start here)

Master single-skill, single-MCP patterns:
1. **Pattern 1** (Skill-Guided MCP Tools)
   - Learn: How Skills route requests to MCP tools
   - Build: Simple task manager or single-domain skill
   - Example: task-organizer skill we already have

### Phase 2: Single Skill, Multiple MCPs

Expand to coordinating multiple servers:
1. **Pattern 2** (Multi-MCP Orchestration)
   - Learn: How Skills coordinate across MCP servers
   - Build: Skill that uses 2-3 MCPs together
   - Example: ecommerce-orchestration (what we just built!)

2. **Pattern 4** (MCP Prompts as Workflows)
   - Learn: How to trigger pre-built workflows from Skills
   - Build: Add MCP prompts that Skills invoke

### Phase 3: Advanced Single Skill

Add sophistication to single skill:
1. **Pattern 7** (Stateful Conversation)
   - Learn: Maintain context across conversation turns
   - Build: Debug or iterative design workflows

2. **Pattern 13** (Chain-of-Thought)
   - Learn: Guide multi-step reasoning in Skills
   - Build: Architecture design or complex problem-solving skill

### Phase 4: Multiple Skills and Pipelines

Scale across many skills:
1. **Pattern 11** (Hierarchical Skills)
   - Learn: Parent-child skill delegation
   - Build: Large systems with specialized sub-skills

2. **Pattern 8** (Data Pipeline)
   - Learn: Sequential data orchestration
   - Build: ETL or data processing workflows

---

## Common Pitfalls and Solutions

### Pitfall 1: Vague Skill Activation Triggers

❌ **Wrong**: "Manages stuff" - Too vague, Claude won't know when to activate

✅ **Right**: "Process customer returns. Check eligibility, calculate refunds, route for fulfillment." - Specific keywords trigger the skill

**Lesson**: Skill descriptions and "When This Skill Activates" sections are critical. Be explicit about activation triggers.

### Pitfall 2: Poor Skill-MCP Orchestration Documentation

❌ **Wrong**: Skill describes what it does, but no clear steps for how it coordinates MCPs

✅ **Right**: Skill explicitly documents orchestration steps (e.g., "Create task → Check policy → Update task")

**Lesson**: Skills should document HOW they orchestrate, not just WHAT they do. See ecommerce-orchestration for an example.

### Pitfall 3: Assuming All MCP Calls Succeed

❌ **Wrong**: Skill orchestrates 3 MCP calls assuming all succeed

✅ **Right**: Handle partial failures, provide fallbacks, clear error messages

**Lesson**: Real systems fail. Skills must handle failures gracefully and inform the user.

### Pitfall 4: Overcomplicating Too Early

❌ **Wrong**: "We might need stateful conversations someday, so build Pattern 7 now"

✅ **Right**: Start with Pattern 1, refactor to Pattern 7 only when you actually need conversation state

**Lesson**: Don't over-engineer. Start with simplest pattern (1), scale as needed.

### Pitfall 5: Ignoring Token Costs in Skills

❌ **Wrong**: Using Pattern 13 (complex reasoning, 2000+ tokens) for simple operations

✅ **Right**: Use Pattern 1 (600-1000 tokens) for straightforward routing

**Lesson**: Match pattern complexity to problem complexity. Simpler skills = lower cost.

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

This catalog focuses on **how Skills actively orchestrate MCP servers** to build intelligent agent systems.

**Key Takeaways**:

1. **Start with Pattern 1** (Skill-Guided MCP Tools)
   - Learn how Skills route requests to MCP tools
   - Foundation for all other patterns

2. **Graduate to Pattern 2** (Multi-MCP Orchestration) when you need multiple servers
   - Learn how Skills coordinate complex workflows
   - Real-world systems often need this pattern

3. **Add sophistication as needed**
   - Pattern 4: Trigger pre-built workflows
   - Pattern 7: Handle multi-turn conversations
   - Pattern 13: Guide complex reasoning
   - Pattern 11: Scale with multiple skills
   - Pattern 8: Build data pipelines

4. **Document your Skills effectively**
   - "When This Skill Activates" section is critical
   - Document orchestration steps explicitly
   - Show how the Skill uses MCP servers

**Remember**:
- Start simple. Scale as needed.
- The best pattern is the simplest one that solves your problem.
- Focus on how the Skill orchestrates, not just what it does.

**Your learning journey**:
Pattern 1 → Pattern 2 → (Pattern 4 or 7) → (Pattern 13 or 11) → Pattern 8

---

## Further Reading

- See `MCP_SERVER.md` for MCP implementation details
- See `SKILL_GUIDE.md` for skill development best practices
- See `SDK_USAGE.md` for integration examples
- See `EXAMPLES.md` for real-world code samples
