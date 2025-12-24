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
│  └─ Sequential? → Pattern 5: Data Pipeline
│
├─ Skill should TRIGGER pre-built workflows
│  └─ Pattern 3: MCP Prompts as Workflows
│
├─ Skill coordinates MULTIPLE SKILLS
│  └─ Pattern 6: Hierarchical Skills
│
├─ Skill needs to handle MULTI-TURN conversations
│  └─ Pattern 4: Stateful Conversation MCP
│
└─ Skill needs COMPLEX REASONING across steps
   └─ Pattern 7: Chain-of-Thought with MCP
```

---

## Pattern 1: Skill-Guided MCP Tools ⭐

**Status**: Implemented | **Complexity**: Medium | **Token Efficiency**: High

### Overview

A Claude Agent skill provides guidance that helps Claude automatically decide which MCP tools to use. The skill acts as an intelligent router, describing when and how to use each tool. Claude's inference layer handles tool selection and multi-step orchestration.

### Architecture Diagram

```
User Request (Natural Language)
       ↓
Claude Model + Skill Context
       ↓
Automatic Tool Selection
       ↓
[MCP Server Execution]
       ↓
Results → Formatted Response
```

### When to Use

✅ **Ideal for**:
- Natural language interfaces
- Multi-step workflows requiring intelligence
- User-defined workflows
- Task management, project planning, customer service

❌ **Avoid when**:
- Need 100% predictable tool execution
- Performance is critical (latency-sensitive)
- Building internal CLI tools

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | Medium | Skill design + MCP tools + SDK config |
| **Token Efficiency** | High | ~600-1000 tokens per operation |
| **Setup Effort** | Medium | Skill file, MCP server, configuration |
| **User Experience** | Excellent | Natural language, no memorization |

### Pros & Cons

**Pros**: Natural language, automatic intelligence, flexible workflows, self-documenting, multi-step automation

**Cons**: Added latency, higher token cost than direct calls, less control over execution path, requires good skill design

### Token Usage Analysis

**Typical Request**: "Create a project with 5 tasks, prioritize by date"

```
Skill context + request:         ~250 tokens
Claude reasoning:                ~150 tokens
Tool invocations (5 calls):      ~300 tokens
Results processing:              ~200 tokens
Final output:                    ~100 tokens
────────────────────────────────────────────
Total:                          ~1000 tokens
```

### Example Use Cases

1. **Task Management**: "Create a project for website redesign with 5 tasks"
   - Tools: create_project, create_task (5x)

2. **Analytics**: "Show me completion rate and top priority tasks"
   - Tools: task_statistics, filter_tasks

3. **Search**: "Find authentication bugs that are overdue"
   - Tools: search_tasks, filter_tasks, get_overdue_tasks

### Code Example

**Skill** (`.claude/skills/task-organizer/SKILL.md`):
```yaml
---
name: task-organizer
description: Manage tasks and projects. Create, filter by priority/status, track progress.
---

# Task Organizer

Operations: Create/update tasks, filter by priority/status/project, statistics, overdue items.
```

**SDK**:
```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["project"],
    allowed_tools=["Skill", "mcp__task-manager__*"],
    mcp_servers={"task-manager": task_server}
)

async for message in query(
    prompt="Create a task to review the PR",
    options=options
):
    print(message)
```

---

## Pattern 2: Multi-MCP Orchestration

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Integration-heavy systems

### Overview

Multiple MCP servers work together, coordinated by Claude and skills. Each MCP server handles a specific domain (database, API, files), and Claude orchestrates interactions between them based on skill guidance.

### Architecture Diagram

```
User Request
    ↓
[Orchestration Skill]
    ↓
Claude Intelligence Layer
  - Decides server sequence
  - Coordinates data flow
  - Handles cross-domain logic
    ↓
Parallel/Sequential Calls
  /        |         \
 ↓         ↓          ↓
[DB MCP] [API MCP] [File MCP]
```

### When to Use

✅ **Ideal for**:
- Systems with multiple data sources
- Complex integrations (database + API + files)
- Workflows spanning multiple domains
- Enterprise systems with specialized services

**Example scenarios**:
- E-commerce: Order MCP + Inventory MCP + Shipping MCP
- Data pipeline: Extract MCP + Transform MCP + Load MCP
- Backup system: Database MCP + Storage MCP + Notification MCP

❌ **Avoid when**:
- Single domain is sufficient
- Simple workflows
- Need minimal latency
- Limited token budget

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | Very High | Multiple servers, coordination logic |
| **Token Efficiency** | Medium | ~1000-1500 tokens per operation |
| **Setup Effort** | High | Configure multiple MCP servers |
| **Scalability** | Excellent | Easy to add new servers |
| **Reliability** | Medium | Depends on all servers being available |

### Pros & Cons

**Pros**: 
- Separation of concerns (each MCP = one domain)
- Reusable across applications
- Specialized servers optimized per domain
- Parallel execution possible
- Easy to add new servers

**Cons**: 
- Complex debugging (multiple failure points)
- All servers must be operational
- Higher token costs (~2x single MCP)
- Network/latency considerations
- Eventual consistency issues

### Token Usage Analysis

**Typical Request**: "Process order: check inventory, reserve items, create shipment"

```
Orchestration request:           ~200 tokens
Multi-server coordination:       ~500 tokens
  - Inventory check
  - Reservation logic
  - Shipment creation
Database operations:             ~150 tokens
External API calls:              ~200 tokens
Result synthesis:                ~150 tokens
────────────────────────────────────────────
Total:                          ~1200 tokens

(vs. single MCP: ~600 tokens)
Cost multiplier: ~2x
```

### Example Use Cases

1. **E-commerce Order Processing**
   - Request: "Process order #12345"
   - Servers: Inventory MCP (check stock) → Order MCP (create) → Shipping MCP (schedule)
   - Result: Complete order fulfillment

2. **Data Pipeline**
   - Request: "Generate quarterly sales report"
   - Servers: Database MCP (extract) → Analytics MCP (transform) → Export MCP (output)
   - Result: Formatted report file

3. **Backup & Recovery**
   - Request: "Backup production database"
   - Servers: Database MCP (backup) → Cloud MCP (upload) → Notify MCP (alert)
   - Result: Secure backup with confirmation

4. **Customer Support Integration**
   - Request: "Create ticket from email #567"
   - Servers: Email MCP (read) → CRM MCP (create ticket) → Notify MCP (alert team)
   - Result: Automated ticket creation

### Implementation Complexity

**Setup requirements**:
- Design skill to coordinate multiple servers
- Configure each MCP server independently
- Define data flow between servers
- Handle partial failures gracefully
- Test cross-server integration

**Maintenance considerations**:
- Monitor all server dependencies
- Update coordination logic as servers evolve
- Ensure data consistency across calls
- Track which server failed in errors
- Version compatibility management

**Testing strategy**:
- Test each MCP server independently
- Test skill coordination logic
- Test partial failure scenarios
- Test data flow between servers
- Integration tests with all servers

### Code Example

**Skill** (`.github/skills/ecommerce-orchestrator/SKILL.md`):
```yaml
---
name: ecommerce-orchestrator
description: Process orders using inventory, order, and shipping systems
---

