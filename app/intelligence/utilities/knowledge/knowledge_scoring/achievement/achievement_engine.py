"""
Enterprise Achievement Engine V5

Graph-native achievement engine.

Architecture

KnowledgeGraph
      ↓
Graph Nodes
Graph Edges
      ↓
Achievement Cards
      ↓
Achievement Scores

No ImpactEngine
No MagnitudeEngine

Enterprise V5
"""

from collections import defaultdict


class AchievementEngine:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):
        pass

    ####################################################################
    # MAIN
    ####################################################################

    def score(self, graph):

        achievements = []

        total_score = 0

        impact_total = 0
        magnitude_total = 0

        # --------------------------------------------------------
        # Quick lookup
        # --------------------------------------------------------

        nodes = graph.nodes

        outgoing = defaultdict(list)

        for edge in graph.edges:

            outgoing[edge.source_id].append(edge)

        # --------------------------------------------------------
        # Every action becomes a possible achievement
        # --------------------------------------------------------

        for node in nodes.values():

            if node.entity_type.lower() != "action":
                continue

            action = node

            metric = None
            measurement = None
            domain = None

            # ----------------------------------------------------
            # Traverse graph
            # ----------------------------------------------------

            for edge in outgoing.get(action.node_id, []):

                target = nodes.get(edge.target_id)

                if target is None:
                    continue

                t = target.entity_type.lower()

                if t == "metric":
                    metric = target

                elif t == "measurement":
                    measurement = target

                elif t == "domain":
                    domain = target

            # ----------------------------------------------------
            # Scores
            # ----------------------------------------------------

            impact_score = self.compute_impact(
                action,
                metric,
            )

            magnitude_score = self.compute_magnitude(
                measurement,
            )

            overall = round(
                impact_score + magnitude_score,
                2,
            )

            total_score += overall
            impact_total += impact_score
            magnitude_total += magnitude_score

            achievements.append(

                {

                    "action":
                        action.label,

                    "metric":
                        metric.label if metric else "",

                    "measurement":
                        measurement.metadata.get(
                            "value",
                            "",
                        )
                        if measurement
                        else "",

                    "from_value":
                        measurement.metadata.get(
                            "from_value"
                        )
                        if measurement
                        else None,

                    "to_value":
                        measurement.metadata.get(
                            "to_value"
                        )
                        if measurement
                        else None,

                    "change_value":
                        measurement.metadata.get(
                            "change_value"
                        )
                        if measurement
                        else None,

                    "percent_change":
                        measurement.metadata.get(
                            "percent_change"
                        )
                        if measurement
                        else None,

                    "direction":
                        measurement.metadata.get(
                            "direction",
                            "",
                        )
                        if measurement
                        else "",

                    "classification":
                        self.classification(
                            measurement
                        ),

                    "business_area":
                        metric.business_area
                        if metric
                        else "",

                    "domain":
                        domain.label
                        if domain
                        else "",

                    "impact_score":
                        impact_score,

                    "magnitude_score":
                        magnitude_score,

                    "overall_score":
                        overall,

                    "business_value":
                        self.business_value(
                            overall
                        ),

                    "executive_ready":
                        overall >= 25,

                }

            )

        # --------------------------------------------------------

        achievements.sort(

            key=lambda x: x["overall_score"],

            reverse=True,

        )

        return {

            "achievement_score":
                round(total_score, 2),

            "achievement_count":
                len(achievements),

            "impact_score":
                round(impact_total, 2),

            "magnitude_score":
                round(magnitude_total, 2),

            "achievements":
                achievements,

        }

    ####################################################################
    # IMPACT
    ####################################################################

    def compute_impact(
        self,
        action,
        metric,
    ):

        score = 0

        score += getattr(
            action,
            "impact_weight",
            1,
        )

        if metric:

            score += getattr(
                metric,
                "impact_weight",
                1,
            )

        return round(score, 2)

    ####################################################################
    # MAGNITUDE
    ####################################################################

    def compute_magnitude(
        self,
        measurement,
    ):

        if measurement is None:
            return 0

        percent = measurement.metadata.get(
            "percent_change",
            0,
        )

        if percent is None:
            percent = 0

        if percent >= 100:
            return 20

        if percent >= 50:
            return 15

        if percent >= 20:
            return 10

        if percent >= 10:
            return 5

        return 2

    ####################################################################
    # CLASSIFICATION
    ####################################################################

    def classification(
        self,
        measurement,
    ):

        if measurement is None:
            return "Unknown"

        percent = measurement.metadata.get(
            "percent_change",
            0,
        )

        if percent >= 100:
            return "Exceptional"

        if percent >= 50:
            return "High"

        if percent >= 20:
            return "Moderate"

        return "Low"

    ####################################################################
    # BUSINESS VALUE
    ####################################################################

    def business_value(
        self,
        score,
    ):

        if score >= 35:
            return "Exceptional"

        if score >= 25:
            return "High"

        if score >= 15:
            return "Moderate"

        return "Low"