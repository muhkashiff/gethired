"""
Enterprise Extraction Result
Enterprise V5

Every extractor returns this object.

Pipeline
--------
Sentence
    ↓
KnowledgeV5Pipeline
    ↓
List[MatchResult]
    ↓
BaseExtractor
    ↓
ExtractionResult
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, TypeVar

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import MatchResult

T = TypeVar("T")


@dataclass(slots=True)
class ExtractionResult(Generic[T]):

    ####################################################################
    # Identity
    ####################################################################

    ontology: str = ""

    ####################################################################
    # Pipeline Objects
    ####################################################################

    matches: list[MatchResult] = field(default_factory=list)

    entities: list[T] = field(default_factory=list)

    ####################################################################
    # Statistics
    ####################################################################

    @property
    def count(self) -> int:

        return len(self.entities)

    ####################################################################
    # Convenience
    ####################################################################

    @property
    def first(self):

        if self.entities:

            return self.entities[0]

        return None

    ####################################################################

    @property
    def found(self):

        return bool(self.entities)

    ####################################################################

    def add(

        self,

        match: MatchResult,

        entity: T,

    ):

        self.matches.append(match)

        self.entities.append(entity)

    ####################################################################

    def clear(self):

        self.matches.clear()

        self.entities.clear()

    ####################################################################

    def __len__(self):

        return len(self.entities)

    ####################################################################

    def __iter__(self):

        return iter(self.entities)

    ####################################################################

    def __getitem__(self, index):

        return self.entities[index]

    ####################################################################

    def __bool__(self):

        return self.found

    ####################################################################

    def __repr__(self):

        return (

            f"ExtractionResult("

            f"ontology='{self.ontology}', "

            f"count={self.count}"

            f")"

        )