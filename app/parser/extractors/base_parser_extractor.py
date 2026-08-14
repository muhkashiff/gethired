"""
Enterprise Base Extractor
Enterprise V5
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import ExtractionRequest
from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_result import ExtractionResult


T = TypeVar("T")


class KnowledgePipelineProtocol(Protocol):

    def run(
        self,
        ontology: str,
        sentence: str,
    ) -> list[MatchResult]:
        ...


class BaseParserExtractor(
    ABC,
    Generic[T],
):
    """
    Abstract base for every extractor/parser.

    Responsibility:

        ExtractionRequest
                ↓
        Knowledge Pipeline
                ↓
        MatchResult
                ↓
        Domain Knowledge Object
                ↓
        ExtractionResult[T]
    """

    def __init__(
        self,
        ontology: str,
        pipeline: KnowledgePipelineProtocol,
    ) -> None:

        if not ontology or not ontology.strip():
            raise ValueError(
                "Extractor ontology must not be empty."
            )

        if pipeline is None:
            raise ValueError(
                "Extractor pipeline must not be None."
            )

        self._ontology = ontology
        self._pipeline = pipeline

    # ==============================================================
    # ONTOLOGY
    # ==============================================================

    @property
    def ontology(self) -> str:
        return self._ontology

    # ==============================================================
    # EXTRACT
    # ==============================================================

    def extract(
        self,
        request: ExtractionRequest,
    ) -> ExtractionResult[T]:

        if not isinstance(
            request,
            ExtractionRequest,
        ):
            raise TypeError(
                "request must be an ExtractionRequest object."
            )

        result = ExtractionResult[T](
            ontology=self.ontology
        )

        sentence = (
            request.sentence.strip()
        )

        if not sentence:
            return result

        matches = self._pipeline.run(
            ontology=self.ontology,
            sentence=sentence,
        )

        for match in matches:

            if not self.should_include(
                match=match,
                request=request,
            ):
                continue

            entity = self.build_entity(
                match=match,
                request=request,
            )

            if entity is None:
                continue

            result.add(
                match=match,
                entity=entity,
            )

        return result

    # ==============================================================
    # CALLABLE
    # ==============================================================

    def __call__(
        self,
        request: ExtractionRequest,
    ) -> ExtractionResult[T]:

        return self.extract(request)

    # ==============================================================
    # FIRST
    # ==============================================================

    def extract_first(
        self,
        request: ExtractionRequest,
    ) -> T | None:

        return self.extract(
            request
        ).first

    # ==============================================================
    # HAS MATCH
    # ==============================================================

    def has_match(
        self,
        request: ExtractionRequest,
    ) -> bool:

        return self.extract(
            request
        ).found

    # ==============================================================
    # FILTER HOOK
    # ==============================================================

    def should_include(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> bool:

        return True

    # ==============================================================
    # ENTITY BUILDER
    # ==============================================================

    @abstractmethod
    def build_entity(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> T | None:
        raise NotImplementedError