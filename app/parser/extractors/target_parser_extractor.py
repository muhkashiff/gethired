"""
Enterprise Target Parser Extractor

Enterprise V5

Parser layer.

Architecture:

BaseParserExtractor
        ↓
GenericOntologyParserExtractor
        ↓
TargetParserExtractor
        ↓
TargetParserModel
"""

from __future__ import annotations

from app.parser.extractors.generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)

from app.parser.parsed_models.target import (
    TargetParserModel,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)


class TargetParserExtractor(
    GenericOntologyParserExtractor[TargetParserModel]
):
    """
    Parser extractor for enterprise targets.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "targets"

    knowledge_class = TargetParserModel

    entity_type = "target"

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
    # TARGET-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity,
        metadata,
    ) -> dict:

        return {

            ################################################################
            # TARGET OBJECT
            ################################################################

            "object_family": metadata.get(
                "object_family",
                "",
            ),

            "object_group": metadata.get(
                "object_group",
                "",
            ),

            "tangible": metadata.get(
                "tangible",
                False,
            ),

            "intangible": metadata.get(
                "intangible",
                False,
            ),

            "measurable": metadata.get(
                "measurable",
                False,
            ),

            "critical": metadata.get(
                "critical",
                False,
            ),

            ################################################################
            # CLASSIFICATION
            ################################################################

            "lifecycle": metadata.get(
                "lifecycle",
                "",
            ),

            "ownership": metadata.get(
                "ownership",
                "",
            ),

            "parent_object": metadata.get(
                "parent_object",
                "",
            ),

            ################################################################
            # PARSING
            ################################################################

            "role": metadata.get(
                "role",
                "",
            ),

            ################################################################
            # GRAPH
            ################################################################

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),

        }