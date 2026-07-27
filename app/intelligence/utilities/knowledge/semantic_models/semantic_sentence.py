"""
Semantic Sentence
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.semantic_models.semantic_clause import (
    SemanticClause,
)


@dataclass
class SemanticSentence:

    original_text: str = ""

    clauses: list[SemanticClause] = field(default_factory=list)

    confidence: float = 0.0