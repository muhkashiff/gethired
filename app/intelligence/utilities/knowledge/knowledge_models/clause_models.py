"""
Clause Models

A Clause is the smallest semantic unit
that represents one complete achievement,
responsibility or accomplishment.

Every clause owns its own semantic knowledge.

Sentence
    ↓
Clause
    ↓
Knowledge
"""

from dataclasses import dataclass, field
from typing import List

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
class Clause:

    # ---------------------------------------------
    # Original text
    # ---------------------------------------------

    text: str = ""

    normalized_text: str = ""

    parent_sentence: str = ""

    index: int = 0

    connector: str = ""

    is_independent: bool = True

    confidence: float = 0.0

    # ---------------------------------------------
    # Semantic Knowledge
    # ---------------------------------------------

    action: ActionKnowledge = field(
        default_factory=ActionKnowledge
    )

    object: ObjectKnowledge = field(
        default_factory=ObjectKnowledge
    )

    domain: DomainKnowledge = field(
        default_factory=DomainKnowledge
    )

    metric: MetricKnowledge = field(
        default_factory=MetricKnowledge
    )

    measurement: MeasurementKnowledge = field(
        default_factory=MeasurementKnowledge
    )

    modifiers: List[ModifierKnowledge] = field(
        default_factory=list
    )

    interpretation: KnowledgeInterpretation = field(
        default_factory=KnowledgeInterpretation
    )

    # ---------------------------------------------
    # Semantic Flags
    # ---------------------------------------------

    achievement: bool = False

    quantified: bool = False

    executive_signal: bool = False

    semantic_type: str = ""

    business_area: str = ""

    source: str = "resume"