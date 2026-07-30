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

        # Rule mapping
        self.rules = self.repository.get_domain_reasoning()

        # Canonical domain metadata
        #self.domains = self.repository.get_domains()

    # ---------------------------------------------------------

    def reason(self, action, obj):

        if not action.found:

            return DomainKnowledge()

        action_category = action.category.lower()

        object_category = ""

        if obj.found:

            object_category = obj.category.lower()

        # -------------------------------------------------
        # Rule lookup
        # -------------------------------------------------

        if action_category not in self.rules:

            return DomainKnowledge()

        mapping = self.rules[action_category]

        if object_category not in mapping:

            return DomainKnowledge()

        rule = mapping[object_category]

        domain_id = rule.get("domain_id", "")

        canonical = rule.get("canonical", "")

        # -------------------------------------------------
        # Entity lookup
        # -------------------------------------------------

        domain_entity = self.repository.get_domain(canonical)

        if domain_entity is None:
            return DomainKnowledge(
                found=True,
                entity_id=domain_id,
                domain=canonical,
                reasoning=f"{action_category} + {object_category}",
                confidence=0.95,
            )

        return DomainKnowledge(

            found=True,

            entity_id=domain_entity.entity_id,

            domain=domain_entity.canonical,

            business_area=domain_entity.business_area,

            impact_weight=domain_entity.impact_weight,

            source=domain_entity.source,

            metadata=domain_entity.metadata,

            reasoning=f"{action_category} + {object_category}",

            confidence=0.95,

        )