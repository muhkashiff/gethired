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
# Knowledge Clause
# ---------------------------------------------------------

@dataclass
class KnowledgeClause:
    """
    Represents one semantic clause.

    Example

    Implemented ISO9001,
    trained staff,
    improved productivity.

    One sentence may contain multiple clauses.
    """

    original_text: str = ""

    facts: List[KnowledgeFact] = field(default_factory=list)

    confidence: float = 0.0


# ---------------------------------------------------------
# Parsed Sentence
# ---------------------------------------------------------

@dataclass
class KnowledgeSentence:
    """
    One parsed sentence.

    Contains one or more semantic clauses.
    """

    original_text: str = ""

    clauses: List[KnowledgeClause] = field(default_factory=list)

    facts: List[KnowledgeFact] = field(default_factory=list)

    confidence: float = 0.0


# ---------------------------------------------------------
# Knowledge Document
# ---------------------------------------------------------

@dataclass
class KnowledgeDocument:
    """
    Complete parsed document.

    Resume
    Job Description
    Interview
    Recruiter Notes

    Everything becomes a KnowledgeDocument.
    """

    sentences: List[KnowledgeSentence] = field(default_factory=list)

    # Flattened index of every fact
    facts: List[KnowledgeFact] = field(default_factory=list)

    statistics: Dict = field(default_factory=dict)

    confidence: float = 0.0