"""
Enterprise Action → Metric Edge Builder

Creates

Action --------affects--------> Metric

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class ActionMetricEdgeBuilder(BaseEdgeBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        ################################################################
        # Read Business Statement Collections
        ################################################################

        actions = getattr(
            statement,
            "actions",
            [],
        )

        metrics = getattr(
            statement,
            "metrics",
            [],
        )

        if not actions:
            return

        if not metrics:
            return

        ################################################################
        # Create Edges
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

            for metric in metrics:

                if metric is None:
                    continue

                if not getattr(
                    metric,
                    "found",
                    False,
                ):
                    continue

                edge = self.create_edge(

                    source=action,

                    target=metric,

                    relation="affects",

                    reasoning="Action affects KPI",

                    confidence=min(
                        action.confidence,
                        metric.confidence,
                    ),

                )

                self.register_edge(

                    context,

                    edge,

                )