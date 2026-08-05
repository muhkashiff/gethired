"""
Metric Defaults

Enterprise V12 Compatible
"""

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricDefaults:

    @staticmethod
    def unknown():

        return MetricKnowledge(

            # Detection
            found=False,
            confidence=0.0,

            # KnowledgeEntity
            original="",
            canonical="Unknown Metric",
            normalized="unknown_metric",

            entity_id="UNKNOWN_METRIC",
            entity_type="metric",

            category="unknown",
            ontology_name="metrics",

            business_area="unknown",
            domain="",

            impact_weight=0.0,

            source="metric_reasoner",

            metadata={
                "temporary": False,
                "reason": "Metric not found",
            },

            # Metric specific
            metric_family="",
            metric_group="",
            unit="",

            higher_is_better=False,
            lower_is_better=False,

            percentage_metric=False,
            financial_metric=False,
            quality_metric=False,
            productivity_metric=False,
            operational_metric=False,

            kpi=False,
            benchmark_available=False,
            target_value=0.0,

            measurement_expected=False,
        )