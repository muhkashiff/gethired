"""
Enterprise Semantic Models
Enterprise V12

Canonical semantic contracts used by the GETHIRED
Intelligence Engine.

Pipeline

Knowledge Extractors
        ↓
SemanticEntity
        ↓
DependencyResolver
        ↓
SemanticDependency
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement
        ↓
KnowledgeGraphBuilder
        ↓
KnowledgeGraph
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


# ============================================================
# SEMANTIC ENTITY
# ============================================================

@dataclass
class SemanticEntity(KnowledgeEntity):
    """
    Enterprise semantic entity.

    Extends KnowledgeEntity with information required
    during semantic reasoning and statement construction.
    """

    # --------------------------------------------------------
    # Semantic information
    # --------------------------------------------------------

    matched_text: str = ""

    semantic_role: str = ""

    relation_role: str = ""

    reasoning: str = ""

    # --------------------------------------------------------
    # Statement membership
    # --------------------------------------------------------

    statement_id: str = ""

    # --------------------------------------------------------
    # Convenience properties
    # --------------------------------------------------------

    @property
    def name(self) -> str:
        return self.canonical

    @property
    def text(self) -> str:
        return self.original

    @property
    def id(self) -> str:
        return self.entity_id


# ============================================================
# SEMANTIC DEPENDENCY
# ============================================================

@dataclass(init=False)
class SemanticDependency:
    """
    Semantic relationship between two entities.

    Canonical field:
        relation

    Backward-compatible field:
        dependency_type

    Both are accepted by the constructor.

    Example:

        SemanticDependency(
            source_entity="ACTION_1",
            target_entity="KPI_1",
            relation="improved",
            confidence=0.98,
        )

    Legacy-compatible:

        SemanticDependency(
            source_entity="ACTION_1",
            target_entity="KPI_1",
            dependency_type="improved",
            confidence=0.98,
        )
    """

    source_entity: str = ""

    target_entity: str = ""

    relation: str = ""

    confidence: float = 1.0

    metadata: dict = field(
        default_factory=dict
    )

    def __init__(
        self,
        source_entity: str = "",
        target_entity: str = "",
        relation: str = "",
        confidence: float = 1.0,
        metadata: Optional[dict] = None,
        dependency_type: Optional[str] = None,
    ) -> None:

        self.source_entity = source_entity

        self.target_entity = target_entity

        # ----------------------------------------------------
        # Canonical relation wins.
        # Otherwise use legacy dependency_type.
        # ----------------------------------------------------

        if relation:
            self.relation = relation

        elif dependency_type:
            self.relation = dependency_type

        else:
            self.relation = ""

        self.confidence = confidence

        self.metadata = (
            metadata
            if metadata is not None
            else {}
        )

    # --------------------------------------------------------
    # Backward compatibility
    # --------------------------------------------------------

    @property
    def dependency_type(self) -> str:
        """
        Legacy alias for relation.
        """

        return self.relation

    @dependency_type.setter
    def dependency_type(
        self,
        value: str,
    ) -> None:

        self.relation = value


# ============================================================
# SEMANTIC CLUSTER
# ============================================================

@dataclass
class SemanticCluster:
    """
    Groups semantically related entities.
    """

    cluster_id: str = ""

    label: str = ""

    semantic_type: str = ""

    business_area: str = ""

    primary_domain: str = ""

    confidence: float = 1.0

    entities: list[SemanticEntity] = field(
        default_factory=list
    )

    dependencies: list[SemanticDependency] = field(
        default_factory=list
    )

    metadata: dict = field(
        default_factory=dict
    )


# ============================================================
# SEMANTIC STATISTICS
# ============================================================

@dataclass
class SemanticStatistics:
    """
    Statistics generated during semantic resolution.
    """

    entities: int = 0

    dependencies: int = 0

    clusters: int = 0

    actions: int = 0

    objects: int = 0

    targets: int = 0

    domains: int = 0

    metrics: int = 0

    measurements: int = 0

    methodologies: int = 0

    standards: int = 0

    skills: int = 0

    kpis: int = 0


# ============================================================
# SEMANTIC METADATA
# ============================================================

@dataclass
class SemanticMetadata:
    """
    Metadata describing resolved semantic content.
    """

    primary_domain: str = ""

    primary_business_area: str = ""

    semantic_type: str = ""

    achievement: bool = False

    statistics: SemanticStatistics = field(
        default_factory=SemanticStatistics
    )


# ============================================================
# STATEMENT RELATION
# ============================================================

@dataclass
class StatementRelation:
    """
    Relationship inside a BusinessStatement.

    This is the canonical semantic relationship that
    later becomes a graph edge.

    BusinessStatement owns these relations.
    KnowledgeGraphBuilder consumes them.
    """

    source_id: str = ""

    target_id: str = ""

    relation_type: str = ""

    confidence: float = 1.0

    reasoning: str = ""

    metadata: dict = field(
        default_factory=dict
    )

    # --------------------------------------------------------
    # Backward compatibility
    # --------------------------------------------------------

    @property
    def relation(self) -> str:
        return self.relation_type

    @relation.setter
    def relation(
        self,
        value: str,
    ) -> None:

        self.relation_type = value


# ============================================================
# BUSINESS STATEMENT
# ============================================================

@dataclass
class BusinessStatement:
    """
    Enterprise Business Statement.

    Single source of truth for:

        entities
        relations
        statement metadata

    KnowledgeGraphBuilder consumes BusinessStatement.
    """

    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    statement_id: str = ""

    label: str = ""

    confidence: float = 1.0

    semantic_type: str = ""

    primary_domain: str = ""

    business_area: str = ""

    achievement: bool = False

    metadata: dict = field(
        default_factory=dict
    )

    # --------------------------------------------------------
    # Legacy compatibility
    # --------------------------------------------------------

    intent: Optional[object] = None

    action: Optional[object] = None

    technologies: list = field(
        default_factory=list
    )

    # --------------------------------------------------------
    # SINGLE SOURCE OF TRUTH
    # --------------------------------------------------------

    entities: list[SemanticEntity] = field(
        default_factory=list
    )

    relations: list[StatementRelation] = field(
        default_factory=list
    )

    # ========================================================
    # ENTITY LOOKUP
    # ========================================================

    def entity(
        self,
        entity_id: str,
    ) -> Optional[SemanticEntity]:

        for entity in self.entities:

            if entity.entity_id == entity_id:
                return entity

        return None

    # ========================================================
    # ENTITY FILTER
    # ========================================================

    def entities_of_type(
        self,
        entity_type: str,
    ) -> list[SemanticEntity]:

        entity_type = entity_type.lower()

        return [
            entity
            for entity in self.entities
            if entity.entity_type.lower()
            == entity_type
        ]

    # ========================================================
    # ENTITY PROPERTIES
    # ========================================================

    @property
    def actions(self):

        return self.entities_of_type("action")

    @property
    def targets(self):

        return self.entities_of_type("target")

    @property
    def objects(self):

        return self.targets

    @property
    def domains(self):

        return self.entities_of_type("domain")

    @property
    def skills(self):

        return self.entities_of_type("skill")

    @property
    def standards(self):

        return self.entities_of_type("standard")

    @property
    def methodologies(self):

        return self.entities_of_type("methodology")

    @property
    def metrics(self):

        return self.entities_of_type("metric")

    @property
    def measurements(self):

        return self.entities_of_type("measurement")

    @property
    def kpis(self):

        return self.entities_of_type("kpi")

    # ========================================================
    # RELATION FILTER
    # ========================================================

    def relations_of_type(
        self,
        relation_name: str,
    ) -> list[StatementRelation]:

        relation_name = relation_name.upper()

        return [
            relation
            for relation in self.relations
            if relation.relation_type.upper()
            == relation_name
        ]

    # ========================================================
    # ACTION → TARGET
    # ========================================================

    def action_targets(self):

        for relation in self.relations_of_type(
            "ACTS_ON"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACTION → METRIC
    # ========================================================

    def action_metrics(self):

        for relation in self.relations_of_type(
            "AFFECTS"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # METRIC → MEASUREMENT
    # ========================================================

    def metric_measurements(self):

        for relation in self.relations_of_type(
            "MEASURED_BY"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACTION → SKILL
    # ========================================================

    def action_skills(self):

        for relation in self.relations_of_type(
            "REQUIRES"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACTION → STANDARD
    # ========================================================

    def action_standards(self):

        for relation in self.relations_of_type(
            "COMPLIES_WITH"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACTION → METHODOLOGY
    # ========================================================

    def action_methodologies(self):

        for relation in self.relations_of_type(
            "USES"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACTION → DOMAIN
    # ========================================================

    def action_domains(self):

        for relation in self.relations_of_type(
            "BELONGS_TO"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def achievements(self):

        for relation in self.relations_of_type(
            "ACHIEVED"
        ):

            yield (
                self.entity(relation.source_id),
                self.entity(relation.target_id),
                relation,
            )

    # ========================================================
    # COUNTS
    # ========================================================

    @property
    def entity_count(self) -> int:

        return len(self.entities)

    @property
    def relation_count(self) -> int:

        return len(self.relations)

    def __len__(self):

        return len(self.entities)

    def __repr__(self):

        return (
            f"<BusinessStatement "
            f"id={self.statement_id!r} "
            f"entities={len(self.entities)} "
            f"relations={len(self.relations)} "
            f"confidence={self.confidence}>"
        )


# ============================================================
# SEMANTIC RESOLUTION
# ============================================================

@dataclass
class SemanticResolution:
    """
    Final output produced by SemanticResolver.
    """

    entities: list[SemanticEntity] = field(
        default_factory=list
    )

    dependencies: list[SemanticDependency] = field(
        default_factory=list
    )

    clusters: list[SemanticCluster] = field(
        default_factory=list
    )

    business_statements: list[BusinessStatement] = field(
        default_factory=list
    )

    confidence: float = 0.0

    metadata: SemanticMetadata = field(
        default_factory=SemanticMetadata
    )

    warnings: list[str] = field(
        default_factory=list
    )

    def entity(
        self,
        entity_id: str,
    ) -> Optional[SemanticEntity]:

        for entity in self.entities:

            if entity.entity_id == entity_id:
                return entity

        return None

    def entities_of_type(
        self,
        entity_type: str,
    ):

        entity_type = entity_type.lower()

        return [
            entity
            for entity in self.entities
            if entity.entity_type.lower()
            == entity_type
        ]

    @property
    def actions(self):

        return self.entities_of_type("action")

    @property
    def targets(self):

        return self.entities_of_type("target")

    @property
    def objects(self):

        return self.targets

    @property
    def domains(self):

        return self.entities_of_type("domain")

    @property
    def standards(self):

        return self.entities_of_type("standard")

    @property
    def methodologies(self):

        return self.entities_of_type("methodology")

    @property
    def skills(self):

        return self.entities_of_type("skill")

    @property
    def metrics(self):

        return self.entities_of_type("metric")

    @property
    def measurements(self):

        return self.entities_of_type("measurement")

    @property
    def kpis(self):

        return self.entities_of_type("kpi")

    @property
    def primary_cluster(self):

        if not self.clusters:
            return None

        return max(
            self.clusters,
            key=lambda cluster: cluster.confidence,
        )

    @property
    def semantic_summary(self):

        cluster = self.primary_cluster

        if cluster is None:
            return ""

        return cluster.semantic_type

    @property
    def is_achievement(self):

        return self.metadata.achievement

    def __len__(self):

        return len(self.entities)

    def __repr__(self):

        return (
            f"<SemanticResolution "
            f"entities={len(self.entities)} "
            f"dependencies={len(self.dependencies)} "
            f"clusters={len(self.clusters)} "
            f"statements={len(self.business_statements)} "
            f"confidence={self.confidence}>"
        )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

DependencyEdge = SemanticDependency

SemanticResult = SemanticResolution