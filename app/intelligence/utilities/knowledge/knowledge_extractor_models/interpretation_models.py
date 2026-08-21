"""
Knowledge Interpretation Model

Enterprise V13

Semantic interpretation of one resume knowledge fact.

Architecture
------------

KnowledgeFact
    ↓
KnowledgeInterpretation
    ↓
KnowledgeEntity objects
    ↓
BusinessStatementBuilder
    ↓
KnowledgeGraphBuilder
    ↓
KnowledgeProfile

Responsibilities
----------------
• Aggregate extracted knowledge for one KnowledgeFact
• Hold typed ontology knowledge
• Hold generic KnowledgeEntity objects
• Preserve achievement / quantified information
• Preserve business interpretation
• Provide confidence and impact information

This model does NOT:
• perform extraction
• perform ontology matching
• build BusinessStatements
• build KnowledgeGraph
• calculate profile scores
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.target_models import (
    TargetKnowledge,
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

from app.intelligence.utilities.knowledge.knowledge_extractor_models.practice_models import (
    PracticeKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


@dataclass
class KnowledgeInterpretation:
    """
    Semantic interpretation of one KnowledgeFact.

    This is the bridge between ontology extraction and
    BusinessStatementBuilder.

    Every KnowledgeFact should contain one interpretation.

    Entity storage
    --------------

    `entities` is the canonical entity collection.

    `semantic_entities` is provided as a compatibility alias
    because the Enterprise KnowledgeFact model accesses resolved
    entities using that terminology.

    No second entity collection is maintained.
    """

    # ==========================================================
    # CORE KNOWLEDGE
    # ==========================================================

    action: ActionKnowledge = field(
        default_factory=ActionKnowledge
    )

    target: TargetKnowledge = field(
        default_factory=TargetKnowledge
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

    modifiers: list[ModifierKnowledge] = field(
        default_factory=list
    )

    practice: PracticeKnowledge = field(
        default_factory=PracticeKnowledge
    )

    # ==========================================================
    # UNIVERSAL ENTITIES
    # ==========================================================

    entities: list[KnowledgeEntity] = field(
        default_factory=list
    )

    # ==========================================================
    # BUSINESS INTERPRETATION
    # ==========================================================

    achievement: bool = False

    quantified: bool = False

    semantic_type: str = ""

    business_area: str = ""

    primary_domain: str = ""

    # ==========================================================
    # INTELLIGENCE
    # ==========================================================

    confidence: float = 0.0

    overall_impact_weight: float = 1.0

    explanation: str = ""

    # ==========================================================
    # CONVENIENCE
    # ==========================================================

    @property
    def entity_count(
        self,
    ) -> int:
        """
        Number of universal KnowledgeEntity objects.
        """

        return len(
            self.entities
        )

    @property
    def has_entities(
        self,
    ) -> bool:
        """
        True when at least one KnowledgeEntity exists.

        This is the canonical entity-presence check.
        """

        return bool(
            self.entities
        )

    # ==========================================================
    # SEMANTIC ENTITY COMPATIBILITY
    # ==========================================================

    @property
    def semantic_entities(
        self,
    ) -> list[KnowledgeEntity]:
        """
        Compatibility alias for semantic entities.

        `entities` remains the canonical storage collection.

        The Enterprise KnowledgeFact model expects:

            interpretation.semantic_entities

        Therefore this property exposes the same underlying
        collection without creating a second source of truth.
        """

        return self.entities

    @property
    def semantic_entity_count(
        self,
    ) -> int:
        """
        Number of semantic entities.

        This is intentionally derived from the canonical
        `entities` collection.
        """

        return len(
            self.entities
        )

    @property
    def has_semantic_entities(
        self,
    ) -> bool:
        """
        True when semantic entities are available.
        """

        return bool(
            self.entities
        )

    # ==========================================================
    # TYPED KNOWLEDGE FLAGS
    # ==========================================================

    @property
    def has_action(
        self,
    ) -> bool:
        """
        True when an action was detected.
        """

        return bool(
            getattr(
                self.action,
                "found",
                False,
            )
        )

    @property
    def has_target(
        self,
    ) -> bool:
        """
        True when a target was detected.
        """

        return bool(
            getattr(
                self.target,
                "found",
                False,
            )
        )

    @property
    def has_domain(
        self,
    ) -> bool:
        """
        True when a domain was detected.
        """

        return bool(
            getattr(
                self.domain,
                "found",
                False,
            )
        )

    @property
    def has_metric(
        self,
    ) -> bool:
        """
        True when a metric was detected.
        """

        return bool(
            getattr(
                self.metric,
                "found",
                False,
            )
        )

    @property
    def has_measurement(
        self,
    ) -> bool:
        """
        True when a measurement was detected.
        """

        return bool(
            getattr(
                self.measurement,
                "found",
                False,
            )
        )

    # ==========================================================
    # ENTITY ACCESS
    # ==========================================================

    def add_entity(
        self,
        entity: KnowledgeEntity,
    ) -> None:
        """
        Add a universal KnowledgeEntity.

        Duplicate object references are ignored.
        """

        if entity is None:

            return

        if entity in self.entities:

            return

        self.entities.append(
            entity
        )

    # ==========================================================
    # ENTITY TYPE FILTER
    # ==========================================================

    def entities_of_type(
        self,
        entity_type: str,
    ) -> list[KnowledgeEntity]:
        """
        Return entities matching entity_type.
        """

        if not entity_type:

            return []

        normalized_type = (
            str(
                entity_type
            )
            .strip()
            .casefold()
        )

        return [
            entity
            for entity in self.entities
            if str(
                getattr(
                    entity,
                    "entity_type",
                    "",
                )
            )
            .strip()
            .casefold()
            == normalized_type
        ]

    # ==========================================================
    # COMMON ENTITY TYPES
    # ==========================================================

    @property
    def technologies(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "technologie"
        )

    @property
    def certifications(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "certification"
        )

    @property
    def standards(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "standard"
        )

    @property
    def methodologies(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "methodologie"
        )

    @property
    def skills(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "skill"
        )

    @property
    def metrics(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "metric"
        )

    @property
    def kpis(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "kpi"
        )

    @property
    def domains(
        self,
    ) -> list[KnowledgeEntity]:

        return self.entities_of_type(
            "domain"
        )

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary_dict(
        self,
    ) -> dict:
        """
        Diagnostic representation.

        Useful for enterprise pipeline tests.
        """

        return {
            "entity_count": self.entity_count,

            "achievement": self.achievement,

            "quantified": self.quantified,

            "semantic_type": self.semantic_type,

            "business_area": self.business_area,

            "primary_domain": self.primary_domain,

            "confidence": self.confidence,

            "overall_impact_weight": (
                self.overall_impact_weight
            ),

            "entities": [
                {
                    "entity_id": getattr(
                        entity,
                        "entity_id",
                        "",
                    ),

                    "entity_type": getattr(
                        entity,
                        "entity_type",
                        "",
                    ),

                    "canonical": getattr(
                        entity,
                        "canonical",
                        "",
                    ),

                    "confidence": getattr(
                        entity,
                        "confidence",
                        0.0,
                    ),
                }
                for entity in self.entities
            ],
        }