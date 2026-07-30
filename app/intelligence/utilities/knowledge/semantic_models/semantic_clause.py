"""
Semantic Clause

Represents one semantic clause extracted from a sentence.

Example

Implemented ISO 9001 using Lean Manufacturing.

A sentence may contain multiple clauses.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.entity_models import (
    KnowledgeEntity,
)

from app.intelligence.utilities.knowledge.knowledge_dependency.dependency_models import (
    DependencyEdge,
)


@dataclass
class SemanticClause:

    # ---------------------------------------------------------
    # Original text
    # ---------------------------------------------------------

    text: str = ""

    # ---------------------------------------------------------
    # Parsed knowledge
    # ---------------------------------------------------------

    facts: list[KnowledgeFact] = field(default_factory=list)

    entities: list[KnowledgeEntity] = field(default_factory=list)

    dependencies: list[DependencyEdge] = field(default_factory=list)

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    confidence: float = 0.0

    clause_index: int = 0

    source: str = "resume"

    metadata: dict = field(default_factory=dict)