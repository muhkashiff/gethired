"""
Semantic Document

Highest semantic representation of a resume,
job description or interview transcript.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.semantic_models.semantic_sentence import (
    SemanticSentence,
)


@dataclass
class SemanticDocument:

    sentences: list[SemanticSentence] = field(default_factory=list)

    statistics: dict = field(default_factory=dict)

    confidence: float = 0.0