# E-commerce Orchestrator

Coordinates multiple systems:
1. Check inventory availability
2. Create order and reserve items
3. Schedule shipment
4. Send confirmation

Use for: order processing, inventory management, shipment tracking
```

**SDK**:
```python
options = ClaudeAgentOptions(
    setting_sources=["project"],
    mcp_servers={
        "inventory": inventory_server,
        "orders": orders_server,
        "shipping": shipping_server
    }
)

async for msg in query(
    "Process order #12345 with priority shipping",
    options=options
):
    print(msg)
```

### Decision Checklist

Use this pattern if:
- [ ] You have 2+ distinct data domains
- [ ] Operations need data from multiple sources
- [ ] Each domain has specialized logic
- [ ] You can handle increased complexity
- [ ] Token cost increase is acceptable

Consider alternatives if:
- [ ] Single domain handles everything
- [ ] Coordination overhead not justified
- [ ] Need minimal latency
- [ ] Very limited token budget

---

## Pattern 3: MCP Prompts as Workflows

**Complexity**: Medium | **Token Efficiency**: High | **Recommended for**: Complex recurring operations

### Overview

MCP servers expose prompts (pre-written, structured workflows) that encode complex multi-step procedures. Skills trigger these prompts to execute complete workflows without orchestrating individual steps. Think of prompts as "macro commands" that bundle multiple operations.

### Architecture Diagram

```
User Request ("Weekly review")
    ↓
Skill Matches Request
    ↓
Triggers MCP Prompt
    ↓
┌─────────────────────────────┐
│ Workflow (server-side):     │
│ 1. Get statistics           │
│ 2. Identify bottlenecks     │
│ 3. Format report            │
│ 4. Generate summary         │
└─────────────────────────────┘
    ↓
Complete Report
```

### When to Use

✅ **Ideal for**:
- Recurring complex workflows with fixed steps
- Best practice procedures (code review, audit)
- Multi-step processes that rarely change
- Domain-specific standard operations
- Compliance/audit routines

**Example scenarios**:
- Weekly project review
- Code quality audit
- Security compliance check
- Onboarding checklist execution
- Release preparation workflow

❌ **Avoid when**:
- Workflows need dynamic adaptation
- Steps vary significantly per request
- Need fine-grained control over each step
- Workflows change frequently

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | Medium | Need to design MCP prompts |
| **Token Efficiency** | High | ~400-600 tokens (pre-built flow) |
| **Setup Effort** | Medium | Define prompts in MCP server |
| **Consistency** | Excellent | Same steps every time |
| **Flexibility** | Low | Fixed workflow structure |
| **Maintenance** | Low | Update prompt definition once |

### Pros & Cons

**Pros**: 
- Encodes domain expertise in MCP server
- Highly consistent, repeatable results
- Efficient token usage (workflow on server)
- Easy to understand and invoke
- Reduces coordination complexity in skills
- Clear audit trail

**Cons**: 
- Less flexible than building steps dynamically
- Requires predicting common workflows
- Changes require MCP server update
- Can't easily customize per-request
- Not suitable for ad-hoc workflows

### Token Usage Analysis

**Typical Request**: "Run weekly project review"

```
Request + skill activation:      ~150 tokens
Prompt invocation:               ~100 tokens
  - Trigger MCP prompt
  - Pass parameters
Workflow execution (server):     ~50 tokens
  - Statistics gathering
  - Analysis
  - Formatting
Results returned:                ~200 tokens
────────────────────────────────────────────
Total:                           ~500 tokens

(vs. orchestrating individually: ~1200 tokens)
Savings: ~58% fewer tokens
```

### Example Use Cases

1. **Weekly Project Review**
   - Prompt: `weekly_review`
   - Steps: Get task stats → Identify blockers → Generate report → Highlight priorities
   - Parameters: project_id, date_range
   - Result: Comprehensive project health report

2. **Code Quality Audit**
   - Prompt: `code_audit`
   - Steps: Run linters → Check test coverage → Analyze complexity → Generate recommendations
   - Parameters: repository, branch
   - Result: Quality scorecard with action items

3. **Security Compliance Check**
   - Prompt: `security_audit`
   - Steps: Check dependencies → Scan for vulnerabilities → Verify policies → Generate compliance report
   - Parameters: service_name, environment
   - Result: Compliance status with findings

4. **Release Preparation**
   - Prompt: `prepare_release`
   - Steps: Verify tests pass → Update changelog → Tag version → Generate notes
   - Parameters: version, release_date
   - Result: Release-ready package with documentation

### Implementation Complexity

**Setup requirements**:
- Design reusable workflow prompts in MCP
- Define clear prompt parameters
- Document expected inputs/outputs
- Create skill to invoke prompts
- Test prompt execution end-to-end

**MCP Prompt Definition Example**:
```json
{
  "prompts": {
    "weekly_review": {
      "description": "Generate weekly project review",
      "parameters": {
        "project_id": "string",
        "date_range": "string (e.g., 'last_7_days')"
      },
      "steps": [
        "Get task completion statistics",
        "Identify blocked tasks",
        "Calculate velocity trends",
        "Format comprehensive report"
      ]
    }
  }
}
```

**Maintenance considerations**:
- Update prompts as workflows evolve
- Version prompts for backward compatibility
- Monitor prompt usage and success rates
- Gather feedback on workflow effectiveness
- Refactor prompts that grow too complex

**Testing strategy**:
- Test each prompt with various parameters
- Verify all workflow steps execute
- Test error handling for failed steps
- Validate output format consistency
- Integration test with skill invocation

### Code Example

**MCP Server Prompt Configuration**:
```python
# In your MCP server
@server.prompt("weekly_review")
async def weekly_review_prompt(project_id: str, date_range: str):
    """Execute complete weekly review workflow"""
    
    # Step 1: Gather data
    stats = await get_task_statistics(project_id, date_range)
    blockers = await identify_blockers(project_id)
    
    # Step 2: Analyze
    trends = analyze_velocity(stats)
    priorities = calculate_priorities(blockers, stats)
    
    # Step 3: Format report
    report = format_review_report(stats, blockers, trends, priorities)
    
    return report
```

**Skill** (`.github/skills/project-reviewer/SKILL.md`):
```yaml
---
name: project-reviewer
description: Generate project reviews using pre-built workflows
---

# Project Reviewer

Triggers comprehensive review workflows:
- Weekly review: statistics, blockers, trends
- Sprint retrospective: velocity, completion, learnings
- Milestone report: progress, risks, timeline

