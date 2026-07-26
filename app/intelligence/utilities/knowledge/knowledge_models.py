"""
Knowledge Models

Universal structured knowledge objects
used across every AI engine.
"""

from dataclasses import dataclass, field
from typing import Dict, List

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


# ---------------------------------------------------------
# Atomic Knowledge
# ---------------------------------------------------------

@dataclass
class KnowledgeFact:
    """
    Smallest reusable unit of knowledge.

    One resume bullet may produce one or more KnowledgeFacts.

    Example

    Led cross-functional teams and implemented FSSC22000.

    ↓

    KnowledgeFact 1

    Leadership

    KnowledgeFact 2

    Food Safety
    """

    text: str = ""

    interpretation: KnowledgeInterpretation = field(
        default_factory=KnowledgeInterpretation
    )

    achievement: bool = False

    quantified: bool = False

    source: str = "resume"

    confidence: float = 0.0


# ---------------------------------------------------------
# Parsed Sentence
# ---------------------------------------------------------

@dataclass
class KnowledgeSentence:
    """
    Represents one parsed sentence.

    A sentence can contain multiple KnowledgeFacts.
    """

    original_text: str = ""

    facts: List[KnowledgeFact] = field(default_factory=list)

    confidence: float = 0.0


# ---------------------------------------------------------
# Knowledge Collection
# ---------------------------------------------------------

@dataclass
class KnowledgeDocument:
    """
    Complete parsed document.

    Resume
    Job Description
    Interview Transcript
    Recruiter Notes

    All become KnowledgeDocuments.
    """

    sentences: List[KnowledgeSentence] = field(default_factory=list)

    facts: List[KnowledgeFact] = field(default_factory=list)

    statistics: Dict = field(default_factory=dict)

    confidence: float = 0.0