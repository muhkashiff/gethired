
"""
Enterprise Action Node Builder

Creates Action Nodes from Business Statements.

Architecture
------------
BusinessStatement
        ↓
ActionNodeBuilder
        ↓
KnowledgeGraph

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class ActionNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Actions
        ################################################################

        actions = getattr(
            statement,
            "actions",
            [],
        )

        if not actions:
            return

        ################################################################
        # Create Action Nodes
        ################################################################

        for action in actions:

            if action is None:
                continue

            if not getattr(
                action,
                "found",
                False,
            ):
                continue

            ################################################################
            # Create Node
            ################################################################

            node = self.create_node(
                entity=action,
                entity_type="Action",
            )

            ################################################################
            # Register Node
            ################################################################

            self.register_node(
                context,
                node,
            )