Use when: Need standard project insights
```

**SDK Invocation**:
```python
# Skill automatically triggers the MCP prompt
async for msg in query(
    "Run weekly review for project Phoenix",
    options=options
):
    print(msg)

# Behind the scenes:
# Skill activates → Invokes MCP prompt 'weekly_review'
# → Workflow executes server-side → Returns complete report
```

### Decision Checklist

Use this pattern if:
- [ ] You have recurring, well-defined workflows
- [ ] Workflow steps are consistent
- [ ] Need high consistency across executions
- [ ] Token efficiency is important
- [ ] Domain expertise can be encoded upfront

Consider alternatives if:
- [ ] Workflows vary significantly per request
- [ ] Need dynamic step adaptation
- [ ] Ad-hoc operations are common
- [ ] Steps change frequently

---

## Pattern 4: Stateful Conversation MCP

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Long multi-turn interactions

### Overview

MCP server maintains state across conversation turns, enabling context-aware interactions without resending full history. The server acts as a memory layer, storing conversation state, user preferences, and intermediate results. Skills can reference and update this state across multiple turns.

### Architecture Diagram

```
Turn 1: User request
    ↓
Skill activates → MCP stores context
    ↓
Turn 2: Follow-up request (references state)
    ↓
Skill activates → MCP retrieves + updates state
    ↓
Turn 3+: Continue with preserved context
    ↓
MCP maintains full conversation state
```

### When to Use

✅ **Ideal for**:
- Multi-turn debugging sessions
- Iterative design and refinement
- Conversations requiring memory
- Progressive problem-solving workflows
- Code review discussions
- Tutoring or learning sessions

**Example scenarios**:
- Debugging: "Show error" → "Try fix A" → "That worked, now optimize"
- Design iteration: "Sketch UI" → "Add animation" → "Adjust colors"
- Learning: "Explain concept" → "Give example" → "Test my understanding"

❌ **Avoid when**:
- Single-turn operations sufficient
- State doesn't provide value
- Synchronization is too complex
- Storage overhead not justified

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | High | State management + sync logic |
| **Token Efficiency** | Medium | ~700-1200 tokens per turn |
| **Setup Effort** | High | Design state schema + persistence |
| **Context Preservation** | Excellent | Full conversation memory |
| **User Experience** | Excellent | Natural, continuous dialogue |
| **Reliability** | Medium | State sync can be challenging |

### Pros & Cons

**Pros**: 
- Persistent context across conversation turns
- Better UX for iterative tasks
- Reduces token usage for repeated context
- Enables complex multi-step workflows
- Natural conversation flow
- Can reference earlier discussion points

**Cons**: 
- State management complexity
- Synchronization challenges (race conditions)
- Storage requirements
- State cleanup needed
- Harder debugging (state-dependent)
- Versioning state schema is tricky

### Token Usage Analysis

**Typical Multi-Turn Session**: "Debug API error" → "Try solution A" → "Test it" → "Refine"

```
Turn 1 (Initial):
  Request + context:             ~200 tokens
  State initialization:          ~100 tokens
  Response:                      ~150 tokens
  Subtotal:                      ~450 tokens

Turn 2 (Follow-up):
  Request:                       ~50 tokens
  State retrieval:               ~100 tokens
  State update:                  ~100 tokens
  Response:                      ~150 tokens
  Subtotal:                      ~400 tokens

Turn 3-5 (Continuation):
  Each turn:                     ~400 tokens
────────────────────────────────────────────
Total session (5 turns):        ~2050 tokens

Without state (resending context):
  Each turn:                     ~600 tokens
  Total session (5 turns):       ~3000 tokens

Savings: ~32% fewer tokens
```

### Example Use Cases

1. **Interactive Debugging Session**
   - Turn 1: "Show me the authentication error logs"
     - State: Store error context, stack trace, user session
   - Turn 2: "Try the JWT refresh workaround"
     - State: Track attempted solutions, results
   - Turn 3: "That worked! Now let's add logging"
     - State: Update to resolved, add enhancement tracking
   - Result: Continuous debugging without re-explaining context

2. **Iterative UI Design**
   - Turn 1: "Design a product card component"
     - State: Store design spec, current version
   - Turn 2: "Add hover animations"
     - State: Update design with animation details
   - Turn 3: "Adjust spacing and colors for dark mode"
     - State: Evolve design, track changes
   - Result: Progressive refinement with full history

3. **Code Review Discussion**
   - Turn 1: "Review this pull request"
     - State: PR details, file changes, initial comments
   - Turn 2: "Focus on the security concerns"
     - State: Filtered view, security findings
   - Turn 3: "Suggest fixes for the SQL injection risk"
     - State: Specific issue + fix recommendations
   - Result: Deep-dive review maintaining full context

4. **Learning Tutorial Session**
   - Turn 1: "Explain async/await in Python"
     - State: Concept, user's knowledge level
   - Turn 2: "Show me an example with error handling"
     - State: Add example code, track progression
   - Turn 3: "Quiz me on what I learned"
     - State: Assessment based on session content
   - Result: Personalized learning progression

### Implementation Complexity

**Setup requirements**:
- Design state schema (what to store, structure)
- Implement state persistence (in-memory, database, cache)
- Handle state initialization and cleanup
- Add state versioning for schema changes
- Implement state retrieval and updates
- Create state expiration/garbage collection

**State Schema Example**:
```python
class ConversationState:
    conversation_id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    # Domain-specific state
    context: Dict[str, Any]  # Current focus/context
    history: List[TurnState]  # Past turns
    artifacts: Dict[str, Any]  # Generated content
    
    # Metadata
    skill_name: str
    current_task: Optional[str]
    preferences: Dict[str, Any]
```

**Maintenance considerations**:
- Monitor state storage usage
- Implement state expiration policies
- Handle state migration for schema changes
- Debug state synchronization issues
- Clean up abandoned conversations
- Ensure state privacy/isolation per user

**Testing strategy**:
- Test state initialization
- Test state persistence across turns
- Test state retrieval accuracy
- Test concurrent state updates
- Test state cleanup/expiration
- Integration test full conversation flows

### Code Example

**MCP Server with State Management**:
```python
from typing import Dict, Any
import asyncio

