# Pattern 6: Hierarchical Skills - Test Scenarios

## Overview

This file contains test scenarios for the hierarchical text analysis skill system. Each scenario demonstrates different activation patterns and expected behavior.

---

## Test Data

### Sample Text 1: Blog Post (Mixed Quality)

```
AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms
can now diagnose diseases faster than doctors. This technology is amazing and
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical
datasets for optimal performance metrics. Implementation complexity remains high,
but the potential for disruption cannot be overstated.
```

**Issues to find:**
- Grammar: "Artificial intelligence are" (subject-verb agreement)
- Tone: Overly enthusiastic, marketing-heavy language
- Readability: Inconsistent complexity (simple → very complex)
- SEO: Poor structure, limited keyword optimization

---

### Sample Text 2: Technical Documentation

```
Configuration Guide

The system configuration process involves multiple interdependent components.
Prior to initialization, ensure all prerequisites are satisfied. The configuration
file format utilizes JSON specification. Each configuration object contains
mandatory fields and optional extensions.

Settings can be modified via the command-line interface or configuration files.
Runtime modifications necessitate server restart.
```

**Issues to find:**
- Grammar: Mostly correct
- Tone: Formal, somewhat dry
- Readability: Too complex, overuse of passive voice
- SEO: Technical jargon, poor structure

---

### Sample Text 3: Marketing Copy

```
Revolutionary AI Platform Transforms Your Business

Tired of manual processes? Our revolutionary AI platform absolutely transforms
how you work. Say goodbye to tedious manual tasks forever. You'll wonder how
you ever managed without it!

Our cutting-edge machine learning technology learns from your data and optimizes
workflows automatically. Increase productivity by 300%! Join thousands of happy
customers saving time and money every day.
```

**Issues to find:**
- Grammar: Correct
- Tone: Highly positive, persuasive, marketing-focused
- Readability: Accessible, simple language
- SEO: Good keyword usage, engaging copy

---

## Test Scenarios

### Scenario 1: Full Comprehensive Analysis

**Request**:
```
Analyze this blog post comprehensively for potential publication. Check everything.
```

**Text**: Sample Text 1 (AI Revolution in Healthcare)

**Expected Activation Flow**:
```
1. text-analyzer (parent) receives request
2. Recognizes "comprehensively" and "check everything"
3. Delegates to ALL 4 child skills in sequence:
   → grammar-checker
   → sentiment-analyzer
   → readability-scorer
   → seo-optimizer
4. Synthesizes results into comprehensive report
```

**Expected Output Structure**:
- Executive Summary: Key findings and priority actions
- Grammar & Language: Issues and corrections
- Sentiment: Emotional tone analysis
- Readability: Scores and audience fit
- SEO: Optimization opportunities
- Recommendations: Prioritized action items

**Expected Findings**:
- Grammar: Subject-verb agreement error, awkward phrasing
- Sentiment: Overly enthusiastic first paragraph, too technical second paragraph
- Readability: Inconsistent (easy → very difficult)
- SEO: Needs structure improvements, heading hierarchy

**Token Estimate**: ~1000 tokens

---

### Scenario 2: Specific Analysis (Grammar + Readability)

**Request**:
```
Check this for grammar and readability. I need to make sure it's technically
correct and easy to understand for general readers.
```

**Text**: Sample Text 2 (Configuration Guide)

**Expected Activation Flow**:
```
1. text-analyzer (parent) receives request
2. Recognizes specific focus: "grammar and readability"
3. Delegates to 2 child skills:
   → grammar-checker
   → readability-scorer
4. Provides focused report (skips sentiment and SEO)
```

**Expected Output**:
- Grammar & Language: Assessment and corrections
- Readability: Complexity analysis and simplification suggestions
- Focused recommendations

**Expected Findings**:
- Grammar: Mostly correct, but some passive voice overuse
- Readability: Too complex for general audience, needs simplification
- Suggestions: Break into shorter sentences, use simpler vocabulary

**Token Estimate**: ~600 tokens (40% savings vs. full analysis)

---

### Scenario 3: Marketing Focus (Sentiment + SEO)

**Request**:
```
Optimize this for marketing effectiveness. I want to know if the emotional
impact is strong and if it's optimized for search engines.
```

