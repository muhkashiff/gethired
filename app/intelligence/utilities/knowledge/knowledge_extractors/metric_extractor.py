"""
Metric Extractor

Extracts business KPIs
from resume statements.
"""

import json
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricExtractor:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent.parent

            / "knowledge_knowledge"

            / "ontology"

            / "metrics_dictionary.json"

        )

        with open(path, encoding="utf8") as f:

            self.metrics = json.load(f)

    # ------------------------------------------------------

    def extract(self, sentence):

        sentence = sentence.lower()

        best_match = ""

        for metric in self.metrics:

            if metric in sentence:

                if len(metric) > len(best_match):

                    best_match = metric

        if best_match == "":

            return MetricKnowledge()

        data = self.metrics[best_match]

        return MetricKnowledge(

            found=True,

            metric=best_match,

            canonical=data["canonical"],

            category=data["category"],

            unit=data["unit"],

            confidence=0.95

        )