# Pattern 6: Direct Skill Testing with Claude

## Test 1: Blog Post Analysis

**Text to Analyze:**
```
AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms
can now diagnose diseases faster than doctors. This technology is amazing and
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical
datasets for optimal performance metrics.
```

**Your Request:**
Analyze this blog post comprehensively for potential publication. Check everything - grammar, tone, readability, and SEO optimization.

**Expected Skill Invocations:**
1. ✅ grammar-checker - Fix "are" to "is", improve phrasing
2. ✅ sentiment-analyzer - Analyze marketing tone vs technical tone mismatch
3. ✅ readability-scorer - Note inconsistent complexity (6th grade → 18th grade)
4. ✅ seo-optimizer - Suggest structure, keywords, meta description

**Expected Token Cost:** ~1000 tokens

---

## Test 2: Quick Grammar Check

**Text to Analyze:**
```
The team are working on there project and its going good.
```

**Your Request:**
Just check the grammar and spelling.

**Expected Skill Invocations:**
1. ✅ grammar-checker - Only this child skill invoked

**Not Invoked:**
- ❌ sentiment-analyzer (not requested)
- ❌ readability-scorer (not requested)
- ❌ seo-optimizer (not requested)

**Expected Token Cost:** ~400 tokens (60% savings)

---

## Test 3: Marketing Content Optimization

**Text to Analyze:**
```
Revolutionary AI Platform Transforms Your Business

Tired of manual processes? Our revolutionary AI platform absolutely transforms
how you work. Say goodbye to tedious manual tasks forever. You'll wonder how
you ever managed without it!

Our cutting-edge machine learning technology learns from your data and optimizes
workflows automatically. Increase productivity by 300%! Join thousands of happy
customers saving time and money every day.
```

**Your Request:**
Optimize this for marketing effectiveness - I want to know about emotional impact and search optimization.

**Expected Skill Invocations:**
1. ✅ sentiment-analyzer - Strong positive polarity, effective persuasion
2. ✅ seo-optimizer - Keywords, structure, meta descriptions

