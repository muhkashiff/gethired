"""
Semantic Document

Top-level semantic representation of a resume,
job description or any business document.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.semantic_models.semantic_sentence import (
    SemanticSentence,
)


@dataclass
class SemanticDocument:

    # ---------------------------------------------------------
    # Original document
    # ---------------------------------------------------------

    original_text: str = ""

    # ---------------------------------------------------------
    # Parsed sentences
    # ---------------------------------------------------------

    sentences: list[SemanticSentence] = field(default_factory=list)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    confidence: float = 0.0

    document_type: str = "resume"

    metadata: dict = field(default_factory=dict)