"""
Domain → Entity Builder

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphEdge,
)


class DomainEntityEdgeBuilder:

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

        domain = getattr(
            interpretation,
            "domain",
            None,
        )

        if domain is None:
            return

        if not domain.found:
            return

        entities = [

            interpretation.action,

            interpretation.object,

            interpretation.metric,

            interpretation.standard,

            interpretation.measurement,

        ]

        for entity in entities:

            if entity is None:
                continue

            if not entity.found:
                continue

            edge = GraphEdge(

                edge_id=f"{domain.entity_id}_{entity.entity_id}",

                relation="contains",

                confidence=domain.confidence,

                source_id=domain.entity_id,

                source_type="Domain",

                target_id=entity.entity_id,

                target_type=entity.entity_type,

                reasoning="Domain contains entity",

            )

            graph.add_edge(edge)