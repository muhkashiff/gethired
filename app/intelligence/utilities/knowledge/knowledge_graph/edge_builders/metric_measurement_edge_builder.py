"""
Metric → Measurement Edge Builder

Production Yield

        │

 measured_by

        ▼

99%

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class MetricMeasurementEdgeBuilder:

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

        metric = getattr(
            interpretation,
            "metric",
            None,
        )

        measurement = getattr(
            interpretation,
            "measurement",
            None,
        )

        if metric is None or measurement is None:
            return

        if not metric.found:
            return

        if not measurement.found:
            return

        edge = GraphEdge(

            edge_id=f"{metric.entity_id}_{measurement.entity_id}",

            relation="measured_by",

            confidence=min(
                metric.confidence,
                measurement.confidence,
            ),

            source_id=metric.entity_id,

            source_type="Metric",

            target_id=measurement.entity_id,

            target_type="Measurement",

            reasoning="Metric measured by numeric value",

        )

        graph.add_edge(edge)