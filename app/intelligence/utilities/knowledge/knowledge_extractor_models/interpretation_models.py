"""
Knowledge Interpretation Model

Semantic interpretation of one resume statement.

This object aggregates all extracted knowledge into a single
business interpretation used throughout the intelligence engine.
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import ActionKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.object_models import ObjectKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import DomainKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import MetricKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import MeasurementKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.modifier_models import ModifierKnowledge


@dataclass
class KnowledgeInterpretation:

    # ---------------------------------------------------------
    # Core Knowledge
    # ---------------------------------------------------------

    action: ActionKnowledge = field(default_factory=ActionKnowledge)

    object: ObjectKnowledge = field(default_factory=ObjectKnowledge)

    domain: DomainKnowledge = field(default_factory=DomainKnowledge)

    metric: MetricKnowledge = field(default_factory=MetricKnowledge)

    measurement: MeasurementKnowledge = field(default_factory=MeasurementKnowledge)

    modifiers: list[ModifierKnowledge] = field(default_factory=list)

    # ---------------------------------------------------------
    # Business Interpretation
    # ---------------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    semantic_type: str = ""

    business_area: str = ""

    # ---------------------------------------------------------
    # Intelligence
    # ---------------------------------------------------------

    confidence: float = 0.0

    overall_impact_weight: float = 1.0

    explanation: str = ""