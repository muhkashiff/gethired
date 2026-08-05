"""
Enterprise Base Edge Builder

All Edge Builders inherit from this class.

Responsibilities
----------------
• Build graph relationships
• Register graph edges
• Reuse BaseBuilder functionality

Enterprise V9
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


class BaseEdgeBuilder(BaseBuilder):
    """
    Base class for every Edge Builder.
    """

    BUILDER_TYPE = "edge"

    @abstractmethod
    def build(
        self,
        context: BuildContext,
        statement: BusinessStatement,
    ) -> None:
        """
        Build graph edges from one BusinessStatement.

        Parameters
        ----------
        context : BuildContext
            Shared graph context.

        statement : BusinessStatement
            Enterprise business statement.

        Returns
        -------
        None
        """
        raise NotImplementedError