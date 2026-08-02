"""
Action → Standard Edge Builder

Implement

↓

FSSC22000

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class ActionStandardEdgeBuilder:

    def build(self, graph, fact):

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is None:
            return

        action = interpretation.action

        standard = interpretation.standard

        if not action.found:
            return

        if not standard.found:
            return

        edge = GraphEdge(

            edge_id=f"{action.entity_id}_{standard.entity_id}",

            relation="complies_with",

            confidence=min(
                action.confidence,
                standard.confidence,
            ),

            source_id=action.entity_id,

            source_type="Action",

            target_id=standard.entity_id,

            target_type="Standard",

            reasoning="Action implements standard",

        )

        graph.add_edge(edge)