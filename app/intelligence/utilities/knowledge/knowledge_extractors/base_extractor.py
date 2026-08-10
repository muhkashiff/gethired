"""
Enterprise Base Extractor
Enterprise V5

Pipeline
--------
ExtractionRequest
    ↓
KnowledgeV5Pipeline
    ↓
List[MatchResult]
    ↓
BaseExtractor
    ↓
ExtractionResult[T]
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)

from .extraction_request import ExtractionRequest
from .extraction_result import ExtractionResult

T = TypeVar("T")


class KnowledgePipelineProtocol(Protocol):
    """
    Contract required from the knowledge pipeline.

    KnowledgeV5Pipeline already satisfies this contract because it has:
        run(ontology, sentence) -> list[MatchResult]
    """

    def run(
        self,
        ontology: str,
        sentence: str,
    ) -> list[MatchResult]:
        ...


class BaseExtractor(ABC, Generic[T]):
    """
    Abstract base for all resume extractors.

    Input:
        ExtractionRequest

    Output:
        ExtractionResult[T]

    A child extractor provides:
        1. Its ontology name.
        2. Its conversion from MatchResult to a domain object.
    """

    def __init__(
        self,
        ontology: str,
        pipeline: KnowledgePipelineProtocol,
    ) -> None:
        if not ontology or not ontology.strip():
            raise ValueError("Extractor ontology must not be empty.")

        if pipeline is None:
            raise ValueError("Extractor pipeline must not be None.")

        self._ontology = ontology
        self._pipeline = pipeline

    @property
    def ontology(self) -> str:
        return self._ontology

    def extract(
        self,
        request: ExtractionRequest,
    ) -> ExtractionResult[T]:
        """
        Extract domain entities from one request object.
        """
        if not isinstance(request, ExtractionRequest):
            raise TypeError(
                "request must be an ExtractionRequest object."
            )

        result = ExtractionResult[T](ontology=self.ontology)

        sentence = request.sentence.strip()

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

            if entity is not None:
                result.add(
                    match=match,
                    entity=entity,
                )

        return result

    def __call__(
        self,
        request: ExtractionRequest,
    ) -> ExtractionResult[T]:
        """
        Allows an extractor object to be called like a function.
        """
        return self.extract(request)

    def extract_first(
        self,
        request: ExtractionRequest,
    ) -> T | None:
        return self.extract(request).first

    def has_match(
        self,
        request: ExtractionRequest,
    ) -> bool:
        return self.extract(request).found

    def should_include(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> bool:
        """
        Optional child-class filtering hook.

        Override this when an extractor needs rules such as a minimum
        confidence, permitted category, or permitted business area.
        """
        return True

    @abstractmethod
    def build_entity(
        self,
        match: MatchResult,
        request: ExtractionRequest,
    ) -> T | None:
        """
        Convert a successful knowledge match into one domain object.

        Return None when the match must not produce an output entity.
        """
        raise NotImplementedError