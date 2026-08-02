"""
Action → Metric Edge Builder

Creates

Implement --------affects--------> Production Yield

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class ActionMetricEdgeBuilder:

    def build(self, graph, fact):

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

        metric = getattr(
            interpretation,
            "metric",
            None,
        )

        if action is None or metric is None:
            return

        if not action.found:
            return

        if not metric.found:
            return

        edge = GraphEdge(

            edge_id=f"{action.entity_id}_{metric.entity_id}",

            relation="affects",

            confidence=min(
                action.confidence,
                metric.confidence,
            ),

            source_id=action.entity_id,

            source_type="Action",

            target_id=metric.entity_id,

            target_type="Metric",

            reasoning="Action affects KPI",

        )

        graph.add_edge(edge)