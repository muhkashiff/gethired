"""
Enterprise Action Knowledge Model

Represents an action detected in a sentence.

Examples

Implemented
Developed
Reduced
Improved
Led
Managed
Optimized
Designed
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class ActionKnowledge(KnowledgeEntity):

    ####################################################################
    # Linguistics
    ####################################################################

    entity_type: str = "action"

    ontology_name: str = "actions"

    base: str = ""

    gerund: str = ""

    past: str = ""

    infinitive: str = ""

    ####################################################################
    # Action Semantics
    ####################################################################

    action_family: str = ""

    action_group: str = ""

    business_verb: bool = True

    achievement_action: bool = False

    leadership_action: bool = False

    management_action: bool = False

    analytical_action: bool = False

    operational_action: bool = False

    ####################################################################
    # Parsing
    ####################################################################

    clause_candidate: bool = True