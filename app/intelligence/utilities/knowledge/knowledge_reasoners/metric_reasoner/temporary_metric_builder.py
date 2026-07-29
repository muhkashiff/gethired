"""
Temporary KPI Builder

Creates temporary KPI objects when the
metric is not yet present in the ontology.
"""

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)

from .metric_classifier import MetricClassifier


class TemporaryMetricBuilder:

    def __init__(self):

        self.classifier = MetricClassifier()

    def build(self, metric_name):

        business_area, category = self.classifier.classify(metric_name)

        entity = (

            "TEMP_"

            + metric_name.upper()

            .replace(" ", "_")

            .replace("-", "_")

        )

        return MetricKnowledge(

            found=True,

            confidence=0.70,

            metric=metric_name,

            canonical=metric_name.title(),

            category=category,

            unit="",

            entity_id=entity,

            business_area=business_area,

            impact_weight=3.0,

            source="metric_reasoner",

            metadata={

                "temporary": True,

                "reason": "Ontology inference",

            },

            higher_is_better=None,

            preferred_unit="",

        )