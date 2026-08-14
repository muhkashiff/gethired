
"""
Enterprise Certification Parser Extractor
Enterprise V5

Responsibility
--------------
Convert certification ontology MatchResult objects into
CertificationKnowledge objects.

Common ontology fields are populated by:
    GenericOntologyParserExtractor

Certification-specific fields are populated here
from RepositoryEntity metadata.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.parsed_models.certification import (
    CertificationParserModel,
)

from .generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)

class CertificationParserExtractor(
    GenericOntologyParserExtractor[CertificationParserModel]
):
    """
    Extracts certifications from the certifications ontology.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "certifications"

    knowledge_class = CertificationParserModel

    entity_type = "certification"

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
    # CERTIFICATION-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to CertificationKnowledge.

        All common fields are populated by the generic parser
        extractor.

        Certification-specific information comes from ontology
        metadata.
        """

        return {
            ################################################################
            # CERTIFICATION DEFINITION
            ################################################################

            "certification_family": metadata.get(
                "certification_family",
                "",
            ),

            "certification_group": metadata.get(
                "certification_group",
                "",
            ),

            "issuing_body": metadata.get(
                "issuing_body",
                "",
            ),

            "abbreviation": metadata.get(
                "abbreviation",
                entity.abbreviation,
            ),

            "version": metadata.get(
                "version",
                "",
            ),

            ################################################################
            # CLASSIFICATION
            ################################################################

            "professional": metadata.get(
                "professional",
                False,
            ),

            "regulatory": metadata.get(
                "regulatory",
                False,
            ),

            "food_safety": metadata.get(
                "food_safety",
                False,
            ),

            "quality_management": metadata.get(
                "quality_management",
                False,
            ),

            "project_management": metadata.get(
                "project_management",
                False,
            ),

            "cloud": metadata.get(
                "cloud",
                False,
            ),

            "analytics": metadata.get(
                "analytics",
                False,
            ),

            ################################################################
            # VALIDITY
            ################################################################

            "renewable": metadata.get(
                "renewable",
                False,
            ),

            "validity_years": metadata.get(
                "validity_years",
                0,
            ),

            "examination_required": metadata.get(
                "examination_required",
                False,
            ),

            ################################################################
            # ENTERPRISE
            ################################################################

            "globally_recognized": metadata.get(
                "globally_recognized",
                False,
            ),

            "maturity_level": metadata.get(
                "maturity_level",
                1,
            ),

            ################################################################
            # KNOWLEDGE GRAPH
            ################################################################

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),

            ################################################################
            # ATS
            ################################################################

            "ats_weight": metadata.get(
                "ats_weight",
                entity.impact_weight,
            ),
        }
