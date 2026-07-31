"""
    Semantic Models

    Master data models used throughout the Semantic Intelligence Engine.

    Everything downstream uses these objects.

    SentenceParser
            ↓
    DependencyBuilder
            ↓
    ClusterBuilder
            ↓
    SemanticResolver
            ↓
    KnowledgeGraph
            ↓
    KnowledgeProfile
"""

from dataclasses import dataclass, field


        # ============================================================
        # Semantic Entity
        # ============================================================

@dataclass
class SemanticEntity:

            entity_id: str = ""

            entity_type: str = ""

            canonical: str = ""

            original: str = ""

            matched_text: str = ""

            category: str = ""

            business_area: str = ""

            confidence: float = 1.0

            impact_weight: float = 1.0

            metadata: dict = field(default_factory=dict)


        # ============================================================
        # Semantic Dependency
        # ============================================================

@dataclass
class SemanticDependency:

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

            domains: int = 0

            metrics: int = 0

            measurements: int = 0

            methodologies: int = 0

            standards: int = 0


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

            entities: list[SemanticEntity] = field(default_factory=list)

            dependencies: list[SemanticDependency] = field(default_factory=list)

            clusters: list[SemanticCluster] = field(default_factory=list)

            confidence: float = 0.0

            metadata: SemanticMetadata = field(
                default_factory=SemanticMetadata
            )

            warnings: list[str] = field(default_factory=list)

            business_statements: list["BusinessStatement"] = field(default_factory=list)

        # =========================================================

def entity(self, entity_id):

            for entity in self.entities:

                if entity.entity_id == entity_id:

                    return entity

            return None

        # =========================================================

def entities_of_type(self, entity_type):

            return [

                entity

                for entity in self.entities

                if entity.entity_type.lower() == entity_type.lower()

            ]

        # =========================================================

@property
def actions(self):

            return self.entities_of_type("action")
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
def kpis(self):

            return self.entities_of_type("kpi")

@property
def metrics(self):

            return self.entities_of_type("metric")

@property
def measurements(self):

            return self.entities_of_type("measurement")

        # =========================================================

@property
def primary_cluster(self):

            if not self.clusters:

                return None

            return max(

                self.clusters,

                key=lambda c: c.confidence

            )

        # =========================================================

@property
def semantic_summary(self):

            if self.primary_cluster is None:

                return ""

            return self.primary_cluster.semantic_type

        # =========================================================

@property
def is_achievement(self):

            return self.metadata.achievement

        # =========================================================

def __len__(self):

            return len(self.entities)

        # =========================================================

def __repr__(self):

            return (

                f"<SemanticResolution "

                f"entities={len(self.entities)} "

                f"dependencies={len(self.dependencies)} "

                f"clusters={len(self.clusters)} "

                f"confidence={self.confidence}>"

            )
    # ============================================================
    # Backward Compatibility Aliases
    # ============================================================

        # Older modules still use these names.
KnowledgeEntity = SemanticEntity
DependencyEdge = SemanticDependency
SemanticResult = SemanticResolution

# ============================================================
# Business Statement V2
# ============================================================

@dataclass
class BusinessStatement:

    # -----------------------------
    # Identity
    # -----------------------------

    statement_id: str = ""

    label: str = ""

    # -----------------------------
    # Core Action
    # -----------------------------

    action: SemanticEntity | None = None

    # Master list of every entity
    entities: list[SemanticEntity] = field(default_factory=list)

    # -----------------------------
    # Structured Entity Groups
    # -----------------------------

    targets: list[SemanticEntity] = field(default_factory=list)

    methods: list[SemanticEntity] = field(default_factory=list)

    standards: list[SemanticEntity] = field(default_factory=list)

    skills: list[SemanticEntity] = field(default_factory=list)

    metrics: list[SemanticEntity] = field(default_factory=list)

    domains: list[SemanticEntity] = field(default_factory=list)

    # -----------------------------
    # Dependencies
    # -----------------------------

    dependencies: list[SemanticDependency] = field(default_factory=list)

    # -----------------------------
    # Semantic Intent
    # -----------------------------

    intent = None

    semantic_type: str = ""

    primary_domain: str = ""

    business_area: str = ""

    achievement: bool = False

    # -----------------------------
    # Confidence
    # -----------------------------

    confidence: float = 1.0

    # -----------------------------
    # Metadata
    # -----------------------------

    metadata: dict = field(default_factory=dict)