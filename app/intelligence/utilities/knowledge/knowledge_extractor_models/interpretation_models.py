"""
Knowledge Interpretation Model

Combines every extractor output into
one semantic interpretation.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.object_models import (
    ObjectKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)


@dataclass
class KnowledgeInterpretation:

    action: ActionKnowledge = field(default_factory=ActionKnowledge)

    object: ObjectKnowledge = field(default_factory=ObjectKnowledge)

    domain: DomainKnowledge = field(default_factory=DomainKnowledge)

    confidence: float = 0.0