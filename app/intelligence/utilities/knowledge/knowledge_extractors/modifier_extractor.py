"""
Modifier Extractor

Extracts linguistic modifiers from resume text.

Examples

Successfully
Strategically
Cross-functional
Globally
Consistently
Enterprise-wide

Returns

List[ModifierKnowledge]
"""

import json
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.modifier_models import (
    ModifierKnowledge,
)


class ModifierExtractor:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "data"
            / "modifier_dictionary.json"
        )

        with open(path, encoding="utf8") as f:
            self.dictionary = json.load(f)

    # ----------------------------------------------------------

    def extract(self, sentence):

        sentence_lower = sentence.lower()

        modifiers = []

        for keyword, data in self.dictionary.items():

            if keyword.lower() in sentence_lower:

                modifiers.append(

                    ModifierKnowledge(

                        found=True,

                        original=keyword,

                        canonical=data["canonical"],

                        category=data["category"],

                        strength=float(data["strength"]),

                        executive_weight=float(
                            data["executive_weight"]
                        ),

                        confidence=0.95

                    )

                )

        return modifiers