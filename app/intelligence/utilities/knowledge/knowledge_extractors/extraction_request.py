"""
Enterprise Extraction Request
Enterprise V5

Object input for every knowledge extractor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ExtractionRequest:
    """
    Input object passed to an extractor.

    Attributes:
        sentence:
            The text to analyze.

        context:
            Optional supporting data for future use, such as resume section,
            job description details, parser information, or candidate data.
    """

    sentence: str

    context: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if not isinstance(self.sentence, str):
            raise TypeError(
                "sentence must be a string."
            )