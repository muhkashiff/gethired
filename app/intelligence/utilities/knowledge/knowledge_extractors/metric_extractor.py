"""
Enterprise Metric Extractor

Generic Ontology Version

Enterprise V4
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)


class MetricExtractor(GenericOntologyExtractor):

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "metrics"

    knowledge_class = MetricKnowledge

    entity_type = "metric"

    ####################################################################
    # METRIC SPECIFIC FIELDS
    ####################################################################

    def extra_fields(

        self,

        entity,

        metadata,

    ):

        return {

            "preferred_direction": metadata.get(

                "preferred_direction",

                ""

            ),

            "positive_effect": metadata.get(

                "positive_effect",

                ""

            ),

            "business_meaning": metadata.get(

                "business_meaning",

                ""

            ),

            "measurement_type": metadata.get(

                "measurement_type",

                ""

            ),

            "unit": metadata.get(

                "unit",

                ""

            ),

            "polarity": metadata.get(

                "polarity",

                ""

            ),

            "impact": metadata.get(

                "impact",

                0.0,

            ),

            "financial_driver": metadata.get(

                "financial_driver",

                False,

            ),

            "operational_driver": metadata.get(

                "operational_driver",

                False,

            ),

        }