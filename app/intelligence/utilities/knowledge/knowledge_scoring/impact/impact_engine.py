"""
Impact Engine

Calculates business impact from the Knowledge Graph.

The engine never reads JSON directly.

Knowledge Graph
        │
        ▼
Impact Rules
        │
        ▼
Impact Score
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.impact.impact_rules import (
    ImpactRules,
)


class ImpactEngine:

    def __init__(self):

        self.rules = ImpactRules()

    # -------------------------------------------------------
    # Main
    # -------------------------------------------------------

    def score(self, graph):

        """
        Returns complete impact analysis.
        """

        results = []

        total_score = 0.0

        measurements = graph.measurements()

        for measurement in measurements:

            metric = self._find_metric(graph, measurement)

            action = self._find_action(graph, metric)

            if metric is None:
                continue

            result = self._score_measurement(

                metric=metric,

                measurement=measurement,

                action=action,

            )

            results.append(result)

            total_score += result["score"]

        return {

            "score": round(total_score, 2),

            "count": len(results),

            "measurements": results,

        }

    # -------------------------------------------------------
    # Score One Measurement
    # -------------------------------------------------------

    def _score_measurement(

        self,

        metric,

        measurement,

        action,

    ):

        metric_name = metric.canonical

        weight = self.rules.get_weight(metric_name)

        executive = self.rules.get_executive_weight(metric_name)

        direction = self.rules.evaluate_direction(

            metric_name,

            measurement.metadata.get(

                "direction",

                "neutral",

            ),

        )

        score = float(weight)

        # --------------------------
        # Achievement Bonus
        # --------------------------

        if measurement.metadata.get(

            "achievement",

            True,

        ):

            score += 2

        # --------------------------
        # Quantified Bonus
        # --------------------------

        if measurement.metadata.get(

            "quantified",

            True,

        ):

            score += 1

        # --------------------------
        # Positive Direction Bonus
        # --------------------------

        if direction == "positive":

            score += 2

        elif direction == "negative":

            score -= 2

        # --------------------------
        # Executive Weight
        # --------------------------

        score *= executive

        return {

            "metric": metric_name,

            "value": measurement.metadata.get("value"),

            "unit": measurement.metadata.get("unit"),

            "direction": direction,

            "base_weight": weight,

            "executive_weight": executive,

            "score": round(score, 2),

            "action": action.label if action else "",

        }

    # -------------------------------------------------------
    # Find Metric
    # -------------------------------------------------------

    def _find_metric(

        self,

        graph,

        measurement,

    ):

        """
        Measurement
             ▲
             │ measured_by
        Metric
        """

        for edge in measurement.incoming_edges:

            if edge.relationship == "measured_by":

                return graph.get_node_by_entity(

                    edge.source_node

                )

        return None

    # -------------------------------------------------------
    # Find Action
    # -------------------------------------------------------

    def _find_action(

        self,

        graph,

        metric,

    ):

        """
        Metric
             ▲
             │ affects
        Action
        """

        if metric is None:

            return None

        for edge in metric.incoming_edges:

            if edge.relationship == "affects":

                return graph.get_node_by_entity(

                    edge.source_node

                )

        return None