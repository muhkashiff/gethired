"""
Ontology Driven Domain Reasoner

Determines business domain from

Action Category
+
Object Category

using ontology rules.

No hardcoded business logic.
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)


class DomainReasoner:

    def __init__(self):

        self.repository = Repository()

        self.rules = self.repository.get_dictionary("domains")

    # ---------------------------------------------------------

    def reason(self, action, obj):

        if not action.found:

            return DomainKnowledge()

        action_category = action.category.lower()

        object_category = ""

        if obj.found:

            object_category = obj.category.lower()

        # -------------------------------------------------
        # Ontology lookup
        # -------------------------------------------------

        if action_category in self.rules:

            mapping = self.rules[action_category]

            if object_category in mapping:

                info = mapping[object_category]

                return DomainKnowledge(

                    found=True,

                    entity_id=info.get("domain_id", ""),

                    domain=info.get("canonical", ""),

                    business_area=info.get("business_area", ""),

                    reasoning=f"{action_category} + {object_category}",

                    confidence=0.95,

                    metadata=info,

                )

        # -------------------------------------------------
        # fallback
        # -------------------------------------------------

        return DomainKnowledge()