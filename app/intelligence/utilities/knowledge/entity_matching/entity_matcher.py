import sys
from pathlib import Path

# ------------------------------------------------------------
# Project Root
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

"""
Generic Entity Matcher

Searches ALL ontology dictionaries.
"""

import re

from app.intelligence.utilities.knowledge.entity_matching.entity_result import EntityResult

from app.intelligence.utilities.knowledge.entity_matching.entity_index import EntityIndex

from app.intelligence.utilities.knowledge.entity_matching.entity_priority import EntityPriority


class EntityMatcher:

    def __init__(self):

        self.index = EntityIndex()

        self.sorted_terms = sorted(
            self.index.keys(),
            key=len,
            reverse=True,
        )

    # --------------------------------------------------

    def match(self, sentence):

        sentence_lower = sentence.lower()

        matches = []
        seen_entities = set()

        for term in self.sorted_terms:

            pattern = r"\b" + re.escape(term) + r"\b"

            if not re.search(pattern, sentence_lower):
                continue

            info = self.index.get(term)

            if info is None:
                continue

            entity = info["entity"]
            entity_type = info["entity_type"]

            # Prevent duplicate matches from aliases
            unique_key = (entity.entity_id, entity_type)

            if unique_key in seen_entities:
                continue

            seen_entities.add(unique_key)

            matches.append(

                EntityResult(

                    entity_id=entity.entity_id,

                    entity_type=entity_type,

                    canonical=entity.canonical,

                    matched_text=term,

                    confidence=0.98,

                    category=entity.category,

                    business_area=entity.business_area,

                    source="ontology",

                    priority=EntityPriority.get(entity_type),

                    metadata=entity.metadata,

                )

            )

                

        matches.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        return matches