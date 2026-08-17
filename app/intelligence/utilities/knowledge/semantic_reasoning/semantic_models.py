"""
Enterprise Semantic Models
Enterprise V13

Purpose
-------
Defines the semantic data contracts used by the enterprise
resume intelligence architecture.

Pipeline
--------

    KnowledgeDocument
            ↓
    KnowledgeFact
            ↓
    KnowledgeInterpretation
            ↓
    SemanticResolver
            ↓
    SemanticResolution
       ├── SemanticEntity[]
       ├── StatementRelation[]
       ├── SemanticDependency[]
       └── SemanticCluster[]
            ↓
    BusinessStatementBuilder
            ↓
    BusinessStatement[]
            ↓
    KnowledgeGraphBuilder
            ↓
    KnowledgeProfile

This module contains DATA CONTRACTS ONLY.

It does not:
    - extract ontology entities
    - perform ontology matching
    - resolve semantic relationships
    - build business statements
    - build the knowledge graph
    - calculate scores
    - build the knowledge profile
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =====================================================================
# SEMANTIC ENTITY
# =====================================================================


@dataclass
class SemanticEntity:
    """
    Resolved semantic entity.

    Created by SemanticResolver from ontology-derived
    KnowledgeInterpretation entities.

    Examples
    --------
    action
    target
    domain
    skill
    technology
    certification
    standard
    methodology
    metric
    measurement
    kpi
    business_kpi
    modifier
    practice
    """

    # -----------------------------------------------------------------
    # IDENTITY
    # -----------------------------------------------------------------

    entity_id: str = ""

    entity_type: str = ""

    canonical: str = ""

    normalized: str = ""

    original: str = ""

    label: str = ""

    # -----------------------------------------------------------------
    # CLASSIFICATION
    # -----------------------------------------------------------------

    category: str = ""

    ontology_name: str = ""

    primary_domain: str = ""

    business_area: str = ""

    semantic_type: str = ""

    # -----------------------------------------------------------------
    # SOURCE
    # -----------------------------------------------------------------

    fact_id: str = ""

    statement_id: str = ""

    sentence_index: int = -1

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    token_count: int = 0

    source_text: str = ""

    source: str = "resume"

    extraction_method: str = ""

    # -----------------------------------------------------------------
    # KNOWLEDGE
    # -----------------------------------------------------------------

    description: str = ""

    business_meaning: str = ""

    confidence: float = 0.0

    impact_weight: float = 1.0

    # -----------------------------------------------------------------
    # BUSINESS INFORMATION
    # -----------------------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    preferred_direction: str = ""

    preferred_unit: str = ""

    higher_is_better: bool = True

    related_metrics: List[str] = field(
        default_factory=list
    )

    # -----------------------------------------------------------------
    # ORIGINAL KNOWLEDGE OBJECT
    # -----------------------------------------------------------------

    knowledge_object: Optional[Any] = None

    ontology_object: Optional[Any] = None

    # -----------------------------------------------------------------
    # METADATA
    # -----------------------------------------------------------------

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------
    # COMPATIBILITY
    # -----------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Return the best available semantic name.
        """

        return (
            self.canonical
            or self.label
            or self.normalized
            or self.original
        )

    @property
    def type(self) -> str:
        """
        Compatibility alias for entity_type.
        """

        return self.entity_type

    @property
    def is_valid(self) -> bool:
        """
        True when the entity contains usable identity.
        """

        return bool(
            self.entity_id
            or self.canonical
            or self.normalized
            or self.original
        )

    def __repr__(self) -> str:

        return (
            "SemanticEntity("
            f"id={self.entity_id!r}, "
            f"type={self.entity_type!r}, "
            f"canonical={self.canonical!r}, "
            f"confidence={self.confidence!r}"
            ")"
        )


# =====================================================================
# STATEMENT RELATION
# =====================================================================


