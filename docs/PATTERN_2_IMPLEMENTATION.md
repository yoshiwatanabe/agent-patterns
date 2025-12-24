# Pattern 2: Multi-MCP Orchestration Implementation

## Overview

This document describes the implementation of **Pattern 2: Multi-MCP Orchestration** using e-commerce domain with business rules.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code                             │
│                  (User Interaction)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ ecommerce-orchestration skill
                     │ (Claude decides which servers to use)
                     │
        ┌────────────┴─────────────┐
        │                          │
        ▼                          ▼
  ┌──────────────┐        ┌──────────────────────┐
  │ task-tracker │        │  business-rules      │
  │    MCP       │        │     MCP              │
  │              │        │                      │
  │ Tools:       │        │ Tools:               │
  │ - create     │        │ - check_return      │
  │ - update     │        │ - calc_shipping     │
  │ - filter     │        │ - calc_discount     │
  │ - list       │        │ - get_all_policies  │
  │              │        │                      │
  │ Resources:   │        │ Resources:           │
  │ - tasks      │        │ - return_policies   │
  │ - pending    │        │ - shipping_rules    │
  │ - stats      │        │ - discount_rules    │
  └──────────────┘        └──────────────────────┘
        │                          │
        ▼                          ▼
   Task Database              Business Rules
   (SQLite)                   (In-memory dict)
```

## Directory Structure

```
agent-patterns/
├── mcp-server/                    # Server 1: Task Management
│   ├── pyproject.toml
│   ├── src/task_tracker_mcp/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── database.py
│   │   └── schema.sql
│   └── tests/
│
├── business-rules-mcp/            # Server 2: Business Rules (NEW)
│   ├── pyproject.toml
│   ├── src/business_rules_mcp/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── rules_engine.py
│   │   └── __pycache__/
│   └── tests/
│
├── .mcp.json                      # UPDATED: Both servers registered
│
├── .github/skills/
│   ├── task-organizer/            # Pattern 1 skill (existing)
│   │   └── SKILL.md
│   └── ecommerce-orchestration/   # Pattern 2 skill (NEW)
│       └── SKILL.md
│
└── docs/
    ├── PATTERNS_CATALOG.md
    ├── PATTERN_2_IMPLEMENTATION.md (this file)
    └── ...
```

## Server 1: Task-Tracker MCP

**Purpose**: Track tasks and manage workflows

**Database**: SQLite with projects, tasks, tags

**Tools**:
- `create_task(title, description, priority, status, project_id, due_date)` - Create task
- `update_task(task_id, fields)` - Update task properties
- `get_task(task_id)` - Get single task
- `list_tasks(limit, offset)` - List all tasks with pagination
- `filter_tasks(status, priority, project_id, tag_name)` - Filter by criteria
- `search_tasks(query)` - Full-text search
- `get_task_statistics()` - Get metrics
- `get_overdue_tasks()` - Get overdue items

**Resources**:
- `task://all` - All tasks
- `task://pending` - Pending tasks
- `task://high-priority` - High-priority tasks
- `project://all` - All projects
- `stats://summary` - Statistics summary

## Server 2: Business Rules MCP (NEW)

**Purpose**: Provide dynamic business policies that change independently

**Storage**: In-memory dictionaries (could be database-backed)

**Tools**:
- `check_return_policy(category, days_since_purchase, opened)` - Return eligibility
- `calculate_shipping_cost(order_total, shipping_type)` - Shipping costs
- `calculate_discount(customer_status, loyalty_tier, num_items)` - Discount amounts
- `get_all_policies()` - All policies combined

**Resources**:
- `rules://return-policies` - Return window matrix
- `rules://shipping-rules` - Shipping cost thresholds
- `rules://discount-rules` - All discount types

### Business Rules Details

#### Return Policies

| Category | Window | Restocking Fee (opened) | Notes |
|----------|--------|------------------------|-------|
| Electronics | 14 days | 15% | Includes phones, laptops, tablets |
| Clothing | 30 days | 0% | Unrestricted |
| Books | 60 days | 0% | Generous window |
| Food | No returns | N/A | Consumables never returnable |

#### Shipping Rules

| Condition | Cost | Type |
|-----------|------|------|
| Order > $100 | $0 | Expedited (2 days) |
| $50 - $100 | $0 | Standard (3-5 days) |
| < $50 | $5.99 | Standard (3-5 days) |
| Express | +$15 | Next day |

#### Discount Rules

| Type | Amount | Trigger |
|------|--------|---------|
| New Customer | 10% | First order |
| Loyalty Bronze | 5% | Active membership |
| Loyalty Silver | 10% | Higher tier |
| Loyalty Gold | 15% | Premium member |
| Bulk 5-10 | 5% | Item count |
| Bulk 11-20 | 10% | Item count |
| Bulk 21+ | 15% | Item count |

**Note**: Total discount capped at 25%

## Orchestration Skill

**File**: `.github/skills/ecommerce-orchestration/SKILL.md`

**Purpose**: Guide Claude on how to coordinate between servers

**Key Workflows**:

### Return Processing
```
1. Create return task (task-tracker)
2. Check eligibility (business-rules)
3. Update task with decision (task-tracker)
4. Route to fulfillment (task status update)
```

### Order Processing
```
1. Calculate discounts (business-rules)
2. Calculate shipping (business-rules)
3. Create order task (task-tracker)
4. Update with pricing (task-tracker)
5. Route to fulfillment (task status update)
```

## Configuration

