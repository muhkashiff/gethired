"""
Domain Reasoner

Determines the business domain of a clause by combining
Action + Object.

Reasoning priority

1. Food Safety
2. Quality
3. Manufacturing
4. Operations
5. Supply Chain
6. Leadership (fallback)

Specific business objects always override generic verbs.
"""

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)


class DomainReasoner:

    def __init__(self):
        pass

    # ----------------------------------------------------------

    def reason(
        self,
        action,
        obj,
    ):

        if not action.found:
            return DomainKnowledge()

        action_base = action.base.lower()

        object_category = ""

        if obj.found:
            object_category = obj.category.lower()

        # ======================================================
        # OBJECT-BASED REASONING (Highest Priority)
        # ======================================================

        # -------------------------
        # Food Safety
        # -------------------------

        if object_category == "food_safety":

            return DomainKnowledge(

                found=True,

                domain="food_safety",

                reasoning="food safety object",

                confidence=0.95,

            )

        # -------------------------
        # Quality
        # -------------------------

        if object_category == "quality":

            return DomainKnowledge(

                found=True,

                domain="quality",

                reasoning="quality object",

                confidence=0.95,

            )

        # -------------------------
        # Manufacturing
        # -------------------------

        if object_category == "manufacturing":

            return DomainKnowledge(

                found=True,

                domain="manufacturing",

                reasoning="manufacturing object",

                confidence=0.95,

            )

        # -------------------------
        # Operations
        # -------------------------

        if object_category == "operations":

            return DomainKnowledge(

                found=True,

                domain="operational_excellence",

                reasoning="operations object",

                confidence=0.95,

            )

        # -------------------------
        # Supply Chain
        # -------------------------

        if object_category == "supply_chain":

            return DomainKnowledge(

                found=True,

                domain="supply_chain",

                reasoning="supply chain object",

                confidence=0.95,

            )

        # -------------------------
        # Finance
        # -------------------------

        if object_category == "finance":

            return DomainKnowledge(

                found=True,

                domain="finance",

                reasoning="finance object",

                confidence=0.95,

            )

        # -------------------------
        # Compliance
        # -------------------------

        if object_category == "compliance":

            return DomainKnowledge(

                found=True,

                domain="compliance",

                reasoning="compliance object",

                confidence=0.95,

            )

        # ======================================================
        # ACTION-BASED FALLBACK
        # ======================================================

        if action_base in {

            "lead",
            "manage",
            "coach",
            "train",
            "mentor",
            "supervise",
            "direct",

        }:

            return DomainKnowledge(

                found=True,

                domain="leadership",

                reasoning="leadership action",

                confidence=0.95,

            )

        # -------------------------
        # Continuous Improvement
        # -------------------------

        if action_base in {

            "improve",
            "optimize",
            "enhance",
            "streamline",

        }:

            return DomainKnowledge(

                found=True,

                domain="continuous_improvement",

                reasoning="continuous improvement action",

                confidence=0.95,

            )

        # -------------------------
        # Implementation
        # -------------------------

        if action_base in {

            "implement",
            "develop",
            "create",
            "design",

        }:

            return DomainKnowledge(

                found=True,

                domain="project_implementation",

                reasoning="implementation action",

                confidence=0.90,

            )

        # ======================================================
        # Unknown
        # ======================================================

        return DomainKnowledge()