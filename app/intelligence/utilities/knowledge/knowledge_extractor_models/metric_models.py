
"""
Enterprise Metric Knowledge Model

Represents business metrics extracted from text.

Examples:

Yield
Efficiency
Productivity
Quality Score
Customer Satisfaction
Downtime
OEE
Waste
Complaint Rate
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class MetricKnowledge(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "metric"

    ontology_name: str = "metrics"

    ####################################################################
    # Metric Definition
    ####################################################################

    metric_family: str = ""

    metric_group: str = ""

    unit: str = ""

    ####################################################################
    # Behaviour
    ####################################################################

    higher_is_better: bool = True

    lower_is_better: bool = False

    percentage_metric: bool = False

    financial_metric: bool = False

    quality_metric: bool = False

    productivity_metric: bool = False

    operational_metric: bool = False

    ####################################################################
    # Business
    ####################################################################

    kpi: bool = False

    benchmark_available: bool = False

    target_value: float = 0.0

    ####################################################################
    # Parsing
    ####################################################################

    measurement_expected: bool = True

    ####################################################################
    # OBJECT-ORIENTED METRIC BEHAVIOUR
    ####################################################################

    def direction_for_change(self, change_value):
        """
        Determine the mathematical direction of a measurement change.

        Positive value:
            increase

        Negative value:
            decrease

        Zero:
            unchanged
        """

        if change_value is None:

            return ""

        try:

            change = float(change_value)

        except (TypeError, ValueError):

            return ""

        if change > 0:

            return "increase"

        elif change < 0:

            return "decrease"

        return "unchanged"

    ####################################################################

    def evaluate_change(self, change_value):
        """
        Determine whether a measurement change is an improvement.

        The decision is based on the metric's
        higher_is_better property.

        Examples:

        Production Yield
            higher_is_better = True

            70 -> 99
            change = +29
            improvement = True


        Scrap Rate
            higher_is_better = False

            10 -> 5
            change = -5
            improvement = True


        Scrap Rate
            higher_is_better = False

            5 -> 10
            change = +5
            improvement = False
        """

        if change_value is None:

            return False

        try:

            change = float(change_value)

        except (TypeError, ValueError):

            return False

        ################################################################
        # No change
        ################################################################

        if change == 0:

            return False

        ################################################################
        # Higher value is better
        ################################################################

        if self.higher_is_better:

            return change > 0

        ################################################################
        # Lower value is better
        ################################################################

        return change < 0
