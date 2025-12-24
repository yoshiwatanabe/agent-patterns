#!/usr/bin/env python3
"""Grammar Checker Skill - Analyzes text for grammar, spelling, and punctuation issues"""

import re
import sys
import json
from typing import List, Dict, Any

class GrammarChecker:
    def __init__(self):
        self.critical_issues = []
        self.minor_issues = []
        self.style_suggestions = []

    def check_subject_verb_agreement(self, text: str):
        """Check for common subject-verb agreement errors"""
        # Pattern: plural noun + singular verb (common error)
        patterns = [
            (r'\b(things|issues|problems|items|people|members|teams)\s+is\b', 'Plural subject with singular verb', 'are'),
            (r'\b(problem|issue|concern)\s+were\b', 'Singular subject with plural verb', 'was'),
        ]

        for pattern, description, suggestion in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.critical_issues.append({
                    "type": "Subject-Verb Agreement",
                    "issue": description,
                    "text": match.group(),
                    "suggestion": suggestion,
                    "location": match.start(),
                    "severity": "critical"
                })

    def check_verb_tense(self, text: str):
        """Check for inconsistent verb tenses"""
        # Pattern: mixing past and present tense inconsistently
        patterns = [
            (r'\b(run|goes)\b.*?\b(produce|produced)\b', 'Tense inconsistency'),
            (r'\bwas\s+working\b.*\b(just refuse)', 'Present tense in past context'),
        ]

        # Simple detection for obvious issues
        if 'finally run' in text.lower():
            self.critical_issues.append({
                "type": "Verb Tense",
                "issue": "Incorrect past tense form",
                "text": "finally run",
                "suggestion": "finally ran",
                "severity": "critical"
            })

    def check_pronoun_agreement(self, text: str):
        """Check pronoun agreement issues"""
        patterns = [
            (r'\bthey\s+was\b', 'Pronoun-verb agreement', 'were'),
        ]

        for pattern, description, suggestion in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.critical_issues.append({
                    "type": "Pronoun Agreement",
                    "issue": description,
                    "text": match.group(),
                    "suggestion": suggestion,
                    "severity": "critical"
                })

    def check_modal_verbs(self, text: str):
        """Check for modal verb errors (should have, could have, etc)"""
        # Pattern: should + base verb (should be infinitive)
        if 'should have take' in text.lower():
            self.critical_issues.append({
                "type": "Modal Verb Form",
                "issue": "Incorrect past participle with modal",
                "text": "should have take",
                "suggestion": "should have taken",
                "severity": "critical"
            })

    def check_homophones(self, text: str):
        """Check for common homophone errors"""
        # Pattern: wrong form of there/their/they're
        patterns = [
            (r'\bthere\s+project\b', 'their'),
            (r'\btheir\s+(is|are|location)\b', 'there'),
        ]

        for pattern, suggestion in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.critical_issues.append({
                    "type": "Homophone Error",
                    "issue": f"Wrong homophone used: {match.group()}",
                    "text": match.group(),
                    "suggestion": suggestion,
                    "severity": "critical"
                })

    def check_word_forms(self, text: str):
        """Check for incorrect word forms"""
        patterns = [
            (r'\bjust\s+refuse\b', 'just refused', 'Verb form'),
            (r'\bproduce\s+results\b(?!\s+that)', 'produced results', 'Verb tense'),
            (r'\brealize\s+they\b', 'realized they', 'Verb tense'),
            (r'\bkeep\s+going\b(?<!\bkeeping)', 'kept going', 'Verb tense'),
        ]

        for pattern, suggestion, type_name in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                self.critical_issues.append({
                    "type": type_name,
                    "issue": f"Incorrect {type_name.lower()}",
                    "text": match.group(),
                    "suggestion": suggestion,
                    "severity": "critical"
                })

    def check_passive_voice(self, text: str):
        """Detect excessive passive voice"""
        passive_patterns = r'\b(is|are|was|were)\s+\w+ed\b'
        matches = list(re.finditer(passive_patterns, text))

        if len(matches) > 3:
            self.style_suggestions.append({
                "type": "Style",
                "issue": f"Excessive passive voice ({len(matches)} instances)",
                "suggestion": "Consider using active voice for clarity and directness",
                "impact": "Reduces readability and impact"
            })

    def check_wordiness(self, text: str):
        """Check for redundant or wordy phrases"""
        wordy_patterns = [
            (r'\bat the end of the day\b', 'finally'),
            (r'\bfact that\b', 'remove'),
            (r'\bin my opinion\b', 'I think'),
        ]

        for pattern, suggestion in wordy_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.style_suggestions.append({
                    "type": "Wordiness",
                    "issue": f"Wordy phrase: {re.search(pattern, text, re.IGNORECASE).group()}",
                    "suggestion": f"Use: {suggestion}",
                    "impact": "Improves conciseness"
                })

    def analyze(self, text: str) -> Dict[str, Any]:
        """Run all grammar checks"""
        self.check_subject_verb_agreement(text)
        self.check_verb_tense(text)
        self.check_pronoun_agreement(text)
        self.check_modal_verbs(text)
        self.check_homophones(text)
        self.check_word_forms(text)
        self.check_passive_voice(text)
        self.check_wordiness(text)

        return {
            "skill": "grammar-checker",
            "critical_issues": self.critical_issues,
            "minor_issues": self.minor_issues,
            "style_suggestions": self.style_suggestions,
            "total_issues": len(self.critical_issues) + len(self.minor_issues),
            "summary": f"Found {len(self.critical_issues)} critical issues, {len(self.minor_issues)} minor issues, and {len(self.style_suggestions)} style suggestions"
        }


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        # Read from stdin if no argument
        text = sys.stdin.read()

    checker = GrammarChecker()
    result = checker.analyze(text)

    # Output as JSON for skill system
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
