"""
Enterprise Skill Parser Extractor
Enterprise V5

Responsibility
--------------

Convert skill MatchResult objects into SkillKnowledge objects.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.parsed_models.skills import (
    SkillParserModel,
)

from .generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)


class SkillParserExtractor(
    GenericOntologyParserExtractor[SkillParserModel]
):
    """
    Parses professional skills from the skills ontology.
    """

    # ==============================================================
    # CONFIGURATION
    # ==============================================================

    ontology_name = "skills"

    knowledge_class = SkillParserModel

    entity_type = "skill"

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


    # ==============================================================
    # SKILL-SPECIFIC FIELDS
    # ==============================================================

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to SkillKnowledge.
        """

        skill_type = str(
            metadata.get(
                "skill_type",
                "",
            )
        ).casefold()

        category = str(
            entity.category or ""
        ).casefold()

        return {

            "skill_family": metadata.get(
                "skill_family",
                "",
            ),

            "skill_group": metadata.get(
                "skill_group",
                "",
            ),

            "level": metadata.get(
                "level",
                "",
            ),

            "technical": metadata.get(
                "technical",
                skill_type == "technical",
            ),

            "managerial": metadata.get(
                "managerial",
                category in {
                    "management",
                    "leadership",
                },
            ),

            "analytical": metadata.get(
                "analytical",
                category == "analytical",
            ),

            "operational": metadata.get(
                "operational",
                category == "operations",
            ),

            "compliance": metadata.get(
                "compliance",
                category in {
                    "quality",
                    "food_safety",
                    "compliance",
                },
            ),

            "leadership": metadata.get(
                "leadership",
                category == "leadership",
            ),

            "communication": metadata.get(
                "communication",
                category == "communication",
            ),

            "transferable": metadata.get(
                "transferable",
                True,
            ),

            "certification_required": metadata.get(
                "certification_required",
                False,
            ),

            "years_required": metadata.get(
                "years_required",
                0.0,
            ),

            "ats_weight": metadata.get(
                "ats_weight",
                entity.impact_weight,
            ),

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),
        }