from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ResumeKnowledgePipelineResult:
    """
    Complete extraction result produced by ResumeKnowledgePipeline.

    This object preserves both:

        KnowledgeFact[]
        MatchResult[]

    because downstream layers require different representations.
    """

    facts: list[Any] = field(
        default_factory=list
    )

    matches: list[Any] = field(
        default_factory=list
    )

    sentence_count: int = 0

    match_count: int = 0

    entity_count: int = 0

    confidence: float = 0.0

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def found(self) -> bool:
        return bool(
            self.matches
        )

    def summary(self) -> dict[str, Any]:

        return {
            "sentence_count": self.sentence_count,
            "match_count": self.match_count,
            "entity_count": self.entity_count,
            "confidence": self.confidence,
            "found": self.found,
        }