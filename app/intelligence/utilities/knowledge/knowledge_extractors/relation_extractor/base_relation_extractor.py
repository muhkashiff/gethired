"""
Enterprise Base Relation Extractor
Enterprise V5

Responsibility
--------------
Determine semantic relationships between already extracted
knowledge objects.

Input:
    RelationRequest

Output:
    RelationResult[T]

The extractor does not perform ontology extraction itself.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .relation_request import RelationRequest
from .relation_result import RelationResult


T = TypeVar("T")


class BaseRelationExtractor(ABC, Generic[T]):
    """
    Abstract base for all relation extractors.
    """

    def extract(
        self,
        request: RelationRequest,
    ) -> RelationResult[T]:
        """
        Extract relations from one typed request.
        """

        if not isinstance(
            request,
            RelationRequest,
        ):
            raise TypeError(
                "request must be a RelationRequest object."
            )

        result = RelationResult[T]()

        if not request.sentence.strip():
            return result

        if not self.should_extract(request):
            return result

        relation = self.build_relation(request)

        if relation is not None:
            result.add(relation)

        return result

    def __call__(
        self,
        request: RelationRequest,
    ) -> RelationResult[T]:
        return self.extract(request)

    def should_extract(
        self,
        request: RelationRequest,
    ) -> bool:
        return True

    @abstractmethod
    def build_relation(
        self,
        request: RelationRequest,
    ) -> T | None:
        raise NotImplementedError