"""
Enterprise Domain Extractor

Enterprise V5

Extracts multiple domain entities from a sentence.

Architecture
------------

Sentence
    ↓
ExtractionRequest
    ↓
DomainExtractor
    ↓
GenericOntologyExtractor
    ↓
KnowledgeV5Pipeline
    ↓
MatchResult[]
    ↓
DomainKnowledge[]
    ↓
ExtractionResult[DomainKnowledge]

Important
---------

This is the KNOWLEDGE layer.

The output model is DomainKnowledge, NOT DomainParserModel.

The extractor supports MULTIPLE domains from one sentence.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractors.generic_ontology_extractor import (
    GenericOntologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)


class DomainExtractor(
    GenericOntologyExtractor[DomainKnowledge]
):
    """
    Extract multiple domains from professional text.
    """

    # ================================================================
    # CONFIGURATION
    # ================================================================

    ontology_name = "domains"

    knowledge_class = DomainKnowledge

    entity_type = "domain"

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

    # ================================================================
    # DOMAIN-SPECIFIC FIELDS
    # ================================================================

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate domain-specific fields.

        Generic fields are handled by GenericOntologyExtractor.
        """

        return {

            # --------------------------------------------------------
            # Domain Definition
            # --------------------------------------------------------

            "domain_family": metadata.get(
                "domain_family",
                getattr(
                    entity,
                    "domain_family",
                    "",
                ),
            ),

            "parent_domain": metadata.get(
                "parent_domain",
                getattr(
                    entity,
                    "parent_domain",
                    "",
                ),
            ),

            "business_function": metadata.get(
                "business_function",
                getattr(
                    entity,
                    "business_function",
                    "",
                ),
            ),

            # --------------------------------------------------------
            # Classification
            # --------------------------------------------------------

            "strategic": metadata.get(
                "strategic",
                getattr(
                    entity,
                    "strategic",
                    False,
                ),
            ),

            "operational": metadata.get(
                "operational",
                getattr(
                    entity,
                    "operational",
                    False,
                ),
            ),

            "technical": metadata.get(
                "technical",
                getattr(
                    entity,
                    "technical",
                    False,
                ),
            ),

            "compliance": metadata.get(
                "compliance",
                getattr(
                    entity,
                    "compliance",
                    False,
                ),
            ),

            "management": metadata.get(
                "management",
                getattr(
                    entity,
                    "management",
                    False,
                ),
            ),

            # --------------------------------------------------------
            # Enterprise
            # --------------------------------------------------------

            "enterprise_level": metadata.get(
                "enterprise_level",
                getattr(
                    entity,
                    "enterprise_level",
                    1,
                ),
            ),

            "criticality": metadata.get(
                "criticality",
                getattr(
                    entity,
                    "criticality",
                    1.0,
                ),
            ),

            # --------------------------------------------------------
            # Knowledge Graph
            # --------------------------------------------------------

            "graph_node": metadata.get(
                "graph_node",
                getattr(
                    entity,
                    "graph_node",
                    True,
                ),
            ),

            # --------------------------------------------------------
            # Reasoning compatibility
            # --------------------------------------------------------

            "reasoning_id": metadata.get(
                "reasoning_id",
                "",
            ),

            "reasoning_confidence": metadata.get(
                "reasoning_confidence",
                0.0,
            ),

            "primary_domain": metadata.get(
                "primary_domain",
                "",
            ),

            "secondary_domains": list(
                metadata.get(
                    "secondary_domains",
                    [],
                )
                or []
            ),

            "trigger_actions": list(
                metadata.get(
                    "trigger_actions",
                    [],
                )
                or []
            ),

            "trigger_objects": list(
                metadata.get(
                    "trigger_objects",
                    [],
                )
                or []
            ),

            "trigger_skills": list(
                metadata.get(
                    "trigger_skills",
                    [],
                )
                or []
            ),

            "trigger_metrics": list(
                metadata.get(
                    "trigger_metrics",
                    [],
                )
                or []
            ),

            "trigger_certifications": list(
                metadata.get(
                    "trigger_certifications",
                    [],
                )
                or []
            ),
        }