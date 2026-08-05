"""
Enterprise Domain → Entity Edge Builder

Creates

Domain --------contains--------> Business Entity

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_edge_builder import (
    BaseEdgeBuilder,
)


class DomainEntityEdgeBuilder(BaseEdgeBuilder):

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

        domains = getattr(
            statement,
            "domains",
            [],
        )

        if not domains:
            return

        ################################################################
        # Every Business Entity belongs to a Domain
        ################################################################

        entities = []

        entities.extend(
            getattr(statement, "actions", [])
        )

        entities.extend(
            getattr(statement, "targets", [])
        )

        entities.extend(
            getattr(statement, "metrics", [])
        )

        entities.extend(
            getattr(statement, "measurements", [])
        )

        entities.extend(
            getattr(statement, "standards", [])
        )

        entities.extend(
            getattr(statement, "skills", [])
        )

        entities.extend(
            getattr(statement, "methodologies", [])
        )

        entities.extend(
            getattr(statement, "kpis", [])
        )

        ################################################################
        # Create Edges
        ################################################################

        for domain in domains:

            if domain is None:
                continue

            if not getattr(
                domain,
                "found",
                False,
            ):
                continue

            for entity in entities:

                if entity is None:
                    continue

                if not getattr(
                    entity,
                    "found",
                    False,
                ):
                    continue

                #
                # Avoid self-loop
                #
                if domain.entity_id == entity.entity_id:
                    continue

                edge = self.create_edge(

                    source=domain,

                    target=entity,

                    relation="contains",

                    reasoning="Domain contains business entity",

                    confidence=domain.confidence,

                )

                self.register_edge(

                    context,

                    edge,

                )