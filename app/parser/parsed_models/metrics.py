"""
Enterprise Metric Parser Model

Enterprise V5

Parser-layer model for Metric extraction.

This model is intentionally separate from MetricKnowledge.

Knowledge layer:
    MetricKnowledge

Parser layer:
    MetricParserModel
"""

from __future__ import annotations

from dataclasses import dataclass

from dataclasses import dataclass, field

from .base_parser_models import ParserModel


@dataclass
class MetricParserModel(ParserModel):
    """
    Parser-layer representation of an extracted metric.
    """

    ####################################################################
    # ENTITY
    ####################################################################

    entity_type: str = "metric"

    ontology_name: str = "metrics"

    ####################################################################
    # METRIC DEFINITION
    ####################################################################

    metric_family: str = ""

    metric_group: str = ""

    unit: str = ""

    ####################################################################
    # CLASSIFICATION
    ####################################################################

    higher_is_better: bool = True

    lower_is_better: bool = False

    percentage_metric: bool = False

    financial_metric: bool = False

    quality_metric: bool = False

    productivity_metric: bool = False

    operational_metric: bool = False

    ####################################################################
    # BUSINESS
    ####################################################################

    kpi: bool = False

    benchmark_available: bool = False

    target_value: float = 0.0

    ####################################################################
    # MEASUREMENT
    ####################################################################

    measurement_expected: bool = True

    ####################################################################
    # BUSINESS IMPACT
    ####################################################################

    impact_weight: float = 0.0

    ####################################################################
    # SOURCE
    ####################################################################

    source: str = ""

    ####################################################################
    # DESCRIPTION
    ####################################################################

    description: str = ""

    ####################################################################
    # RAW METADATA
    ####################################################################

    metadata: dict = field(default_factory=dict)

    ####################################################################
    # METRIC BEHAVIOUR
    ####################################################################

    def direction_for_change(
        self,
        change_value,
    ) -> str:

        if change_value is None:

            return ""

        try:

            change = float(
                change_value
            )

        except (
            TypeError,
            ValueError,
        ):

            return ""

        if change > 0:

            return "increase"

        if change < 0:

            return "decrease"

        return "unchanged"

    ####################################################################

    def evaluate_change(
        self,
        change_value,
    ) -> bool:

        if change_value is None:

            return False

        try:

            change = float(
                change_value
            )

        except (
            TypeError,
            ValueError,
        ):

            return False

        ################################################################
        # NO CHANGE
        ################################################################

        if change == 0:

            return False

        ################################################################
        # HIGHER IS BETTER
        ################################################################

        if self.higher_is_better:

            return change > 0

        ################################################################
        # LOWER IS BETTER
        ################################################################

        return change < 0

    @property
    def metric_count(self) -> int:
        """
        Number of related business metrics.
        """
        return len(self.related_metrics)