**Text**: Sample Text 3 (Marketing Copy)

**Expected Activation Flow**:
```
1. text-analyzer (parent) receives request
2. Recognizes "marketing effectiveness" + "emotional impact" + "search engines"
3. Delegates to 2 child skills:
   → sentiment-analyzer
   → seo-optimizer
4. Provides marketing-focused analysis (skips grammar and readability)
```

**Expected Output**:
- Sentiment: Emotional tone analysis with persuasiveness assessment
- SEO: Keyword analysis and optimization opportunities
- Marketing recommendations

**Expected Findings**:
- Sentiment: Strong positive polarity, effective persuasion techniques
- SEO: Good keyword density, could improve structure and meta descriptions
- Suggestions: Add subheadings, enhance CTAs, improve schema markup

**Token Estimate**: ~700 tokens

---

### Scenario 4: Direct Child Skill Invocation (Bypass Parent)

**Request**:
```
Just check the grammar and fix any spelling errors. That's all I need.
```

**Text**: Sample Text 1

**Expected Activation Flow**:
```
1. grammar-checker (child skill) activates directly
2. Detects specific request for grammar only
3. Provides focused grammar report
4. Parent skill not invoked (optimization)
```

**Expected Output**:
- Critical Issues with corrections
- Minor Issues with suggestions
- Style recommendations

**Token Estimate**: ~400 tokens (60% savings vs. full analysis)

---

### Scenario 5: Test Skill Routing Logic

**Request**: "Review this for publication"

**Text**: Sample Text 1

**Expected Behavior**:
- Parent skill recognizes "review for publication" as comprehensive request
- Should delegate to all 4 child skills (not just grammar)
- Should synthesize complete report

**Verification Checklist**:
- [ ] Parent skill activates (not direct child)
- [ ] All 4 children are invoked
- [ ] Results are synthesized coherently
- [ ] Final report includes all 4 perspectives

---

## Skill Activation Pattern Tests

### Test 1: Parent Recognition Patterns

**Trigger Phrases That Activate Parent**:
- ✅ "Analyze this text/document/article/post"
- ✅ "Review this content for publication"
- ✅ "Check this writing quality"
- ✅ "Evaluate this document comprehensively"
- ✅ "Optimize this for marketing" (cross-domain)
- ✅ "Full analysis needed"

**Should Trigger to Children Only**:
- ✅ "Check grammar" → grammar-checker
- ✅ "Analyze sentiment" → sentiment-analyzer
- ✅ "Check readability" → readability-scorer
- ✅ "SEO review" → seo-optimizer

---

### Test 2: Partial Delegation Patterns

**Scenario**: "Check this for grammar and readability"

**Expected**:
- Parent skill activates
- Delegates to: grammar-checker + readability-scorer
- Skips: sentiment-analyzer, seo-optimizer

**Verification**:
- [ ] Parent analyzes request for specific keywords
- [ ] Only relevant children are invoked
- [ ] Results are focused on requested aspects

---

### Test 3: Cross-Domain Request Handling

**Scenario**: "Optimize this for marketing effectiveness"

**Keywords Detected**:
- "optimize" → SEO consideration
- "marketing effectiveness" → sentiment analysis needed

**Expected**:
- Parent recognizes multi-domain request
- Delegates to: sentiment-analyzer + seo-optimizer
- Grammar and readability skipped (not relevant to marketing focus)

---

## Output Format Validation

### Test: Complete Report Structure

**Verify Output Contains**:
- [ ] Executive Summary (key findings)
- [ ] Grammar & Language (if grammar-checker invoked)
- [ ] Sentiment (if sentiment-analyzer invoked)
- [ ] Readability (if readability-scorer invoked)
- [ ] SEO (if seo-optimizer invoked)
- [ ] Recommendations (prioritized action items)

### Test: Consistent Formatting

**Verify Each Section Has**:
- [ ] Clear heading
- [ ] Structured data (scores, assessments)
- [ ] Specific examples from text
- [ ] Actionable recommendations

---

## Performance Benchmarks

### Expected Token Usage

| Scenario | Flow | Tokens | Efficiency |
|----------|------|--------|-----------|
| Full Analysis | Parent → 4 children | ~1000 | Baseline |
| Quick Review | Parent → 2 children | ~600 | 60% of full |
| Marketing Focus | Parent → 2 children | ~700 | 70% of full |
| Direct Child | 1 child only | ~400 | 40% of full |

