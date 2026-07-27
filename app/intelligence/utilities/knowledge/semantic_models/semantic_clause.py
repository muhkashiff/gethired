"""
Semantic Clause

Represents one fully interpreted clause.

Every AI engine should consume SemanticClause
instead of rerunning extractors.
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

from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import (
    MetricKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import (
    MeasurementKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.modifier_models import (
    ModifierKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


@dataclass
class SemanticClause:

    text: str = ""

    normalized_text: str = ""

    index: int = 0

    parent_sentence: str = ""

    confidence: float = 0.0

    action: ActionKnowledge = field(default_factory=ActionKnowledge)

    object: ObjectKnowledge = field(default_factory=ObjectKnowledge)

    domain: DomainKnowledge = field(default_factory=DomainKnowledge)

    metric: MetricKnowledge = field(default_factory=MetricKnowledge)

    measurement: MeasurementKnowledge = field(default_factory=MeasurementKnowledge)

    modifiers: list[ModifierKnowledge] = field(default_factory=list)

    interpretation: KnowledgeInterpretation = field(
        default_factory=KnowledgeInterpretation
    )

    achievement: bool = False

    quantified: bool = False

    executive_signal: bool = False

    semantic_type: str = ""

    business_area: str = ""

    source: str = "resume"