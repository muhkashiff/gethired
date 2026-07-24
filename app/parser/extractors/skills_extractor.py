"""
GetHired
Production Skills Extractor

Extracts skills from resume sections and converts them
into enterprise Skill objects.
"""

from .base_extractor import BaseExtractor

from app.parser.models import Skill

from app.knowledge.skill_categories import SKILL_CATEGORIES


class SkillsExtractor(BaseExtractor):
    """
    Converts the raw Skills section into Skill objects.
    """

    def extract(self, lines):

        skills = []

        seen = set()

        for line in lines:

            # Normalize separators
            line = (
                line.replace("•", ",")
                    .replace(";", ",")
                    .replace("|", ",")
                    .replace("/", ",")
            )

            for chunk in line.split(","):

                name = chunk.strip()

                if not name:
                    continue

                key = name.lower()

                if key in seen:
                    continue

                seen.add(key)

                category = SKILL_CATEGORIES.get(
                    key,
                    "Other"
                )

                skill = Skill(

                    # Required
                    name=name,

                    # Classification
                    category=category,

                    # ATS
                    importance=1,

                    # Experience
                    years=0.0,

                    # Beginner / Intermediate / Advanced / Expert
                    level="",

                    # Resume section
                    source="Skills",

                    # Parser confidence
                    confidence=1.0,

                    # ATS matching
                    matched=False,

                    score=0.0,

                    # Future enrichment
                    aliases=[],

                    found_in_jobs=[],

                    evidence=[],

                    normalized_name=None,
                )

                skills.append(skill)

        return skills