### Expected Latency

- Single child skill: ~1-2 seconds
- Parent + 2 children: ~2-3 seconds
- Parent + 4 children: ~3-4 seconds

---

## Error Handling Tests

### Test: Invalid Text

**Request**: "" (empty text)

**Expected**:
- Skills should recognize empty input
- Provide helpful error message
- Suggest providing text to analyze

---

### Test: Ambiguous Request

**Request**: "Check this" (no specific aspect)

**Expected**:
- Parent skill interprets as general request
- Defaults to full comprehensive analysis
- Provides all perspectives

---

## Integration Tests

### Test: Skill Composition

**Request**: "Full analysis needed"

**Verification**:
- [ ] Parent skill activates correctly
- [ ] All 4 child skills receive appropriate context
- [ ] Results are synthesized into coherent report
- [ ] No information is duplicated
- [ ] Recommendations are prioritized across all dimensions

### Test: Workflow Completeness

**Verification**:
- [ ] Grammar issues found and explained
- [ ] Sentiment analysis includes polarity and intensity
- [ ] Readability includes multiple metrics
- [ ] SEO includes keyword and structure analysis
- [ ] Final recommendations are actionable

---

## Sample Expected Output: Full Analysis

```
COMPREHENSIVE TEXT ANALYSIS REPORT
===================================

EXECUTIVE SUMMARY
─────────────────
Key Findings:
- 3 critical grammar issues requiring immediate fixes
- Highly inconsistent tone (informal vs. overly technical)
- Mixed readability levels (too simple → too complex)
- Needs significant SEO optimization

Priority Actions:
1. Fix subject-verb agreement in first sentence
2. Simplify overly technical second paragraph
3. Add heading hierarchy and structure
4. Improve keyword optimization

GRAMMAR & LANGUAGE
──────────────────
Critical Issues:
1. "Artificial intelligence are" → "Artificial intelligence is"
   Subject-verb agreement: singular subject needs singular verb

2. "will change everything forever" → awkward phrasing
   Suggestion: "will have significant impact"

3. Inconsistent tone between paragraphs
   Para 1: Informal, marketing-like
   Para 2: Overly technical, corporate

Minor Issues:
- "amazing" is too subjective for technical writing
- Consider: "significant" or "transformative"

SENTIMENT
─────────
Overall Sentiment: Mixed (strongly positive first, neutral second)
- Intensity: Strong in first paragraph, neutral in second
- Polarity: Positive
- Dominant Emotion: Excitement (first para), Technical confidence (second para)

Detailed Analysis:
Positive Elements:
- "transforming" - innovation language
- "faster than doctors" - clear benefit
- "potential" - forward-looking

Negative/Warning Signs:
- "will change everything forever" - overpromising
- "so happy" - too casual for healthcare content

Audience Impact:
- First paragraph appeals to healthcare decision-makers
- Second paragraph may confuse general readers
- Inconsistent messaging creates trust concerns

Recommendation: Choose target audience and maintain consistent tone

READABILITY
───────────
Readability Scores:
- Flesch Reading Ease: Mixed (72 first para, 18 second para)
- Overall: Inconsistent
- First paragraph: 6th grade level
- Second paragraph: College graduate level

Vocabulary Analysis:
- Simple language: 60% (first paragraph)
- Complex language: 40% (second paragraph)
- Jargon: "algorithmic implementations", "performance metrics"

Structural Issues:
- No headings or sections
- Paragraph 2 is single long sentence
- No logical flow between paragraphs

Audience Fit:
- First paragraph: General public
- Second paragraph: Technical experts
- Overall: Confusing for both audiences

SEO
───
Keyword Analysis:
- Primary keyword: "artificial intelligence" (2.1% density - low)
- Secondary keywords missing: "healthcare", "diagnosis", "machine learning"
- Keyword placement: Good in title/first sentence, but not reinforced

Content Structure:
- Missing H2/H3 headings
- No sections or logical organization
- Single paragraph, not scannable

On-Page SEO:
Current title: "AI Revolution in Healthcare" (26 chars)
Suggested: "How AI & Machine Learning are Transforming Healthcare Diagnostics" (63 chars)

Meta description needed:
"Explore how artificial intelligence and machine learning are revolutionizing
healthcare diagnostics, improving accuracy and speed. Read our analysis of
AI's impact on medical professionals and patient outcomes."

Content Quality:
- Topic depth: Moderate (needs expansion)
- Unique value: Could be stronger
- E-A-T signals: Weak (no sources, no credentials)

RECOMMENDATIONS (Prioritized)
────────────────────────────

CRITICAL (Fix immediately):
1. Correct "Artificial intelligence are" → "Artificial intelligence is"
2. Choose and maintain consistent tone throughout
3. Simplify second paragraph for general audience

HIGH (Should fix before publication):
1. Add heading hierarchy and sections
2. Expand content to 800+ words for better SEO
3. Add subheadings for scannability
4. Include specific examples and data points
5. Reduce marketing language in healthcare context

MEDIUM (Improve quality):
1. Add author credentials/expertise signals
2. Include sources and citations
3. Add related keywords naturally
4. Improve keyword density for "healthcare" and "machine learning"
5. Add meta description

LOW (Polish):
1. Replace "amazing" with "significant"
2. Tone down "will change everything forever"
3. Consider adding call-to-action

NEXT STEPS:
1. Revise for consistency and clarity
2. Expand with examples and data
3. Add proper structure and SEO elements
4. Fact-check claims with sources
5. Re-analyze after revisions
```

