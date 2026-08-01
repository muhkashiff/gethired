"""
Enterprise Action Extractor

Repository-driven Action Extractor.

Features
--------
✓ Repository Dependency Injection
✓ Multi-word Action Detection
✓ Duplicate Removal
✓ Enterprise Confidence
✓ Backward Compatible
"""

import re

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)


class ActionExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self, repository=None):

        self.repository = repository or Repository()

        self.max_ngram = 4

    ####################################################################
    # BACKWARD COMPATIBLE
    ####################################################################

    def extract(self, sentence):

        actions = self.extract_all(sentence)

        if actions:

            return actions[0]

        return ActionKnowledge()

    ####################################################################
    # EXTRACT ALL ACTIONS
    ####################################################################

    def extract_all(self, sentence):

        results = []

        seen = set()

        sentence_lower = sentence.lower()

        matches = list(
            re.finditer(r"\b[\w-]+\b", sentence_lower)
        )

        words = [m.group() for m in matches]

        ################################################################
        # NGRAM SEARCH
        ################################################################

        for n in range(self.max_ngram, 0, -1):

            for i in range(len(words) - n + 1):

                phrase = " ".join(
                    words[i:i+n]
                )

                entity = self.repository.get_action(
                    phrase
                )

                if entity is None:
                    continue

                if entity.entity_id in seen:
                    continue

                seen.add(entity.entity_id)

                metadata = entity.metadata

                confidence = self._confidence(
                    phrase,
                    entity
                )

                results.append(

                    ActionKnowledge(

                        found=True,

                        confidence=confidence,

                        original=phrase,

                        base=metadata.get(
                            "base",
                            entity.canonical
                        ),

                        gerund=metadata.get(
                            "gerund",
                            ""
                        ),

                        category=entity.category,

                        entity_id=entity.entity_id,

                        business_area=entity.business_area,

                        impact_weight=entity.impact_weight,

                        source="ontology",

                        metadata=metadata,

                        start_char=matches[i].start(),

                        end_char=matches[
                            i+n-1
                        ].end(),

                        token_index=i,

                        sentence_index=0,

                        clause_candidate=True,

                        entity_type="action",

                        matched_phrase=phrase,

                        matched_alias=(
                            phrase.lower()
                            != entity.canonical.lower()
                        )

                    )

                )

        ################################################################
        # SORT
        ################################################################

        results.sort(

            key=lambda x: (

                x.token_index,

                -x.confidence

            )

        )

        return results

    ####################################################################
    # CONFIDENCE
    ####################################################################

    def _confidence(self,
                    phrase,
                    entity):

        canonical = entity.canonical.lower()

        if phrase.lower() == canonical:

            return 0.99

        if phrase.lower() in [

            a.lower()

            for a in entity.aliases

        ]:

            return 0.95

        return 0.90