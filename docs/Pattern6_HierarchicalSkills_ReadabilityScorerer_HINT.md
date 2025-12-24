# Hierarchical Skills Example: Text Analysis System

## Overview

This example demonstrates **Pattern 6: Hierarchical Skills** using pure prompt-based skills (no MCP dependencies). We'll build a text analysis system where a parent skill delegates to specialized child skills for different aspects of language processing.

**Use Case**: Analyze documents for writing quality, sentiment, readability, and SEO optimization.

---

## Architecture

```
User Request: "Analyze this blog post for publication"
    ↓
[Parent Skill: text-analyzer]
  - Determines which analyses to run
  - Coordinates child skills
  - Synthesizes final report
    ↓
    /         |         |         \
   ↓          ↓         ↓          ↓
[grammar-   [sentiment- [readability- [seo-
checker]    analyzer]   scorer]      optimizer]
   ↓          ↓          ↓           ↓
Grammar     Sentiment   Reading     SEO
Report      Analysis    Level       Suggestions
```

---

## Directory Structure

```
.github/skills/
├── text-analyzer/              # Parent Skill
│   └── SKILL.md
├── grammar-checker/            # Child Skill 1
│   └── SKILL.md
├── sentiment-analyzer/         # Child Skill 2
│   └── SKILL.md
├── readability-scorer/         # Child Skill 3
│   └── SKILL.md
└── seo-optimizer/              # Child Skill 4
    └── SKILL.md
```

---

## Parent Skill: Text Analyzer

**File**: `.github/skills/text-analyzer/SKILL.md`

```yaml
---
name: text-analyzer
description: Comprehensive text analysis coordinator. Analyzes documents for grammar, sentiment, readability, and SEO. Delegates to specialized child skills.
---

# Text Analyzer (Parent Skill)

I coordinate comprehensive text analysis by delegating to specialized child skills:

## Child Skills I Use

1. **grammar-checker**: Grammar, spelling, punctuation analysis
2. **sentiment-analyzer**: Emotional tone and sentiment detection
3. **readability-scorer**: Readability metrics and audience appropriateness
4. **seo-optimizer**: SEO recommendations and keyword optimization

## When This Skill Activates

Activate when user requests:
- "Analyze this text/document/article/post"
- "Review this content for publication"
- "Check this writing quality"
- "Evaluate this document comprehensively"
- Any request combining multiple text analysis aspects

## How I Coordinate

For comprehensive analysis, I:
1. Determine which child skills are needed based on request
2. Invoke relevant child skills in appropriate order
3. Synthesize results into coherent report
4. Provide prioritized recommendations

## Typical Workflows

**Full Analysis** (all aspects):
1. grammar-checker → identify language issues
2. sentiment-analyzer → understand emotional tone
3. readability-scorer → assess audience fit
4. seo-optimizer → suggest improvements
5. Synthesize comprehensive report

**Quick Review** (grammar + readability):
1. grammar-checker → language correctness
2. readability-scorer → audience appropriateness
3. Provide concise feedback

**Marketing Focus** (sentiment + SEO):
1. sentiment-analyzer → emotional impact
2. seo-optimizer → search optimization
3. Marketing-focused recommendations

## Output Format

Provide structured analysis report:
- **Executive Summary**: Key findings and priority actions
- **Grammar & Language**: Issues and corrections
- **Sentiment**: Emotional tone analysis
- **Readability**: Scores and audience fit
- **SEO**: Optimization opportunities
- **Recommendations**: Prioritized action items

## Example Requests

✅ "Analyze this blog post before publishing"
✅ "Review this marketing email comprehensively"
✅ "Check this article for grammar and readability"
✅ "Evaluate this content for SEO and sentiment"
```

---

## Child Skill 1: Grammar Checker

**File**: `.github/skills/grammar-checker/SKILL.md`