class StatefulMCPServer:
    def __init__(self):
        self.conversations: Dict[str, ConversationState] = {}
    
    @server.tool("store_context")
    async def store_context(
        self,
        conversation_id: str,
        key: str,
        value: Any
    ):
        """Store context for this conversation"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationState()
        
        state = self.conversations[conversation_id]
        state.context[key] = value
        state.updated_at = datetime.now()
        
        return {"stored": True, "key": key}
    
    @server.tool("retrieve_context")
    async def retrieve_context(
        self,
        conversation_id: str,
        key: Optional[str] = None
    ):
        """Retrieve stored context"""
        if conversation_id not in self.conversations:
            return {"error": "No state found"}
        
        state = self.conversations[conversation_id]
        if key:
            return state.context.get(key)
        return state.context
    
    @server.tool("update_history")
    async def update_history(
        self,
        conversation_id: str,
        turn_data: Dict[str, Any]
    ):
        """Add to conversation history"""
        state = self.conversations[conversation_id]
        state.history.append(TurnState(**turn_data))
        return {"updated": True}
```

**Skill** (`.github/skills/debugging-assistant/SKILL.md`):
```yaml
---
name: debugging-assistant
description: Interactive debugging with conversation memory. Maintains context across turns for iterative problem-solving.
---

# Debugging Assistant

Supports multi-turn debugging:
1. Initial problem analysis (stores context)
2. Iterative solution attempts (tracks attempts)
3. Testing and refinement (maintains full history)

Automatically stores:
- Error details and stack traces
- Attempted solutions
- Test results
- Conversation context

Use for: complex debugging requiring multiple attempts
```

**SDK Usage**:
```python
# Turn 1
conversation_id = "debug-session-123"

async for msg in query(
    "Debug the authentication timeout error",
    options=options,
    metadata={"conversation_id": conversation_id}
):
    print(msg)

# Behind the scenes:
# Skill activates → Stores error details in MCP state

# Turn 2 (minutes later, same session)
async for msg in query(
    "Try increasing the token expiration time",
    options=options,
    metadata={"conversation_id": conversation_id}
):
    print(msg)

# Skill retrieves stored context → Applies solution → Updates state
```

### Decision Checklist

Use this pattern if:
- [ ] Multi-turn interactions are common
- [ ] Context preservation adds value
- [ ] Users expect continuous dialogue
- [ ] Iterative refinement is needed
- [ ] You can handle state management complexity

Consider alternatives if:
- [ ] Most operations are single-turn
- [ ] State doesn't provide clear value
- [ ] Synchronization is too complex
- [ ] Storage overhead not justified

---

## Pattern 5: Data Pipeline Pattern

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: ETL and data processing

### Overview

Sequential orchestration of multiple MCP servers forming a data processing pipeline. Data flows through stages of extraction, transformation, and loading, with each MCP server handling a specific transformation stage. Skills orchestrate the pipeline execution and handle data flow between stages.

### Architecture Diagram

```
Input Data Source
    ↓
[Extract MCP]
  - Read from source
  - Initial validation
    ↓
[Transform MCP]
  - Clean data
  - Apply business logic
  - Enrich data
    ↓
[Load MCP]
  - Format for destination
  - Write to target
  - Verify completion
    ↓
Output Data Destination
```

### When to Use

✅ **Ideal for**:
- ETL (Extract, Transform, Load) processes
- Data migration between systems
- Report generation from multiple sources
- Batch data processing workflows
- Data warehouse updates
- Analytics pipeline automation

**Example scenarios**:
- Migrate customer data from legacy DB to new system
- Generate daily sales reports from transactions
- Process log files and store analytics
- Sync data between microservices
- Aggregate metrics for dashboards

❌ **Avoid when**:
- Real-time processing required (use streaming instead)
- Simple single-stage transformations
- Data fits in single MCP operation
- Need bidirectional data flow

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | High | Multiple servers + data flow logic |
| **Token Efficiency** | Medium | ~1200-1800 tokens per pipeline |
| **Setup Effort** | High | Configure each stage + orchestration |
| **Scalability** | High | Easy to add pipeline stages |
| **Performance** | Good | Sequential processing |
| **Error Recovery** | Complex | Need checkpoints/rollback |

### Pros & Cons

**Pros**: 
- Clear separation of concerns per stage
- Reusable pipeline components
- Easy to test individual stages
- Scales by adding stages
- Can optimize each stage independently
- Good for batch processing
- Audit trail of transformations

**Cons**: 
- Sequential bottleneck (one stage at a time)
- Complex error handling (partial failures)
- Longer overall latency
- Checkpoint/rollback complexity
- Data format compatibility between stages
- Higher token cost than single operation

### Token Usage Analysis

**Typical Pipeline**: Extract sales data → Transform/aggregate → Load to warehouse

```
Pipeline initialization:         ~150 tokens
  - Setup pipeline context
  - Configure stages

Stage 1 (Extract):
  - Read from source DB:         ~300 tokens
  - Validate data:               ~100 tokens

Stage 2 (Transform):
  - Apply business rules:        ~400 tokens
  - Aggregate metrics:           ~200 tokens
  - Enrich with lookups:         ~150 tokens

Stage 3 (Load):
  - Format for warehouse:        ~200 tokens
  - Write to destination:        ~250 tokens
  - Verify completion:           ~100 tokens

Result summary:                  ~150 tokens
────────────────────────────────────────────
Total:                          ~2000 tokens

(vs. manual multi-step: ~2800 tokens)
Savings: ~29% fewer tokens
```

### Example Use Cases

1. **Daily Sales Report Generation**
   - Extract: Pull transactions from DB (last 24 hours)
   - Transform: Calculate totals, group by product/region
   - Load: Generate formatted report, email to stakeholders
   - Result: Automated daily sales insights

2. **Customer Data Migration**
   - Extract: Read customer records from legacy system
   - Transform: Map to new schema, validate fields, deduplicate
   - Load: Insert into new CRM, verify integrity
   - Result: Clean migrated customer database

3. **Log Analytics Processing**
   - Extract: Read application logs from S3
   - Transform: Parse errors, aggregate by type, calculate metrics
   - Load: Store in analytics DB, update dashboards
   - Result: Real-time error monitoring

4. **Data Warehouse ETL**
   - Extract: Pull from multiple microservice databases
   - Transform: Join datasets, apply business logic, normalize
   - Load: Bulk insert into data warehouse
   - Result: Consolidated analytics data

### Implementation Complexity

**Setup requirements**:
- Design pipeline stages and data flow
- Implement each MCP server (extract, transform, load)
- Define data format between stages
- Add checkpointing for error recovery
- Implement rollback mechanisms
- Create skill to orchestrate pipeline

**Pipeline Orchestration Pattern**:
```python
class PipelineStage:
    name: str
    mcp_server: str
    tool: str
    input_format: str
    output_format: str
    
class Pipeline:
    stages: List[PipelineStage]
    
    async def execute(self, input_data):
        data = input_data
        
        for stage in self.stages:
            # Execute stage
            data = await execute_stage(stage, data)
            
            # Checkpoint
            await checkpoint(stage.name, data)
            
            # Validate output format
            validate_format(data, stage.output_format)
        
        return data
```

**Maintenance considerations**:
- Monitor pipeline execution times
- Track failure rates per stage
- Optimize bottleneck stages
- Version data formats between stages
- Handle schema evolution
- Clean up failed pipeline runs

**Testing strategy**:
- Test each stage independently with mock data
- Integration test full pipeline
- Test error scenarios (stage failures)
- Test checkpoint/recovery mechanisms
- Validate data format conversions
- Load test with production-scale data

### Code Example

**Pipeline Skill** (`.github/skills/data-pipeline/SKILL.md`):
```yaml
---
name: data-pipeline
description: Execute multi-stage data pipelines (extract, transform, load)
---

# Data Pipeline Orchestrator

Coordinates data processing through stages:
1. Extract: Read from source systems
2. Transform: Apply business logic, clean, aggregate
3. Load: Write to destination systems

Handles: checkpointing, error recovery, format validation

Use for: ETL jobs, data migration, report generation, batch processing
```

**Pipeline MCP Servers**:
```python
# Extract MCP
@server.tool("extract_from_source")
async def extract_from_source(source: str, query: dict):
    """Extract data from source system"""
    data = await read_from_database(source, query)
    return {"data": data, "count": len(data)}

# Transform MCP
@server.tool("transform_data")
async def transform_data(data: list, rules: dict):
    """Apply transformations to data"""
    cleaned = clean_data(data)
    aggregated = aggregate_data(cleaned, rules)
    enriched = enrich_data(aggregated)
    return {"transformed": enriched}

# Load MCP
@server.tool("load_to_destination")
async def load_to_destination(data: list, destination: str):
    """Load data to destination system"""
    formatted = format_for_destination(data, destination)
    result = await write_to_destination(formatted, destination)
    return {"loaded": result["count"], "success": True}
```

**SDK Usage**:
```python
options = ClaudeAgentOptions(
    setting_sources=["project"],
    mcp_servers={
        "extractor": extract_server,
        "transformer": transform_server,
        "loader": load_server
    }
)

async for msg in query(
    "Run daily sales ETL: extract from transactions DB, aggregate by region, load to warehouse",
    options=options
):
    print(msg)

# Skill orchestrates: extract → transform → load
```

### Decision Checklist

Use this pattern if:
- [ ] You have multi-stage data processing needs
- [ ] Clear separation between extract/transform/load
- [ ] Batch processing is acceptable
- [ ] Need reusable pipeline components
- [ ] Data flows sequentially through stages

Consider alternatives if:
- [ ] Real-time processing required
- [ ] Simple single-stage transformation
- [ ] Need bidirectional data flow
- [ ] Complexity not justified

---

## Pattern 6: Hierarchical Skills

**Status**: Implemented | **Complexity**: Medium | **Token Efficiency**: High | **Recommended for**: Large-scale systems

### Overview

Parent skills delegate to specialized child skills, creating a hierarchy of expertise. This pattern enables modular organization of complex systems where different skills handle different sub-domains. The parent skill acts as a router, determining which child skill should handle each request.

### Implementation Reference

**Example**: Text Analysis System (Pure Prompt Skills)
- **Location**: `.github/skills/`
  - `text-analyzer/` - Parent skill coordinating analysis tasks
  - `grammar-checker/` - Child skill for grammar/spelling/punctuation
  - `sentiment-analyzer/` - Child skill for emotional tone analysis
  - `readability-scorer/` - Child skill for readability metrics
  - `seo-optimizer/` - Child skill for SEO optimization

- **Key Feature**: Pure prompt-based skills (no MCP dependencies)
- **Use Case**: Demonstrates hierarchical skill delegation for language processing tasks
- **Documentation**: See `Pattern6_HierarchicalSkills_SAMPLE.md` for complete design guide

### Architecture Diagram

```
User Request (Complex, multi-domain)
    ↓
[Parent Skill: System Orchestrator]
  - Analyzes request
  - Routes to appropriate child
    ↓
    /         |         \
   ↓          ↓          ↓
[Child     [Child     [Child
Skill:     Skill:     Skill:
Orders]    Inventory] Shipping]
   ↓          ↓          ↓
Order      Inventory  Shipping
MCP        MCP        MCP
```

### When to Use

✅ **Ideal for**:
- Large applications (100+ operations)
- Multi-domain systems (e-commerce, enterprise)
- Team-based development (each team owns skills)
- Modular architectures
- Systems with clear sub-domains
- Microservices coordination

**Example scenarios**:
- E-commerce platform: Orders + Inventory + Shipping + Payments
- Healthcare system: Patients + Appointments + Billing + Records
- DevOps platform: Deploy + Monitor + Alerts + Rollback
- CRM: Leads + Contacts + Deals + Support

❌ **Avoid when**:
- Simple single-domain application
- Few operations (< 20 tools)
- No clear sub-domain boundaries
- Team structure doesn't support it

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | Medium | Parent-child coordination |
| **Token Efficiency** | High | ~600-1000 tokens (similar to single skill) |
| **Setup Effort** | Medium | Design hierarchy + multiple skills |
| **Maintainability** | Excellent | Modular, isolated changes |
| **Scalability** | Excellent | Easy to add new child skills |
| **Team Collaboration** | Excellent | Teams own their skills |

### Pros & Cons

**Pros**: 
- Clear separation of responsibilities
- Easy to add new domains (add child skill)
- Teams can own their skill domains
- Reduces individual skill complexity
- Better organization for large systems
- Easier testing (test each skill independently)
- Parallel development possible

**Cons**: 
- Additional routing overhead (parent decides)
- Need clear domain boundaries
- Can over-complicate simple systems
- Coordination between parent-child
- More files to maintain

### Token Usage Analysis

**Typical Request**: "Process order #123: check inventory, reserve items, create shipment"

```
Parent skill activation:         ~150 tokens
  - Analyze request
  - Determine child skills needed
  
Child skill 1 (Inventory):
  - Check stock:                 ~200 tokens
  - Reserve items:               ~150 tokens

Child skill 2 (Orders):
  - Create order:                ~200 tokens

Child skill 3 (Shipping):
  - Schedule shipment:           ~200 tokens

Result synthesis:                ~100 tokens
────────────────────────────────────────────
Total:                          ~1000 tokens

(vs. single monolithic skill: ~1000 tokens)
Token usage: Similar, but better organized
```

### Example Use Cases

1. **E-commerce Platform**
   - Parent: `ecommerce-orchestrator`
   - Children: `order-manager`, `inventory-manager`, `shipping-coordinator`, `payment-processor`
   - Request: "Process order with express shipping"
   - Flow: Parent → Order child (create) → Inventory child (reserve) → Shipping child (schedule)
   - Result: Complete order processing

2. **DevOps Platform**
   - Parent: `devops-orchestrator`
   - Children: `deployment-manager`, `monitoring-manager`, `alert-manager`, `rollback-handler`
   - Request: "Deploy v2.0 to production with monitoring"
   - Flow: Parent → Deploy child → Monitor child → Alert child (if issues)
   - Result: Deployed and monitored release

3. **Healthcare System**
   - Parent: `healthcare-coordinator`
   - Children: `patient-manager`, `appointment-scheduler`, `billing-processor`, `records-manager`
   - Request: "Schedule follow-up appointment and update billing"
   - Flow: Parent → Appointment child → Billing child → Records child
   - Result: Complete patient workflow

4. **CRM System**
   - Parent: `crm-orchestrator`
   - Children: `lead-manager`, `contact-manager`, `deal-manager`, `support-manager`
   - Request: "Convert lead to contact and create deal"
   - Flow: Parent → Lead child (convert) → Contact child (create) → Deal child (create)
   - Result: Lead progression through pipeline

### Implementation Complexity

**Setup requirements**:
- Design skill hierarchy (parent + children)
- Define clear domain boundaries
- Create parent routing logic
- Implement each child skill independently
- Configure skill discovery
- Test parent-child coordination

**Hierarchy Design Pattern**:
```
Parent Skill:
  - Broad description covering all domains
  - "When to activate": Any cross-domain request
  - Documents which child skills it delegates to
  
Child Skills:
  - Specific description for one domain
  - "When to activate": Domain-specific requests
  - Independent of other child skills
```

**Maintenance considerations**:
- Update parent when adding child skills
- Keep child skills independent
- Version child skills separately
- Monitor routing decisions
- Document domain boundaries clearly

**Testing strategy**:
- Test each child skill independently
- Test parent routing logic
- Integration test parent + children
- Test cross-domain workflows
- Verify skill activation patterns

### Code Example

**Parent Skill** (`.github/skills/ecommerce-orchestrator/SKILL.md`):
```yaml
---
name: ecommerce-orchestrator
description: Coordinate e-commerce operations across orders, inventory, shipping, payments
---

# E-commerce Orchestrator

Parent skill that delegates to specialized child skills:
- `order-manager`: Create, update, cancel orders
- `inventory-manager`: Check stock, reserve items
- `shipping-coordinator`: Schedule, track shipments
- `payment-processor`: Process payments, refunds

Use for: any e-commerce operation spanning multiple domains
```

**Child Skill 1** (`.github/skills/order-manager/SKILL.md`):
```yaml
---
name: order-manager
description: Manage customer orders (create, update, cancel, refund)
---

# Order Manager

Handles all order operations using order-service MCP.

Operations: create order, update status, cancel, refund, get details

Use when: request mentions orders, purchases, refunds
```

**Child Skill 2** (`.github/skills/inventory-manager/SKILL.md`):
```yaml
---
name: inventory-manager
description: Manage inventory (check stock, reserve, release items)
---

# Inventory Manager

Handles inventory operations using inventory-service MCP.

Operations: check stock levels, reserve items, release reservations

Use when: request mentions inventory, stock, availability
```

**SDK Usage**:
```python
options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads all skills
    mcp_servers={
        "order-service": order_server,
        "inventory-service": inventory_server,
        "shipping-service": shipping_server
    }
)

# Complex cross-domain request
async for msg in query(
    "Process order #123: check if items are in stock, create order, schedule express shipping",
    options=options
):
    print(msg)

# Flow:
# 1. Parent skill activates (cross-domain request)
# 2. Delegates to inventory-manager (check stock)
# 3. Delegates to order-manager (create order)
# 4. Delegates to shipping-coordinator (schedule)
```

### Decision Checklist

Use this pattern if:
- [ ] System has 3+ clear sub-domains
- [ ] 50+ total operations across domains
- [ ] Multiple teams developing features
- [ ] Need modular architecture
- [ ] Want independent skill evolution

Consider alternatives if:
- [ ] Simple single-domain system
- [ ] Fewer than 20 operations total
- [ ] No clear domain boundaries
- [ ] Single team, simple coordination

---

## Pattern 7: Chain-of-Thought with MCP

**Complexity**: High | **Token Efficiency**: Medium | **Recommended for**: Complex problem-solving

### Overview

Skills guide Claude through multi-step reasoning processes, using different MCP tools at each phase (analysis, design, implementation, verification). This pattern breaks complex problems into explicit thinking stages, with each stage potentially using different MCP servers or tools.

### Architecture Diagram

```
Complex Problem
    ↓
[Phase 1: Analyze]
  - Problem analysis MCP
  - Gather context/data
    ↓
[Phase 2: Design]
  - Design tools MCP
  - Propose solutions
    ↓
[Phase 3: Implement]
  - Implementation MCP
  - Execute solution
    ↓
[Phase 4: Verify]
  - Validation MCP
  - Test and confirm
    ↓
Validated Solution
```

### When to Use

✅ **Ideal for**:
- Complex problem-solving requiring explicit reasoning
- Architecture design decisions
- Multi-phase projects (design → implement → test)
- Research and analysis workflows
- Scientific computing
- Systems requiring audit trails of reasoning

**Example scenarios**:
- Design new system architecture
- Debug complex multi-component failures
- Research and analysis projects
- Optimization problems
- Strategic planning
- Root cause analysis

❌ **Avoid when**:
- Simple straightforward operations
- Speed is critical (reasoning adds latency)
- Problem doesn't benefit from explicit phases
- Token budget is extremely limited

### Characteristics

| Aspect | Rating | Details |
|--------|--------|---------|
| **Complexity** | High | Multi-phase orchestration + reasoning |
| **Token Efficiency** | Medium | ~1500-2500 tokens (reasoning overhead) |
| **Setup Effort** | High | Design phases + appropriate tools |
| **Solution Quality** | Excellent | Structured reasoning → better results |
| **Explainability** | Excellent | Clear reasoning trail |
| **Reliability** | High | Validates at each phase |

### Pros & Cons

**Pros**: 
- Higher quality solutions (structured thinking)
- Clear audit trail of reasoning
- Catches errors early (validates per phase)
- Easier to debug (see which phase failed)
- Better for complex problems
- Explainable AI (show reasoning steps)
- Can iterate on individual phases

**Cons**: 
- Higher token costs (reasoning overhead)
- Longer latency (multiple phases)
- Over-engineering for simple problems
- Requires careful phase design
- More complex error handling

### Token Usage Analysis

**Typical Request**: "Design and implement a caching system for our API"

```
Phase 1 (Analyze):
  - Problem understanding:       ~300 tokens
  - Requirements gathering:      ~200 tokens
  - Context from analysis MCP:   ~200 tokens

Phase 2 (Design):
  - Generate design options:     ~400 tokens
  - Evaluate tradeoffs:          ~300 tokens
  - Design tools MCP:            ~200 tokens

Phase 3 (Implement):
  - Create implementation:       ~500 tokens
  - Implementation MCP calls:    ~300 tokens

Phase 4 (Verify):
  - Validation checks:           ~200 tokens
  - Testing MCP:                 ~200 tokens

Phase coordination:              ~200 tokens
────────────────────────────────────────────
Total:                          ~2800 tokens

(vs. direct implementation: ~1200 tokens)
Cost: ~2.3x more, but higher quality
```

### Example Use Cases

1. **System Architecture Design**
   - Phase 1 (Analyze): Gather requirements, analyze constraints
     - Tools: requirements_analyzer, constraint_checker
   - Phase 2 (Design): Propose architectures, evaluate tradeoffs
     - Tools: architecture_designer, tradeoff_evaluator
   - Phase 3 (Implement): Create design documents, diagrams
     - Tools: doc_generator, diagram_creator
   - Phase 4 (Verify): Review against requirements, validate
     - Tools: requirement_validator, architecture_reviewer
   - Result: Well-reasoned, validated architecture

2. **Complex Bug Investigation**
   - Phase 1 (Analyze): Gather logs, reproduce issue
     - Tools: log_analyzer, reproduction_tester
   - Phase 2 (Design): Hypothesize root causes
     - Tools: hypothesis_generator, code_analyzer
   - Phase 3 (Implement): Create and test fixes
     - Tools: code_patcher, test_runner
   - Phase 4 (Verify): Confirm fix, check side effects
     - Tools: regression_tester, impact_analyzer
   - Result: Thoroughly investigated and fixed bug

3. **Performance Optimization**
   - Phase 1 (Analyze): Profile system, identify bottlenecks
     - Tools: profiler, bottleneck_detector
   - Phase 2 (Design): Propose optimizations
     - Tools: optimization_suggester, benchmark_estimator
   - Phase 3 (Implement): Apply optimizations
     - Tools: code_optimizer, config_updater
   - Phase 4 (Verify): Benchmark improvements
     - Tools: benchmark_runner, performance_validator
   - Result: Data-driven performance improvements

4. **Research Project**
   - Phase 1 (Analyze): Literature review, problem scoping
     - Tools: paper_search, citation_analyzer
   - Phase 2 (Design): Methodology design
     - Tools: experiment_designer, hypothesis_formulator
   - Phase 3 (Implement): Run experiments, collect data
     - Tools: experiment_runner, data_collector
   - Phase 4 (Verify): Analyze results, validate conclusions
     - Tools: statistical_analyzer, result_validator
   - Result: Rigorous research with clear methodology

### Implementation Complexity

**Setup requirements**:
- Design clear phase definitions
- Select appropriate MCP tools per phase
- Create skill with phase orchestration
- Define phase transitions
- Add validation gates between phases
- Implement rollback for failed phases

**Phase Design Pattern**:
```yaml
Phase Structure:
  name: Phase name
  goal: What this phase achieves
  tools: MCP tools to use
  outputs: What this phase produces
  validation: How to verify success
  next_phase: Which phase follows
```

**Maintenance considerations**:
- Monitor phase execution times
- Track which phases fail most often
- Optimize bottleneck phases
- Update validation criteria
- Refine phase transitions
- Balance thoroughness vs. speed

**Testing strategy**:
- Test each phase independently
- Test phase transitions
- Test validation gates
- Test rollback scenarios
- Integration test full chain
- Validate reasoning quality

### Code Example

**Chain-of-Thought Skill** (`.github/skills/architecture-designer/SKILL.md`):
```yaml
---
name: architecture-designer
description: Design system architectures using structured reasoning (analyze → design → implement → verify)
---

# Architecture Designer

Multi-phase architecture design:

Phase 1 (Analyze): Understand requirements and constraints
  - Gather functional requirements
  - Identify technical constraints
  - Analyze current system (if exists)

Phase 2 (Design): Propose and evaluate architectures
  - Generate design options
  - Evaluate tradeoffs
  - Select recommended approach

Phase 3 (Implement): Create design artifacts
  - Write architecture document
  - Generate diagrams
  - Document decisions

Phase 4 (Verify): Validate against requirements
  - Check requirement coverage
  - Validate design decisions
  - Review with stakeholders

Use for: complex system design requiring structured thinking
```

**MCP Tools for Each Phase**:
```python
# Phase 1: Analysis Tools
@server.tool("analyze_requirements")
async def analyze_requirements(description: str):
    """Extract and structure requirements"""
    return extract_requirements(description)

@server.tool("check_constraints")
async def check_constraints(requirements: dict):
    """Identify technical constraints"""
    return identify_constraints(requirements)

# Phase 2: Design Tools
@server.tool("generate_design_options")
async def generate_design_options(requirements: dict):
    """Propose architecture options"""
    return create_architecture_options(requirements)

@server.tool("evaluate_tradeoffs")
async def evaluate_tradeoffs(options: list):
    """Analyze pros/cons of each option"""
    return evaluate_options(options)

# Phase 3: Implementation Tools
@server.tool("create_architecture_doc")
async def create_architecture_doc(design: dict):
    """Generate architecture document"""
    return generate_doc(design)

# Phase 4: Verification Tools
@server.tool("validate_design")
async def validate_design(design: dict, requirements: dict):
    """Verify design meets requirements"""
    return validate_coverage(design, requirements)
```

**SDK Usage**:
```python
async for msg in query(
    "Design a caching system for our API with Redis, handling 10K req/s",
    options=options
):
    print(msg)

# Skill orchestrates phases:
# 1. Analyze: extract requirements, constraints
# 2. Design: propose architectures, evaluate
# 3. Implement: create docs and diagrams
# 4. Verify: validate against requirements
```

### Decision Checklist

Use this pattern if:
- [ ] Problem is genuinely complex
- [ ] Structured reasoning improves quality
- [ ] Need explainable reasoning trail
- [ ] Quality more important than speed
- [ ] Can afford higher token costs

Consider alternatives if:
- [ ] Problem is straightforward
- [ ] Speed is critical
- [ ] Token budget is very limited
- [ ] Simpler pattern works fine

---

## Skills-Centric Pattern Comparison Matrix

| Pattern | Complexity | Token Efficiency | Skill's Role | Best For |
|---------|------------|------------------|-------------|----------|
| 1. Skill-Guided MCP Tools | Medium | High (~600-1000) | Routes to ONE MCP | Single-domain apps |
| 2. Multi-MCP Orchestration | Very High | Medium (~1000-1500) | Coordinates MULTIPLE MCPs | Integration-heavy |
| 3. MCP Prompts as Workflows | Medium | High (~400-600) | Triggers workflows | Recurring operations |
| 4. Stateful Conversation | High | Medium (~700-1200) | Manages state | Multi-turn dialogue |
| 5. Data Pipeline | High | Medium (~1200-1800) | Orchestrates data flow | ETL/batch processing |
| 6. Hierarchical Skills | Medium | High (~600-1000) | Delegates to children | Large-scale systems |
| 7. Chain-of-Thought | High | Medium (~1500-2500) | Guides reasoning | Complex problems |

---

## Skills-Centric Decision Framework

### Question 1: How many MCP servers should your Skill coordinate?

- **One MCP server** → Pattern 1: Skill-Guided MCP Tools
- **Multiple MCP servers** → Continue to Question 2

### Question 2: What type of data flow does your Skill need?

- **Real-time parallel/mixed** → Pattern 2: Multi-MCP Orchestration
- **Sequential pipeline** → Pattern 5: Data Pipeline
- **Pre-built workflows** → Pattern 3: MCP Prompts as Workflows

### Question 3: Does your Skill need conversation context?

- **Single-turn** → Use pattern from above
- **Multi-turn** → Pattern 4: Stateful Conversation

### Question 4: How complex is your skill system?

- **Single Skill** → Use pattern from above
- **Multiple coordinated Skills** → Pattern 6: Hierarchical Skills

### Question 5: Does your Skill need complex reasoning?

- **Straightforward** → Use pattern from above
- **Multi-step problem solving** → Pattern 7: Chain-of-Thought

---

## Token Efficiency Ranking

From most to least efficient:

```
1. Pattern 3 (Prompts as Workflows)  ~400-600 tokens   ⚡⚡⚡
2. Pattern 1 (Skill-Guided MCP)      ~600-1000 tokens  ⚡⚡⚡
3. Pattern 6 (Hierarchical Skills)   ~600-1000 tokens  ⚡⚡⚡
4. Pattern 4 (Stateful Conversation) ~700-1200 tokens  ⚡⚡
5. Pattern 2 (Multi-MCP)             ~1000-1500 tokens ⚡⚡
6. Pattern 5 (Data Pipeline)         ~1200-1800 tokens ⚡
7. Pattern 7 (Chain-of-Thought)      ~1500-2500 tokens ⚡
```

---

## Complexity Ranking

From simplest to most complex:

```
1. Pattern 1 (Skill-Guided MCP) - Single MCP routing
2. Pattern 3 (Prompts as Workflows) - Trigger workflows
3. Pattern 6 (Hierarchical Skills) - Delegate to children
4. Pattern 4 (Stateful Conversation) - State management
5. Pattern 5 (Data Pipeline) - Sequential orchestration
6. Pattern 2 (Multi-MCP Orchestration) - Multiple servers
7. Pattern 7 (Chain-of-Thought) - Multi-phase reasoning
```

---

## Implementation Roadmap

### Phase 1: Foundations (Week 1-2)
**Goal**: Master single-skill, single-MCP patterns

1. **Pattern 1** (Skill-Guided MCP Tools) ⭐ START HERE
   - Build: Simple task manager
   - Learn: Skill activation, tool routing
   - Deliverable: Working single-domain skill

### Phase 2: Multiple MCPs (Week 3-4)
**Goal**: Coordinate multiple servers

2. **Pattern 2** (Multi-MCP Orchestration)
   - Build: Multi-domain workflow (e.g., e-commerce)
   - Learn: Cross-server coordination
   - Deliverable: Skill orchestrating 2-3 MCPs

3. **Pattern 3** (MCP Prompts as Workflows)
   - Build: Add workflow prompts to MCPs
   - Learn: Trigger pre-built workflows
   - Deliverable: Reusable workflow prompts

### Phase 3: Advanced Single Skill (Week 5-6)
**Goal**: Add sophistication

4. **Pattern 4** (Stateful Conversation)
   - Build: Multi-turn debugging assistant
   - Learn: State management
   - Deliverable: Conversation-aware skill

5. **Pattern 7** (Chain-of-Thought)
   - Build: Architecture designer
   - Learn: Multi-phase reasoning
   - Deliverable: Reasoning-guided skill

### Phase 4: Scale (Week 7-8)
**Goal**: Multiple skills and pipelines

6. **Pattern 6** (Hierarchical Skills)
   - Build: Parent skill + 3 child skills
   - Learn: Skill delegation
   - Deliverable: Hierarchical skill system

7. **Pattern 5** (Data Pipeline)
   - Build: ETL pipeline
   - Learn: Sequential data flow
   - Deliverable: Working data pipeline

---

## Common Pitfalls and Solutions

### Pitfall 1: Vague Skill Descriptions
❌ **Wrong**: "Manages stuff"
✅ **Right**: "Process customer returns. Check eligibility, calculate refunds, route for fulfillment."

**Lesson**: Be explicit about activation triggers and operations.

### Pitfall 2: Poor Orchestration Documentation
❌ **Wrong**: Skill describes what, not how
✅ **Right**: "Create task → Check policy → Update task" (clear steps)

**Lesson**: Document HOW the skill orchestrates, not just WHAT.

### Pitfall 3: Ignoring Failures
❌ **Wrong**: Assumes all MCP calls succeed
✅ **Right**: Handle partial failures, provide fallbacks

**Lesson**: Real systems fail. Handle gracefully.

### Pitfall 4: Overcomplicating Early
❌ **Wrong**: "Might need X someday, build now"
✅ **Right**: Start simple, refactor when needed

**Lesson**: Start with Pattern 1, scale as needed.

### Pitfall 5: Ignoring Token Costs
❌ **Wrong**: Using Pattern 7 (2500 tokens) for simple operations
✅ **Right**: Use Pattern 1 (600 tokens) for straightforward tasks

**Lesson**: Match pattern complexity to problem complexity.

---

## Metrics and Monitoring

### Key Metrics

**Pattern Usage**:
- Which patterns used most?
- Skill activation rate
- Tool invocation frequency
- Average tokens per request

**Performance**:
- Response latency (P50, P95, P99)
- Error rate per pattern
- MCP server availability
- Cache hit rate

**Cost**:
- Tokens per session
- Cost per operation
- Cost trends

### Optimization Checklist

- [ ] Monitor skill activation patterns
- [ ] Identify underutilized patterns
- [ ] Measure token usage by pattern
- [ ] Track error rates and causes
- [ ] Monitor MCP performance
- [ ] Measure user satisfaction
- [ ] Identify refactoring opportunities

---

## Conclusion

This catalog focuses on **how Skills actively orchestrate MCP servers** to build intelligent agent systems.

**Key Takeaways**:

1. **Start with Pattern 1** - Foundation for all others
2. **Graduate to Pattern 2** - When multiple servers needed
3. **Add sophistication as needed** - Patterns 3-7
4. **Document effectively** - Activation triggers + orchestration steps

**Learning Journey**:
Pattern 1 → Pattern 2 → (Pattern 3 or 4) → (Pattern 7 or 6) → Pattern 5

**Remember**: The best pattern is the simplest one that solves your problem.

---

## Further Reading

- See `MCP_SERVER.md` for MCP implementation details
- See `SKILL_GUIDE.md` for skill development best practices
- See `SDK_USAGE.md` for integration examples
- See `EXAMPLES.md` for real-world code samples