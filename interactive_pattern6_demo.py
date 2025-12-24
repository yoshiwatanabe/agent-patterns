#!/usr/bin/env python3
"""
Pattern 6: Hierarchical Skills - Interactive Demo

This script provides an interactive console experience for testing Pattern 6.
Send text and requests to see which skills get invoked and what analyses they would perform.

Usage:
    python interactive_pattern6_demo.py
"""

import asyncio
from typing import List, Dict, Optional


class SkillDemoSimulator:
    """Simulates Pattern 6 skill invocation with realistic examples"""

    def __init__(self):
        self.conversation_history = []

    # Sample analysis outputs
    SAMPLE_OUTPUTS = {
        "grammar-checker": """
GRAMMAR & LANGUAGE ANALYSIS
────────────────────────────

Critical Issues Found:
1. Subject-verb agreement: "Artificial intelligence are" → "Artificial intelligence is"
2. Missing apostrophe: "its going" → "it's going"
3. Awkward phrasing: "will change everything forever" → Consider "will have significant impact"

Minor Issues:
- Tone: "amazing" is too subjective → Consider "significant" or "transformative"
- Consistency: First paragraph is casual, second is overly technical

Style Suggestions:
- Use active voice more consistently
- Break up long sentences for clarity
- Reduce marketing language in technical context

Total Issues: 3 critical, 2 minor, 2 style suggestions
""",

        "sentiment-analyzer": """
SENTIMENT & EMOTIONAL TONE ANALYSIS
────────────────────────────────────

Overall Sentiment:
- Polarity: Mixed (Strongly positive first paragraph, neutral second)
- Intensity: Strong (marketing-heavy language)
- Dominant Emotion: Excitement + Technical confidence

Detailed Analysis:
Positive Elements:
- "revolutionizing" - Innovation signal
- "faster than doctors" - Clear value proposition
- "will transform" - Forward-looking optimism

Warning Signals:
- "will change everything forever" - Overpromising
- "so happy" - Too casual for healthcare content

Tone Characteristics:
- Voice: Marketing/promotional, enthusiastic
- Attitude: Overly optimistic
- Subjectivity: Highly subjective with strong claims

Audience Impact:
✓ Appeals to decision-makers with benefits
✗ May create trust concerns with overpromising
✗ Inconsistent messaging confuses audience

Recommendation: Choose target audience and maintain consistent tone throughout
""",

        "readability-scorer": """
READABILITY & COMPLEXITY ANALYSIS
──────────────────────────────────

Readability Scores:
- Flesch Reading Ease: 45 (Fairly Difficult)
- Flesch-Kincaid Grade: 10.5 (10th grade)
- Overall Assessment: Inconsistent (easy to very difficult)

Detailed Breakdown:
Paragraph 1:
- Flesch Reading Ease: 72 (Fairly Easy)
- Grade Level: 6th grade
- Simple language, accessible to general readers

Paragraph 2:
- Flesch Reading Ease: 18 (Very Difficult)
- Grade Level: 18+ (College graduate)
- Heavy jargon, complex sentence structure

Vocabulary Analysis:
- Complex words: 35%
- Technical jargon: "algorithmic implementations", "performance metrics"
- Passive voice: 15%
- Recommended: Simplify or remove technical jargon

Structural Issues:
- No headings or sections
- Inconsistent paragraph focus
- Lacks transition words between ideas

Audience Fit:
- Paragraph 1: General public (easy to understand)
- Paragraph 2: Technical experts only
- Overall: Confusing for both audiences

Recommendations:
1. Choose your target audience (general vs. technical)
2. Maintain consistent complexity throughout
3. Break second paragraph into smaller sentences
4. Define technical terms or use simpler alternatives
5. Add subheadings for better organization
""",

        "seo-optimizer": """
SEO & SEARCH OPTIMIZATION ANALYSIS
───────────────────────────────────

Keyword Analysis:
- Primary keyword: "artificial intelligence" (2.1% density - LOW)
- Keyword placement: ✓ In title, ✗ Not emphasized throughout
- Secondary keywords needed: "healthcare", "diagnosis", "machine learning"
- Opportunities: Add "AI in healthcare", "medical diagnosis"

Content Structure:
- Heading hierarchy: ✗ Missing (no H2/H3 tags)
- Content length: 87 words (✗ Too short - aim for 800+)
- Paragraph organization: ✗ Poor (single block)
- Scanability: ✗ Low (no lists, bullets, or sections)

On-Page SEO Elements:
Current Title: "AI Revolution in Healthcare" (26 chars)
Suggested: "How AI & Machine Learning Transform Healthcare Diagnostics" (59 chars)

Missing Meta Description (should be 150-160 chars):
"Explore how artificial intelligence and machine learning are revolutionizing
healthcare, improving diagnosis accuracy and speed. Learn about AI's
impact on medical professionals and patient outcomes."

Content Quality Assessment:
- Topic depth: Moderate (needs expansion)
- Search intent: Informational (well-aligned)
- Unique value: Weak (generic statements)
- E-A-T signals: Missing (no sources, credentials, or expertise)

High Priority Recommendations:
1. ⭐ Expand content to 800+ words minimum
2. ⭐ Add proper H2/H3 heading structure
3. ⭐ Create meta description (150-160 chars)
4. ⭐ Add author credentials and expertise signals
5. ⭐ Include data points, statistics, real examples

Medium Priority:
6. Add internal links to related topics
7. Improve keyword density naturally (2.1% → 3-5%)
8. Add schema markup (Article or HowTo)
9. Optimize images with alt text

Estimated SEO Score: 32/100 (Needs significant improvement)
""",

        "text-analyzer": """
COMPREHENSIVE TEXT ANALYSIS REPORT
──────────────────────────────────

Executive Summary:
Your text has 3 critical issues and significant improvement opportunities:
1. Grammar errors that affect professionalism
2. Inconsistent tone and complexity levels
3. Poor SEO optimization and structure

Priority Actions:
✓ Fix grammar issues immediately
✓ Simplify or restructure second paragraph
✓ Expand content and add heading structure
✓ Optimize for search engines

Report Summary:
- Grammar Issues: 3 critical
- Sentiment: Mixed (marketing + technical)
- Readability: Inconsistent (6th to 18th grade)
- SEO: Needs major improvement

Next Steps:
1. Review grammar corrections
2. Choose target audience
3. Expand and restructure content
4. Add SEO optimizations
5. Re-analyze after revisions
"""
    }

    def analyze_request(self, user_request: str) -> Dict:
        """Analyze user request and determine which skills to invoke"""
        request_lower = user_request.lower()

        # Initialize response
        response = {
            "parent_skill": "text-analyzer",
            "child_skills": [],
            "reasoning": []
        }

        # Check for specific skill triggers
        grammar_keywords = ["grammar", "spelling", "punctuation", "correct", "proofread", "language"]
        sentiment_keywords = ["sentiment", "tone", "emotional", "mood", "psychology", "persuade"]
        readability_keywords = ["readability", "complex", "simple", "audience", "easy", "difficult", "understand"]
        seo_keywords = ["seo", "search", "keyword", "optimize", "marketing", "discover", "rank"]

        if any(word in request_lower for word in grammar_keywords):
            response["child_skills"].append("grammar-checker")
            response["reasoning"].append(f"Request mentions: {[w for w in grammar_keywords if w in request_lower][0]}")

        if any(word in request_lower for word in sentiment_keywords):
            response["child_skills"].append("sentiment-analyzer")
            response["reasoning"].append(f"Request mentions: {[w for w in sentiment_keywords if w in request_lower][0]}")

        if any(word in request_lower for word in readability_keywords):
            response["child_skills"].append("readability-scorer")
            response["reasoning"].append(f"Request mentions: {[w for w in readability_keywords if w in request_lower][0]}")

        if any(word in request_lower for word in seo_keywords):
            response["child_skills"].append("seo-optimizer")
            response["reasoning"].append(f"Request mentions: {[w for w in seo_keywords if w in request_lower][0]}")

        # If no specific keywords, check for comprehensive analysis
        comprehensive_keywords = ["comprehensive", "everything", "full", "complete", "all", "analyze", "evaluate", "review"]
        if any(word in request_lower for word in comprehensive_keywords) and not response["child_skills"]:
            response["child_skills"] = ["grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"]
            response["reasoning"] = [f"Comprehensive request detected: {[w for w in comprehensive_keywords if w in request_lower][0]}"]

        # Default: if vague, do comprehensive
        if not response["child_skills"]:
            response["child_skills"] = ["grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"]
            response["reasoning"] = ["Vague request - defaulting to comprehensive analysis"]

        return response

    def generate_output(self, skills: List[str], sample_text: str) -> str:
        """Generate analysis output"""
        output = []
        output.append("\n" + "="*80)
        output.append("SKILL INVOCATION RESULTS")
        output.append("="*80 + "\n")

        # Show which skills were invoked
        output.append(f"Parent Skill: text-analyzer")
        output.append(f"Child Skills Invoked: {', '.join(skills)}\n")
        output.append(f"Text Length: {len(sample_text)} characters, {len(sample_text.split())} words\n")

        # Show each skill's output
        for skill in skills:
            output.append(f"\n{'─'*80}")
            output.append(f"SKILL: {skill.upper()}")
            output.append(f"{'─'*80}\n")

            if skill in self.SAMPLE_OUTPUTS:
                output.append(self.SAMPLE_OUTPUTS[skill])

        output.append("\n" + "="*80)
        return "\n".join(output)

    async def interactive_demo(self):
        """Run interactive demo"""
        print("\n" + "="*80)
        print("PATTERN 6: HIERARCHICAL SKILLS - INTERACTIVE DEMO")
        print("="*80)
        print("\nWelcome! Test Pattern 6 by sending text and requests.")
        print("The skills will analyze your request and show what would be invoked.\n")

        # Sample texts for quick testing
        sample_texts = {
            "1": {
                "name": "Healthcare Blog Post",
                "text": """AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms
can now diagnose diseases faster than doctors. This technology is amazing and
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical
datasets for optimal performance metrics."""
            },
            "2": {
                "name": "Marketing Copy",
                "text": """Revolutionary AI Platform Transforms Your Business

Tired of manual processes? Our revolutionary AI platform absolutely transforms
how you work. Say goodbye to tedious manual tasks forever. You'll wonder how
you ever managed without it!

Our cutting-edge machine learning technology learns from your data and optimizes
workflows automatically. Increase productivity by 300%! Join thousands of happy
customers saving time and money every day."""
            },
            "3": {
                "name": "Technical Documentation",
                "text": """Configuration Guide

The system configuration process involves multiple interdependent components.
Prior to initialization, ensure all prerequisites are satisfied. The configuration
file format utilizes JSON specification. Each configuration object contains
mandatory fields and optional extensions.

Settings can be modified via the command-line interface or configuration files.
Runtime modifications necessitate server restart."""
            }
        }

        while True:
            print("\nOptions:")
            print("  [1-3]  Use sample text")
            print("  [p]    Paste your own text")
            print("  [q]    Quit\n")

            choice = input("Select option: ").strip().lower()

            if choice == "q":
                print("\nThanks for testing Pattern 6! 👋\n")
                break

            if choice in sample_texts:
                sample = sample_texts[choice]
                print(f"\nUsing: {sample['name']}")
                text = sample["text"]
            elif choice == "p":
                print("\nPaste your text (press Enter twice when done):")
                lines = []
                try:
                    while True:
                        line = input()
                        if line == "":
                            if lines and lines[-1] == "":
                                break
                        lines.append(line)
                except EOFError:
                    pass
                text = "\n".join(lines[:-1]) if lines else ""

                if not text.strip():
                    print("No text provided!")
                    continue
            else:
                print("Invalid option!")
                continue

            # Get the request
            print("\nWhat would you like to analyze?")
            print("  Examples:")
            print("    - 'Check grammar and readability'")
            print("    - 'Optimize for marketing'")
            print("    - 'Full comprehensive analysis'")
            print("    - 'Just check the grammar'\n")

            request = input("Your request: ").strip()
            if not request:
                print("Please provide a request!")
                continue

            # Analyze and show results
            analysis = self.analyze_request(request)

            print("\n" + "="*80)
            print("REQUEST ANALYSIS")
            print("="*80)
            print(f"\nYour Request: '{request}'")
            print(f"\nSkill Routing Decision:")
            print(f"  Parent Skill: {analysis['parent_skill']}")
            print(f"  Child Skills to Invoke: {', '.join(analysis['child_skills'])}")
            print(f"\nReasoning:")
            for reason in analysis['reasoning']:
                print(f"  • {reason}")

            # Show the outputs
            output = self.generate_output(analysis['child_skills'], text)
            print(output)

            # Ask if they want to try another
            again = input("\nAnalyze another text? (y/n): ").strip().lower()
            if again != "y":
                print("\nThanks for testing Pattern 6! 👋\n")
                break


async def main():
    """Main entry point"""
    demo = SkillDemoSimulator()
    await demo.interactive_demo()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋\n")