```yaml
---
name: grammar-checker
description: Analyze text for grammar, spelling, punctuation, and style issues. Provide corrections and explanations.
---

# Grammar Checker

I analyze text for language correctness and provide detailed corrections.

## What I Check

### Grammar Issues
- Subject-verb agreement
- Verb tense consistency
- Pronoun agreement and clarity
- Sentence fragments and run-ons
- Misplaced modifiers

### Spelling & Punctuation
- Spelling errors (including commonly confused words)
- Punctuation mistakes (commas, semicolons, apostrophes)
- Capitalization errors
- Hyphenation issues

### Style & Clarity
- Passive voice overuse
- Wordiness and redundancy
- Unclear antecedents
- Awkward phrasing
- Inconsistent tone

## When This Skill Activates

Activate when user requests:
- "Check grammar"
- "Fix spelling and punctuation"
- "Proofread this text"
- "Find language errors"
- Any request about correctness of writing

## Analysis Process

1. **Scan Text**: Identify all grammar/spelling/punctuation issues
2. **Categorize**: Group issues by type and severity
3. **Provide Corrections**: Suggest specific fixes
4. **Explain**: Brief explanation for each correction
5. **Prioritize**: Mark critical vs. minor issues

## Output Format

Provide structured grammar report:

**Critical Issues** (must fix):
- Issue description
- Location in text
- Correction
- Explanation

**Minor Issues** (should fix):
- Issue description
- Suggested improvement
- Reasoning

**Style Suggestions** (consider):
- Observation
- Alternative phrasing
- Impact on clarity

## Example Analysis

**Input**: "The team are working on there project and its going good."

**Output**:
```
Critical Issues:
1. Subject-verb agreement: "team are" → "team is"
   - Collective nouns take singular verbs
   
2. Wrong homophone: "there project" → "their project"
   - "There" (location) vs. "their" (possession)
   
3. Missing apostrophe: "its going" → "it's going"
   - Contraction of "it is"

Style Suggestions:
1. Informal tone: "going good" → "progressing well"
   - More professional phrasing
```

## Tone

- Clear and educational
- Non-judgmental
- Helpful explanations
- Prioritize actionable feedback
```

---

## Child Skill 2: Sentiment Analyzer

**File**: `.github/skills/sentiment-analyzer/SKILL.md`

```yaml
---
name: sentiment-analyzer
description: Analyze emotional tone, sentiment polarity, and psychological impact of text. Identify mood, attitude, and emotional triggers.
---

# Sentiment Analyzer

I analyze the emotional tone and psychological impact of text.

## What I Analyze

### Sentiment Dimensions
- **Polarity**: Positive, negative, neutral, mixed
- **Intensity**: Strength of emotion (mild, moderate, strong)
- **Subjectivity**: Objective facts vs. subjective opinions
- **Emotional Tone**: Joy, anger, sadness, fear, surprise, disgust, trust

### Psychological Aspects
- **Voice & Attitude**: Authoritative, friendly, aggressive, passive
- **Persuasion Techniques**: Appeals to emotion, logic, credibility
- **Emotional Triggers**: Words/phrases that evoke strong feelings
- **Overall Mood**: Optimistic, pessimistic, neutral, balanced

### Audience Impact
- How text likely makes readers feel
- Potential emotional reactions
- Alignment with intended message
- Persuasiveness for target audience

## When This Skill Activates

Activate when user requests:
- "Analyze sentiment" or "check emotional tone"
- "How does this sound?" or "what's the mood?"
- "Is this too negative/positive?"
- "Analyze psychological impact"
- Any request about emotional aspects

## Analysis Process

1. **Identify Sentiment Markers**: Emotional words, phrases, punctuation
2. **Assess Polarity**: Overall positive/negative/neutral balance
3. **Measure Intensity**: Strength of emotional expression
4. **Detect Tone**: Dominant emotional characteristics
5. **Evaluate Impact**: Likely reader response

## Output Format

Provide structured sentiment report:

**Overall Sentiment**:
- Polarity: [Positive/Negative/Neutral/Mixed]
- Intensity: [Mild/Moderate/Strong]
- Dominant Emotion: [Primary emotional tone]

**Detailed Analysis**:
- Positive elements: [Specific examples]
- Negative elements: [Specific examples]
- Neutral/factual elements: [Specific examples]

**Emotional Triggers**:
- Powerful phrases and their emotional impact
- Words that evoke strong feelings

**Tone Characteristics**:
- Voice: [Authoritative/Friendly/Casual/Formal]
- Attitude: [Optimistic/Pessimistic/Balanced]
- Subjectivity: [Highly subjective/Mostly objective]

**Audience Impact**:
- Likely reader emotions
- Persuasiveness assessment
- Alignment with intent

## Example Analysis

**Input**: "Our revolutionary product absolutely transforms your workflow! Say goodbye to tedious manual tasks forever. You'll wonder how you ever managed without it."

**Output**:
```
Overall Sentiment:
- Polarity: Strongly Positive
- Intensity: Strong
- Dominant Emotion: Excitement / Enthusiasm

