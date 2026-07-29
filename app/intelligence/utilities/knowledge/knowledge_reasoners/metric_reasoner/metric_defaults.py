"""
Metric Defaults

Provides safe fallback KPI objects whenever
a metric cannot be identified.

This prevents empty fields propagating through
the pipeline.
"""

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricDefaults:

    @staticmethod
    def unknown():

        return MetricKnowledge(

            found=False,

            confidence=0.0,

            metric="Unknown Metric",

            canonical="No KPI Detected",

            category="unknown",

            unit="",

            entity_id="UNKNOWN_METRIC",

            business_area="unknown",

            impact_weight=0.0,

            source="metric_reasoner",

            metadata={

                "temporary": False,

                "reason": "Metric not found",

                "higher_is_better": None,

            },

            higher_is_better=None,

            preferred_unit="",

        )