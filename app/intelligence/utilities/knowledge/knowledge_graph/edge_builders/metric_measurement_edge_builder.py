"""
Enterprise Metric → Measurement Edge Builder

Creates

Metric --------measured_by--------> Measurement

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class MetricMeasurementEdgeBuilder(BaseEdgeBuilder):

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

        metrics = getattr(
            statement,
            "metrics",
            [],
        )

        measurements = getattr(
            statement,
            "measurements",
            [],
        )

        if not metrics:
            return

        if not measurements:
            return

        ################################################################
        # Create Edges
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

            for measurement in measurements:

                if measurement is None:
                    continue

                if not getattr(
                    measurement,
                    "found",
                    False,
                ):
                    continue

                edge = self.create_edge(

                    source=metric,

                    target=measurement,

                    relation="measured_by",

                    reasoning="Metric measured by numeric value",

                    confidence=min(
                        metric.confidence,
                        measurement.confidence,
                    ),

                )

                self.register_edge(

                    context,

                    edge,

                )