Detailed Analysis:
Positive Elements:
- "revolutionary" - innovation, breakthrough
- "absolutely transforms" - powerful change
- "forever" - permanence, reliability

Emotional Triggers:
- "Say goodbye to tedious manual tasks" - relief from pain point
- "You'll wonder how you ever managed" - creates FOMO

Tone Characteristics:
- Voice: Marketing/promotional, enthusiastic
- Attitude: Very optimistic, confident
- Subjectivity: Highly subjective with strong claims

Audience Impact:
- Likely creates excitement and curiosity
- May feel overly promotional to skeptical readers
- Effective for marketing-receptive audience
- Consider toning down for professional/technical audiences
```

## Tone

- Objective and analytical
- Psychologically informed
- Balanced perspective
- Contextual awareness
```

---

## Child Skill 3: Readability Scorer

**File**: `.github/skills/readability-scorer/SKILL.md`

```yaml
---
name: readability-scorer
description: Assess text readability using multiple metrics. Evaluate complexity, sentence structure, vocabulary, and audience appropriateness.
---

# Readability Scorer

I assess how easy text is to read and understand for different audiences.

## What I Measure

### Readability Metrics
- **Flesch Reading Ease**: 0-100 scale (higher = easier)
- **Flesch-Kincaid Grade Level**: U.S. school grade equivalent
- **Average Sentence Length**: Words per sentence
- **Average Word Length**: Syllables per word
- **Complex Words**: Percentage of 3+ syllable words

### Structural Analysis
- Sentence variety (simple, compound, complex)
- Paragraph length and structure
- Use of transition words
- Logical flow and organization

### Vocabulary Assessment
- Technical jargon usage
- Common vs. rare words
- Active vs. passive voice ratio
- Concrete vs. abstract language

### Audience Fit
- Recommended audience (general public, professionals, experts)
- Education level required
- Domain expertise needed

## When This Skill Activates

Activate when user requests:
- "Check readability" or "reading level"
- "Is this too complex/simple?"
- "What audience is this for?"
- "Simplify this text" or "make more accessible"
- Any request about comprehension difficulty

## Analysis Process

1. **Calculate Metrics**: Compute readability scores
2. **Analyze Structure**: Evaluate sentence and paragraph patterns
3. **Assess Vocabulary**: Identify complex/technical terms
4. **Determine Audience Fit**: Match to reader profiles
5. **Provide Recommendations**: Suggest improvements

## Output Format

Provide structured readability report:

**Readability Scores**:
- Flesch Reading Ease: [Score] ([Interpretation])
- Flesch-Kincaid Grade: [Level] ([Equivalent])
- Overall Assessment: [Very Easy/Easy/Moderate/Difficult/Very Difficult]

**Structural Analysis**:
- Average sentence length: [X words] ([Assessment])
- Sentence variety: [Good/Needs improvement]
- Paragraph structure: [Assessment]
- Logical flow: [Clear/Confusing]

**Vocabulary Analysis**:
- Complex words: [X%]
- Technical jargon: [Examples]
- Passive voice: [X%]
- Recommendations: [Specific suggestions]

**Audience Fit**:
- Best suited for: [Audience description]
- Education level: [Grade level or equivalent]
- Domain expertise: [None/Basic/Intermediate/Advanced]

**Improvement Suggestions**:
- Specific recommendations to improve readability
- Examples of simplifications

## Example Analysis

**Input**: "The implementation of our sophisticated algorithmic framework necessitates comprehensive documentation to facilitate subsequent modifications and enhancements."

**Output**:
```
Readability Scores:
- Flesch Reading Ease: 12 (Very Difficult)
- Flesch-Kincaid Grade: 18+ (College graduate level)
- Overall Assessment: Very Difficult

