"""
Standard Node Builder
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class StandardNodeBuilder(BaseNodeBuilder):

    def build(self, graph, fact):

        interpretation = getattr(fact, "interpretation", None)

        if interpretation is None:
            return

        standard = getattr(
            interpretation,
            "standard",
            None,
        )

        if standard is None:
            return

        if not standard.found:
            return

        node = self.create_node(

            entity=standard,

            entity_type="Standard",

        )

        self.register_node(graph, node)