@dataclass
class StatementRelation:
    """
    Explicit semantic relation between two entities.

    These relations are consumed by BusinessStatementBuilder
    and KnowledgeGraphBuilder.
    """

    relation_id: str = ""

    relation_type: str = ""

    source_id: str = ""

    target_id: str = ""

    confidence: float = 0.0

    weight: float = 1.0

    fact_id: str = ""

    statement_id: str = ""

    sentence_index: int = -1

    source_text: str = ""

    explanation: str = ""

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def relation(self) -> str:
        """
        Compatibility alias.
        """

        return self.relation_type

    @property
    def source(self) -> str:
        return self.source_id

    @property
    def target(self) -> str:
        return self.target_id

    def __repr__(self) -> str:

        return (
            "StatementRelation("
            f"id={self.relation_id!r}, "
            f"type={self.relation_type!r}, "
            f"source={self.source_id!r}, "
            f"target={self.target_id!r}, "
            f"confidence={self.confidence!r}"
            ")"
        )


# =====================================================================
# SEMANTIC DEPENDENCY
# =====================================================================


@dataclass
class SemanticDependency:
    """
    Semantic dependency discovered during reasoning.

    IMPORTANT
    ---------
    This is different from StatementRelation.

    SemanticDependency:
        internal reasoning relationship.

    StatementRelation:
        explicit business relationship consumed
        by downstream business-statement logic.
    """

    dependency_id: str = ""

    dependency_type: str = ""

    source_id: str = ""

    target_id: str = ""

    confidence: float = 0.0

    weight: float = 1.0

    fact_id: str = ""

    statement_id: str = ""

    sentence_index: int = -1

    explanation: str = ""

    evidence: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------
    # COMPATIBILITY
    # -----------------------------------------------------------------

    @property
    def relation_type(self) -> str:
        return self.dependency_type

    @property
    def relation(self) -> str:
        return self.dependency_type

    @property
    def source(self) -> str:
        return self.source_id

    @property
    def target(self) -> str:
        return self.target_id

    # Older code may use these names.
    # They are READ-ONLY compatibility aliases.

    @property
    def source_entity(self) -> str:
        return self.source_id

    @property
    def target_entity(self) -> str:
        return self.target_id

    def __repr__(self) -> str:

        return (
            "SemanticDependency("
            f"id={self.dependency_id!r}, "
            f"type={self.dependency_type!r}, "
            f"source={self.source_id!r}, "
            f"target={self.target_id!r}, "
            f"confidence={self.confidence!r}"
            ")"
        )


# =====================================================================
# SEMANTIC CLUSTER
# =====================================================================


@dataclass
class SemanticCluster:
    """
    Group of semantically related entities.

    A cluster is NOT a knowledge-graph node.

    It is a semantic reasoning structure used before
    BusinessStatementBuilder.
    """

    cluster_id: str = ""

    label: str = ""

    cluster_type: str = ""

    entity_ids: List[str] = field(
        default_factory=list
    )

    dependency_ids: List[str] = field(
        default_factory=list
    )

    primary_domain: str = ""

    business_area: str = ""

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def size(self) -> int:

        return len(
            self.entity_ids
        )

    def add_entity(
        self,
        entity_id: str,
    ) -> None:

        if (
            entity_id
            and entity_id not in self.entity_ids
        ):
            self.entity_ids.append(
                entity_id
            )

    def add_dependency(
        self,
        dependency_id: str,
    ) -> None:

        if (
            dependency_id
            and dependency_id not in self.dependency_ids
        ):
            self.dependency_ids.append(
                dependency_id
            )

    def __repr__(self) -> str:

        return (
            "SemanticCluster("
            f"id={self.cluster_id!r}, "
            f"label={self.label!r}, "
            f"entities={len(self.entity_ids)}, "
            f"confidence={self.confidence!r}"
            ")"
        )


# =====================================================================
# SEMANTIC EVIDENCE
# =====================================================================


@dataclass
class SemanticEvidence:
    """
    Evidence supporting a semantic relationship.
    """

    evidence_id: str = ""

    source_id: str = ""

    target_id: str = ""

    evidence_type: str = ""

    text: str = ""

    confidence: float = 0.0

    weight: float = 1.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


# =====================================================================
# SEMANTIC RESOLUTION
# =====================================================================


