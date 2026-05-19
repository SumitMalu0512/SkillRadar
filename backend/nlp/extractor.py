"""
Skill Extraction Engine.

Given a job description (raw text), pull out the skills mentioned.
We use a hybrid approach:
  1. Whole word matching against our taxonomy (fast, high precision)
  2. Multi-word phrase matching for compound skills
  3. Normalization to canonical names
  4. Confidence scoring based on context

This is intentionally simpler than using a heavy ML model. Keyword based
extraction is fast, explainable, and works well when you have a good taxonomy.
Important - we explain this design choice in the project report.
"""
import re
from collections import Counter
from typing import List, Dict, Tuple
from .skill_taxonomy import SKILL_TAXONOMY, build_lookup_index, get_category


class SkillExtractor:
    def __init__(self):
        self.lookup = build_lookup_index()
        # sort by length descending - we want to match "machine learning" before "machine"
        self.sorted_terms = sorted(self.lookup.keys(), key=len, reverse=True)
        # precompile a regex of all terms for fast matching
        self._compile_pattern()

    def _compile_pattern(self):
        # escape special regex chars in each term
        escaped = [re.escape(t) for t in self.sorted_terms]
        # word boundaries so we don't match "java" inside "javascript"
        # we use lookarounds because some terms contain non-word chars like "c++" or "c#"
        pattern_str = r"(?<![a-zA-Z0-9])(" + "|".join(escaped) + r")(?![a-zA-Z0-9+#.])"
        self.pattern = re.compile(pattern_str, re.IGNORECASE)

    def extract(self, text: str, return_counts: bool = False):
        """
        Extract skills from a job description.

        Args:
            text: the raw job description text
            return_counts: if True, return [(skill, count)] tuples;
                           otherwise just a list of unique skill names

        Returns:
            List of canonical skill names (deduplicated) or list of (skill, count) tuples
        """
        if not text:
            return []

        # find all matches
        matches = self.pattern.findall(text)

        # normalize each match to its canonical name
        canonical = [self.lookup[m.lower()] for m in matches]

        if return_counts:
            counter = Counter(canonical)
            return counter.most_common()

        # dedupe but preserve order of first appearance
        seen = set()
        result = []
        for skill in canonical:
            if skill not in seen:
                seen.add(skill)
                result.append(skill)
        return result

    def extract_with_details(self, text: str) -> List[Dict]:
        """
        Returns rich info for each extracted skill - useful for the API.
        """
        if not text:
            return []

        skill_counts = self.extract(text, return_counts=True)
        results = []
        for skill, count in skill_counts:
            results.append({
                "skill": skill,
                "category": get_category(skill),
                "mention_count": count,
                "confidence": self._calculate_confidence(count, len(text)),
            })
        return results

    def _calculate_confidence(self, mentions: int, text_length: int) -> float:
        """
        Simple confidence score. A skill mentioned multiple times in a JD
        is more likely a real requirement than one mentioned once.
        """
        if mentions >= 3:
            return 1.0
        elif mentions == 2:
            return 0.85
        else:
            # one mention - lower confidence
            return 0.7

    def batch_extract(self, texts: List[str]) -> List[List[str]]:
        """Extract skills from many job descriptions at once."""
        return [self.extract(t) for t in texts]


# convenience singleton for easy import
_default_extractor = None


def get_extractor() -> SkillExtractor:
    """Get the shared SkillExtractor instance (lazy-loaded)."""
    global _default_extractor
    if _default_extractor is None:
        _default_extractor = SkillExtractor()
    return _default_extractor
