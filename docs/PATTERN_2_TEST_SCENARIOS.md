# Pattern 2: Multi-MCP Orchestration - Test Scenarios

## Overview

This document contains test scenarios to verify Pattern 2 (multi-server orchestration) is working correctly. Each scenario tests a different workflow using both the task-tracker and business-rules MCP servers.

## Test Setup

Before testing, ensure:
1. ✅ Both servers are registered in `.mcp.json`
2. ✅ You're in the `/agent-patterns` project directory
3. ✅ The `ecommerce-orchestration` skill is available in `.github/skills/`
4. ✅ Claude Code has reloaded to pick up new servers

## Test Scenarios

### Test 1: Simple Return - Eligible Item

**Scenario**: Customer wants to return a sweater bought 20 days ago, unopened.

**Expected Flow**:
1. Creates return task with order details
2. Checks return policy: clothing = 30 days, unopened = no fee
3. Returns: ELIGIBLE for full refund
4. Task updated with decision

**Prompt to Test**:
```
Process a return for a sweater purchased 20 days ago. It's in perfect condition, unopened.
```

**Expected Output**:
```
✓ Created return task
✓ Checked policy: Clothing items have 30-day return window
✓ Status: ELIGIBLE - Full refund (30-20 = 10 days remaining)
✓ Task ready for refund processing
```

**What It Tests**:
- ✅ business-rules: `check_return_policy("clothing", 20, false)`
- ✅ task-tracker: `create_task()` + `update_task()`
- ✅ Multi-server coordination

---

### Test 2: Return with Restocking Fee

**Scenario**: Customer returns opened electronics purchased 8 days ago.

**Expected Flow**:
1. Creates return task
2. Checks policy: electronics = 14 days, opened = 15% fee
3. Returns: ELIGIBLE with 15% restocking fee
4. Calculates refund amount

**Prompt to Test**:
```
I need to process a return for an opened laptop purchased 8 days ago. It cost $500.
```

**Expected Output**:
```
✓ Created return task for laptop
✓ Checked policy: Electronics - 14 day window (opened = 15% restocking fee)
✓ Status: ELIGIBLE - Refund: $500 × 0.85 = $425
✓ Days remaining: 6 days
✓ Task updated with refund amount
```

**What It Tests**:
- ✅ business-rules: Restocking fee calculation
- ✅ task-tracker: Task with financial data
- ✅ Conditional business logic

---

### Test 3: Return - Ineligible (Outside Window)

**Scenario**: Customer tries to return electronics purchased 20 days ago.

**Expected Flow**:
1. Creates return task
2. Checks policy: electronics = 14 days, outside window
3. Returns: NOT ELIGIBLE
4. Task marked as rejected

**Prompt to Test**:
```
Customer wants to return a tablet purchased 20 days ago. Electronics, unopened condition.
```

**Expected Output**:
```
✓ Created return task for tablet
✓ Checked policy: Electronics - 14 day window
✗ Status: NOT ELIGIBLE - Return window expired (20 > 14 days)
✓ Task marked as: REJECTED - outside return window
```

**What It Tests**:
- ✅ business-rules: Policy enforcement
- ✅ task-tracker: Status management for rejected returns
- ✅ Error handling and clear messaging

---

### Test 4: Shipping Cost Calculation

**Scenario**: Calculate shipping for orders of different sizes.

**Expected Flow**:
1. Check order total
2. Apply shipping rule
3. Return cost and method

**Prompt to Test**:
```
I need to calculate shipping for these orders:
- Order 1: $45 total
- Order 2: $75 total
- Order 3: $150 total
All standard shipping.
```

**Expected Output**:
```
Order 1 ($45):
- Standard shipping: $5.99 (below $50 threshold)

Order 2 ($75):
- Standard shipping: FREE (order > $50)

Order 3 ($150):
- Expedited shipping: FREE (order > $100)
```

**What It Tests**:
- ✅ business-rules: `calculate_shipping_cost()` with different thresholds
- ✅ Conditional pricing logic
- ✅ No task creation (rules-only operation)

