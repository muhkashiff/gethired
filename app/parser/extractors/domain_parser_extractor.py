from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.parser.extractors.generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)

from app.parser.parsed_models.domain import (
    DomainParserModel,
)


class DomainParserExtractor(
    GenericOntologyParserExtractor[DomainParserModel]
):
    """
    Enterprise V5 Domain Parser Extractor.

    Parser-layer extractor.

    Supports multiple domain entities from one sentence.
    """

    # ================================================================
    # CONFIGURATION
    # ================================================================

    ontology_name = "domains"

    knowledge_class = DomainParserModel

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

        return {

            # --------------------------------------------------------
            # Domain definition
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

            "strategic": bool(
                metadata.get(
                    "strategic",
                    getattr(
                        entity,
                        "strategic",
                        False,
                    ),
                )
            ),

            "operational": bool(
                metadata.get(
                    "operational",
                    getattr(
                        entity,
                        "operational",
                        False,
                    ),
                )
            ),

            "technical": bool(
                metadata.get(
                    "technical",
                    getattr(
                        entity,
                        "technical",
                        False,
                    ),
                )
            ),

            "compliance": bool(
                metadata.get(
                    "compliance",
                    getattr(
                        entity,
                        "compliance",
                        False,
                    ),
                )
            ),

            "management": bool(
                metadata.get(
                    "management",
                    getattr(
                        entity,
                        "management",
                        False,
                    ),
                )
            ),

            # --------------------------------------------------------
            # Enterprise
            # --------------------------------------------------------

            "enterprise_level": int(
                metadata.get(
                    "enterprise_level",
                    getattr(
                        entity,
                        "enterprise_level",
                        1,
                    ),
                )
                or 1
            ),

            "criticality": float(
                metadata.get(
                    "criticality",
                    getattr(
                        entity,
                        "criticality",
                        1.0,
                    ),
                )
                or 1.0
            ),

            # --------------------------------------------------------
            # Knowledge graph
            # --------------------------------------------------------

            "graph_node": bool(
                metadata.get(
                    "graph_node",
                    getattr(
                        entity,
                        "graph_node",
                        True,
                    ),
                )
            ),

            # --------------------------------------------------------
            # Compatibility fields
            # --------------------------------------------------------

            "reasoning_id": metadata.get(
                "reasoning_id",
                "",
            ),

            "reasoning_confidence": float(
                metadata.get(
                    "reasoning_confidence",
                    0.0,
                )
                or 0.0
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