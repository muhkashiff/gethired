"""
Enterprise Actions Parser Extractor

Enterprise V5

Responsibility
--------------
Convert action ontology MatchResult objects into
ActionParserKnowledge objects.

The extractor does NOT perform business reasoning.

Action semantics are obtained from repository metadata.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.parsed_models.actions import (
    ActionParserModel,
)

from .generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)

class ActionsParserExtractor(
    GenericOntologyParserExtractor[ActionParserModel]
):
    """
    Extracts action verbs from the actions ontology.

    Example:

        "Led the implementation of ISO 9001"

    produces an ActionParserKnowledge object representing
    the detected action.

    Business interpretation remains ontology-driven and
    reasoner-driven rather than being hard-coded here.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "actions"

    knowledge_class = ActionParserModel

    entity_type = "action"

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
    # ACTION-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate fields specific to ActionParserKnowledge.

        Common repository fields such as:

            canonical
            normalized
            base
            past
            gerund
            category
            business_area
            impact_weight
            entity_id

        are populated by GenericOntologyParserExtractor.

        Only action-specific fields are populated here.
        """

        base = (
            entity.base
            or entity.canonical
        )

        return {

            ################################################################
            # LINGUISTIC PARSER FIELD
            ################################################################

            "infinitive": base,

            ################################################################
            # ACTION CLASSIFICATION
            ################################################################

            "action_family": metadata.get(
                "action_family",
                "",
            ),

            "action_group": metadata.get(
                "action_group",
                "",
            ),

            "business_verb": metadata.get(
                "business_verb",
                True,
            ),

            "achievement_action": metadata.get(
                "achievement_action",
                False,
            ),

            "leadership_action": metadata.get(
                "leadership_action",
                False,
            ),

            "management_action": metadata.get(
                "management_action",
                False,
            ),

            "analytical_action": metadata.get(
                "analytical_action",
                False,
            ),

            "operational_action": metadata.get(
                "operational_action",
                False,
            ),

            ################################################################
            # PARSING
            ################################################################

            "clause_candidate": metadata.get(
                "clause_candidate",
                True,
            ),
        }