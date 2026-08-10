"""
Enterprise Skills Extractor
Enterprise V5

Responsibility
--------------
Convert skill MatchResult objects into SkillKnowledge objects.

Pipeline:

ExtractionRequest
        ↓
KnowledgeV5Pipeline
        ↓
MatchResult
        ↓
SkillsExtractor
        ↓
SkillKnowledge
        ↓
ExtractionResult[SkillKnowledge]
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractor_models.skill_models import (
    SkillKnowledge,
)

from .generic_ontology_extractor import GenericOntologyExtractor


class SkillsExtractor(
    GenericOntologyExtractor[SkillKnowledge]
):
    """
    Extracts professional skills from the skills ontology.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "skills"

    knowledge_class = SkillKnowledge

    entity_type = "skill"

    ####################################################################
    # SKILL-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to SkillKnowledge.

        Repository metadata is used as the source of enterprise
        skill classification.
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