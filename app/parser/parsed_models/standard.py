"""
Enterprise Standard Parser Model

Enterprise V5

Represents a standard detected by the parser layer.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base_parser_models import ParserModel


@dataclass
class StandardParserModel(ParserModel):

    ####################################################################
    # ENTITY
    ####################################################################

    entity_type: str = "standard"

    ontology_name: str = "standards"

    ####################################################################
    # KNOWLEDGE GRAPH
    ####################################################################

    graph_node: bool = True