Structural Analysis:
- Average sentence length: 19 words (Long)
- Single complex sentence - needs variety
- Heavy noun stacking

Vocabulary Analysis:
- Complex words: 65%
- Technical jargon: "algorithmic framework"
- Passive voice: 0% (good)
- Unnecessarily complex: "implementation", "necessitates", "facilitate", "subsequent"

Audience Fit:
- Best suited for: Technical experts
- Education level: College graduate+
- Domain expertise: Advanced programming/CS

Improvement Suggestions:
1. Break into multiple sentences
2. Replace complex words:
   - "implementation" → "use"
   - "necessitates" → "requires" or "needs"
   - "facilitate" → "enable" or "help"
   - "subsequent" → "future" or "later"

Simplified version:
"Our algorithm framework needs good documentation. This will help us make changes and improvements later."

New scores:
- Flesch Reading Ease: 72 (Fairly Easy)
- Grade Level: 7th grade
```

## Tone

- Educational and constructive
- Data-driven
- Audience-aware
- Practical recommendations
```

---

## Child Skill 4: SEO Optimizer

**File**: `.github/skills/seo-optimizer/SKILL.md`

```yaml
---
name: seo-optimizer
description: Analyze and optimize text for search engines. Evaluate keyword usage, metadata, structure, and provide SEO recommendations.
---

# SEO Optimizer

I analyze text for search engine optimization and provide actionable recommendations.

## What I Analyze

### Keyword Optimization
- Primary keyword identification and density
- Secondary keyword usage
- Keyword placement (title, headers, first paragraph)
- Long-tail keyword opportunities
- Keyword stuffing detection

### Content Structure
- Heading hierarchy (H1, H2, H3)
- Paragraph length and scanability
- Use of lists and bullet points
- Internal linking opportunities
- Content length and depth

### On-Page SEO Elements
- Title tag optimization
- Meta description suggestions
- URL structure recommendations
- Image alt text (if applicable)
- Schema markup opportunities

### Content Quality
- Topic coverage and depth
- Search intent alignment
- Unique value proposition
- Content freshness indicators
- E-A-T signals (Expertise, Authoritativeness, Trustworthiness)

## When This Skill Activates

Activate when user requests:
- "Optimize for SEO" or "improve search ranking"
- "Check keywords" or "keyword density"
- "SEO review" or "search optimization"
- "Make this more discoverable"
- Any request about search visibility

## Analysis Process

1. **Identify Target Keywords**: Determine primary/secondary keywords
2. **Analyze Current Optimization**: Assess keyword usage and placement
3. **Evaluate Structure**: Check heading hierarchy and organization
4. **Assess Content Quality**: Evaluate depth, uniqueness, and value
5. **Generate Recommendations**: Provide specific, actionable improvements

## Output Format

Provide structured SEO report:

**Keyword Analysis**:
- Primary keyword: [Identified keyword]
- Keyword density: [X%] ([Too low/Good/Too high])
- Keyword placement: [Assessment]
- Secondary keywords: [List]
- Opportunities: [Suggested keywords]

**Content Structure**:
- Heading hierarchy: [Assessment]
- Content length: [X words] ([Assessment])
- Paragraph structure: [Assessment]
- Scanability: [Good/Needs improvement]

**On-Page SEO**:
- Suggested title tag (50-60 chars)
- Suggested meta description (150-160 chars)
- URL recommendation
- Internal linking opportunities

**Content Quality**:
- Topic depth: [Shallow/Moderate/Comprehensive]
- Search intent: [Informational/Transactional/Navigational]
- Unique value: [Assessment]
- E-A-T signals: [Present/Weak/Missing]

**Recommendations** (prioritized):
1. [High priority item]
2. [Medium priority item]
3. [Low priority item]

## Example Analysis

**Input**: "Machine Learning Guide

Machine learning is cool. It uses computers to learn stuff. There are different types. Supervised learning is one type. Unsupervised is another."

**Output**:
```
Keyword Analysis:
- Primary keyword: "machine learning" (detected)
- Keyword density: 2.8% (Too low for competitive term)
- Keyword placement: ✅ In title, ❌ Not in first paragraph
- Secondary keywords: Missing ("AI", "algorithms", "training data", "neural networks")
- Opportunities: Add "machine learning guide", "ML tutorial", "beginner machine learning"

