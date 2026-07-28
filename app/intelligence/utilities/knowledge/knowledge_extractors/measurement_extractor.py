"""
Measurement Extractor

Uses the modular Measurement Parser to extract
measurements from resume achievements.
"""

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.measurement_parser import (
    MeasurementParser,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import (
    MeasurementKnowledge,
)


class MeasurementExtractor:

    def __init__(self):

        self.parser = MeasurementParser()

    # ----------------------------------------------------------

    def extract(self, sentence, metric):

        if not metric.found:
            return MeasurementKnowledge()

        result = self.parser.parse(sentence)

        if result is None:
            return MeasurementKnowledge()

        return MeasurementKnowledge(

            # --------------------------------------------------
            # Detection
            # --------------------------------------------------

            found=True,

            confidence=0.98,

            # --------------------------------------------------
            # Metric
            # --------------------------------------------------

            metric=metric.canonical,

            canonical=metric.canonical,

            category=metric.category,

            # --------------------------------------------------
            # Original Measurement
            # --------------------------------------------------

            value=result.get("raw_value", ""),

            numeric_value=float(
                result.get("numeric_value", 0.0)
            ),

            normalized_value=float(
                result.get("numeric_value", 0.0)
            ),

            unit=result.get("unit", ""),

            operator=result.get(
                "comparison_operator",
                "",
            ),

            # --------------------------------------------------
            # Advanced Measurement
            # --------------------------------------------------

            measurement_type=result.get(
                "measurement_type",
                "absolute",
            ),

            from_value=result.get("from_value"),

            to_value=result.get("to_value"),

            change_value=result.get("change_value"),

            percent_change=result.get("percent_change"),

            comparison_operator=result.get(
                "comparison_operator",
                "",
            ),

            # --------------------------------------------------
            # Business Interpretation
            # --------------------------------------------------

            direction="",

            effect="",

            business_meaning="",

            # --------------------------------------------------
            # Ontology
            # --------------------------------------------------

            entity_id=metric.entity_id,

            business_area=metric.business_area,

            impact_weight=metric.impact_weight,

            source=metric.source,

            metadata=metric.metadata,

        )