---

## Running the Tests

### Using Claude Agent SDK

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads all skills from .github/skills/
    allowed_tools=["Skill"]  # Pure skills only
)

# Test Scenario 1: Full Analysis
async for message in query(
    "Analyze this blog post comprehensively for publication:\n\n" + sample_text_1,
    options=options
):
    print(message)

# Test Scenario 2: Quick Review
async for message in query(
    "Check this for grammar and readability:\n\n" + sample_text_2,
    options=options
):
    print(message)

# Test Scenario 3: Marketing Focus
async for message in query(
    "Optimize this for marketing effectiveness:\n\n" + sample_text_3,
    options=options
):
    print(message)

# Test Scenario 4: Direct Child
async for message in query(
    "Just check grammar:\n\n" + sample_text_1,
    options=options
):
    print(message)
```

---

## Success Criteria

### Skill Activation
- [ ] Parent skill activates for comprehensive requests
- [ ] Child skills activate for specific requests
- [ ] Partial delegation works (2-3 children)
- [ ] Direct child invocation bypasses parent

### Output Quality
- [ ] All reports are well-structured
- [ ] Examples are specific to provided text
- [ ] Recommendations are actionable
- [ ] Tone is appropriate for each skill

### Performance
- [ ] Full analysis completes in <4 seconds
- [ ] Token usage matches estimates
- [ ] Error handling is graceful
- [ ] Results are reproducible

### Pattern Demonstration
- [ ] Hierarchical structure is evident
- [ ] Skill composition works correctly
- [ ] Flexible invocation patterns function
- [ ] Pure prompt-based approach succeeds

---

## Test Results Summary

**Run Date**: [Date]
**Tester**: [Name]
**Status**: ☐ PASS / ☐ FAIL / ☐ PARTIAL

### Results by Scenario

| Scenario | Expected | Actual | Status |
|----------|----------|--------|--------|
| Full Analysis | Comprehensive | | ☐ |
| Quick Review | Focused | | ☐ |
| Marketing Focus | Targeted | | ☐ |
| Direct Child | Specific | | ☐ |

### Key Findings

- [ ] Skill routing works correctly
- [ ] Output quality meets expectations
- [ ] Performance is acceptable
- [ ] Pattern demonstrates hierarchy effectively

### Notes

[Space for test notes and observations]

---

## Conclusion

This test suite comprehensively validates Pattern 6: Hierarchical Skills implementation. It demonstrates:

1. **Parent skill routing** - Intelligent delegation based on request
2. **Child skill specialization** - Focused analysis for specific domains
3. **Flexible composition** - Full or partial analysis based on needs
4. **Output synthesis** - Coherent reports combining multiple perspectives
5. **Token efficiency** - Significant savings for focused requests

The pattern successfully shows how to organize complex systems using hierarchical skill delegation.
