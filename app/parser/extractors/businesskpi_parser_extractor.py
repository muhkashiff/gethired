"""
Enterprise Business KPI Parser Extractor
Enterprise V5

Responsibility
--------------
Convert Business KPI ontology matches into
BusinessKPIParserModel objects.

Business reasoning is NOT performed here.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.parsed_models.businesskpi import (
    BusinessKPIParserModel,
)

from .generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)



class BusinessKPIParserExtractor(
    GenericOntologyParserExtractor[BusinessKPIParserModel]
):
    """
    Extracts Business KPI entities from the business_kpi ontology.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "business_kpis"

    knowledge_class = BusinessKPIParserModel

    entity_type = "business_kpi"

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
    # KPI-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate Business KPI specific parser fields.

        Values are taken directly from RepositoryEntity metadata.
        No business reasoning is performed here.
        """

        return {
            "description": getattr(
                entity,
                "description",
                "",
            ),

            "related_metrics": list(
                getattr(
                    entity,
                    "related_metrics",
                    [],
                )
                or []
            ),

            "higher_is_better": getattr(
                entity,
                "higher_is_better",
                True,
            ),

            "impact_weight": getattr(
                entity,
                "impact_weight",
                1.0,
            ),

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),
        }