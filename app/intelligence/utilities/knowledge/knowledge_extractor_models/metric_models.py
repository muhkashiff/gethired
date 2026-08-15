"""
Enterprise Metric Knowledge Model
Enterprise V5

Represents a business metric extracted from the metrics ontology.

Examples
--------
Production Yield
Efficiency
Productivity
Quality Score
Customer Satisfaction
Downtime
OEE
Waste
Complaint Rate
Scrap Rate
"""

from __future__ import annotations

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class MetricKnowledge(KnowledgeEntity):
    """
    Enterprise V5 knowledge model for metrics.

    Extends KnowledgeEntity with metric-specific semantic,
    classification, KPI, and measurement information.
    """

    # ==============================================================
    # ENTITY
    # ==============================================================

    entity_type: str = "metric"

    ontology_name: str = "metrics"

    # ==============================================================
    # METRIC DEFINITION
    # ==============================================================
    
    metric_family: str = ""

    metric_group: str = ""

    unit: str = ""

    # ==============================================================
    # METRIC BEHAVIOUR
    # ==============================================================

    higher_is_better: bool = True

    lower_is_better: bool = False

    # ==============================================================
    # METRIC CLASSIFICATION
    # ==============================================================

    percentage_metric: bool = False

    financial_metric: bool = False

    quality_metric: bool = False

    productivity_metric: bool = False

    operational_metric: bool = False

    # ==============================================================
    # KPI / BUSINESS
    # ==============================================================

    kpi: bool = False

    benchmark_available: bool = False

    target_value: float = 0.0

    # ==============================================================
    # MEASUREMENT
    # ==============================================================

    measurement_expected: bool = True

    # ==============================================================
    # METRIC BEHAVIOUR
    # ==============================================================

    def direction_for_change(
        self,
        change_value,
    ) -> str:
        """
        Determine the mathematical direction of a measurement change.

        Parameters
        ----------
        change_value:
            Numeric change in the metric.

        Returns
        -------
        str
            "increase"
            "decrease"
            "unchanged"
            ""

        Examples
        --------
        +29  -> increase
        -5   -> decrease
         0   -> unchanged
        None -> ""
        """

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

    # ==============================================================
    # IMPROVEMENT EVALUATION
    # ==============================================================

    def evaluate_change(
        self,
        change_value,
    ) -> bool:
        """
        Determine whether a metric change represents improvement.

        The decision is based on higher_is_better.

        Examples
        --------
        Production Yield
            higher_is_better = True

            +29 -> True
            -10 -> False

        Scrap Rate
            higher_is_better = False

            -5 -> True
            +5 -> False

        Zero change is never considered an improvement.
        """

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

        # ----------------------------------------------------------
        # NO CHANGE
        # ----------------------------------------------------------

        if change == 0:
            return False

        # ----------------------------------------------------------
        # HIGHER IS BETTER
        # ----------------------------------------------------------

        if self.higher_is_better:
            return change > 0

        # ----------------------------------------------------------
        # LOWER IS BETTER
        # ----------------------------------------------------------

        return change < 0