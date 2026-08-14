# Base Non-Ontology Extractor

"""
GetHired
Enterprise V5

Base extractor for non-ontology resume extraction.

Non-ontology extractors work directly on parsed resume
section content and do NOT interact with the ontology
knowledge pipeline.

Examples:
    ContactExtractor
    ExperienceExtractor
    EducationExtractor
    LanguageExtractor
    ProjectExtractor
    AwardExtractor
    ReferenceExtractor
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseNonOntologyExtractor(ABC):
    """
    Base class for traditional structured resume extraction.

    Input:
        list[str]
        or compatible iterable of section content.

    Output:
        Structured Python objects / dictionaries depending
        on the concrete extractor.
    """

    def extract(self, content: Any):
        """
        Public extraction method.

        Performs basic input normalization and delegates
        actual extraction to the concrete implementation.
        """

        if content is None:
            return self.empty_result()

        if isinstance(content, str):
            content = [content]

        content = list(content)

        if not content:
            return self.empty_result()

        return self._extract(content)

    @abstractmethod
    def _extract(self, content: list[str]):
        """
        Concrete extractor implementation.
        """

        raise NotImplementedError

    def empty_result(self):
        """
        Default empty result.

        Child classes may override this when their natural
        empty value is different.
        """

        return []

