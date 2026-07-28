"""
Modifier Extractor

Extracts linguistic modifiers from resume text.

Repository Driven Version
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.modifier_models import (
    ModifierKnowledge,
)


class ModifierExtractor:

    def __init__(self):

        self.repository = Repository()

        self.dictionary = self.repository.get_modifier_dictionary()

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

                        canonical=data.get("canonical", keyword),

                        category=data.get("category", ""),

                        strength=float(
                            data.get("strength", 1.0)
                        ),

                        executive_weight=float(
                            data.get("executive_weight", 1.0)
                        ),

                        confidence=0.95,

                        # -------------------------
                        # Ontology
                        # -------------------------

                        entity_id=data.get("entity_id", ""),

                        business_area=data.get("business_area", ""),

                        impact_weight=float(
                            data.get("impact_weight", 1.0)
                        ),

                        source="ontology",

                        metadata=data,

                    )

                )

        return modifiers