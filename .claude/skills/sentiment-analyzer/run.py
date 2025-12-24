#!/usr/bin/env python3
"""Sentiment Analyzer Skill - Analyzes emotional tone and sentiment of text"""

import re
import sys
import json
from typing import Dict, List, Any

class SentimentAnalyzer:
    def __init__(self):
        # Sentiment word lists
        self.positive_words = {
            'good': 1, 'great': 2, 'excellent': 2, 'amazing': 2, 'wonderful': 2,
            'happy': 2, 'pleased': 1, 'satisfied': 1, 'joy': 2, 'love': 2,
            'brilliant': 2, 'fantastic': 2, 'perfect': 2, 'best': 2
        }

        self.negative_words = {
            'bad': 1, 'terrible': 2, 'awful': 2, 'horrible': 2, 'hate': 2,
            'frustrating': 2, 'frustrated': 2, 'disappointed': 2, 'sad': 2,
            'ugly': 2, 'wrong': 1, 'refuse': 1, 'problem': 1, 'issue': 1,
            'mistake': 1, 'bug': 1, 'fail': 2, 'failed': 2, 'incorrect': 1
        }

        self.neutral_words = {
            'thing': 0, 'stuff': 0, 'happens': 0, 'often': 0
        }

        self.intensity_modifiers = {
            'very': 1.5, 'really': 1.5, 'extremely': 2, 'absolutely': 2,
            'so': 1.3, 'quite': 1.2, 'rather': 1.2, 'too': 1.3
        }

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze overall sentiment of the text"""
        words = text.lower().split()

        sentiment_score = 0
        positive_count = 0
        negative_count = 0
        emotional_words_found = []

        for i, word in enumerate(words):
            # Clean word
            clean_word = re.sub(r'[^\w]', '', word)

            # Check for intensity modifiers
            intensity = 1.0
            if i > 0:
                prev_word = re.sub(r'[^\w]', '', words[i-1])
                if prev_word in self.intensity_modifiers:
                    intensity = self.intensity_modifiers[prev_word]

            # Check sentiment
            if clean_word in self.positive_words:
                score = self.positive_words[clean_word] * intensity
                sentiment_score += score
                positive_count += 1
                emotional_words_found.append(f"+{clean_word}")

            elif clean_word in self.negative_words:
                score = -self.negative_words[clean_word] * intensity
                sentiment_score += score
                negative_count += 1
                emotional_words_found.append(f"-{clean_word}")

        # Determine sentiment polarity
        if sentiment_score > 5:
            polarity = "positive"
        elif sentiment_score < -5:
            polarity = "negative"
        else:
            polarity = "neutral"

        return {
            "overall_sentiment": polarity,
            "sentiment_score": round(sentiment_score, 2),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "emotional_words_found": emotional_words_found
        }

    def analyze_tone(self, text: str) -> Dict[str, Any]:
        """Analyze the tone/mood of the text"""
        tone = []
        text_lower = text.lower()

        # Detect various tones
        if any(word in text_lower for word in ['frustrat', 'annoying', 'irritating']):
            tone.append("frustrated")

        if any(word in text_lower for word in ['happy', 'pleased', 'good']):
            tone.append("pleased")

        if any(word in text_lower for word in ['tired', 'exhausted', 'weary']):
            tone.append("weary")

        if any(word in text_lower for word in ['mistake', 'rush', 'quickly']):
            tone.append("hurried/careless")

        if any(word in text_lower for word in ['reflect', 'lesson', 'learn', 'realize']):
            tone.append("reflective")

        if any(word in text_lower for word in ['should', 'could', 'should have']):
            tone.append("regretful")

        return {
            "detected_tones": tone if tone else ["neutral"],
            "tone_description": ", ".join(tone) if tone else "neutral and factual"
        }

    def analyze_emotional_impact(self, text: str) -> Dict[str, Any]:
        """Analyze psychological/emotional impact"""
        impact = []
        text_lower = text.lower()

        # Patterns that suggest struggle
        if any(phrase in text_lower for phrase in ['didn\'t go as planned', 'refuse to behave', 'took longer']):
            impact.append("struggle/adversity")

        # Patterns suggesting reflection
        if any(phrase in text_lower for phrase in ['should have', 'lesson', 'realize', 'mistake']):
            impact.append("self-awareness/regret")

        # Patterns suggesting resolution
        if any(phrase in text_lower for phrase in ['in the end', 'finally', 'fixing']):
            impact.append("resolution attempt")

        return {
            "emotional_themes": impact if impact else ["neutral"],
            "overall_mood": "reflective and slightly frustrated" if impact else "neutral"
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        """Run all sentiment analyses"""
        sentiment = self.analyze_sentiment(text)
        tone = self.analyze_tone(text)
        emotional = self.analyze_emotional_impact(text)

        return {
            "skill": "sentiment-analyzer",
            "sentiment": sentiment,
            "tone": tone,
            "emotional_impact": emotional,
            "summary": f"The text conveys a {sentiment['overall_sentiment']} sentiment with {tone['tone_description']} tone. Overall mood: {emotional['overall_mood']}"
        }


def main():
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = sys.stdin.read()

    analyzer = SentimentAnalyzer()
    result = analyzer.analyze(text)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