Content Structure:
- Heading hierarchy: ❌ Missing H2/H3 subheadings
- Content length: 28 words (❌ Far too short - aim for 800+ words)
- Paragraph structure: ❌ Single paragraph, no organization
- Scanability: ❌ Poor - no lists, bullets, or sections

On-Page SEO:
- Title: "Machine Learning Guide" (Too generic)
  Suggested: "Machine Learning for Beginners: Complete Guide 2024"
  
- Meta description: (Missing)
  Suggested: "Learn machine learning basics with our beginner-friendly guide. Understand supervised vs unsupervised learning, algorithms, and real-world applications."
  
- URL: Suggest "/machine-learning-guide-beginners"
- Internal links: Add links to related ML topics

Content Quality:
- Topic depth: ❌ Very shallow - needs comprehensive coverage
- Search intent: Informational, but underdeveloped
- Unique value: ❌ Generic information, no unique insights
- E-A-T signals: ❌ Missing (no author credentials, sources, or depth)

High Priority Recommendations:
1. **Expand content to 1000+ words**
   - Add sections: "What is Machine Learning?", "Types of ML", "How It Works", "Applications", "Getting Started"
   
2. **Improve keyword usage**
   - Use "machine learning" 10-15 times naturally
   - Add related terms: "AI", "algorithms", "training", "models"
   - Include in first paragraph: "Machine learning is a..."

3. **Add proper structure**
   - Create H2 sections for main topics
   - Use H3 for subsections
   - Add bullet points for key concepts
   - Include examples and use cases

4. **Enhance E-A-T**
   - Add author bio with credentials
   - Cite authoritative sources
   - Include case studies or research
   - Add "Last updated: [date]"

5. **Optimize technical elements**
   - Title tag with primary keyword + year
   - Meta description highlighting unique value
   - Add schema markup (Article or HowTo)
```

## Tone

- Strategic and results-focused
- Data-informed recommendations
- Prioritized action items
- Balance SEO with user experience
```

---

## Usage Example

### Request 1: Full Comprehensive Analysis

```python
from claude_agent_sdk import query, ClaudeAgentOptions

text = """
AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms 
can now diagnose diseases faster than doctors. This technology is amazing and 
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical 
datasets for optimal performance metrics.
"""

options = ClaudeAgentOptions(
    setting_sources=["project"],  # Loads all skills from .github/skills/
    allowed_tools=["Skill"]  # Only pure skills, no MCP
)

async for message in query(
    f"Analyze this healthcare article comprehensively:\n\n{text}",
    options=options
):
    print(message)
```

