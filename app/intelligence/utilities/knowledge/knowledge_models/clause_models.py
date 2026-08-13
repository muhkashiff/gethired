"""
Clause Models

Represents one semantic clause extracted from a sentence.

Sentence
    ↓
Clause
    ↓
Facts
"""

from dataclasses import dataclass, field
from typing import List

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import ActionKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.target_models import TargetKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import DomainKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.metric_models import MetricKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.measurement_models import MeasurementKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.modifier_models import ModifierKnowledge
from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import KnowledgeInterpretation
from app.intelligence.utilities.knowledge.knowledge_models import KnowledgeFact


@dataclass
class Clause:

    # --------------------------------------------------
    # Original Text
    # --------------------------------------------------

    text: str = ""

    normalized_text: str = ""

    original_text: str = ""

    parent_sentence: str = ""

    index: int = 0

    # --------------------------------------------------
    # Clause Metadata
    # --------------------------------------------------

    connector: str = ""

    clause_type: str = "independent"

    is_independent: bool = True

    confidence: float = 0.0

    source: str = "resume"

    # --------------------------------------------------
    # Semantic Knowledge
    # --------------------------------------------------

    action: ActionKnowledge = field(default_factory=ActionKnowledge)

    target: TargetKnowledge = field(default_factory=TargetKnowledge)

    domain: DomainKnowledge = field(default_factory=DomainKnowledge)

    metric: MetricKnowledge = field(default_factory=MetricKnowledge)

    measurement: MeasurementKnowledge = field(default_factory=MeasurementKnowledge)

    modifiers: List[ModifierKnowledge] = field(default_factory=list)

    interpretation: KnowledgeInterpretation = field(default_factory=KnowledgeInterpretation)

    # --------------------------------------------------
    # Facts
    # --------------------------------------------------

    facts: List[KnowledgeFact] = field(default_factory=list)

    # --------------------------------------------------
    # Intelligence Flags
    # --------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    executive_signal: bool = False

    semantic_type: str = ""

    business_area: str = ""