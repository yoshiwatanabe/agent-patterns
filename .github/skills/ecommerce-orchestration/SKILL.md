---
name: ecommerce-orchestration
description: Manage e-commerce orders and returns using task management and business rules together. Use for order processing, returns, shipping calculations, and discount applications.
---

# E-commerce Orchestration Skill

## Overview

This skill demonstrates **Pattern 2: Multi-MCP Orchestration** by coordinating between two MCP servers:

1. **task-tracker**: Manages order/return tasks and workflows
2. **business-rules**: Provides e-commerce policies (return windows, shipping costs, discounts)

## Multi-Server Workflows

### Return Request Workflow

When processing a customer return:

1. Create a return task using `task-tracker` with order details
2. Check return eligibility using `business-rules` (category, days since purchase, condition)
3. Determine if restocking fees apply (especially for opened electronics)
4. Update task with eligibility decision and refund amount
5. Route to appropriate fulfillment team based on eligibility

**Example**: "Process a return for a laptop purchased 10 days ago"
- Creates return task
- Checks return policy (electronics = 14 days, 15% restocking fee if opened)
- Result: Eligible with 15% fee (refund = original_price × 0.85)

### Order Processing Workflow

When creating a new order:

1. Calculate applicable discounts using `business-rules` (new customer, loyalty tier, bulk order)
2. Calculate shipping costs using `business-rules` (order total, shipping type)
3. Create order fulfillment task using `task-tracker` with final pricing
4. Update task with order summary (subtotal, discount, shipping, tax, total)
5. Route to fulfillment center

**Example**: "Create an order for a new customer buying 12 items totaling $85"
- Applies discounts: 10% new customer + 10% bulk (capped at 25% total)
- Calculates shipping: Free standard (order > $50)
- Creates task: "Order fulfillment - $85 order, $14.25 discount, $0 shipping, $76.63 total"

### Complex Scenario: Return Evaluation

"Evaluate a return for 3 opened books and 1 unopened laptop purchased 20 days ago for $500 each"

**Books**:
- Category: books, days: 20, opened: true
- Check: books = 60 days, no restocking fee
- Result: All eligible, full refund = $300

**Laptop**:
- Category: electronics, days: 20, opened: true
- Check: electronics = 14 days ✓ within window, opened ✓ 15% fee
- Result: Eligible with fee = $500 × 0.85 = $425

**Total return**: $725 (3 × $100 + $425)

## Available Operations

### From task-tracker MCP:
- `create_task` - Create order/return task with metadata
- `update_task` - Update task status, add notes
- `filter_tasks` - Find tasks by priority, status, project
- `list_tasks` - List pending/completed tasks
- `get_task_statistics` - Get completion rates, metrics

### From business-rules MCP:
- `check_return_policy` - Validate return eligibility
- `calculate_shipping_cost` - Get shipping costs by order amount
- `calculate_discount` - Apply customer/order discounts
- `get_all_policies` - View all business rules

## Best Practices

1. **Always check rules first**: Before creating tasks, validate using business-rules to provide accurate information
2. **Embed results in tasks**: Include policy decisions and calculations in task descriptions for auditing
3. **Use specific categories**: Use exact category names (electronics, clothing, books, food) for accurate policies
4. **Consider customer context**: Loyalty tier, purchase history affect discounts and eligibility
5. **Chain operations**: Discount → Shipping → Task creation creates complete order workflows
6. **Document decisions**: When rules block actions, clearly state why in task notes

## Example Prompts

### Return Processing
- "Process a return for clothing purchased 20 days ago, unopened"
- "Evaluate return for opened electronics purchased 5 days ago"
- "Check if customer can return books purchased 45 days ago"

### Order Creation
- "Create an order for a new customer buying 8 items for $65"
- "Create an order for a gold loyalty member buying 3 items for $120"
- "Process an order for 25 bulk items totaling $500 with standard shipping"

### Policy Inquiries
- "What's our shipping cost for a $75 order?"
- "What discounts apply for a silver member buying 12 items?"
- "How long can customers return clothing?"

## Integration Example

```
User: "I need to process a return for a dress. Customer bought it 20 days ago for $45, and it's unworn."

Steps:
1. task-tracker: Create task "Return: Dress - $45 - Unworn"
2. business-rules: check_return_policy("clothing", 20, opened=false)
   → {eligible: true, days_remaining: 10, restocking_fee: 0%, refund_method: "original_payment"}
3. task-tracker: Update task with "✓ ELIGIBLE - Full refund $45 via original payment method"
4. Result: Task ready for fulfillment, customer gets full refund
```

## Token Efficiency Note

This pattern (Pattern 2) uses 2 MCP servers, which increases token usage compared to Pattern 1:
- **Pattern 1** (single server): ~600-1000 tokens
- **Pattern 2** (multi-server): ~1000-1500 tokens

The additional tokens are worth it because:
- Business rules are independently versioned and managed
- Rule changes don't require server restarts
- Clear separation of concerns (tasks vs. policies)
- Demonstrates real-world orchestration patterns

## See Also

- [PATTERNS_CATALOG.md](../../docs/PATTERNS_CATALOG.md) - Pattern 2 detailed documentation
- [PATTERN_2_IMPLEMENTATION.md](../../docs/PATTERN_2_IMPLEMENTATION.md) - Implementation details
