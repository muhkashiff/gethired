"""
Measurement Node Builder

Creates Measurement Nodes.

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.base_node_builder import (
    BaseNodeBuilder,
)


class MeasurementNodeBuilder(BaseNodeBuilder):

    def build(self, graph, fact):

        interpretation = getattr(fact, "interpretation", None)

        if interpretation is None:
            return

        measurement = getattr(
            interpretation,
            "measurement",
            None,
        )

        if measurement is None:
            return

        if not measurement.found:
            return

        node = self.create_node(

            entity=measurement,

            entity_type="Measurement",

        )

        self.register_node(graph, node)