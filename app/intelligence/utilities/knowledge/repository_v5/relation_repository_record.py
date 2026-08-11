"""
Enterprise Relation Repository Record

Enterprise V5

Represents one relationship stored in the repository.

This is repository data.

It is NOT the extraction result.

Repository:
    RelationRepositoryRecord

Extraction:
    RelationKnowledge
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RelationRepositoryRecord:

    ####################################################################
    # IDENTITY
    ####################################################################

    relation_id: str = ""

    relation_type: str = ""

    ####################################################################
    # GRAPH ENDPOINTS
    ####################################################################

    source: str = ""

    target: str = ""

    ####################################################################
    # SEMANTIC
    ####################################################################

    weight: float = 1.0

    description: str = ""

    ####################################################################
    # REPOSITORY CONTROL
    ####################################################################

    searchable: bool = True

    active: bool = True

    source_name: str = "relations"

    ####################################################################
    # METADATA
    ####################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict
    )