"""
Enterprise Action Extractor
Enterprise V5

Responsibility
--------------
Convert action ontology matches into ActionKnowledge objects.

The extractor does NOT perform business reasoning.

Action semantics are obtained from the ontology/repository metadata.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)

from .generic_ontology_extractor import GenericOntologyExtractor


class ActionExtractor(
    GenericOntologyExtractor[ActionKnowledge]
):
    """
    Extracts action verbs from the actions ontology.

    Example:

        "Led the implementation of ISO 9001"

    produces an ActionKnowledge object representing
    the detected action.

    Business interpretation remains ontology-driven and
    reasoner-driven rather than being hard-coded here.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "actions"

    knowledge_class = ActionKnowledge

    entity_type = "action"

    ####################################################################
    # ACTION-SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate action-specific fields.

        Linguistic forms come from RepositoryEntity.

        Action classifications come from ontology metadata.

        The extractor does not infer business semantics.
        """

        base = entity.base or entity.canonical

        return {
            ################################################################
            # Linguistics
            ################################################################

            "base": base,

            "past": entity.past,

            "gerund": entity.gerund,

            "infinitive": base,

            ################################################################
            # Action classification
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
            # Parsing
            ################################################################

            "clause_candidate": metadata.get(
                "clause_candidate",
                True,
            ),
        }