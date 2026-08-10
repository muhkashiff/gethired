"""
Enterprise Relation Extraction Result
Enterprise V5
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterator, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class RelationResult(Generic[T]):
    """
    Result produced by a relation extractor.
    """

    relations: list[T] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.relations)

    @property
    def first(self) -> T | None:
        if not self.relations:
            return None

        return self.relations[0]

    @property
    def found(self) -> bool:
        return bool(self.relations)

    def add(
        self,
        relation: T,
    ) -> None:
        self.relations.append(relation)

    def clear(self) -> None:
        self.relations.clear()

    def __len__(self) -> int:
        return len(self.relations)

    def __iter__(self) -> Iterator[T]:
        return iter(self.relations)

    def __getitem__(self, index: int) -> T:
        return self.relations[index]

    def __bool__(self) -> bool:
        return self.found