"""
Action Extractor

Repository-driven Action Extractor.

Identifies one or more actions from a sentence using the
central ontology repository.

No JSON files are opened here.

Repository is the single source of truth.
"""

import re

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)


class ActionExtractor:

    def __init__(self):

        self.repository = Repository()

    # ----------------------------------------------------------
    # Backward compatible API
    # ----------------------------------------------------------

    def extract(self, sentence: str) -> ActionKnowledge:
        """
        Returns the first detected action.

        Existing parser code can continue calling extract()
        without modification.
        """

        actions = self.extract_all(sentence)

        if actions:
            return actions[0]

        return ActionKnowledge()

    # ----------------------------------------------------------
    # Extract every action
    # ----------------------------------------------------------

    def extract_all(self, sentence: str):

        results = []

        sentence_lower = sentence.lower()

        token_index = 0

        pattern = re.compile(r"\b[\w-]+\b")

        for match in pattern.finditer(sentence_lower):

            word = match.group()

            # --------------------------------------------
            # Repository lookup
            # --------------------------------------------

            entity = self.repository.get_action(word)

            if entity is None:

                token_index += 1
                continue

            metadata = entity.metadata

            base = metadata.get("base", word)

            gerund = metadata.get(
                "gerund",
                base + "ing"
            )

            # --------------------------------------------
            # Build Knowledge Model
            # --------------------------------------------

            results.append(

                ActionKnowledge(

                    found=True,

                    confidence=0.95,

                    # -----------------------
                    # Linguistics
                    # -----------------------

                    original=word,

                    base=base,

                    gerund=gerund,

                    category=entity.category,

                    # -----------------------
                    # Ontology
                    # -----------------------

                    entity_id=entity.entity_id,

                    business_area=entity.business_area,

                    impact_weight=entity.impact_weight,

                    source="ontology",

                    metadata=metadata,

                    # -----------------------
                    # Position
                    # -----------------------

                    start_char=match.start(),

                    end_char=match.end(),

                    token_index=token_index,

                    sentence_index=0,

                    clause_candidate=True,

                )

            )

            token_index += 1

        return results