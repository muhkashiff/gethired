"""
Enterprise Base Semantic Builder

All Semantic Builders inherit from this class.

Responsibilities
----------------
• Build semantic relationships
• Build semantic graph enrichments
• Register semantic edges
• Reuse BaseBuilder functionality

Enterprise V10
"""

from abc import abstractmethod

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_builder import (
    BaseBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_graph.build_context import (
    BuildContext,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.business_statement_builder import (
    BusinessStatement,
)


class BaseSemanticBuilder(BaseBuilder):
    """
    Base class for every Semantic Builder.

    Semantic Builders execute AFTER:

        • Node Builders
        • Edge Builders

    They enrich the graph by discovering higher-level
    business relationships.
    """

    builder_type = "semantic"

    ####################################################################
    # ABSTRACT BUILD
    ####################################################################

    @abstractmethod
    def build(
        self,
        context: BuildContext,
        statement: BusinessStatement,
    ) -> None:
        """
        Enrich the graph using one Business Statement.

        Parameters
        ----------
        context : BuildContext
            Shared graph construction context.

        statement : BusinessStatement
            Enterprise business statement.

        Returns
        -------
        None
        """
        raise NotImplementedError

    ####################################################################
    # OPTIONAL HELPERS
    ####################################################################

    def entity_found(
        self,
        entity,
    ) -> bool:
        """
        Safe entity validation helper.
        """

        if entity is None:
            return False

        return getattr(
            entity,
            "found",
            False,
        )

    ####################################################################

    def confidence(
        self,
        *entities,
    ) -> float:
        """
        Returns minimum confidence among entities.
        """

        confidences = [

            getattr(
                entity,
                "confidence",
                1.0,
            )

            for entity in entities

            if entity is not None

        ]

        if not confidences:
            return 1.0

        return min(confidences)