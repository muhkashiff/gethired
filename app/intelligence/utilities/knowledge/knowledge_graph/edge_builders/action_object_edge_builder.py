"""
Action → Object Edge Builder

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class ActionObjectEdgeBuilder:

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

        action = getattr(
            interpretation,
            "action",
            None,
        )

        obj = getattr(
            interpretation,
            "object",
            None,
        )

        if action is None or obj is None:
            return

        if not action.found:
            return

        if not obj.found:
            return

        edge = GraphEdge(

            edge_id=f"{action.entity_id}_{obj.entity_id}",

            relation="acts_on",

            confidence=min(
                action.confidence,
                obj.confidence,
            ),

            source_id=action.entity_id,

            source_type="Action",

            target_id=obj.entity_id,

            target_type="Object",

            reasoning="Action acts on object",

        )

        graph.add_edge(edge)