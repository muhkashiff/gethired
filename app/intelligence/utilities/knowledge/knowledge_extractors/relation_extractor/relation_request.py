"""
Enterprise Relation Extraction Request
Enterprise V5
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


TSource = TypeVar("TSource")
TTarget = TypeVar("TTarget")


@dataclass(frozen=True, slots=True)
class RelationRequest(Generic[TSource, TTarget]):
    """
    Typed input for relation extraction.

    The relation extractor receives already extracted
    knowledge objects and determines whether a semantic
    relationship exists between them.
    """

    source: TSource

    target: TTarget

    sentence: str

    sentence_index: int = 0

    start_char: int = -1

    end_char: int = -1