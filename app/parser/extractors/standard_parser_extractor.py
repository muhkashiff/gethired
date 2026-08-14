"""
Enterprise Standard Parser Extractor

Enterprise V5

Responsibility
--------------
Convert standard ontology MatchResult objects into
StandardParserModel objects.

The extractor does not perform:

• matching
• overlap resolution
• ranking
• business reasoning
• deduplication

Those responsibilities belong to their respective pipeline stages.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.parsed_models.standard import (
    StandardParserModel,
)

from .generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)

class StandardParserExtractor(
    GenericOntologyParserExtractor[StandardParserModel]
):
    """
    Extract recognized standards from text.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "standards"

    knowledge_class = StandardParserModel

    entity_type = "standard"

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
    # STANDARD-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to StandardParserModel.

        Standard-specific information comes from ontology metadata.
        """

        return {
            "graph_node": metadata.get(
                "graph_node",
                True,
            ),
        }