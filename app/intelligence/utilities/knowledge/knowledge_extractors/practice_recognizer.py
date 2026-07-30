"""
Practice Recognizer

Recognizes Continuous Improvement Practices
from ontology.

Examples

Lean Manufacturing
Six Sigma
TPM
Kaizen
SMED
DMAIC
5S
Kanban
JIT
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository
from app.intelligence.utilities.knowledge.knowledge_extractor_models.practice_models import (
    PracticeKnowledge,
)


class PracticeRecognizer:

    def __init__(self):

        self.repository = Repository()

        self.practices = self.repository.get_dictionary("methodologies")

        self.sorted_practices = sorted(
            self.practices.keys(),
            key=len,
            reverse=True,
        )

    # ----------------------------------------------------

    def recognize(self, sentence):

        sentence = sentence.lower()

        for phrase in self.sorted_practices:

            if phrase.lower() in sentence:

                entity = self.repository.get_methodology(phrase)

                if entity is None:
                    continue

                return PracticeKnowledge(

                    found=True,

                    entity_id=entity.entity_id,

                    canonical=entity.canonical,

                    category=entity.category,

                    business_area=entity.business_area,

                    confidence=0.98,

                    impact_weight=entity.impact_weight,

                    source=entity.source,

                    metadata=entity.metadata,

                )

        return PracticeKnowledge()