from dataclasses import dataclass

from app.intelligence.utilities.knowledge.knowledge_models import KnowledgeDocument

from app.intelligence.utilities.knowledge.knowledge_graph.graph_document import (
    KnowledgeGraphDocument,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    KnowledgeProfile,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticResolution,
)

@dataclass
class PipelineResult:

    knowledge_document: KnowledgeDocument

    graph_document: KnowledgeGraphDocument

    knowledge_profile: KnowledgeProfile

    semantic_result: SemanticResolution 