"""
Semantic Models

Enterprise V11

Master semantic data models used throughout the
GetHired Intelligence Engine.

Pipeline

SentenceParser
        ↓
DependencyBuilder
        ↓
ClusterBuilder
        ↓
SemanticResolver
        ↓
BusinessStatement
        ↓
KnowledgeGraph
        ↓
KnowledgeProfile
"""

from dataclasses import dataclass, field

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


# ============================================================
# Semantic Entity
# ============================================================

@dataclass
class SemanticEntity(KnowledgeEntity):
    """
    Enterprise Semantic Entity

    Extends KnowledgeEntity with semantic reasoning
    information.
    """

    matched_text: str = ""

    semantic_role: str = ""

    relation_role: str = ""

    reasoning: str = ""

    # ---------------------------------------------------------

    @property
    def name(self):
        return self.canonical

    @property
    def text(self):
        return self.original

    @property
    def id(self):
        return self.entity_id


# ============================================================
# Semantic Dependency
# ============================================================

@dataclass
class SemanticDependency:
    """
    Dependency between semantic entities.
    """

    source_entity: str = ""

    target_entity: str = ""

    relation: str = ""

    confidence: float = 1.0

    metadata: dict = field(default_factory=dict)


# ============================================================
# Semantic Cluster
# ============================================================

@dataclass
class SemanticCluster:
    """
    Groups semantically-related entities.
    """

    cluster_id: str = ""

    label: str = ""

    semantic_type: str = ""

    business_area: str = ""

    primary_domain: str = ""

    confidence: float = 1.0

    entities: list[SemanticEntity] = field(default_factory=list)

    dependencies: list[SemanticDependency] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


# ============================================================
# Statistics
# ============================================================

@dataclass
class SemanticStatistics:

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
# Metadata
# ============================================================

@dataclass
class SemanticMetadata:

    primary_domain: str = ""

    primary_business_area: str = ""

    semantic_type: str = ""

    achievement: bool = False

    statistics: SemanticStatistics = field(
        default_factory=SemanticStatistics
    )


# ============================================================
# Semantic Resolution
# ============================================================

@dataclass
class SemanticResolution:
    """
    Final output produced by Semantic Resolver.
    """

    entities: list[SemanticEntity] = field(default_factory=list)

    dependencies: list[SemanticDependency] = field(default_factory=list)

    clusters: list[SemanticCluster] = field(default_factory=list)

    confidence: float = 0.0

    metadata: SemanticMetadata = field(
        default_factory=SemanticMetadata
    )

    warnings: list[str] = field(default_factory=list)

    business_statements: list["BusinessStatement"] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Entity Lookup
    # ---------------------------------------------------------

    def entity(
        self,
        entity_id: str,
    ):

        for entity in self.entities:

            if entity.entity_id == entity_id:

                return entity

        return None

    # ---------------------------------------------------------

    def entities_of_type(
        self,
        entity_type: str,
    ):

        return [

            entity

            for entity in self.entities

            if entity.entity_type.lower()
            == entity_type.lower()

        ]

    # ---------------------------------------------------------
    # Convenience Properties
    # ---------------------------------------------------------

    @property
    def actions(self):

        return self.entities_of_type("action")

    @property
    def targets(self):

        return self.entities_of_type("target")

    @property
    def objects(self):

        return self.entities_of_type("object")

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

    # ---------------------------------------------------------

    @property
    def primary_cluster(self):

        if not self.clusters:

            return None

        return max(

            self.clusters,

            key=lambda cluster: cluster.confidence,

        )

    # ---------------------------------------------------------

    @property
    def semantic_summary(self):

        cluster = self.primary_cluster

        if cluster is None:

            return ""

        return cluster.semantic_type

    # ---------------------------------------------------------

    @property
    def is_achievement(self):

        return self.metadata.achievement

    # ---------------------------------------------------------

    def __len__(self):

        return len(self.entities)

    # ---------------------------------------------------------

    def __repr__(self):

        return (

            f"<SemanticResolution "

            f"entities={len(self.entities)} "

            f"dependencies={len(self.dependencies)} "

            f"clusters={len(self.clusters)} "

            f"confidence={self.confidence}>"

        )


