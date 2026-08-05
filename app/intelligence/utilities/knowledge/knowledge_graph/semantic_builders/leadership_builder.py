"""
Enterprise Leadership Builder

Builds enterprise leadership relationships.

Purpose
-------
Creates semantic leadership relationships from
Business Statements.

Runs AFTER

    RelationshipBuilder
    MeasurementBuilder
    AchievementBuilder
    DependencyBuilder

Runs BEFORE

    LeadershipReasoner

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_semantic_builder import (
    BaseSemanticBuilder,
)


class LeadershipBuilder(BaseSemanticBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        self._build_leadership_relationships(
            context,
            statement,
        )

        self._build_ownership_relationships(
            context,
            statement,
        )

        self._build_cross_functional_relationships(
            context,
            statement,
        )

    ####################################################################
    # ACTION → LEADS → DOMAIN
    ####################################################################

    def _build_leadership_relationships(
        self,
        context,
        statement,
    ) -> None:

        actions = statement.actions
        domains = statement.domains

        if not actions:
            return

        if not domains:
            return

        for action in actions:

            metadata = getattr(
                action,
                "metadata",
                {},
            )

            if not metadata.get(
                "leadership",
                False,
            ):
                continue

            business_area = getattr(
                action,
                "business_area",
                "",
            )

            for domain in domains:

                if domain.business_area.lower() != business_area.lower():
                    continue

                edge = self.create_edge(

                    source=action,

                    target=domain,

                    relation="LEADS",

                    reasoning="Action leads business area",

                    confidence=min(
                        action.confidence,
                        domain.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # ACTION → OWNS → METRIC
    ####################################################################

    def _build_ownership_relationships(
        self,
        context,
        statement,
    ) -> None:

        actions = statement.actions
        metrics = statement.metrics

        if not actions:
            return

        if not metrics:
            return

        for action in actions:

            metadata = getattr(
                action,
                "metadata",
                {},
            )

            if not metadata.get(
                "ownership",
                False,
            ):
                continue

            for metric in metrics:

                edge = self.create_edge(

                    source=action,

                    target=metric,

                    relation="OWNS",

                    reasoning="Action owns metric",

                    confidence=min(
                        action.confidence,
                        metric.confidence,
                    ),

                )

                self.register_edge(
                    context,
                    edge,
                )

    ####################################################################
    # DOMAIN ↔ COLLABORATES_WITH ↔ DOMAIN
    ####################################################################

    def _build_cross_functional_relationships(
        self,
        context,
        statement,
    ) -> None:

        domains = statement.domains

        if len(domains) < 2:
            return

        for source in domains:

            for target in domains:

                if source.entity_id == target.entity_id:
                    continue

                if (
                    source.business_area
                    and
                    target.business_area
                    and
                    source.business_area.lower()
                    !=
                    target.business_area.lower()
                ):

                    edge = self.create_edge(

                        source=source,

                        target=target,

                        relation="COLLABORATES_WITH",

                        reasoning="Cross functional collaboration",

                        confidence=min(
                            source.confidence,
                            target.confidence,
                        ),

                    )

                    self.register_edge(
                        context,
                        edge,
                    )