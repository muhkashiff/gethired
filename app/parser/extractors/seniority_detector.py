"""
GetHired
Seniority Detector
"""

import re

from app.parser.models.seniority import Seniority
from app.knowledge.seniority_loader import SeniorityKnowledge


class SeniorityDetector:

    def __init__(self):

        self.knowledge = SeniorityKnowledge()

    def detect(

        self,

        title,

        responsibilities=None,

        achievements=None

    ):

        responsibilities = responsibilities or []

        achievements = achievements or []

        text = " ".join(

            [title]

            + responsibilities

            + achievements

        )

        knowledge = self.knowledge.lookup(text)

        if knowledge:

            return Seniority(

                name=knowledge["name"],

                level=knowledge["level"],

                confidence=0.95,

                matched=True,

                evidence=[title],

                normalized_name=knowledge["name"].lower()

            )

        return Seniority(

            name="Professional",

            level=3,

            confidence=0.50,

            matched=False,

            evidence=[],

            normalized_name="professional"

        )