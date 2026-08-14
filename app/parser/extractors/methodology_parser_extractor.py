"""
Enterprise Methodology Parser Extractor

Enterprise V5

Parser layer.

Architecture:

BaseParserExtractor
        ↓
GenericOntologyParserExtractor
        ↓
MethodologyParserExtractor
        ↓
MethodologyParserModel
"""

from __future__ import annotations

from app.parser.extractors.generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)

from app.parser.parsed_models.methodology import (
    MethodologyParserModel,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)


class MethodologyParserExtractor(
    GenericOntologyParserExtractor[MethodologyParserModel]
):
    """
    Parser extractor for methodologies.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "methodologies"

    knowledge_class = MethodologyParserModel

    # IMPORTANT:
    # This must match RepositoryEntity.entity_type.
    entity_type = "methodologie"

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
        metadata,
    ) -> dict:

        return {

            ################################################################
            # METHODOLOGY DEFINITION
            ################################################################

            "methodology_family": metadata.get(
                "methodology_family",
                getattr(
                    entity,
                    "methodology_family",
                    "",
                ),
            ),

            "methodology_group": metadata.get(
                "methodology_group",
                getattr(
                    entity,
                    "methodology_group",
                    "",
                ),
            ),

            "version": metadata.get(
                "version",
                getattr(
                    entity,
                    "version",
                    "",
                ),
            ),

            "abbreviation": metadata.get(
                "abbreviation",
                getattr(
                    entity,
                    "abbreviation",
                    "",
                ),
            ),

            ################################################################
            # CLASSIFICATION
            ################################################################

            "continuous_improvement": metadata.get(
                "continuous_improvement",
                getattr(
                    entity,
                    "continuous_improvement",
                    False,
                ),
            ),

            "quality_management": metadata.get(
                "quality_management",
                getattr(
                    entity,
                    "quality_management",
                    False,
                ),
            ),

            "food_safety": metadata.get(
                "food_safety",
                getattr(
                    entity,
                    "food_safety",
                    False,
                ),
            ),

            "risk_management": metadata.get(
                "risk_management",
                getattr(
                    entity,
                    "risk_management",
                    False,
                ),
            ),

            "analytical": metadata.get(
                "analytical",
                getattr(
                    entity,
                    "analytical",
                    False,
                ),
            ),

            "problem_solving": metadata.get(
                "problem_solving",
                getattr(
                    entity,
                    "problem_solving",
                    False,
                ),
            ),

            "statistical": metadata.get(
                "statistical",
                getattr(
                    entity,
                    "statistical",
                    False,
                ),
            ),

            ################################################################
            # ENTERPRISE
            ################################################################

            "certification_related": metadata.get(
                "certification_related",
                getattr(
                    entity,
                    "certification_related",
                    False,
                ),
            ),

            "implementation_required": metadata.get(
                "implementation_required",
                getattr(
                    entity,
                    "implementation_required",
                    False,
                ),
            ),

            "maturity_level": metadata.get(
                "maturity_level",
                getattr(
                    entity,
                    "maturity_level",
                    1,
                ),
            ),

            ################################################################
            # KNOWLEDGE GRAPH
            ################################################################

            "graph_node": metadata.get(
                "graph_node",
                getattr(
                    entity,
                    "graph_node",
                    True,
                ),
            ),

            ################################################################
            # ATS
            ################################################################

            "ats_weight": metadata.get(
                "ats_weight",
                getattr(
                    entity,
                    "ats_weight",
                    getattr(
                        entity,
                        "impact_weight",
                        1.0,
                    ),
                ),
            ),

        }