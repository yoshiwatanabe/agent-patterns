#!/usr/bin/env python3
"""SEO Optimizer Skill - Analyzes and optimizes text for search engines"""

import re
import sys
import json
from typing import Dict, List, Any
from collections import Counter

class SEOOptimizer:
    def __init__(self):
        self.min_word_count = 300
        self.recommended_keyword_density = 2  # percent

    def extract_keywords(self, text: str) -> Dict[str, Any]:
        """Extract and analyze keywords"""
        words = text.lower().split()

        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'can', 'that', 'this', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }

        # Clean and filter words
        clean_words = []
        for word in words:
            clean = re.sub(r'[^\w]', '', word.lower())
            if clean and len(clean) > 3 and clean not in stop_words:
                clean_words.append(clean)

        # Get keyword frequency
        keyword_freq = Counter(clean_words)
        top_keywords = keyword_freq.most_common(10)

        return {
            "top_keywords": [{"keyword": k, "frequency": f} for k, f in top_keywords],
            "total_unique_keywords": len(keyword_freq),
            "keywords": list(keyword_freq.keys())[:20]
        }

    def analyze_keyword_density(self, text: str, keyword: str) -> float:
        """Calculate keyword density percentage"""
        words = text.lower().split()
        clean_words = [re.sub(r'[^\w]', '', w) for w in words]

        total_words = len(clean_words)
        keyword_count = clean_words.count(keyword.lower())

        if total_words == 0:
            return 0

        return round((keyword_count / total_words) * 100, 2)

    def check_content_length(self, text: str) -> Dict[str, Any]:
        """Check if content is long enough for SEO"""
        word_count = len(text.split())

        if word_count < self.min_word_count:
            status = "too short"
            recommendation = f"Expand content to at least {self.min_word_count} words"
        else:
            status = "good"
            recommendation = "Content length is appropriate for SEO"

        return {
            "word_count": word_count,
            "min_recommended": self.min_word_count,
            "status": status,
            "recommendation": recommendation
        }

    def identify_seo_issues(self, text: str) -> List[str]:
        """Identify SEO-related issues"""
        issues = []
        text_lower = text.lower()

        # Check for headings (basic markdown)
        if '#' not in text:
            issues.append("No headings detected - use headings to structure content")

        # Check for links
        if 'http' not in text and '[' not in text:
            issues.append("No links detected - include relevant internal/external links")

        # Check for meta description length (if we can infer one from first sentence)
        first_sentence = re.split(r'[.!?]', text)[0]
        if len(first_sentence) > 160:
            issues.append("Opening text is too long - first 160 chars should be compelling")

        # Check keyword repetition
        keywords = re.findall(r'\b\w{4,}\b', text_lower)
        if keywords:
            keyword_freq = Counter(keywords)
            most_common = keyword_freq.most_common(1)
            if most_common[0][1] < 2:
                issues.append("Consider using primary keywords more frequently (2-3% density)")

        # Check for meta elements
        if '<meta' not in text and 'description' not in text_lower:
            issues.append("No meta description found - add one for better SERP appearance")

        return issues if issues else ["No major SEO issues detected"]

    def generate_seo_suggestions(self, text: str, keywords: Dict[str, Any]) -> List[str]:
        """Generate actionable SEO recommendations"""
        suggestions = []

        if keywords['total_unique_keywords'] < 5:
            suggestions.append("Use more diverse keywords (target 5+ unique keywords)")

        # Suggest title optimization
        first_words = ' '.join(text.split()[:10])
        if len(first_words) < 30:
            suggestions.append("Consider a more descriptive title (30-60 characters)")

        # Internal linking suggestion
        if 'project' in text.lower():
            suggestions.append("Add internal links to related articles about project management")

        # Content structure suggestion
        word_count = len(text.split())
        if word_count > 500:
            suggestions.append("Add subheadings to break up long content (every 300 words)")

        return suggestions if suggestions else ["Content is well-optimized for SEO"]

    def analyze(self, text: str) -> Dict[str, Any]:
        """Run all SEO analyses"""
        keywords = self.extract_keywords(text)
        content_length = self.check_content_length(text)
        issues = self.identify_seo_issues(text)
        suggestions = self.generate_seo_suggestions(text, keywords)

        # Primary keyword analysis (first top keyword)
        primary_keyword = keywords['top_keywords'][0]['keyword'] if keywords['top_keywords'] else "none"
        keyword_density = self.analyze_keyword_density(text, primary_keyword)

        return {
            "skill": "seo-optimizer",
            "content_length": content_length,
            "keywords": keywords,
            "primary_keyword": primary_keyword,
            "primary_keyword_density": f"{keyword_density}%",
            "issues": issues,
            "suggestions": suggestions,
            "seo_score": self.calculate_seo_score(content_length, keyword_density, len(issues)),
            "summary": f"SEO score: {self.calculate_seo_score(content_length, keyword_density, len(issues))}/100. Focus on: {', '.join(suggestions[:2])}"
        }

    def calculate_seo_score(self, content_length: Dict, keyword_density: float, issue_count: int) -> int:
        """Calculate overall SEO score"""
        score = 50  # Base score

        # Content length bonus
        if content_length['status'] == 'good':
            score += 25
        else:
            score += 10

        # Keyword density bonus
        if 1 <= keyword_density <= 3:
            score += 15
        elif keyword_density > 0:
            score += 5

        # Issue penalty
        score -= (issue_count * 5)

        return max(0, min(100, score))


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    optimizer = SEOOptimizer()
    result = optimizer.analyze(text)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
