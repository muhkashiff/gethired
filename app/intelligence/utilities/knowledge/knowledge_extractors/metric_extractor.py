"""
Metric Extractor

Extracts business KPIs
from resume statements.

Repository Driven Version
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricExtractor:

    def __init__(self):

        self.repository = Repository()

        # Load KPI dictionary
        self.metrics = self.repository.get_dictionary("metrics")

        # Longest metric phrases first
        self.sorted_metrics = sorted(
            self.metrics.keys(),
            key=len,
            reverse=True,
        )

    # ------------------------------------------------------

    def extract(self, sentence):

        sentence = sentence.lower()

        best_match = ""

        # Search longest phrases first
        for metric in self.sorted_metrics:

            if metric in sentence:

                best_match = metric
                break

        if best_match == "":

            return MetricKnowledge()

        entity = self.repository.get_metric(best_match)

        if entity is None:

            return MetricKnowledge()

        return MetricKnowledge(

            found=True,

            confidence=0.95,

            metric=best_match,

            canonical=entity.canonical,

            category=entity.category,

            unit=entity.preferred_unit,

            entity_id=entity.entity_id,

            business_area=entity.business_area,

            impact_weight=entity.impact_weight,

            source=entity.source,

            metadata=entity.metadata,

            higher_is_better=entity.metadata.get(
                "higher_is_better",
                True,
            ),

            preferred_unit=entity.preferred_unit,

        )