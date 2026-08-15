"""
Enterprise Metric Extractor
Enterprise V5

Responsibility
--------------
Convert metric MatchResult objects into MetricKnowledge objects.

Pipeline:

ExtractionRequest
        ↓
KnowledgeV5Pipeline
        ↓
MatchResult
        ↓
MetricExtractor
        ↓
MetricKnowledge
        ↓
ExtractionResult[MetricKnowledge]

Architecture
------------
This extractor intentionally inherits from GenericOntologyExtractor.

The generic extractor is responsible for:

    - multi-match extraction
    - confidence filtering
    - entity filtering
    - common KnowledgeEntity fields
    - repository metadata
    - match positions
    - alias information
    - ExtractionResult construction

MetricExtractor is responsible only for
metric-specific fields.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)

from .generic_ontology_extractor import (
    GenericOntologyExtractor,
)


class MetricExtractor(
    GenericOntologyExtractor[MetricKnowledge]
):
    """
    Enterprise V5 metric knowledge extractor.

    Extracts one or more metric entities from a sentence
    and converts every MatchResult into a MetricKnowledge object.
    """

    # ==================================================================
    # CONFIGURATION
    # ==================================================================

    ontology_name = "metrics"

    knowledge_class = MetricKnowledge

    entity_type = "metric"

    # ==================================================================
    # METRIC-SPECIFIC FIELDS
    # ==================================================================

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to MetricKnowledge.

        All common KnowledgeEntity fields are populated by
        GenericOntologyExtractor.populate_entity().
        """

        # --------------------------------------------------------------
        # HIGHER / LOWER IS BETTER
        # --------------------------------------------------------------

        higher_is_better = metadata.get(
            "higher_is_better",
            getattr(
                entity,
                "higher_is_better",
                True,
            ),
        )

        higher_is_better = bool(
            higher_is_better
        )

        # --------------------------------------------------------------
        # TARGET VALUE
        # --------------------------------------------------------------

        target_value = metadata.get(
            "target_value",
            0.0,
        )

        try:
            target_value = float(
                target_value
            )
        except (
            TypeError,
            ValueError,
        ):
            target_value = 0.0

        # --------------------------------------------------------------
        # IMPACT WEIGHT
        # --------------------------------------------------------------

        impact_weight = metadata.get(
            "impact_weight",
            getattr(
                entity,
                "impact_weight",
                1.0,
            ),
        )

        try:
            impact_weight = float(
                impact_weight
            )
        except (
            TypeError,
            ValueError,
        ):
            impact_weight = 1.0

        # --------------------------------------------------------------
        # METRIC-SPECIFIC VALUES
        # --------------------------------------------------------------

        return {

            # ==========================================================
            # IDENTITY
            # ==========================================================

            "metric_family": metadata.get(
                "metric_family",
                "",
            ),

            "metric_group": metadata.get(
                "metric_group",
                "",
            ),

            "unit": metadata.get(
                "unit",
                metadata.get(
                    "preferred_unit",
                    "",
                ),
            ),

            # ==========================================================
            # DIRECTION
            # ==========================================================

            "higher_is_better": (
                higher_is_better
            ),

            "lower_is_better": (
                not higher_is_better
            ),

            # ==========================================================
            # METRIC CLASSIFICATION
            # ==========================================================

            "percentage_metric": metadata.get(
                "percentage_metric",
                False,
            ),

            "financial_metric": metadata.get(
                "financial_metric",
                False,
            ),

            "quality_metric": metadata.get(
                "quality_metric",
                False,
            ),

            "productivity_metric": metadata.get(
                "productivity_metric",
                False,
            ),

            "operational_metric": metadata.get(
                "operational_metric",
                False,
            ),

            # ==========================================================
            # KPI
            # ==========================================================

            "kpi": metadata.get(
                "kpi",
                False,
            ),

            "benchmark_available": metadata.get(
                "benchmark_available",
                False,
            ),

            "target_value": (
                target_value
            ),

            # ==========================================================
            # MEASUREMENT
            # ==========================================================

            "measurement_expected": metadata.get(
                "measurement_expected",
                True,
            ),

            # ==========================================================
            # BUSINESS
            # ==========================================================

            "impact_weight": (
                impact_weight
            ),
        }