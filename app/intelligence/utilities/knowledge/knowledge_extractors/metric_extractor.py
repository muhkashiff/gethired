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

            ########################################################
            # Metric Definition
            ########################################################

            "metric_family": metadata.get(
                "metric_family",
                "",
            ),

            "metric_group": metadata.get(
                "metric_group",
                "",
            ),

            "unit": metadata.get(
                "unit",
                "",
            ),

            ########################################################
            # Behaviour
            ########################################################

            "higher_is_better": metadata.get(
                "higher_is_better",
                True,
            ),

            "lower_is_better": metadata.get(
                "lower_is_better",
                False,
            ),

            "percentage_metric": metadata.get(
                "percentage_metric",
                False,
            ),

            "financial_metric": metadata.get(
                "financial_metric",
                False,
            ),

            "quality_metric": metadata.get(
                "quality_metric",
                False,
            ),

            "productivity_metric": metadata.get(
                "productivity_metric",
                False,
            ),

            "operational_metric": metadata.get(
                "operational_metric",
                False,
            ),

            ########################################################
            # Business
            ########################################################

            "kpi": metadata.get(
                "kpi",
                False,
            ),

            "benchmark_available": metadata.get(
                "benchmark_available",
                False,
            ),

            "target_value": float(
                metadata.get(
                    "target_value",
                    0.0,
                )
            ),

            ########################################################
            # Parsing
            ########################################################

            "measurement_expected": metadata.get(
                "measurement_expected",
                True,
            ),
        }