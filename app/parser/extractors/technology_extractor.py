"""
GetHired
Production Technology Extractor

Extracts technologies, software, programming languages,
ERP systems, cloud platforms, databases, BI tools,
frameworks and QA software from resume text.
"""

import re

from .base_extractor import BaseExtractor

from app.parser.models import Technology
from app.knowledge.technology_loader import TechnologyKnowledge


class TechnologyExtractor(BaseExtractor):

    def __init__(self):

        self.knowledge = TechnologyKnowledge()

    # ==========================================================
    # Main Extractor
    # ==========================================================

    def extract(self, lines):

        technologies = []

        seen = set()

        for line in self.clean(lines):

            if not line.strip():
                continue

            matches = self.knowledge.lookup_all(line)

            for record in matches:

                name = record.get(
                    "canonical_name",
                    ""
                )

                normalized = self.normalize_name(name)

                if normalized in seen:
                    continue

                seen.add(normalized)

                technology = Technology(

                    name=name,

                    category=record.get(
                        "category",
                        "Other"
                    ),

                    vendor=record.get(
                        "vendor",
                        ""
                    ),

                    confidence=0.95,

                    matched=False,

                    score=0.0,

                    raw_text=line,

                    normalized_name=normalized

                )

                technologies.append(technology)

        return technologies

    # ==========================================================
    # Normalize Technology Name
    # ==========================================================

    def normalize_name(self, text):

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9#+.]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()