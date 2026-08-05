"""
Enterprise Standard Node Builder

Creates Standard Nodes from Business Statements.

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class StandardNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Standards
        ################################################################

        standards = getattr(
            statement,
            "standards",
            [],
        )

        if not standards:
            return

        ################################################################
        # Create Standard Nodes
        ################################################################

        for standard in standards:

            if standard is None:
                continue

            if not getattr(
                standard,
                "found",
                False,
            ):
                continue

            node = self.create_node(

                entity=standard,

                entity_type="Standard",

            )

            self.register_node(

                context,

                node,

            )