### .mcp.json (Multi-Server Setup)

```json
{
  "mcpServers": {
    "task-tracker": {
      "command": "bash",
      "args": ["-c", "PYTHONPATH=mcp-server/src python3 -m task_tracker_mcp.server"],
      "disabled": false
    },
    "business-rules": {
      "command": "bash",
      "args": ["-c", "PYTHONPATH=business-rules-mcp/src python3 -m business_rules_mcp.server"],
      "disabled": false
    }
  }
}
```

Both servers start automatically when Claude Code loads the project.

## Example Workflows

### Example 1: Simple Return

**Request**: "Process a return for a sweater bought 15 days ago"

**Execution**:
1. task-tracker: Create task "Return: Sweater - Bought 15 days ago"
2. business-rules: `check_return_policy("clothing", 15, false)`
   - Response: `{eligible: true, days_remaining: 15, restocking_fee: 0%}`
3. task-tracker: Update task status to "eligible_for_return"
4. Result: Task ready for refund processing

### Example 2: Order with Discounts

**Request**: "Create order for new customer buying 8 items for $75"

**Execution**:
1. business-rules: `calculate_discount("new", null, 8)`
   - Response: `{discounts: [{type: "new_customer", amount: 0.10}, {type: "bulk", amount: 0.05}], total: 15%}`
2. business-rules: `calculate_shipping_cost(75, "standard")`
   - Response: `{cost: 0.0, type: "standard", message: "Free shipping"}`
3. task-tracker: Create task "Order - $75 order, $11.25 discount, free shipping = $63.75"
4. Result: Order task with complete pricing

### Example 3: Complex Return with Multiple Items

**Request**: "Process return for 3 books ($20 ea) and 1 laptop ($500), all purchased 25 days ago, books unopened, laptop opened"

**Execution**:

**Books** (3 × $20 = $60):
- `check_return_policy("books", 25, false)` → eligible, days_remaining: 35, fee: 0%
- Refund: $60

**Laptop** (1 × $500):
- `check_return_policy("electronics", 25, true)` → ineligible (25 > 14 days)
- Refund: $0

**Total**: $60 refund authorized

Task created: "Return - Partial approval: Books ($60) approved, Laptop ($500) ineligible (outside 14-day window)"

## Testing Workflow

### 1. Verify Both Servers Load

```bash
# Should show both servers in logs
clauderunning /home/ywatanabe/dev/agent-patterns
# Check if .mcp.json is loaded correctly
```

### 2. Test Individual Servers

**Test task-tracker**:
```
Prompt: "Create a test task called 'Pattern 2 Test'"
Expected: Task created successfully
```

**Test business-rules**:
```
Prompt: "What's the return policy for electronics? Check after 10 days."
Expected: Eligible, 4 days remaining, 15% restocking fee if opened
```

### 3. Test Multi-Server Orchestration

```
Prompt: "Process a return for a camera purchased 8 days ago, unopened, for $250"

Expected:
1. Creates return task
2. Checks policy (electronics, 8 days) → eligible
3. Updates task with "Eligible - Full refund $250"
```

### 4. Test Orchestration Skill Activation

```
Prompt: "I need to handle an e-commerce order. Customer is new, wants 10 items for $120."

Check:
- Does ecommerce-orchestration skill activate?
- Does it use both servers?
- Is pricing calculated correctly?
```

## Token Usage Analysis

**Pattern 2 vs Pattern 1**:

| Aspect | Pattern 1 | Pattern 2 |
|--------|-----------|----------|
| Servers | 1 (task-tracker) | 2 (task + rules) |
| Avg Tokens | 600-1000 | 1000-1500 |
| Complexity | Medium | Medium-High |
| Separation of Concerns | Single domain | Clear domains |
| Scalability | Good | Excellent |

**Trade-off**: +500 tokens for better architecture and independent rule management

## Deployment Notes

### Development
- Both servers run locally via stdio
- Skill activates based on prompts
- Perfect for testing and iteration

### Production
- Could migrate to HTTP transport (separate plan)
- Business-rules server could become database-backed
- Task-tracker could scale independently
- Could add caching for rules (rarely change)

## Maintenance

### Adding New Rules
Edit `/home/ywatanabe/dev/agent-patterns/business-rules-mcp/src/business_rules_mcp/rules_engine.py`:
1. Update relevant `*_RULES` dictionary
2. Add/modify method in `RulesEngine` class
3. Restart business-rules server
4. No task-tracker changes needed

### Adding New Tasks Operations
Edit `/home/ywatanabe/dev/agent-patterns/mcp-server/src/task_tracker_mcp/server.py`:
1. Add new tool with `@mcp.tool()` decorator
2. Implement logic
3. Restart task-tracker server
4. Update skill if new tool is user-facing

## Key Learnings

1. **Separation of Concerns**: Business rules separate from task management
2. **Independent Scaling**: Each server can be updated independently
3. **Clear Orchestration**: Skill shows how servers work together
4. **Token Efficiency**: Multi-server adds cost but architectural benefits justify it
5. **Real-World Pattern**: Mirrors actual e-commerce systems with rules engines

## See Also

- [PATTERNS_CATALOG.md](./PATTERNS_CATALOG.md) - Pattern 2 detailed documentation
- [ecommerce-orchestration skill](./../.github/skills/ecommerce-orchestration/SKILL.md)
- Business Rules MCP: `business-rules-mcp/src/business_rules_mcp/`
- Task-Tracker MCP: `mcp-server/src/task_tracker_mcp/`
