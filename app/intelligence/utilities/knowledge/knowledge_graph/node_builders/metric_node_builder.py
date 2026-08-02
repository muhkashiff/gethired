"""
Metric Node Builder

Creates Metric Nodes.

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class MetricNodeBuilder(BaseNodeBuilder):

    def build(self, graph, fact):

        interpretation = getattr(fact, "interpretation", None)

        if interpretation is None:
            return

        metric = getattr(interpretation, "metric", None)

        if metric is None:
            return

        if not metric.found:
            return

        node = self.create_node(

            entity=metric,

            entity_type="Metric",

        )

        self.register_node(graph, node)