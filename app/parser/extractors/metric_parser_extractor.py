"""
Enterprise Metric Parser Extractor

Enterprise V5

Parser layer.

Architecture:

BaseParserExtractor
        ↓
GenericOntologyParserExtractor
        ↓
MetricParserExtractor
        ↓
MetricParserModel
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.extractors.generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)

from app.parser.parsed_models.metrics import (
    MetricParserModel,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)


class MetricParserExtractor(
    GenericOntologyParserExtractor[MetricParserModel]
):
    """
    Parser extractor for business metrics.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "metrics"

    knowledge_class = MetricParserModel

    entity_type = "metric"

    # ================================================================
    # INITIALIZATION
    # ================================================================
    
    def __init__(
            self,
            pipeline: KnowledgeV5Pipeline | None = None,
        ) -> None:
    
            if pipeline is None:
                pipeline = KnowledgeV5Pipeline()
    
            super().__init__(
                pipeline=pipeline
            )
    ####################################################################
    # EXTRA FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity,
        metadata: Mapping[str, Any],
    ) -> dict:

        return {

            ################################################################
            # METRIC DEFINITION
            ################################################################

            "metric_family": metadata.get(
                "metric_family",
                "",
            ),

            "metric_group": metadata.get(
                "metric_group",
                "",
            ),

            # ------------------------------------------------------------
            # UNIT IS A FIRST-CLASS RepositoryEntity SEMANTIC FIELD ONLY
            # IF preferred_unit is used by repository.
            #
            # Your metric JSON currently uses "unit", which is NOT in
            # RepositoryEntity, so it is preserved in metadata.
            # ------------------------------------------------------------

            "unit": metadata.get(
                "unit",
                "",
            ),

            ################################################################
            # BEHAVIOUR
            ################################################################

            # These are FIRST-CLASS RepositoryEntity fields.
            # Do NOT read them from metadata.

            "higher_is_better": bool(
                entity.higher_is_better
            ),

            "lower_is_better": not bool(
                entity.higher_is_better
            ),

            ################################################################
            # METRIC TYPE
            ################################################################

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

            ################################################################
            # BUSINESS
            ################################################################

            "kpi": metadata.get(
                "kpi",
                False,
            ),

            "benchmark_available": metadata.get(
                "benchmark_available",
                False,
            ),

            "target_value": metadata.get(
                "target_value",
                0.0,
            ),

            ################################################################
            # MEASUREMENT
            ################################################################

            "measurement_expected": metadata.get(
                "measurement_expected",
                True,
            ),

            ################################################################
            # IMPACT
            ################################################################

            # FIRST-CLASS RepositoryEntity field.
            "impact_weight": entity.impact_weight,

            ################################################################
            # SOURCE
            ################################################################

            # FIRST-CLASS RepositoryEntity field.
            "source": entity.source,

            ################################################################
            # DESCRIPTION
            ################################################################

            # FIRST-CLASS RepositoryEntity field.
            "description": entity.description,

            ################################################################
            # GRAPH
            ################################################################

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),
        }