# MCP Integration Patterns Reference

## Overview

This document contains supplementary patterns that don't center on Skills orchestration. These patterns are useful as reference material for specific use cases, but are outside the scope of the main **[PATTERNS_CATALOG.md](PATTERNS_CATALOG.md)** which focuses on Skills-centric patterns.

**When to use this document**:
- You need MCP patterns that don't involve Skills
- You're looking for supporting infrastructure patterns
- You need specialized patterns for specific infrastructure scenarios
- You want to understand the full MCP ecosystem beyond Skills

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

## All Reference Patterns Comparison

| Pattern | Type | Complexity | Token Efficiency | Use Case |
|---------|------|------------|------------------|----------|
| 3. MCP Resources as Context | Context enrichment | Low | Medium | Knowledge bases, schemas |
| 5. Skill Without Custom MCP | Skill + built-in tools | Low | Very High | File operations |
| 6. Direct MCP Usage | Direct calls | Very Low | Very High | Scripts, automation |
| 9. Hybrid Local + Remote | Infrastructure | High | Low | Mixed cloud/on-prem |
| 10. Security/Authorization | Security layer | Very High | Medium | Regulated systems |
| 12. Event-Driven MCP | Event handling | Very High | Low | CI/CD, monitoring |
| 14. Caching + Resources | Optimization | Medium | Very High | Read-heavy systems |

---

## When to Reference This Document

These patterns are useful when:
- You need non-Skills approaches to MCP
- You're optimizing for specific infrastructure scenarios
- You're building automation without Skills layer
- You need security/authorization enforcement
- You're caching resources for performance

For **Skills-centric patterns**, see the main [PATTERNS_CATALOG.md](PATTERNS_CATALOG.md).

---

## Further Reading

- [PATTERNS_CATALOG.md](PATTERNS_CATALOG.md) - Skills-centric integration patterns (main focus)
- See `MCP_SERVER.md` for MCP implementation details
- See `SKILL_GUIDE.md` for skill development best practices
