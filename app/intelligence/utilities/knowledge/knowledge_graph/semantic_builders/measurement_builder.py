"""
Enterprise Measurement Builder

Builds enterprise measurement relationships.

Purpose
-------
Enriches the Knowledge Graph with measurement semantics.

Runs AFTER:
    - MeasurementNodeBuilder
    - MetricNodeBuilder

Runs BEFORE:
    - AchievementBuilder
    - DependencyBuilder

Enterprise V10
"""

from app.intelligence.utilities.knowledge.knowledge_graph.builders.base_semantic_builder import (
    BaseSemanticBuilder,
)


class MeasurementBuilder(BaseSemanticBuilder):

    ####################################################################
    # BUILD
    ####################################################################

    def build(
        self,
        context,
        statement,
    ) -> None:

        self._link_measurements_to_metrics(
            context,
            statement,
        )

        self._normalize_measurement_metadata(
            statement,
        )

    ####################################################################
    # Measurement → Metric
    ####################################################################

    def _link_measurements_to_metrics(
        self,
        context,
        statement,
    ) -> None:

        metrics = {
            metric.entity_id: metric
            for metric in statement.metrics
            if metric is not None
        }

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

            metric_id = metadata.get(
                "metric_id",
                None,
            )

            if metric_id is None:
                continue

            metric = metrics.get(
                metric_id,
            )

            if metric is None:
                continue

            edge = self.create_edge(

                source=metric,

                target=measurement,

                relation="HAS_MEASUREMENT",

                reasoning="Metric has measurement",

                confidence=0.98,

            )

            self.register_edge(

                context,

                edge,

            )

    ####################################################################
    # NORMALIZE MEASUREMENT METADATA
    ####################################################################

    def _normalize_measurement_metadata(
        self,
        statement,
    ) -> None:

        """
        Ensures every Measurement entity contains
        normalized metadata for downstream builders.
        """

        for measurement in statement.measurements:

            if measurement is None:
                continue

            metadata = getattr(
                measurement,
                "metadata",
                {},
            )

            metadata.setdefault(
                "unit",
                "",
            )

            metadata.setdefault(
                "direction",
                "",
            )

            metadata.setdefault(
                "baseline",
                None,
            )

            metadata.setdefault(
                "target",
                None,
            )

            metadata.setdefault(
                "value",
                None,
            )

            measurement.metadata = metadata