**Expected Flow**:
1. Parent skill (`text-analyzer`) activates
2. Recognizes need for full analysis
3. Delegates to all 4 child skills:
   - `grammar-checker` → finds "AI are" error, awkward phrasing
   - `sentiment-analyzer` → identifies overly enthusiastic tone, marketing language
   - `readability-scorer` → notes inconsistent complexity, second paragraph too complex
   - `seo-optimizer` → suggests keyword optimization, structure improvements
4. Synthesizes comprehensive report with prioritized recommendations

---

### Request 2: Specific Analysis (Grammar + Readability)

```python
async for message in query(
    f"Check this for grammar and readability:\n\n{text}",
    options=options
):
    print(message)
```

**Expected Flow**:
1. Parent skill activates
2. Recognizes specific request (only grammar + readability)
3. Delegates to 2 child skills:
   - `grammar-checker` → language corrections
   - `readability-scorer` → complexity assessment
4. Provides focused report

---

### Request 3: Marketing Focus (Sentiment + SEO)

```python
async for message in query(
    f"Optimize this for marketing effectiveness:\n\n{text}",
    options=options
):
    print(message)
```

**Expected Flow**:
1. Parent skill activates
2. Interprets "marketing effectiveness" → sentiment + SEO
3. Delegates to 2 child skills:
   - `sentiment-analyzer` → emotional impact
   - `seo-optimizer` → discoverability
4. Provides marketing-focused recommendations

---

## Key Benefits of This Design

### 1. Pure Prompt Skills (No MCP Complexity)
- Each skill is self-contained prompt engineering
- No external dependencies or servers
- Easy to understand and maintain
- Fast to develop and iterate

### 2. Clear Separation of Concerns
- Each child skill has one job
- Parent skill handles coordination
- No overlap in responsibilities

### 3. Flexible Invocation
- Can use all skills or subset
- Parent adapts to request
- Natural language routing

### 4. Modular and Extensible
- Easy to add new child skills (e.g., `plagiarism-checker`, `fact-checker`)
- Update one skill without affecting others
- Can have multiple parent skills for different domains

### 5. Real-World Language Processing
- Demonstrates practical NLP applications
- Each skill shows different analysis dimension
- Realistic output examples

---

## Adding New Child Skills

To extend this system, simply add a new skill:

```
.github/skills/
└── plagiarism-checker/
    └── SKILL.md
```

Then update parent skill to mention it:

```yaml
## Child Skills I Use

1. grammar-checker
2. sentiment-analyzer
3. readability-scorer
4. seo-optimizer
5. **plagiarism-checker**: Detect copied content (NEW!)
```

No code changes needed - just pure prompt engineering!

---

## Testing the Hierarchy

```python
# Test 1: Verify parent skill activates
result = query("Analyze this document", options)
# Expected: Parent skill recognizes "analyze" and coordinates

# Test 2: Verify specific child activates directly
result = query("Check grammar in this text", options)
# Expected: grammar-checker activates directly (bypasses parent)

# Test 3: Verify parent delegates correctly
result = query("Full analysis needed", options)
# Expected: Parent → all 4 children → synthesized report

# Test 4: Verify partial delegation
result = query("SEO and sentiment check", options)
# Expected: Parent → seo-optimizer + sentiment-analyzer only
```

---

## Comparison with MCP-Based Patterns

| Aspect | Pure Skill Hierarchy | Skill + MCP Hierarchy |
|--------|---------------------|----------------------|
| **Complexity** | Low (just prompts) | Medium-High (MCP servers) |
| **Dependencies** | None | External MCP servers |
| **Setup Time** | Minutes | Hours-Days |
| **Maintenance** | Easy (edit .md files) | Complex (MCP + skills) |
| **Best For** | Language/analysis tasks | Data operations, integrations |
| **Example** | Text analysis (this example) | E-commerce (order + inventory + shipping) |

This pure skill approach is perfect when you don't need external data sources or systems - just Claude's intelligence organized into specialized roles!