**Not Invoked:**
- ❌ grammar-checker (marketing copy is grammatically correct)
- ❌ readability-scorer (readability isn't the concern for marketing)

**Expected Token Cost:** ~700 tokens

---

## How to Test: Copy & Paste Method

### Step 1: Copy a test request below
### Step 2: Paste it into Claude
### Step 3: Observe which skills Claude invokes

---

## Copy-Paste Tests

### Test Request 1: Comprehensive Analysis

```
I'm publishing this blog post about AI in healthcare. Please analyze it comprehensively before I publish.

Text:
"AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms
can now diagnose diseases faster than doctors. This technology is amazing and
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical
datasets for optimal performance metrics."

Please check everything - grammar, emotional tone, readability, and search optimization.
```

**Copy this and paste into Claude ↑**

---

### Test Request 2: Focused Grammar Check

```
Quick question - can you check the grammar in this sentence?

"The team are working on there project and its going good."

Just fix the grammar and spelling errors.
```

**Copy this and paste into Claude ↑**

---

### Test Request 3: Marketing Optimization

```
I have marketing copy I need optimized. I want to know:
1. How emotionally compelling is it?
2. Is it optimized for search engines?

Marketing copy:
"Revolutionary AI Platform Transforms Your Business

Tired of manual processes? Our revolutionary AI platform absolutely transforms
how you work. Say goodbye to tedious manual tasks forever. You'll wonder how
you ever managed without it!

Our cutting-edge machine learning technology learns from your data and optimizes
workflows automatically. Increase productivity by 300%! Join thousands of happy
customers saving time and money every day."

Focus on sentiment analysis and SEO optimization.
```

**Copy this and paste into Claude ↑**

---

### Test Request 4: Vague Request (Default to Comprehensive)

```
Review this content before I publish it.

"Configuration Guide

The system configuration process involves multiple interdependent components.
Prior to initialization, ensure all prerequisites are satisfied. The configuration
file format utilizes JSON specification. Each configuration object contains
mandatory fields and optional extensions.

Settings can be modified via the command-line interface or configuration files.
Runtime modifications necessitate server restart."
```

**Copy this and paste into Claude ↑**

---

## What Claude Will Do

When you send a test request, Claude will:

1. **Recognize the pattern**: Identify that this is a Pattern 6 request
2. **Analyze the request**: Look at keywords like "comprehensive", "grammar", "sentiment", "readability", "SEO"
3. **Invoke appropriate skills**:
   - Parent skill: `text-analyzer` (if comprehensive)
   - Child skills: Based on request keywords
4. **Provide analysis**: Show results from each invoked skill
5. **Synthesize results**: Combine findings into structured report

---

## Example: What Comprehensive Analysis Looks Like

When you ask Claude to "Analyze comprehensively", here's what happens:

```
COMPREHENSIVE TEXT ANALYSIS REPORT
═══════════════════════════════════

EXECUTIVE SUMMARY
─────────────────
Key Findings:
- 3 critical grammar issues
- Mixed sentiment (marketing vs technical)
- Inconsistent readability (6th to 18th grade)
- Needs SEO optimization

Priority Actions:
1. Fix grammar errors
2. Clarify target audience
3. Add structure and headings
4. Optimize for keywords

─────────────────────────────────────────────────────────────

GRAMMAR & LANGUAGE
──────────────────
(Results from grammar-checker skill)

Critical Issues:
1. Subject-verb agreement: "intelligence are" → "intelligence is"
2. Consistency: Marketing tone vs technical jargon
3. Phrasing: "will change everything forever" → overpromising

─────────────────────────────────────────────────────────────

SENTIMENT
─────────
(Results from sentiment-analyzer skill)

Polarity: Mixed (Strong positive + Neutral technical)
- First paragraph: Excited, marketing-focused
- Second paragraph: Formal, technical

Audience Impact:
- Marketing audience: Persuaded
- Technical audience: Confused by mixed messages

─────────────────────────────────────────────────────────────

READABILITY
───────────
(Results from readability-scorer skill)

Flesch Reading Ease: 45 (Fairly Difficult)
- Paragraph 1: 72 (6th grade - Easy)
- Paragraph 2: 18 (18th grade - Very Difficult)

Issue: Massive inconsistency in complexity level

─────────────────────────────────────────────────────────────

SEO OPTIMIZATION
────────────────
(Results from seo-optimizer skill)

Keywords: "artificial intelligence" 2.1% (too low)
Structure: Missing headings, poor scanability
Meta: Missing description, title too generic

Recommendations:
1. Expand to 800+ words
2. Add H2/H3 structure
3. Improve keyword density
4. Add meta description

─────────────────────────────────────────────────────────────

RECOMMENDATIONS (Prioritized)
────────────────────────────
1. Fix grammar errors immediately
2. Choose target audience (general vs technical)
3. Expand content and add structure
4. Optimize for search engines
```

---

## Watch the Skills in Action

### What You'll See:

When Claude invokes skills, you'll notice:
- **Specific analysis sections** for each skill domain
- **Detailed findings** with examples
- **Actionable recommendations** from each skill
- **Synthesized final report** combining all perspectives

### Token Efficiency in Action:

- **Full analysis**: ~1000 tokens
  - All 4 skills invoked
  - Comprehensive report

- **Focused queries**: ~400-700 tokens
  - Only relevant skills
  - Faster response
  - 40-60% savings

---

## Try It Now!

Pick any test above and paste it into Claude. You'll see:

✅ Skills being identified and invoked
✅ Detailed analysis from each skill
✅ Combined recommendations
✅ Efficient token usage

The skills work together seamlessly to provide comprehensive, multi-dimensional analysis!

---

## Key Points

### Parent Skill (text-analyzer) Routes Based On:
- "comprehensive" → All 4 children
- "grammar" → grammar-checker
- "sentiment" / "tone" → sentiment-analyzer
- "readability" / "complexity" → readability-scorer
- "seo" / "search" / "marketing" → seo-optimizer
- Vague requests → All 4 (comprehensive default)

### Each Child Skill Provides:
- **grammar-checker**: Issues, corrections, explanations
- **sentiment-analyzer**: Polarity, intensity, emotional triggers
- **readability-scorer**: Flesch scores, grade level, vocabulary analysis
- **seo-optimizer**: Keywords, structure, meta elements, recommendations

### Results Are Synthesized Into:
- Executive summary
- Section for each relevant skill
- Prioritized recommendations
- Actionable next steps

---

## Questions?

The skills are designed to handle:
- Complex multi-dimensional requests ✓
- Focused specific requests ✓
- Vague requests with intelligent defaults ✓
- Real-world text analysis scenarios ✓

Just paste a test and see the skills in action!