---

### Test 5: Discount Calculation - Complex

**Scenario**: Calculate discounts for different customer types and order sizes.

**Expected Flow**:
1. Evaluate customer status
2. Check loyalty tier
3. Check bulk quantity
4. Stack applicable discounts (up to 25% cap)

**Prompt to Test**:
```
Calculate discounts for:
1. New customer, no loyalty, buying 3 items
2. Gold member, buying 15 items
3. New customer, buying 25 items (bulk)
```

**Expected Output**:
```
Customer 1 (New, 3 items):
- New customer: 10%
- Bulk: Not applicable (< 5 items)
- Total discount: 10%

Customer 2 (Gold, 15 items):
- Loyalty (Gold): 15%
- Bulk (11-20): 10%
- Total discount: 25% (capped)

Customer 3 (New, 25 items):
- New customer: 10%
- Bulk (21+): 15%
- Total discount: 25% (capped)
```

**What It Tests**:
- ✅ business-rules: Discount stacking logic
- ✅ Discount cap enforcement
- ✅ Multiple rule types combining

---

### Test 6: Complete Order Workflow

**Scenario**: Create a complete order with all pricing calculated.

**Expected Flow**:
1. Calculate applicable discounts
2. Calculate shipping cost
3. Create order task
4. Include all pricing in task description
5. Ready for fulfillment

**Prompt to Test**:
```
Create an order for a new customer buying 8 items with a subtotal of $85. Standard shipping.
```

**Expected Output**:
```
✓ Calculated discount:
  - New customer: 10%
  - Bulk (5-10): 5%
  - Total: 15% = $12.75 off

✓ Calculated shipping: FREE (order > $50)

✓ Created fulfillment task:
  - Subtotal: $85.00
  - Discount: -$12.75 (15%)
  - Shipping: $0.00
  - Tax (estimated): ~$5.73
  - Total: ~$77.98

✓ Task status: PENDING_FULFILLMENT
✓ Ready for warehouse
```

**What It Tests**:
- ✅ task-tracker: `create_task()` with complex data
- ✅ business-rules: Multiple calculations (discount + shipping)
- ✅ Full multi-server coordination
- ✅ Real-world workflow

---

### Test 7: Complex Scenario - Multiple Item Return

**Scenario**: Customer returns mixed items purchased on same date.

**Expected Flow**:
1. Evaluate each item separately
2. Apply appropriate policies
3. Calculate total refund
4. Create comprehensive task

**Prompt to Test**:
```
Process a return with these items purchased 25 days ago:
- 2 books ($15 each, unopened): $30 total
- 1 clothing item ($50, unworn): $50 total
- 1 opened electronics ($200, opened): $200 total
```

**Expected Output**:
```
Books (2 × $15 = $30):
✓ Policy: Books - 60 day window, unopened
✓ Days remaining: 35
✓ Restocking fee: 0%
✓ Refund: $30.00

Clothing ($50):
✓ Policy: Clothing - 30 day window, unworn
✓ Days remaining: 5
✓ Restocking fee: 0%
✓ Refund: $50.00

Electronics ($200):
✗ Policy: Electronics - 14 day window
✗ Days remaining: OUTSIDE window (25 > 14)
✗ Refund: $0.00

---
Total Return: $80.00 (Books + Clothing approved, Electronics rejected)
Task: PARTIAL_APPROVAL - Full details for fulfillment team
```

**What It Tests**:
- ✅ business-rules: Multiple policies in one request
- ✅ Conditional logic per item
- ✅ Complex refund calculation
- ✅ task-tracker: Rich task data

---

### Test 8: Policy Inquiry - View All Rules

**Scenario**: Customer service wants to see all current policies.

**Expected Flow**:
1. Fetch all business rules
2. Display in readable format
3. No task creation needed

**Prompt to Test**:
```
Show me all e-commerce business policies - return windows, shipping rules, and discounts.
```

