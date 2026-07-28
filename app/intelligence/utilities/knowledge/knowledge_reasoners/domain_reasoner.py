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
        self.domains = self.repository.get_domains()

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
        # Metadata lookup
        # -------------------------------------------------

        domain_metadata = self.domains.get(canonical, {})

        return DomainKnowledge(

            found=True,

            entity_id=domain_id,

            domain=canonical,

            business_area=domain_metadata.get(
                "business_area",
                ""
            ),

            impact_weight=float(
                domain_metadata.get(
                    "impact_weight",
                    1.0,
                )
            ),

            source="ontology",

            metadata=domain_metadata,

            reasoning=f"{action_category} + {object_category}",

            confidence=0.95,

        )