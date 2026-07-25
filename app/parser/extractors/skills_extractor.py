"""
GetHired
Production Skills Extractor
"""

import re

from .base_extractor import BaseExtractor

from app.parser.parsed_models import Skill
from app.knowledge.skill_loader import SkillKnowledge


class SkillsExtractor(BaseExtractor):

    def __init__(self):

        self.knowledge = SkillKnowledge()

    # =====================================================
    # Main Extractor
    # =====================================================

    def extract(self, lines):

        skills = []

        seen = set()

        for line in self.clean(lines):

            # Split while preserving commas inside ()
            parts = self.smart_split(line)

            for part in parts:

                skill_text = part.strip()

                if not skill_text:
                    continue

                # ---------------------------------------
                # Find ALL matching skills
                # ---------------------------------------

                matches = self.knowledge.lookup_all(skill_text)

                # ---------------------------------------
                # Known Skills
                # ---------------------------------------

                if matches:

                    for knowledge in matches:

                        name = (
                            knowledge.get("canonical_name")
                            or skill_text
                        )

                        normalized = self.normalize_name(name)

                        if normalized in seen:
                            continue

                        seen.add(normalized)

                        skill = Skill(

                            name=name,

                            category=knowledge.get(
                                "category",
                                "Other"
                            ),

                            level=knowledge.get(
                                "level"
                            ) or self.detect_level(skill_text),

                            years=self.detect_years(skill_text),

                            confidence=knowledge.get(
                                "confidence",
                                0.95
                            ),

                            matched=False,

                            score=0.0,

                            raw_text=skill_text,

                            normalized_name=normalized

                        )

                        skills.append(skill)

                # ---------------------------------------
                # Unknown Skill
                # ---------------------------------------

                else:

                    normalized = self.normalize_name(skill_text)

                    if normalized in seen:
                        continue

                    seen.add(normalized)

                    skill = Skill(

                        name=skill_text,

                        category="Other",

                        level=self.detect_level(skill_text),

                        years=self.detect_years(skill_text),

                        confidence=0.50,

                        matched=False,

                        score=0.0,

                        raw_text=skill_text,

                        normalized_name=normalized

                    )

                    skills.append(skill)

        return skills

    # =====================================================
    # Smart Split
    # =====================================================

    def smart_split(self, line):

        results = []

        current = ""

        depth = 0

        for ch in line:

            if ch == "(":
                depth += 1

            elif ch == ")":
                depth -= 1

            if ch in [",", ";", "|"] and depth == 0:

                if current.strip():

                    results.append(current.strip())

                current = ""

            else:

                current += ch

        if current.strip():

            results.append(current.strip())

        return results

    # =====================================================
    # Detect Level
    # =====================================================

    def detect_level(self, text):

        lower = text.lower()

        if "expert" in lower:
            return "Expert"

        if "advanced" in lower:
            return "Advanced"

        if "intermediate" in lower:
            return "Intermediate"

        if "beginner" in lower:
            return "Beginner"

        return ""

    # =====================================================
    # Detect Years
    # =====================================================

    def detect_years(self, text):

        match = re.search(

            r"(\d+(?:\.\d+)?)\+?\s*years?",

            text,

            re.I

        )

        if match:

            return float(match.group(1))

        return None

    # =====================================================
    # Normalize
    # =====================================================

    def normalize_name(self, text):

        text = text.lower()

        text = re.sub(r"[^a-z0-9 ]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()