# ============================================================
# Backward Compatibility
# ============================================================

KnowledgeEntity = SemanticEntity

DependencyEdge = SemanticDependency

SemanticResult = SemanticResolution


# ============================================================
# Statement Relation
# ============================================================

@dataclass
class StatementRelation:
    

    source_id: str = ""

    target_id: str = ""

    relation_type: str = ""

    confidence: float = 1.0

    reasoning: str = ""

    metadata: dict = field(default_factory=dict)

# ============================================================
# Business Statement V11
# ============================================================

@dataclass
class BusinessStatement:

    # -------------------------------------------------
    # Identity
    # -------------------------------------------------

    statement_id: str = ""

    label: str = ""

    confidence: float = 1.0

    semantic_type: str = ""

    primary_domain: str = ""

    business_area: str = ""

    achievement: bool = False

    metadata: dict = field(default_factory=dict)

    intent = None

    # ---------------------------
    # NEW
    # ---------------------------

    action = None

    objects: list = field(default_factory=list)

    metrics: list = field(default_factory=list)

    measurements: list = field(default_factory=list)

    technologies: list = field(default_factory=list)

    standards: list = field(default_factory=list)

    methodologies: list = field(default_factory=list)

    # -------------------------------------------------
    # Single Source of Truth
    # -------------------------------------------------

    entities: list[SemanticEntity] = field(default_factory=list)

    relations: list[StatementRelation] = field(default_factory=list)

    # -------------------------------------------------
    # Entity Lookup
    # -------------------------------------------------

    def entity(self, entity_id: str):

        for entity in self.entities:

            if entity.entity_id == entity_id:

                return entity

        return None

    # -------------------------------------------------
    # Generic Entity Filter
    # -------------------------------------------------

    def entities_of_type(self, entity_type: str):

        return [

            entity

            for entity in self.entities

            if entity.entity_type.lower() == entity_type.lower()

        ]

    # -------------------------------------------------
    # Entity Properties
    # -------------------------------------------------

    @property
    def actions(self):
        return self.entities_of_type("action")

    @property
    def targets(self):
        return self.entities_of_type("target")

    @property
    def objects(self):
        """
        Backward compatibility.

        Targets replace Objects.
        """
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

    # -------------------------------------------------
    # Generic Relation Filter
    # -------------------------------------------------

    def relations_of_type(self, relation_name: str):

        return [

            relation

            for relation in self.relations

            if relation.relation.upper() == relation_name.upper()

        ]

    # -------------------------------------------------
    # ACTION -> TARGET
    # -------------------------------------------------

    def action_targets(self):

        for relation in self.relations_of_type("ACTS_ON"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> METRIC
    # -------------------------------------------------

    def action_metrics(self):

        for relation in self.relations_of_type("AFFECTS"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # METRIC -> MEASUREMENT
    # -------------------------------------------------

    def metric_measurements(self):

        for relation in self.relations_of_type("MEASURED_BY"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> SKILL
    # -------------------------------------------------

    def action_skills(self):

        for relation in self.relations_of_type("REQUIRES"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> STANDARD
    # -------------------------------------------------

    def action_standards(self):

        for relation in self.relations_of_type("COMPLIES_WITH"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> METHODOLOGY
    # -------------------------------------------------

    def action_methodologies(self):

        for relation in self.relations_of_type("USES"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> DOMAIN
    # -------------------------------------------------

    def action_domains(self):

        for relation in self.relations_of_type("BELONGS_TO"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # ACTION -> ACHIEVED -> METRIC
    # -------------------------------------------------

    def achievements(self):

        for relation in self.relations_of_type("ACHIEVED"):

            yield (

                self.entity(relation.source_id),

                self.entity(relation.target_id),

                relation,

            )

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------

    def __len__(self):

        return len(self.entities)

    def __repr__(self):

        return (

            f"<BusinessStatement "

            f"entities={len(self.entities)} "

            f"relations={len(self.relations)} "

            f"confidence={self.confidence}>"

        )