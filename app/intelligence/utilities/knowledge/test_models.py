"""
Enterprise Skills Extractor Integration Test
Enterprise V5

Uses the real KnowledgeV5Pipeline and skills repository.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ============================================================
# IMPORTS
# ============================================================

from app.intelligence.utilities.knowledge.knowledge_extractors.skills_extractor import (
    SkillsExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.skill_models import (
    SkillKnowledge,
)


# ============================================================
# TEST
# ============================================================

class TestSkillsExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        pipeline = KnowledgeV5Pipeline()

        cls.extractor = SkillsExtractor(
            pipeline=pipeline,
        )

    # ========================================================
    # SINGLE SENTENCE CHECK
    # ========================================================

    def _check_skill(
        self,
        sentence: str,
        expected: str,
    ) -> None:

        request = ExtractionRequest(
            sentence=sentence,
        )

        result = self.extractor.extract(
            request
        )

        detected = [
            skill.canonical
            for skill in result
        ]

        print()
        print("=" * 70)
        print("Sentence:")
        print(sentence)

        print()
        print("Expected:")
        print(expected)

        print()
        print("Detected:")
        print(detected)

        self.assertTrue(
            result.found,
            f"No skill detected.\nSentence: {sentence}",
        )

        self.assertTrue(
            any(
                expected.casefold()
                in skill.casefold()
                for skill in detected
            ),
            (
                f"Expected skill '{expected}' "
                f"was not detected.\n"
                f"Sentence: {sentence}\n"
                f"Detected: {detected}"
            ),
        )

        # Verify that the extractor actually produced
        # SkillKnowledge objects.

        for skill in result:

            self.assertIsInstance(
                skill,
                SkillKnowledge,
            )

    # ========================================================
    # SKILL TESTS
    # ========================================================

    def test_food_safety_management(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Food Safety Management."
            ),
            expected="Food Safety Management",
        )

    def test_root_cause_analysis(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Root Cause Analysis."
            ),
            expected="Root Cause Analysis",
        )

    def test_quality_management(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Quality Management."
            ),
            expected="Quality Assurance",
        )

    def test_problem_solving(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Problem Solving."
            ),
            expected="Problem Solving",
        )

    def test_data_analysis(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Data Analysis."
            ),
            expected="Data Analysis",
        )

    def test_statistical_analysis(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Statistical Analysis."
            ),
            expected="Statistical Analysis",
        )

    def test_project_management(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Project Management."
            ),
            expected="Project Management",
        )

    def test_leadership(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Leadership."
            ),
            expected="Leadership",
        )

    def test_team_building(self):

        self._check_skill(
            sentence=(
                "Demonstrated strong experience in "
                "Team Building."
            ),
            expected="Team Building",
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    unittest.main(
        verbosity=2
    )