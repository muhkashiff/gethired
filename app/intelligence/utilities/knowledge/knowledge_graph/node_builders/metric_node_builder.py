"""
Enterprise Metric Node Builder

Creates Metric Nodes from Business Statements.

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_node_builder import (
    BaseNodeBuilder,
)


class MetricNodeBuilder(BaseNodeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Business Statement may contain multiple Metrics
        ################################################################

        metrics = getattr(
            statement,
            "metrics",
            [],
        )

        if not metrics:
            return

        ################################################################
        # Create Metric Nodes
        ################################################################

        for metric in metrics:

            if metric is None:
                continue

            if not getattr(
                metric,
                "found",
                False,
            ):
                continue

            node = self.create_node(

                entity=metric,

                entity_type="Metric",

            )

            self.register_node(

                context,

                node,

            )