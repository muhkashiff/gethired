"""
Enterprise Achievement Builder

Builds enterprise achievement relationships.

Purpose
-------
Creates enterprise achievement semantics.

Action
   │
 ACHIEVED
   ▼
Metric

Measurement relationships are handled separately
by MeasurementBuilder.

Runs AFTER

    RelationshipBuilder

    MeasurementBuilder

Runs BEFORE

    DependencyBuilder

Enterprise V11
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_semantic_builder import (
    BaseSemanticBuilder,
)


class AchievementBuilder(BaseSemanticBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        self._build_achievement_relationships(
            context,
            statement,
        )

        self._identify_quantified_results(
            statement,
        )

    ####################################################################
    # ACTION → ACHIEVED → METRIC
    ####################################################################

    def _build_achievement_relationships(
        self,
        context,
        statement,
    ) -> None:

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

                    relation="ACHIEVED",

                    reasoning="Action achieved business metric",

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
    # QUANTIFIED RESULTS
    ####################################################################

    def _identify_quantified_results(
        self,
        statement,
    ) -> None:
        """
        Marks measurements that represent
        quantified business results.
        """

        for measurement in statement.measurements:

            if measurement is None:
                continue

            if not getattr(
                measurement,
                "found",
                False,
            ):
                continue

            metadata = getattr(
                measurement,
                "metadata",
                {},
            )

            value = metadata.get(
                "value",
                None,
            )

            if value is None:
                continue

            metadata["quantified"] = True

            metadata.setdefault(
                "achievement_type",
                "business_result",
            )

            measurement.metadata = metadata