
from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)

from app.intelligence.utilities.knowledge.knowledge_parser.measurement.measurement_parser import (
    MeasurementParser,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import (
    MeasurementKnowledge,
)


class MeasurementExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self, repository=None):

        self.repository = repository or Repository()

        self.parser = MeasurementParser()

    ####################################################################
    # MAIN
    ####################################################################

    def extract(
        self,
        sentence,
        metric,
    ):

        ################################################################
        # Metric validation
        ################################################################

        if metric is None:

            return MeasurementKnowledge()

        if not metric.found:

            return MeasurementKnowledge()

        ################################################################
        # Parse measurement
        ################################################################

        result = self.parser.parse(sentence)

        if result is None:

            return MeasurementKnowledge()

        ################################################################
        # Change
        ################################################################

        change_value = result.get(
            "change_value"
        )

        ################################################################
        # Direction
        ################################################################

        direction = metric.direction_for_change(
            change_value
        )

        ################################################################
        # Improvement
        ################################################################

        improvement = metric.evaluate_change(
            change_value
        )

        ################################################################
        # Business Effect
        ################################################################

        effect = metric.metadata.get(
            "positive_effect",
            ""
        )

        ################################################################
        # Business Meaning
        ################################################################

        business_meaning = metric.metadata.get(
            "business_meaning",
            ""
        )

        ################################################################
        # Measurement Object
        ################################################################

        return MeasurementKnowledge(

            ################################################################
            # Detection
            ################################################################

            found=True,

            confidence=0.99,

            ################################################################
            # Metric
            ################################################################

            metric=metric.entity_id,

            metric_object=metric,

            canonical=metric.canonical,

            category=metric.category,

            ################################################################
            # Raw Measurement
            ################################################################

            value=result.get(
                "raw_value",
                ""
            ),

            numeric_value=float(
                result.get(
                    "numeric_value",
                    0.0
                )
            ),

            normalized_value=float(
                result.get(
                    "numeric_value",
                    0.0
                )
            ),

            unit=result.get(
                "unit",
                ""
            ),

            operator=result.get(
                "comparison_operator",
                ""
            ),

            ################################################################
            # Measurement Type
            ################################################################

            measurement_type=result.get(
                "measurement_type",
                "absolute"
            ),

            ################################################################
            # Change Detection
            ################################################################

            from_value=result.get(
                "from_value"
            ),

            to_value=result.get(
                "to_value"
            ),

            change_value=change_value,

            percent_change=result.get(
                "percent_change"
            ),

            comparison_operator=result.get(
                "comparison_operator",
                ""
            ),

            ################################################################
            # Direction
            ################################################################

            direction=direction,

            improvement=improvement,

            ################################################################
            # Business Meaning
            ################################################################

            effect=effect,

            business_meaning=business_meaning,

            ################################################################
            # Ontology
            ################################################################

            entity_id=metric.entity_id,

            entity_type="measurement",

            business_area=metric.business_area,

            impact_weight=metric.impact_weight,

            source=metric.source,

            metadata=metric.metadata,

        )