**Expected Output**:
```
E-COMMERCE POLICIES:

Return Policies:
- Electronics: 14 days (15% fee if opened)
- Clothing: 30 days (no fee)
- Books: 60 days (no fee)
- Food: No returns allowed

Shipping Rules:
- Orders > $100: Free expedited (2 days)
- Orders $50-$100: Free standard (3-5 days)
- Orders < $50: $5.99 standard
- Express: +$15 (next day)

Discount Tiers:
- New customer: 10%
- Loyalty Bronze: 5%
- Loyalty Silver: 10%
- Loyalty Gold: 15%
- Bulk 5-10: 5%
- Bulk 11-20: 10%
- Bulk 21+: 15%
- Maximum combined: 25%
```

**What It Tests**:
- ✅ business-rules: `get_all_policies()` tool
- ✅ Resource access (rules://*)
- ✅ Information retrieval (no task-tracker needed)

---

## Test Execution Checklist

### Before Testing
- [ ] Verified `.mcp.json` has both servers
- [ ] Claude Code project is loaded in `/agent-patterns`
- [ ] Skill file exists at `.github/skills/ecommerce-orchestration/SKILL.md`
- [ ] Documentation files created

### During Testing
- [ ] Run each test scenario in order
- [ ] Observe which MCP servers are invoked
- [ ] Verify task creation (check task-tracker)
- [ ] Verify policy application (check business-rules)
- [ ] Check multi-server coordination

### Success Criteria
- ✅ Test 1: Simple return processes correctly
- ✅ Test 2: Restocking fee calculated
- ✅ Test 3: Outside-window returns rejected
- ✅ Test 4: Shipping rules applied correctly
- ✅ Test 5: Discounts stack and cap correctly
- ✅ Test 6: Complete order with all pricing
- ✅ Test 7: Multiple items handled separately
- ✅ Test 8: All policies viewable

## Troubleshooting

### Server Not Starting?
```bash
# Verify servers are configured
cat .mcp.json

# Check if files exist
ls -la business-rules-mcp/src/business_rules_mcp/
ls -la mcp-server/src/task_tracker_mcp/
```

### Skill Not Activating?
- Ensure file is at: `.github/skills/ecommerce-orchestration/SKILL.md`
- Check skill name in frontmatter: `name: ecommerce-orchestration`
- Reload Claude Code project

### Tasks Not Creating?
- Verify task-tracker server is running
- Check if task-tracker MCP is active in .mcp.json
- Look for error messages in console

### Wrong Policy Applied?
- Verify business-rules server is running
- Check RulesEngine logic in `rules_engine.py`
- Test `get_all_policies()` to see current rules

## Expected Token Usage

**Per Test Scenario** (approximate):
- Test 1 (simple): ~400-600 tokens
- Test 2 (with fee): ~600-800 tokens
- Test 3 (rejection): ~400-500 tokens
- Test 4 (shipping): ~300-400 tokens
- Test 5 (discount): ~400-600 tokens
- Test 6 (complete): ~800-1200 tokens
- Test 7 (complex): ~1000-1500 tokens
- Test 8 (policies): ~300-400 tokens

**Total for all tests**: ~4000-6500 tokens

## Results Recording

Document your findings:

```markdown
## Test Results

### Test 1: Simple Return ✅/❌
- Servers invoked: task-tracker, business-rules
- Discount calculated: [expected vs actual]
- Task created: [yes/no]
- Notes: [any observations]

### Test 2: Return with Fee ✅/❌
- Servers invoked: task-tracker, business-rules
- Fee calculated: [expected vs actual]
- Task updated: [yes/no]
- Notes: [any observations]

...
```

## Next Steps After Testing

1. ✅ All tests pass? → Proceed to Pattern 3
2. ❌ Some tests fail? → Debug and fix
3. 🔧 Want to extend? → Add new rules or workflows
4. 📊 Want to measure? → Compare with Pattern 1 token usage
5. 🚀 Ready for production? → Migrate to HTTP transport

---

**Pattern 2 successfully demonstrates multi-server orchestration!**
