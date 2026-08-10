"""
Enterprise Extraction Result
Enterprise V5

Every extractor returns this object.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)

T = TypeVar("T")


@dataclass(slots=True)
class ExtractionResult(Generic[T]):
    """
    Immutable-by-convention result produced by an extractor.

    Each entity is stored alongside the MatchResult that produced it.
    """

    ontology: str = ""

    matches: list[MatchResult] = field(default_factory=list)

    entities: list[T] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.entities)

    @property
    def first(self) -> T | None:
        if not self.entities:
            return None

        return self.entities[0]

    @property
    def found(self) -> bool:
        return bool(self.entities)

    def add(
        self,
        match: MatchResult,
        entity: T,
    ) -> None:
        self.matches.append(match)
        self.entities.append(entity)

    def clear(self) -> None:
        self.matches.clear()
        self.entities.clear()

    def __len__(self) -> int:
        return len(self.entities)

    def __iter__(self):
        return iter(self.entities)

    def __getitem__(self, index: int) -> T:
        return self.entities[index]

    def __bool__(self) -> bool:
        return self.found

    def __repr__(self) -> str:
        return (
            f"ExtractionResult("
            f"ontology='{self.ontology}', "
            f"count={self.count}"
            f")"
        )