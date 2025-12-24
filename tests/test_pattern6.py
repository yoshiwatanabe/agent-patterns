#!/usr/bin/env python3
"""
Pattern 6: Hierarchical Skills - Test Runner

This script demonstrates how to test the text analysis skill hierarchy
using the Claude Agent SDK.
"""

import asyncio
from dataclasses import dataclass
from typing import AsyncGenerator


# Sample texts for testing
SAMPLE_TEXTS = {
    "healthcare_blog": """AI Revolution in Healthcare

Artificial intelligence are transforming healthcare. Machine learning algorithms
can now diagnose diseases faster than doctors. This technology is amazing and
will change everything forever! Patients will be so happy.

Our sophisticated algorithmic implementations necessitate comprehensive medical
datasets for optimal performance metrics.""",

    "tech_docs": """Configuration Guide

The system configuration process involves multiple interdependent components.
Prior to initialization, ensure all prerequisites are satisfied. The configuration
file format utilizes JSON specification. Each configuration object contains
mandatory fields and optional extensions.

Settings can be modified via the command-line interface or configuration files.
Runtime modifications necessitate server restart.""",

    "marketing_copy": """Revolutionary AI Platform Transforms Your Business

Tired of manual processes? Our revolutionary AI platform absolutely transforms
how you work. Say goodbye to tedious manual tasks forever. You'll wonder how
you ever managed without it!

Our cutting-edge machine learning technology learns from your data and optimizes
workflows automatically. Increase productivity by 300%! Join thousands of happy
customers saving time and money every day.""",
}


@dataclass
class TestScenario:
    """Represents a test scenario"""
    name: str
    description: str
    request: str
    text_key: str
    expected_skills: list[str]
    estimated_tokens: int


# Test scenarios
TEST_SCENARIOS = [
    TestScenario(
        name="Full Comprehensive Analysis",
        description="Analyze text using all 4 child skills",
        request="Analyze this blog post comprehensively for potential publication. Check everything.",
        text_key="healthcare_blog",
        expected_skills=["grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"],
        estimated_tokens=1000,
    ),
    TestScenario(
        name="Quick Review (Grammar + Readability)",
        description="Focus on grammar and readability only",
        request="Check this for grammar and readability. I need to make sure it's technically correct and easy to understand.",
        text_key="tech_docs",
        expected_skills=["grammar-checker", "readability-scorer"],
        estimated_tokens=600,
    ),
    TestScenario(
        name="Marketing Focus (Sentiment + SEO)",
        description="Optimize for marketing effectiveness",
        request="Optimize this for marketing effectiveness. I want emotional impact and search optimization.",
        text_key="marketing_copy",
        expected_skills=["sentiment-analyzer", "seo-optimizer"],
        estimated_tokens=700,
    ),
    TestScenario(
        name="Direct Child Skill (Grammar Only)",
        description="Bypass parent, invoke grammar-checker directly",
        request="Just check the grammar and fix spelling errors.",
        text_key="healthcare_blog",
        expected_skills=["grammar-checker"],
        estimated_tokens=400,
    ),
    TestScenario(
        name="Parent Recognition Test",
        description="Verify parent recognizes comprehensive request",
        request="Review this for publication",
        text_key="healthcare_blog",
        expected_skills=["text-analyzer", "grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"],
        estimated_tokens=1000,
    ),
]


