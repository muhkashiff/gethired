"""
Semantic Sentence

Represents one parsed sentence.

A sentence contains one or more semantic clauses.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.semantic_models.semantic_clause import (
    SemanticClause,
)


@dataclass
class SemanticSentence:

    # ---------------------------------------------------------
    # Original text
    # ---------------------------------------------------------

    text: str = ""

    # ---------------------------------------------------------
    # Parsed clauses
    # ---------------------------------------------------------

    clauses: list[SemanticClause] = field(default_factory=list)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    confidence: float = 0.0

    sentence_index: int = 0

    metadata: dict = field(default_factory=dict)