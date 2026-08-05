"""
Enterprise Future Readiness Analyzer

Infers future capabilities from skill clusters.

This is inference rather than scoring.

Examples

Python + Pandas + SQL + Power BI

↓

Data Ready

-------------------------

Python + Docker + Azure

↓

Cloud Ready

-------------------------

Python + Machine Learning

↓

AI Ready

-------------------------

Python + Docker + APIs

↓

Automation Ready
"""

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    FutureReadiness,
)


class FutureReadinessAnalyzer:

    """
    Infers enterprise future readiness from capability clusters.
    """

    def analyze(self, clusters):

        readiness = FutureReadiness()

        cluster_names = {

            cluster.name

            for cluster in clusters

        }

        # ------------------------------------------------------
        # AI Ready
        # ------------------------------------------------------

        if "Machine Learning" in cluster_names:

            readiness.ai_ready = 100

        # ------------------------------------------------------
        # Data Ready
        # ------------------------------------------------------

        if (

            "Machine Learning" in cluster_names

            or

            "Data Analytics" in cluster_names

        ):

            readiness.data_ready = 90

        # ------------------------------------------------------
        # Cloud Ready
        # ------------------------------------------------------

        if "Cloud Engineering" in cluster_names:

            readiness.cloud_ready = 90

        # ------------------------------------------------------
        # Automation Ready
        # ------------------------------------------------------

        if (

            "Backend Development" in cluster_names

            and

            "Cloud Engineering" in cluster_names

        ):

            readiness.automation_ready = 95

        elif "Backend Development" in cluster_names:

            readiness.automation_ready = 70

        # ------------------------------------------------------
        # Digital Ready
        # ------------------------------------------------------

        digital_clusters = {

            "Machine Learning",

            "Data Analytics",

            "Cloud Engineering",

            "Backend Development",

        }

        readiness.digital_ready = (

            len(

                cluster_names.intersection(

                    digital_clusters

                )

            )

            * 25

        )

        readiness.digital_ready = min(

            readiness.digital_ready,

            100,

        )

        # ------------------------------------------------------
        # Analytics Ready
        # ------------------------------------------------------

        if "Data Analytics" in cluster_names:

            readiness.analytics_ready = 90

        # ------------------------------------------------------
        # Overall
        # ------------------------------------------------------

        values = [

            readiness.ai_ready,

            readiness.automation_ready,

            readiness.digital_ready,

            readiness.analytics_ready,

            readiness.cloud_ready,

            readiness.data_ready,

        ]

        readiness.overall = round(

            sum(values) / len(values),

            2,

        )

        return readiness