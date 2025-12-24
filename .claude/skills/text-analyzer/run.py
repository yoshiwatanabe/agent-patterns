#!/usr/bin/env python3
"""Text Analyzer Coordinator - Delegates to child skills and synthesizes results"""

import sys
import json
import subprocess
import os
from pathlib import Path
from typing import Dict, Any, List

class TextAnalyzerCoordinator:
    def __init__(self):
        self.skills_dir = Path(__file__).parent.parent
        self.child_skills = [
            "grammar-checker",
            "sentiment-analyzer",
            "readability-scorer",
            "seo-optimizer"
        ]

    def invoke_child_skill(self, skill_name: str, text: str) -> Dict[str, Any]:
        """Invoke a child skill and return its analysis"""
        skill_path = self.skills_dir / skill_name / "run.py"

        if not skill_path.exists():
            return {
                "skill": skill_name,
                "status": "error",
                "error": f"Skill not found: {skill_path}"
            }

        try:
            # Run the child skill script
            result = subprocess.run(
                [sys.executable, str(skill_path), text],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {
                    "skill": skill_name,
                    "status": "error",
                    "error": result.stderr
                }
        except Exception as e:
            return {
                "skill": skill_name,
                "status": "error",
                "error": str(e)
            }

    def synthesize_results(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from all child skills into a comprehensive report"""
        grammar = analyses.get("grammar-checker", {})
        sentiment = analyses.get("sentiment-analyzer", {})
        readability = analyses.get("readability-scorer", {})
        seo = analyses.get("seo-optimizer", {})

        # Extract key findings
        key_findings = []

        # Grammar findings
        if "critical_issues" in grammar:
            critical_count = len(grammar["critical_issues"])
            if critical_count > 0:
                key_findings.append(f"Grammar: {critical_count} critical issues found")

        # Sentiment findings
        if "sentiment" in sentiment:
            polarity = sentiment["sentiment"]["overall_sentiment"]
            key_findings.append(f"Sentiment: {polarity} tone detected")

        # Readability findings
        if "flesch_kincaid_grade" in readability:
            grade = readability["flesch_kincaid_grade"]
            key_findings.append(f"Readability: Grade {grade} ({readability.get('audience_fit', {}).get('accessibility', 'unknown')})")

        # SEO findings
        if "seo_score" in seo:
            score = seo["seo_score"]
            key_findings.append(f"SEO: Score {score}/100")

        # Prioritize recommendations
        recommendations = []

        # Critical grammar issues first
        if grammar.get("critical_issues"):
            recommendations.append({
                "priority": 1,
                "category": "Grammar",
                "action": f"Fix {len(grammar['critical_issues'])} critical grammar issues",
                "issues": grammar["critical_issues"][:3]  # Top 3
            })

        # Style suggestions
        if grammar.get("style_suggestions"):
            recommendations.append({
                "priority": 2,
                "category": "Style",
                "action": "Apply style improvements",
                "suggestions": grammar["style_suggestions"][:2]
            })

        # Readability improvements
        if readability.get("readability_issues"):
            recommendations.append({
                "priority": 3,
                "category": "Readability",
                "action": "Improve text readability",
                "issues": readability["readability_issues"][:2]
            })

        # SEO optimization
        if seo.get("suggestions"):
            recommendations.append({
                "priority": 4,
                "category": "SEO",
                "action": "Optimize for search engines",
                "suggestions": seo["suggestions"][:2]
            })

        return {
            "key_findings": key_findings,
            "recommendations": recommendations,
            "all_analyses": analyses
        }

    def generate_executive_summary(self, text: str, synthesis: Dict[str, Any]) -> str:
        """Generate a human-readable executive summary"""
        findings = synthesis["key_findings"]
        recommendations = synthesis["recommendations"]

        summary = f"""
═══════════════════════════════════════════════════════════════════
COMPREHENSIVE TEXT ANALYSIS REPORT
═══════════════════════════════════════════════════════════════════

TEXT ANALYSIS:
{chr(10).join(findings)}

PRIORITIZED RECOMMENDATIONS:
"""
        for i, rec in enumerate(recommendations, 1):
            summary += f"\n{i}. {rec['category']} - {rec['action']}\n"

        return summary

    def analyze(self, text: str) -> Dict[str, Any]:
        """Coordinate analysis across all child skills"""
        print("Analyzing text with all child skills...", file=sys.stderr)

        # Invoke all child skills
        analyses = {}
        for skill_name in self.child_skills:
            print(f"Invoking {skill_name}...", file=sys.stderr)
            analyses[skill_name] = self.invoke_child_skill(skill_name, text)

        # Synthesize results
        synthesis = self.synthesize_results(analyses)

        # Generate summary
        summary = self.generate_executive_summary(text, synthesis)

        return {
            "skill": "text-analyzer",
            "type": "coordinator",
            "text_length": len(text),
            "child_skills_invoked": self.child_skills,
            "executive_summary": summary,
            "key_findings": synthesis["key_findings"],
            "recommendations": synthesis["recommendations"],
            "detailed_analyses": analyses
        }


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    coordinator = TextAnalyzerCoordinator()
    result = coordinator.analyze(text)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
