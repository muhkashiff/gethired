"""
Action → Skill Edge Builder

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class ActionSkillEdgeBuilder:

    def build(self, graph, fact):

        interpretation = getattr(
            fact,
            "interpretation",
            None,
        )

        if interpretation is None:
            return

        action = interpretation.action

        if not action.found:
            return

        for entity in interpretation.entities:

            if entity.entity_type.lower() != "skill":
                continue

            edge = GraphEdge(

                edge_id=f"{action.entity_id}_{entity.entity_id}",

                relation="requires",

                confidence=min(
                    action.confidence,
                    entity.confidence,
                ),

                source_id=action.entity_id,

                source_type="Action",

                target_id=entity.entity_id,

                target_type="Skill",

                reasoning="Action requires skill",

            )

            graph.add_edge(edge)