@dataclass
class SemanticResolution:
    """
    Complete output of SemanticResolver.

    This is the semantic-layer contract.

    It is consumed by BusinessStatementBuilder.

    It contains:

        entities
        relations
        dependencies
        clusters

    Business statements are intentionally optional because
    BusinessStatementBuilder is the component responsible
    for creating them.
    """

    entities: List[SemanticEntity] = field(
        default_factory=list
    )

    relations: List[StatementRelation] = field(
        default_factory=list
    )

    dependencies: List[SemanticDependency] = field(
        default_factory=list
    )

    clusters: List[SemanticCluster] = field(
        default_factory=list
    )

    business_statements: List[Any] = field(
        default_factory=list
    )

    fact_count: int = 0

    sentence_count: int = 0

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # -----------------------------------------------------------------
    # COUNTS
    # -----------------------------------------------------------------

    @property
    def entity_count(self) -> int:

        return len(
            self.entities
        )

    @property
    def relation_count(self) -> int:

        return len(
            self.relations
        )

    @property
    def dependency_count(self) -> int:

        return len(
            self.dependencies
        )

    @property
    def cluster_count(self) -> int:

        return len(
            self.clusters
        )

    @property
    def statement_count(self) -> int:

        return len(
            self.business_statements
        )

    # -----------------------------------------------------------------
    # STATUS
    # -----------------------------------------------------------------

    @property
    def has_entities(self) -> bool:

        return bool(
            self.entities
        )

    @property
    def has_relations(self) -> bool:

        return bool(
            self.relations
        )

    @property
    def has_dependencies(self) -> bool:

        return bool(
            self.dependencies
        )

    @property
    def has_clusters(self) -> bool:

        return bool(
            self.clusters
        )

    # -----------------------------------------------------------------
    # LOOKUP
    # -----------------------------------------------------------------

    def entity(
        self,
        entity_id: str,
    ) -> Optional[SemanticEntity]:

        for entity in self.entities:

            if entity.entity_id == entity_id:

                return entity

        return None

    # -----------------------------------------------------------------
    # TYPE FILTER
    # -----------------------------------------------------------------

    def entities_of_type(
        self,
        entity_type: str,
    ) -> List[SemanticEntity]:

        normalized_type = (
            str(entity_type)
            .strip()
            .casefold()
        )

        return [
            entity
            for entity in self.entities
            if (
                str(entity.entity_type)
                .strip()
                .casefold()
                == normalized_type
            )
        ]

    # -----------------------------------------------------------------
    # RELATION FILTER
    # -----------------------------------------------------------------

    def relations_of_type(
        self,
        relation_type: str,
    ) -> List[StatementRelation]:

        normalized_relation = (
            str(relation_type)
            .strip()
            .casefold()
        )

        return [
            relation
            for relation in self.relations
            if (
                str(relation.relation_type)
                .strip()
                .casefold()
                == normalized_relation
            )
        ]

    # -----------------------------------------------------------------
    # DEPENDENCY FILTER
    # -----------------------------------------------------------------

    def dependencies_of_type(
        self,
        dependency_type: str,
    ) -> List[SemanticDependency]:

        normalized_type = (
            str(dependency_type)
            .strip()
            .casefold()
        )

        return [
            dependency
            for dependency in self.dependencies
            if (
                str(dependency.dependency_type)
                .strip()
                .casefold()
                == normalized_type
            )
        ]

    # -----------------------------------------------------------------
    # ADD METHODS
    # -----------------------------------------------------------------

    def add_entity(
        self,
        entity: SemanticEntity,
    ) -> None:

        if entity is not None:
            self.entities.append(
                entity
            )

    def add_relation(
        self,
        relation: StatementRelation,
    ) -> None:

        if relation is not None:
            self.relations.append(
                relation
            )

    def add_dependency(
        self,
        dependency: SemanticDependency,
    ) -> None:

        if dependency is not None:
            self.dependencies.append(
                dependency
            )

    def add_cluster(
        self,
        cluster: SemanticCluster,
    ) -> None:

        if cluster is not None:
            self.clusters.append(
                cluster
            )

    # -----------------------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate the semantic contract.
        """

        entity_ids = set()

        for entity in self.entities:

            if not isinstance(
                entity,
                SemanticEntity,
            ):
                raise ValueError(
                    "SemanticResolution.entities "
                    "contains an invalid object."
                )

            if entity.entity_id:

                entity_ids.add(
                    entity.entity_id
                )

        for dependency in self.dependencies:

            if not isinstance(
                dependency,
                SemanticDependency,
            ):
                raise ValueError(
                    "SemanticResolution.dependencies "
                    "contains an invalid object."
                )

            if (
                dependency.source_id
                and dependency.source_id
                not in entity_ids
            ):
                raise ValueError(
                    "SemanticDependency source_id "
                    f"{dependency.source_id!r} "
                    "does not exist."
                )

            if (
                dependency.target_id
                and dependency.target_id
                not in entity_ids
            ):
                raise ValueError(
                    "SemanticDependency target_id "
                    f"{dependency.target_id!r} "
                    "does not exist."
                )

        for relation in self.relations:

            if not isinstance(
                relation,
                StatementRelation,
            ):
                raise ValueError(
                    "SemanticResolution.relations "
                    "contains an invalid object."
                )

    def __repr__(self) -> str:

        return (
            "SemanticResolution("
            f"entities={len(self.entities)}, "
            f"relations={len(self.relations)}, "
            f"dependencies={len(self.dependencies)}, "
            f"clusters={len(self.clusters)}, "
            f"statements={len(self.business_statements)}, "
            f"confidence={self.confidence!r}"
            ")"
        )

# =====================================================================
# BUSINESS STATEMENT
# =====================================================================


@dataclass
class BusinessStatement:
    """
    Enterprise business statement.

    Represents a resolved professional achievement
    or capability statement extracted from resume knowledge.

    Created by:

        BusinessStatementBuilder

    Consumed by:

        KnowledgeGraphBuilder
        KnowledgeProfileBuilder


    Example:

        "Implemented FSSC 22000 system resulting in certification"

    becomes:

        Action:
            ACT_IMPLEMENT

        Target:
            FSSC 22000

        Domain:
            Food Safety

        Impact:
            Certification

    """

    # -------------------------------------------------------------
    # IDENTITY
    # -------------------------------------------------------------

    statement_id: str = ""

    canonical: str = ""

    text: str = ""

    normalized: str = ""


    # -------------------------------------------------------------
    # SOURCE
    # -------------------------------------------------------------

    fact_id: str = ""

    sentence_index: int = -1

    source_text: str = ""

    source: str = "resume"


    # -------------------------------------------------------------
    # SEMANTIC COMPONENTS
    # -------------------------------------------------------------

    action: Optional[SemanticEntity] = None

    target: Optional[SemanticEntity] = None

    domain: Optional[SemanticEntity] = None

    metric: Optional[SemanticEntity] = None


    entities: List[SemanticEntity] = field(
        default_factory=list
    )


    relations: List[StatementRelation] = field(
        default_factory=list
    )


    dependencies: List[SemanticDependency] = field(
        default_factory=list
    )


    # -------------------------------------------------------------
    # BUSINESS MEANING
    # -------------------------------------------------------------

    achievement: bool = False

    quantified: bool = False

    impact: str = ""

    business_value: str = ""

    category: str = ""

    business_area: str = ""


    # -------------------------------------------------------------
    # SCORING
    # -------------------------------------------------------------

    confidence: float = 0.0

    impact_weight: float = 1.0


    # -------------------------------------------------------------
    # METADATA
    # -------------------------------------------------------------

    metadata: Dict[str,Any] = field(
        default_factory=dict
    )


    # -------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------

    @property
    def entity_count(self):

        return len(
            self.entities
        )


    @property
    def is_valid(self):

        return bool(
            self.statement_id
            or self.text
            or self.entities
        )


    def add_entity(
        self,
        entity: SemanticEntity,
    ):

        if entity is not None:

            self.entities.append(
                entity
            )


    def add_relation(
        self,
        relation: StatementRelation,
    ):

        if relation is not None:

            self.relations.append(
                relation
            )


    def __repr__(self):

        return (
            "BusinessStatement("
            f"id={self.statement_id!r}, "
            f"text={self.text!r}, "
            f"entities={len(self.entities)}, "
            f"confidence={self.confidence!r}"
            ")"
        )
# =====================================================================
# PUBLIC EXPORTS
# =====================================================================

__all__ = [
    "SemanticEntity",
    "StatementRelation",
    "SemanticDependency",
    "SemanticCluster",
    "SemanticEvidence",
    "SemanticResolution",
    "BusinessStatement",
]