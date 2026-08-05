"""
Enterprise Base Node Builder

Every Node Builder inherits from this class.

Responsibilities
----------------
• Build graph nodes
• Uses BaseBuilder infrastructure
• Node-specific abstraction only

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


class BaseNodeBuilder(BaseBuilder):
    """
    Base class for all Node Builders.

    All common functionality comes from BaseBuilder.

    Concrete builders only implement node creation logic.
    """

    ####################################################################
    # BUILDER METADATA
    ####################################################################

    BUILDER_TYPE = "node"

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
        Build graph nodes from a BusinessStatement.

        Parameters
        ----------
        context : BuildContext

        statement : BusinessStatement
        """
        raise NotImplementedError