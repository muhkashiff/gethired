"""
Cluster Classifier

Determines the semantic meaning of a cluster.

Example

Action + KPI + Measurement
        -> achievement

Action + Staff
        -> leadership

Action + Standard
        -> certification

Action + Process
        -> improvement

Action only
        -> responsibility
"""

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
)


class ClusterClassifier:

    def classify(self, cluster: SemanticCluster):

        entity_types = {

            e.entity_type.lower()

            for e in cluster.entities

        }

        labels = {

            e.canonical.lower()

            for e in cluster.entities

        }

        # ---------------------------------------------
        # Achievement
        # ---------------------------------------------

        if "measurement" in entity_types:

            cluster.semantic_type = "achievement"

            return cluster

        # ---------------------------------------------
        # KPI improvement
        # ---------------------------------------------

        if "kpi" in entity_types:

            cluster.semantic_type = "achievement"

            return cluster

        # ---------------------------------------------
        # Leadership
        # ---------------------------------------------

        if "object" in entity_types:

            if any(

                x in labels

                for x in [

                    "staff",

                    "employees",

                    "team",

                    "people",

                    "workforce",

                ]

            ):

                cluster.semantic_type = "leadership"

                return cluster

        # ---------------------------------------------
        # Certification
        # ---------------------------------------------

        if "standard" in entity_types:

            cluster.semantic_type = "certification"

            return cluster

        # ---------------------------------------------
        # Methodology
        # ---------------------------------------------

        if "methodology" in entity_types:

            cluster.semantic_type = "continuous_improvement"

            return cluster

        # ---------------------------------------------
        # Responsibility
        # ---------------------------------------------

        if "action" in entity_types:

            cluster.semantic_type = "responsibility"

            return cluster

        # ---------------------------------------------

        cluster.semantic_type = "statement"

        return cluster