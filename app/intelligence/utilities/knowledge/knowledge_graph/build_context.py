"""
Enterprise Build Context

Shared runtime context used by all graph builders.

Enterprise V7
"""

from dataclasses import dataclass
from typing import Optional

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph import KnowledgeGraph
from app.intelligence.utilities.knowledge.knowledge_models import KnowledgeFact


@dataclass
class BuildContext:

    graph: KnowledgeGraph

    fact: Optional[KnowledgeFact] = None