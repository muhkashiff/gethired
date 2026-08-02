"""
Domain Node Builder
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class DomainNodeBuilder(BaseNodeBuilder):

    def build(self, graph, fact):

        interpretation = getattr(fact, "interpretation", None)

        if interpretation is None:
            return

        domain = getattr(
            interpretation,
            "domain",
            None,
        )

        if domain is None:
            return

        if not domain.found:
            return

        node = self.create_node(

            entity=domain,

            entity_type="Domain",

        )

        self.register_node(graph, node)