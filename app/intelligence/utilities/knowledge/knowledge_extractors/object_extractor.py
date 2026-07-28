"""
Object Extractor

Extracts ontology-backed business objects.

Repository Driven Version
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.object_models import (
    ObjectKnowledge,
)


class ObjectExtractor:

    def __init__(self):

        self.repository = Repository()

        self.objects = self.repository.get_dictionary("objects")

        # longest phrase first
        self.sorted_objects = sorted(
            self.objects.keys(),
            key=len,
            reverse=True,
        )

    # ------------------------------------------------------------

    def extract(self, sentence):

        sentence_lower = sentence.lower()

        for phrase in self.sorted_objects:

            if phrase in sentence_lower:

                entity = self.repository.get_object(phrase)

                if entity is None:
                    continue

                return ObjectKnowledge(

                    found=True,

                    original=phrase,

                    canonical=entity.canonical,

                    category=entity.category,

                    confidence=0.95,

                    # ---------------------------------
                    # Ontology
                    # ---------------------------------

                    entity_id=entity.entity_id,

                    business_area=entity.business_area,

                    impact_weight=entity.impact_weight,
                    
                    source="ontology",

                    metadata=entity.metadata,

                )

        return ObjectKnowledge()