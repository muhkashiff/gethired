"""
Knowledge Graph Document

Represents one complete graph extracted from
one resume.

This becomes the top-level object passed to:

• ATS Engine
• Resume Optimizer
• Interview Generator
• Executive Summary
• Career Intelligence
• Job Matching
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    KnowledgeGraph,
)

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
)


@dataclass
class KnowledgeGraphDocument:
    """
    Complete graph representation of one resume.
    """

    # -------------------------------------------------
    # Original Parsed Knowledge
    # -------------------------------------------------

    knowledge_document: KnowledgeDocument = field(
        default_factory=KnowledgeDocument
    )

    # -------------------------------------------------
    # Semantic Graph
    # -------------------------------------------------

    graph: KnowledgeGraph = field(
        default_factory=KnowledgeGraph
    )

    # -------------------------------------------------
    # Metadata
    # -------------------------------------------------

    source: str = "resume"

    version: str = "1.0"

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    statistics: dict = field(default_factory=dict)