"""
Enterprise Action Parser Knowledge Model

Enterprise V5

Represents an action detected by the ontology parser.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base_parser_models import ParserModel


@dataclass
class ActionParserModel(ParserModel):

    ####################################################################
    # ENTITY
    ####################################################################

    entity_type: str = "action"

    ontology_name: str = "actions"

    ####################################################################
    # LINGUISTICS
    ####################################################################

    base: str = ""

    past: str = ""

    gerund: str = ""

    infinitive: str = ""

    ####################################################################
    # ACTION SEMANTICS
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
    # PARSING
    ####################################################################

    clause_candidate: bool = True