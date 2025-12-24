#!/usr/bin/env python3
"""Readability Scorer Skill - Assesses text readability and audience appropriateness"""

import re
import sys
import json
from typing import Dict, Any

class ReadabilityScorer:
    def calculate_flesch_kincaid(self, text: str) -> float:
        """Calculate Flesch-Kincaid Grade Level"""
        # Count sentences (approximate)
        sentences = len(re.split(r'[.!?]+', text)) - 1
        sentences = max(sentences, 1)

        # Count words
        words = len(text.split())
        words = max(words, 1)

        # Count syllables (approximate)
        syllables = self.count_syllables(text)

        # Formula: 0.39(W/S) + 11.8(SY/W) - 15.59
        if sentences > 0 and words > 0:
            grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
            return max(0, round(grade, 1))
        return 0

    def count_syllables(self, text: str) -> int:
        """Approximate syllable count"""
        text = text.lower()
        syllable_count = 0

        vowels = 'aeiouy'
        previous_was_vowel = False

        for char in text:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent e
        if text.endswith('e'):
            syllable_count -= 1

        # Ensure at least 1 syllable
        return max(1, syllable_count)

    def analyze_sentence_structure(self, text: str) -> Dict[str, Any]:
        """Analyze sentence structure and complexity"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return {"avg_sentence_length": 0, "complexity": "unknown"}

        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = sum(sentence_lengths) / len(sentence_lengths)

        # Determine complexity
        if avg_length < 10:
            complexity = "simple"
        elif avg_length < 15:
            complexity = "moderate"
        elif avg_length < 20:
            complexity = "complex"
        else:
            complexity = "very complex"

        return {
            "avg_sentence_length": round(avg_length, 1),
            "sentence_count": len(sentences),
            "complexity": complexity,
            "longest_sentence": max(sentence_lengths),
            "shortest_sentence": min(sentence_lengths)
        }

    def analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """Analyze vocabulary complexity"""
        words = text.lower().split()
        unique_words = set(words)

        # Common/simple words
        simple_words = {
            'the', 'a', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been',
            'have', 'has', 'do', 'does', 'did', 'will', 'would', 'should', 'could',
            'can', 'may', 'might', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'this', 'that', 'these', 'those', 'what', 'which', 'who', 'when', 'where', 'why'
        }

        simple_count = len([w for w in unique_words if w in simple_words])
        complex_words = len(unique_words) - simple_count

        vocabulary_level = "simple" if complex_words < 5 else "moderate" if complex_words < 15 else "complex"

        return {
            "unique_words": len(unique_words),
            "total_words": len(words),
            "vocabulary_diversity": round(len(unique_words) / len(words), 2),
            "complex_words": complex_words,
            "vocabulary_level": vocabulary_level
        }

    def analyze_audience_fit(self, grade_level: float) -> Dict[str, Any]:
        """Determine appropriate audience based on grade level"""
        if grade_level < 6:
            audience = "Elementary school (grades 3-5)"
            accessibility = "very easy"
        elif grade_level < 8:
            audience = "Middle school (grades 6-8)"
            accessibility = "easy"
        elif grade_level < 10:
            audience = "High school (grades 9-10)"
            accessibility = "moderate"
        elif grade_level < 12:
            audience = "High school (grades 11-12)"
            accessibility = "challenging"
        else:
            audience = "College/Academic"
            accessibility = "very challenging"

        return {
            "recommended_audience": audience,
            "accessibility": accessibility,
            "grade_level": grade_level
        }

    def identify_readability_issues(self, text: str) -> list:
        """Identify specific readability problems"""
        issues = []

        # Check for passive voice overuse
        passive_count = len(re.findall(r'\b(is|are|was|were)\s+\w+ed\b', text))
        if passive_count > 3:
            issues.append(f"Excessive passive voice ({passive_count} instances) - reduces clarity")

        # Check for jargon/complex words
        complex_pattern = r'\b[a-z]{15,}\b'
        complex_words = re.findall(complex_pattern, text)
        if len(complex_words) > 2:
            issues.append(f"Several long/complex words ({len(complex_words)}) - may reduce readability")

        # Check for run-on sentences
        long_sentences = len(re.findall(r'[^.!?]{100,}[.!?]', text))
        if long_sentences > 2:
            issues.append(f"Some very long sentences - consider breaking them up")

        # Check for clarity
        if 'refuse to behave' in text.lower():
            issues.append("Vague phrases like 'refuse to behave' - be more specific")

        return issues if issues else ["Text is generally readable"]

    def analyze(self, text: str) -> Dict[str, Any]:
        """Run all readability analyses"""
        grade_level = self.calculate_flesch_kincaid(text)
        sentence_structure = self.analyze_sentence_structure(text)
        vocabulary = self.analyze_vocabulary(text)
        audience = self.analyze_audience_fit(grade_level)
        issues = self.identify_readability_issues(text)

        return {
            "skill": "readability-scorer",
            "flesch_kincaid_grade": grade_level,
            "sentence_structure": sentence_structure,
            "vocabulary": vocabulary,
            "audience_fit": audience,
            "readability_issues": issues,
            "overall_readability": "Good" if grade_level < 12 else "Challenging",
            "summary": f"Text is suitable for {audience['recommended_audience']} with {audience['accessibility']} readability (Grade {grade_level})"
        }


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    scorer = ReadabilityScorer()
    result = scorer.analyze(text)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
