"""
Enterprise Measurement Extractor

Uses MeasurementParser
Repository Compatible
Enterprise V3
"""

from app.intelligence.utilities.knowledge.repository.repository import Repository

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

        ##############################################################
        # Metric must exist
        ##############################################################

        if metric is None:

            return MeasurementKnowledge()

        if not metric.found:

            return MeasurementKnowledge()

        ##############################################################

        result = self.parser.parse(

            sentence

        )

        if result is None:

            return MeasurementKnowledge()

        ##############################################################
        # Direction
        ##############################################################

        direction = metric.metadata.get(

            "preferred_direction",

            ""

        )

        ##############################################################
        # Effect
        ##############################################################

        effect = metric.metadata.get(

            "positive_effect",

            ""

        )

        ##############################################################
        # Meaning
        ##############################################################

        business_meaning = metric.metadata.get(

            "business_meaning",

            ""

        )

        ##############################################################

        return MeasurementKnowledge(

            ##########################################################
            # Detection
            ##########################################################

            found=True,

            confidence=0.99,

            ##########################################################
            # Metric
            ##########################################################

            metric=metric.entity_id,

            metric_object=metric,

            canonical=metric.canonical,

            category=metric.category,

            ##########################################################
            # Raw Measurement
            ##########################################################

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

            ##########################################################
            # Advanced
            ##########################################################

            measurement_type=result.get(

                "measurement_type",

                "absolute"

            ),

            from_value=result.get(

                "from_value"

            ),

            to_value=result.get(

                "to_value"

            ),

            change_value=result.get(

                "change_value"

            ),

            percent_change=result.get(

                "percent_change"

            ),

            comparison_operator=result.get(

                "comparison_operator",

                ""

            ),

            ##########################################################
            # Business
            ##########################################################

            direction=direction,

            effect=effect,

            business_meaning=business_meaning,

            ##########################################################
            # Ontology
            ##########################################################

            entity_id=metric.entity_id,

            entity_type="measurement",

            business_area=metric.business_area,

            impact_weight=metric.impact_weight,

            source=metric.source,

            metadata=metric.metadata,

        )