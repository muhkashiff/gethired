"""
Impact Rules

Business interpretation layer for impact scoring.

This module does not calculate scores.

It only answers questions:

- What is the importance of a metric?
- Is increasing this metric good?
- What is the executive multiplier?
- What category does it belong to?

Source:
impact_dictionary.json
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.impact.impact_repository import (
    ImpactRepository,
)


class ImpactRules:

    def __init__(self):

        self.repository = ImpactRepository()

        self.rules = self.repository.get_rules()

    # -------------------------------------------------
    # Metric lookup
    # -------------------------------------------------

    def get_metric_rule(self, metric):

        """
        Returns complete rule for metric.

        Example:

        Production Yield

        {
            weight:9,
            higher_is_better:True,
            executive_weight:1.2
        }
        """

        if not metric:
            return {}

        return self.rules.get(
            metric,
            {}
        )


    # -------------------------------------------------
    # Weight
    # -------------------------------------------------

    def get_weight(self, metric):

        rule = self.get_metric_rule(metric)

        return rule.get(
            "weight",
            1
        )


    # -------------------------------------------------
    # Executive importance
    # -------------------------------------------------

    def get_executive_weight(self, metric):

        rule = self.get_metric_rule(metric)

        return rule.get(
            "executive_weight",
            1.0
        )


    # -------------------------------------------------
    # Metric direction
    # -------------------------------------------------

    def higher_is_better(self, metric):

        rule = self.get_metric_rule(metric)

        return rule.get(
            "higher_is_better",
            True
        )


    # -------------------------------------------------
    # Category
    # -------------------------------------------------

    def get_category(self, metric):

        rule = self.get_metric_rule(metric)

        return rule.get(
            "category",
            ""
        )


    # -------------------------------------------------
    # Impact classification
    # -------------------------------------------------

    def evaluate_direction(
        self,
        metric,
        action_direction,
    ):

        """
        Determines whether an action creates
        positive or negative impact.

        Example:

        Production Yield
        higher_is_better=True

        increase -> positive
        decrease -> negative


        Customer Complaints
        higher_is_better=False

        increase -> negative
        decrease -> positive
        """

        better = self.higher_is_better(metric)


        if action_direction == "neutral":

            return "neutral"


        if better:

            if action_direction == "increase":
                return "positive"

            if action_direction == "decrease":
                return "negative"


        else:

            if action_direction == "increase":
                return "negative"

            if action_direction == "decrease":
                return "positive"


        return "neutral"