"""
Action Node Builder

Creates Action Nodes.

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class ActionNodeBuilder(BaseNodeBuilder):

    def build(
        self,
        graph,
        fact,
    ):

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is None:
            return

        action = getattr(
            interpretation,
            "action",
            None,
        )

        if action is None:
            return

        if not action.found:
            return

        node = self.create_node(

            entity=action,

            entity_type="Action",

        )

        self.register_node(

            graph,
            node,

        )