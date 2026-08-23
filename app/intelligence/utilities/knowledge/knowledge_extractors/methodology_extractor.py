"""
Enterprise Methodology Extractor
Enterprise V5

Reusable ontology extractor for methodology entities.

Flow:

Sentence
    ↓
ExtractionRequest
    ↓
GenericOntologyExtractor
    ↓
KnowledgeV5Pipeline
    ↓
MatchResult
    ↓
MethodologyKnowledge
    ↓
ExtractionResult[MethodologyKnowledge]
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractor_models.methodology_models import (
    MethodologyKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)


class MethodologyExtractor(
    GenericOntologyExtractor[MethodologyKnowledge]
):
    """
    Extract methodologies from the methodologies ontology.

    Examples:

    HACCP
    DMAIC
    PDCA
    Lean Manufacturing
    Six Sigma
    5S
    Root Cause Analysis
    Kaizen
    FMEA
    SPC
    """

    # ================================================================
    # CONFIGURATION
    # ================================================================

    ontology_name = "methodologies"

    knowledge_class = MethodologyKnowledge

    entity_type = "methodology"

    # ================================================================
    # METHODOLOGY-SPECIFIC FIELDS
    # ================================================================

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate methodology-specific fields from repository metadata.

        Common knowledge fields are handled by GenericOntologyExtractor.
        Only methodology-specific metadata is handled here.
        """

        return {

            # --------------------------------------------------------
            # Methodology definition
            # --------------------------------------------------------

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

            # --------------------------------------------------------
            # Classification
            # --------------------------------------------------------

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

            # --------------------------------------------------------
            # Enterprise
            # --------------------------------------------------------

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

            # --------------------------------------------------------
            # Knowledge graph
            # --------------------------------------------------------

            "graph_node": metadata.get(
                "graph_node",
                getattr(
                    entity,
                    "graph_node",
                    True,
                ),
            ),

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