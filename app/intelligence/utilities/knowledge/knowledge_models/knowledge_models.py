"""
Knowledge Models

Universal structured knowledge objects
used across every AI engine.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

from app.intelligence.utilities.knowledge.knowledge_dependency.dependency_models import (
    DependencyEdge,
)
from app.intelligence.utilities.knowledge.knowledge_extractor_models.practice_models import (
    PracticeKnowledge,
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

    # -----------------------------
    # NEW
    # -----------------------------

    dependency_edges: List[DependencyEdge] = field(default_factory=list)

    # -----------------------------
    # Existing
    # -----------------------------

    achievement: bool = False

    quantified: bool = False

    source: str = "resume"

    confidence: float = 0.0

    practice: PracticeKnowledge = field(default_factory=PracticeKnowledge)


# ---------------------------------------------------------
# Knowledge Clause
# ---------------------------------------------------------

@dataclass
class KnowledgeClause:
    """
    Represents one semantic clause.
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
    Master object passed through every AI layer.
    """

    # Original document

    raw_text: str = ""

    # NLP

    sentences: List[KnowledgeSentence] = field(default_factory=list)

    facts: List[KnowledgeFact] = field(default_factory=list)

    # Statistics

    statistics: Dict = field(default_factory=dict)

    confidence: float = 0.0

    #------------------------------
    # Standar 
    #------------------------------

    version: str = ""

    publisher: str = ""

    standard_type: str = ""


    # -----------------------------
    # Pipeline Objects
    # -----------------------------

    interpretation: Any = None

    graph: Any = None

    semantic_result: Any = None

    knowledge_profile: Any = None