class SkillTestRunner:
    """Test runner for Pattern 6 skills"""

    def __init__(self, use_real_sdk: bool = False):
        """
        Initialize test runner

        Args:
            use_real_sdk: If True, use real Claude Agent SDK (requires API key)
                         If False, simulate the skill invocation
        """
        self.use_real_sdk = use_real_sdk
        self.results = []

    async def run_test(self, scenario: TestScenario) -> dict:
        """Run a single test scenario"""
        print(f"\n{'='*70}")
        print(f"TEST: {scenario.name}")
        print(f"{'='*70}")
        print(f"Description: {scenario.description}")
        print(f"Expected Skills: {', '.join(scenario.expected_skills)}")
        print(f"Estimated Tokens: ~{scenario.estimated_tokens}")
        print(f"\nRequest:\n  {scenario.request}")
        print(f"\nText Sample:\n  {SAMPLE_TEXTS[scenario.text_key][:100]}...\n")

        if self.use_real_sdk:
            result = await self._run_with_sdk(scenario)
        else:
            result = await self._simulate_run(scenario)

        self.results.append({
            "scenario": scenario.name,
            "passed": result.get("passed", False),
            "skills_invoked": result.get("skills_invoked", []),
            "estimated_tokens": scenario.estimated_tokens,
        })

        return result

    async def _run_with_sdk(self, scenario: TestScenario) -> dict:
        """
        Run test using actual Claude Agent SDK

        This requires:
        - Claude Agent SDK installed
        - API key configured
        - Skills available in .github/skills/
        """
        try:
            from claude_agent_sdk import query, ClaudeAgentOptions

            print("Running with Claude Agent SDK...")

            options = ClaudeAgentOptions(
                setting_sources=["project"],  # Load skills from .github/skills/
                allowed_tools=["Skill"],  # Pure skills only
            )

            full_prompt = f"{scenario.request}\n\n{SAMPLE_TEXTS[scenario.text_key]}"

            response_text = ""
            async for message in query(full_prompt, options=options):
                response_text += str(message)
                print(f"  Received: {str(message)[:80]}...")

            # Check which skills were invoked by analyzing response
            invoked_skills = self._detect_invoked_skills(response_text)

            passed = all(
                skill in invoked_skills
                for skill in scenario.expected_skills
                if not skill.startswith("text-analyzer") or len(scenario.expected_skills) > 1
            )

            return {
                "passed": passed,
                "skills_invoked": invoked_skills,
                "response_sample": response_text[:200],
            }

        except ImportError:
            print("⚠️  Claude Agent SDK not available. Running simulation instead.")
            return await self._simulate_run(scenario)

    async def _simulate_run(self, scenario: TestScenario) -> dict:
        """Simulate skill invocation without actual SDK"""
        print("Simulating skill invocation...")

        # Simulate the parent skill routing logic
        skills_invoked = self._simulate_skill_routing(scenario.request)

        print(f"  ✓ Parent skill (text-analyzer) activated")
        for skill in skills_invoked:
            if skill != "text-analyzer":
                print(f"  ✓ Delegated to: {skill}")

        # Check if correct skills were invoked
        expected = set(scenario.expected_skills)
        invoked = set(skills_invoked)

        passed = expected.issubset(invoked)

        if passed:
            print(f"✅ PASS: All expected skills invoked")
        else:
            missing = expected - invoked
            print(f"❌ FAIL: Missing skills: {missing}")

        return {
            "passed": passed,
            "skills_invoked": skills_invoked,
        }

    def _simulate_skill_routing(self, request: str) -> list[str]:
        """
        Simulate parent skill routing logic

        Parent skill analyzes request and determines which children to invoke
        """
        request_lower = request.lower()
        skills = ["text-analyzer"]  # Parent always starts

        # Check for specific keywords that trigger children
        if any(word in request_lower for word in ["grammar", "spelling", "punctuation", "proofread", "language", "correct"]):
            skills.append("grammar-checker")

        if any(word in request_lower for word in ["sentiment", "tone", "emotional", "mood", "psychology"]):
            skills.append("sentiment-analyzer")

        if any(word in request_lower for word in ["readability", "complex", "simple", "audience", "easy", "difficult"]):
            skills.append("readability-scorer")

        if any(word in request_lower for word in ["seo", "search", "keyword", "optimize", "marketing", "discovery"]):
            skills.append("seo-optimizer")

        # If request asks for comprehensive analysis, include all
        if any(word in request_lower for word in ["comprehensive", "everything", "full", "complete", "all"]):
            skills = ["text-analyzer", "grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"]

        # If request seems vague or says "review for publication", do full analysis
        if any(word in request_lower for word in ["review", "publication", "publish", "analyze", "evaluate"]):
            if len(skills) == 1:  # Only parent activated
                skills = ["text-analyzer", "grammar-checker", "sentiment-analyzer", "readability-scorer", "seo-optimizer"]

        return skills

    def _detect_invoked_skills(self, response_text: str) -> list[str]:
        """Detect which skills were invoked from response text"""
        invoked = []

        if "text-analyzer" in response_text.lower() or "analyzing" in response_text.lower():
            invoked.append("text-analyzer")

        if any(word in response_text.lower() for word in ["grammar", "spelling", "punctuation"]):
            invoked.append("grammar-checker")

        if any(word in response_text.lower() for word in ["sentiment", "emotional", "tone"]):
            invoked.append("sentiment-analyzer")

        if any(word in response_text.lower() for word in ["readability", "reading ease", "flesch"]):
            invoked.append("readability-scorer")

        if any(word in response_text.lower() for word in ["keyword", "seo", "optimization"]):
            invoked.append("seo-optimizer")

        return invoked

    def print_summary(self):
        """Print test results summary"""
        print(f"\n\n{'='*70}")
        print("TEST SUMMARY")
        print(f"{'='*70}")

        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)

        print(f"\nResults: {passed}/{total} tests passed\n")

        for result in self.results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{status} | {result['scenario']}")
            print(f"     Skills: {', '.join(result['skills_invoked'])}")
            print(f"     Tokens: ~{result['estimated_tokens']}")
            print()

        total_tokens = sum(r["estimated_tokens"] for r in self.results)
        print(f"Total estimated tokens: ~{total_tokens}")
        print(f"Test execution: {'✅ SUCCESS' if passed == total else '⚠️  PARTIAL'}")


async def main():
    """Main test runner"""
    print("Pattern 6: Hierarchical Skills - Test Suite")
    print("=" * 70)
    print("\nConfiguration:")
    print("  Skills: text-analyzer (parent)")
    print("           ├─ grammar-checker")
    print("           ├─ sentiment-analyzer")
    print("           ├─ readability-scorer")
    print("           └─ seo-optimizer")
    print("\nTest Mode: Simulation (no SDK required)")
    print("Note: For real SDK tests, set use_real_sdk=True and configure API key")

    # Create test runner (simulation mode)
    runner = SkillTestRunner(use_real_sdk=False)

    # Run all test scenarios
    for scenario in TEST_SCENARIOS:
        await runner.run_test(scenario)

    # Print summary
    runner.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
