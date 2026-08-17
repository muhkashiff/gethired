"""
Enterprise Semantic Resolver
Enterprise V13

Purpose
-------
Convert KnowledgeInterpretation objects into SemanticResolution.

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

The resolver does NOT:

    - build BusinessStatement
    - build KnowledgeGraph
    - build KnowledgeProfile
    - calculate final resume scores

It is responsible for semantic normalization and
semantic relationship discovery only.
"""

from __future__ import annotations

from typing import Any, Iterable

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticCluster,
    SemanticDependency,
    SemanticEntity,
    SemanticResolution,
    StatementRelation,
)


class SemanticResolver:
    """
    Enterprise semantic resolver.

    Converts extracted KnowledgeInterpretation objects
    into the semantic contract used by the rest of the
    enterprise pipeline.
    """

    # ================================================================
    # PUBLIC API
    # ================================================================

    def resolve(
        self,
        knowledge_document: Any,
    ) -> SemanticResolution:
        """
        Resolve an entire KnowledgeDocument.
        """

        resolution = SemanticResolution()

        if knowledge_document is None:

            return resolution

        facts = self._extract_facts(
            knowledge_document
        )

        resolution.fact_count = len(
            facts
        )

        resolution.sentence_count = self._sentence_count(
            knowledge_document
        )

        for fact_index, fact in enumerate(facts):

            interpretation = self._get_interpretation(
                fact
            )

            if interpretation is None:

                continue

            source_text = self._source_text(
                fact,
                interpretation,
            )

            statement_id = self._statement_id(
                fact_index,
                fact,
                interpretation,
            )

            entities = self._resolve_interpretation(
                interpretation=interpretation,
                fact=fact,
                statement_id=statement_id,
                source_text=source_text,
            )

            for entity in entities:

                self._append_unique_entity(
                    resolution,
                    entity,
                )

            relations = self._build_relations(
                entities=entities,
                interpretation=interpretation,
                fact=fact,
                statement_id=statement_id,
                source_text=source_text,
            )

            for relation in relations:

                self._append_unique_relation(
                    resolution,
                    relation,
                )

            dependencies = self._build_dependencies(
                entities=entities,
                relations=relations,
                fact=fact,
                statement_id=statement_id,
            )

            for dependency in dependencies:

                self._append_unique_dependency(
                    resolution,
                    dependency,
                )

        resolution.clusters = (
            self._build_clusters(
                resolution.entities,
                resolution.dependencies,
            )
        )

        resolution.confidence = (
            self._calculate_resolution_confidence(
                resolution
            )
        )

        resolution.metadata = {

            "resolver": self.__class__.__name__,

            "architecture": "Enterprise V13",

            "fact_count": resolution.fact_count,

            "entity_count": resolution.entity_count,

            "relation_count": resolution.relation_count,

            "dependency_count": resolution.dependency_count,

            "cluster_count": resolution.cluster_count,

        }

        return resolution

    # ================================================================
    # FACT EXTRACTION
    # ================================================================

    @staticmethod
    def _extract_facts(
        knowledge_document: Any,
    ) -> list[Any]:
        """
        Safely retrieve KnowledgeFact objects.

        Supports both:

            document.facts

        and documents where facts are stored inside
        sentences.
        """

        facts = getattr(
            knowledge_document,
            "facts",
            None,
        )

        if facts:

            return list(
                facts
            )

        sentences = getattr(
            knowledge_document,
            "sentences",
            [],
        ) or []

        output = []

        for sentence in sentences:

            sentence_facts = getattr(
                sentence,
                "facts",
                [],
            ) or []

            output.extend(
                sentence_facts
            )

        return output

    # ================================================================
    # SENTENCE COUNT
    # ================================================================

    @staticmethod
    def _sentence_count(
        knowledge_document: Any,
    ) -> int:

        sentences = getattr(
            knowledge_document,
            "sentences",
            [],
        ) or []

        if sentences:

            return len(
                sentences
            )

        return 0

    # ================================================================
    # INTERPRETATION
    # ================================================================

    @staticmethod
    def _get_interpretation(
        fact: Any,
    ) -> Any:

        return getattr(
            fact,
            "interpretation",
            None,
        )

    # ================================================================
    # SOURCE TEXT
    # ================================================================

    @staticmethod
    def _source_text(
        fact: Any,
        interpretation: Any,
    ) -> str:

        text = getattr(
            fact,
            "text",
            "",
        )

        if text:

            return str(
                text
            ).strip()

        text = getattr(
            interpretation,
            "original_text",
            "",
        )

        return str(
            text or ""
        ).strip()

    # ================================================================
    # STATEMENT ID
    # ================================================================

    @staticmethod
    def _statement_id(
        fact_index: int,
        fact: Any,
        interpretation: Any,
    ) -> str:

        metadata = getattr(
            interpretation,
            "metadata",
            {},
        )

        if isinstance(
            metadata,
            dict,
        ):

            value = metadata.get(
                "statement_id"
            )

            if value:

                return str(
                    value
                )

            value = metadata.get(
                "sentence_id"
            )

            if value:

                return str(
                    value
                )

        value = getattr(
            fact,
            "statement_id",
            "",
        )

        if value:

            return str(
                value
            )

        return (
            f"STATEMENT_{fact_index + 1}"
        )

    # ================================================================
    # INTERPRETATION → ENTITIES
    # ================================================================

    def _resolve_interpretation(
        self,
        interpretation: Any,
        fact: Any,
        statement_id: str,
        source_text: str,
    ) -> list[SemanticEntity]:

        entities: list[SemanticEntity] = []

        # ------------------------------------------------------------
        # Explicit entity collection
        # ------------------------------------------------------------

        raw_entities = getattr(
            interpretation,
            "entities",
            [],
        ) or []

        for item in raw_entities:

            entity_type = self._entity_type(
                item
            )

            entity = self._convert_knowledge_object(
                item=item,
                entity_type=entity_type,
                fact=fact,
                statement_id=statement_id,
                source_text=source_text,
            )

            if entity:

                entities.append(
                    entity
                )

        # ------------------------------------------------------------
        # If the interpretation has no explicit entities,
        # inspect the structured fields.
        # ------------------------------------------------------------

        if not entities:

            structured_fields = (
                "action",
                "target",
                "domain",
                "metric",
                "measurement",
                "practice",
            )

            for field_name in structured_fields:

                item = getattr(
                    interpretation,
                    field_name,
                    None,
                )

                if item is None:

                    continue

                entity = self._convert_knowledge_object(
                    item=item,
                    entity_type=field_name,
                    fact=fact,
                    statement_id=statement_id,
                    source_text=source_text,
                )

                if entity:

                    entities.append(
                        entity
                    )

            modifiers = getattr(
                interpretation,
                "modifiers",
                [],
            ) or []

            for item in modifiers:

                entity = self._convert_knowledge_object(
                    item=item,
                    entity_type="modifier",
                    fact=fact,
                    statement_id=statement_id,
                    source_text=source_text,
                )

                if entity:

                    entities.append(
                        entity
                    )

        return self._deduplicate_entities(
            entities
        )

    # ================================================================
    # KNOWLEDGE OBJECT → SEMANTIC ENTITY
    # ================================================================

    def _convert_knowledge_object(
        self,
        item: Any,
        entity_type: str,
        fact: Any,
        statement_id: str,
        source_text: str,
    ) -> SemanticEntity | None:

        if item is None:

            return None

        # ------------------------------------------------------------
        # Already SemanticEntity
        # ------------------------------------------------------------

        if isinstance(
            item,
            SemanticEntity,
        ):

            if not item.fact_id:

                item.fact_id = self._fact_id(
                    fact
                )

            if not item.statement_id:

                item.statement_id = (
                    statement_id
                )

            if not item.source_text:

                item.source_text = (
                    source_text
                )

            return item

        # ------------------------------------------------------------
        # Identity
        # ------------------------------------------------------------

        canonical = self._first_value(
            item,
            (
                "canonical",
                "name",
                "label",
                "normalized",
                "original",
                "matched_phrase",
            ),
        )

        original = self._first_value(
            item,
            (
                "original",
                "matched_phrase",
                "canonical",
                "name",
                "label",
            ),
        )

        normalized = self._first_value(
            item,
            (
                "normalized",
                "canonical",
                "original",
            ),
        )

        if not canonical and not original:

            return None

        canonical = str(
            canonical or original
        ).strip()

        original = str(
            original or canonical
        ).strip()

        normalized = str(
            normalized or canonical
        ).strip().casefold()

        if not canonical:

            return None

        # ------------------------------------------------------------
        # Entity ID
        # ------------------------------------------------------------

        entity_id = self._entity_id(
            item=item,
            entity_type=entity_type,
            canonical=canonical,
            fact=fact,
        )

        # ------------------------------------------------------------
        # Metadata
        # ------------------------------------------------------------

        metadata = getattr(
            item,
            "metadata",
            {},
        )

        if not isinstance(
            metadata,
            dict,
        ):

            metadata = {}

        metadata = dict(
            metadata
        )

        metadata.setdefault(
            "source_text",
            source_text,
        )

        metadata.setdefault(
            "fact_id",
            self._fact_id(fact),
        )

        metadata.setdefault(
            "statement_id",
            statement_id,
        )

        # ------------------------------------------------------------
        # Build semantic entity
        # ------------------------------------------------------------

        return SemanticEntity(

            entity_id=entity_id,

            entity_type=(
                entity_type
                or getattr(
                    item,
                    "entity_type",
                    "",
                )
                or "unknown"
            ),

            canonical=canonical,

            normalized=normalized,

            original=original,

            label=canonical,

            category=str(
                getattr(
                    item,
                    "category",
                    "",
                )
                or ""
            ),

            ontology_name=str(
                getattr(
                    item,
                    "ontology_name",
                    "",
                )
                or ""
            ),

            primary_domain=str(
                getattr(
                    item,
                    "primary_domain",
                    getattr(
                        item,
                        "domain",
                        "",
                    ),
                )
                or ""
            ),

            business_area=str(
                getattr(
                    item,
                    "business_area",
                    "",
                )
                or ""
            ),

            semantic_type=(
                entity_type
                or "unknown"
            ),

            fact_id=self._fact_id(
                fact
            ),

            statement_id=statement_id,

            sentence_index=self._int_value(
                item,
                "sentence_index",
                self._int_value(
                    fact,
                    "sentence_index",
                    -1,
                ),
            ),

            start_char=self._int_value(
                item,
                "start_char",
                -1,
            ),

            end_char=self._int_value(
                item,
                "end_char",
                -1,
            ),

            token_index=self._int_value(
                item,
                "token_index",
                -1,
            ),

            token_count=self._int_value(
                item,
                "token_count",
                0,
            ),

            source_text=source_text,

            source="resume",

            extraction_method=str(
                getattr(
                    item,
                    "extraction_method",
                    "",
                )
                or ""
            ),

            description=str(
                getattr(
                    item,
                    "description",
                    "",
                )
                or ""
            ),

            business_meaning=str(
                getattr(
                    item,
                    "business_meaning",
                    "",
                )
                or ""
            ),

            confidence=self._float_value(
                item,
                "confidence",
                self._float_value(
                    fact,
                    "confidence",
                    0.0,
                ),
            ),

            impact_weight=self._float_value(
                item,
                "impact_weight",
                1.0,
            ),

            achievement=self._bool_value(
                item,
                "achievement",
                self._bool_value(
                    fact,
                    "achievement",
                    False,
                ),
            ),

            quantified=self._bool_value(
                item,
                "quantified",
                self._bool_value(
                    fact,
                    "quantified",
                    False,
                ),
            ),

            preferred_direction=str(
                getattr(
                    item,
                    "preferred_direction",
                    "",
                )
                or ""
            ),

            preferred_unit=str(
                getattr(
                    item,
                    "preferred_unit",
                    "",
                )
                or ""
            ),

            higher_is_better=self._bool_value(
                item,
                "higher_is_better",
                True,
            ),

            related_metrics=list(
                getattr(
                    item,
                    "related_metrics",
                    [],
                )
                or []
            ),

            knowledge_object=item,

            ontology_object=getattr(
                item,
                "ontology_object",
                None,
            ),

            metadata=metadata,
        )

    # ================================================================
    # ENTITY TYPE
    # ================================================================

    @staticmethod
    def _entity_type(
        item: Any,
    ) -> str:

        value = getattr(
            item,
            "entity_type",
            "",
        )

        if value:

            return str(
                value
            ).strip().casefold()

        value = getattr(
            item,
            "type",
            "",
        )

        if value:

            return str(
                value
            ).strip().casefold()

        value = getattr(
            item,
            "semantic_type",
            "",
        )

        if value:

            return str(
                value
            ).strip().casefold()

        return (
            item.__class__.__name__
            .replace(
                "Knowledge",
                "",
            )
            .casefold()
        )

    # ================================================================
    # RELATION BUILDING
    # ================================================================

    def _build_relations(
        self,
        entities: list[SemanticEntity],
        interpretation: Any,
        fact: Any,
        statement_id: str,
        source_text: str,
    ) -> list[StatementRelation]:

        if len(
            entities
        ) < 2:

            return []

        relations: list[
            StatementRelation
        ] = []

        action_entities = [
            entity
            for entity in entities
            if entity.entity_type
            .casefold()
            == "action"
        ]

        target_entities = [
            entity
            for entity in entities
            if entity.entity_type
            .casefold()
            in {
                "target",
                "object",
                "practice",
            }
        ]

        metric_entities = [
            entity
            for entity in entities
            if entity.entity_type
            .casefold()
            in {
                "metric",
                "kpi",
                "business_kpi",
            }
        ]

        domain_entities = [
            entity
            for entity in entities
            if entity.entity_type
            .casefold()
            == "domain"
        ]

        # ------------------------------------------------------------
        # ACTION → TARGET
        # ------------------------------------------------------------

        for action in action_entities:

            for target in target_entities:

                relations.append(
                    self._relation(
                        relation_type="ACTS_ON",
                        source=action,
                        target=target,
                        fact=fact,
                        statement_id=statement_id,
                        source_text=source_text,
                    )
                )

        # ------------------------------------------------------------
        # ACTION → METRIC
        # ------------------------------------------------------------

        for action in action_entities:

            for metric in metric_entities:

                relations.append(
                    self._relation(
                        relation_type="AFFECTS",
                        source=action,
                        target=metric,
                        fact=fact,
                        statement_id=statement_id,
                        source_text=source_text,
                    )
                )

        # ------------------------------------------------------------
        # ACTION → DOMAIN
        # ------------------------------------------------------------

        for action in action_entities:

            for domain in domain_entities:

                relations.append(
                    self._relation(
                        relation_type="BELONGS_TO",
                        source=action,
                        target=domain,
                        fact=fact,
                        statement_id=statement_id,
                        source_text=source_text,
                    )
                )

        return self._deduplicate_relations(
            relations
        )

    # ================================================================
    # DEPENDENCY BUILDING
    # ================================================================

    def _build_dependencies(
        self,
        entities: list[SemanticEntity],
        relations: list[StatementRelation],
        fact: Any,
        statement_id: str,
    ) -> list[SemanticDependency]:

        dependencies: list[
            SemanticDependency
        ] = []

        for relation in relations:

            dependencies.append(

                SemanticDependency(

                    dependency_id=(
                        f"DEP_"
                        f"{relation.source_id}_"
                        f"{relation.relation_type}_"
                        f"{relation.target_id}"
                    ),

                    dependency_type=(
                        relation.relation_type
                    ),

                    source_id=(
                        relation.source_id
                    ),

                    target_id=(
                        relation.target_id
                    ),

                    confidence=(
                        relation.confidence
                    ),

                    weight=(
                        relation.weight
                    ),

                    fact_id=(
                        self._fact_id(
                            fact
                        )
                    ),

                    statement_id=(
                        statement_id
                    ),

                    sentence_index=(
                        relation.sentence_index
                    ),

                    explanation=(
                        relation.explanation
                    ),

                    evidence=[
                        relation.source_text
                    ],

                    metadata={
                        "relation_type":
                            relation.relation_type,
                    },
                )
            )

        return self._deduplicate_dependencies(
            dependencies
        )

    # ================================================================
    # RELATION OBJECT
    # ================================================================

    @staticmethod
    def _relation(
        relation_type: str,
        source: SemanticEntity,
        target: SemanticEntity,
        fact: Any,
        statement_id: str,
        source_text: str,
    ) -> StatementRelation:

        confidence = min(
            source.confidence,
            target.confidence,
        )

        relation_id = (
            f"REL_"
            f"{source.entity_id}_"
            f"{relation_type}_"
            f"{target.entity_id}"
        )

        explanation = (
            f"{source.canonical} "
            f"{relation_type.replace('_', ' ').lower()} "
            f"{target.canonical}"
        )

        return StatementRelation(

            relation_id=relation_id,

            relation_type=relation_type,

            source_id=source.entity_id,

            target_id=target.entity_id,

            confidence=confidence,

            weight=min(
                source.impact_weight,
                target.impact_weight,
            ),

            fact_id=(
                SemanticResolver._fact_id(
                    fact
                )
            ),

            statement_id=statement_id,

            sentence_index=(
                source.sentence_index
            ),

            source_text=source_text,

            explanation=explanation,

            metadata={
                "source_type":
                    source.entity_type,

                "target_type":
                    target.entity_type,
            },
        )

    # ================================================================
    # CLUSTER BUILDING
    # ================================================================

    @staticmethod
    def _build_clusters(
        entities: list[SemanticEntity],
        dependencies: list[SemanticDependency],
    ) -> list[SemanticCluster]:

        if not entities:

            return []

        clusters: dict[
            str,
            SemanticCluster,
        ] = {}

        # ------------------------------------------------------------
        # Group by business area/domain
        # ------------------------------------------------------------

        for entity in entities:

            key = (
                entity.business_area
                or entity.primary_domain
                or entity.entity_type
                or "general"
            ).strip().casefold()

            if not key:

                key = "general"

            if key not in clusters:

                cluster_id = (
                    "CLUSTER_"
                    + SemanticResolver._safe_id(
                        key
                    )
                )

                clusters[key] = (
                    SemanticCluster(
                        cluster_id=cluster_id,

                        label=(
                            entity.business_area
                            or entity.primary_domain
                            or entity.entity_type
                            or "General"
                        ),

                        cluster_type=(
                            "business_area"
                            if entity.business_area
                            else "domain"
                        ),

                        primary_domain=(
                            entity.primary_domain
                        ),

                        business_area=(
                            entity.business_area
                        ),

                        confidence=(
                            entity.confidence
                        ),
                    )
                )

            clusters[key].add_entity(
                entity.entity_id
            )

            clusters[key].confidence = max(
                clusters[key].confidence,
                entity.confidence,
            )

        # ------------------------------------------------------------
        # Attach dependencies
        # ------------------------------------------------------------

        for dependency in dependencies:

            for cluster in clusters.values():

                if (
                    dependency.source_id
                    in cluster.entity_ids
                    or
                    dependency.target_id
                    in cluster.entity_ids
                ):

                    cluster.add_dependency(
                        dependency.dependency_id
                    )

        return list(
            clusters.values()
        )

    # ================================================================
    # DEDUPLICATION
    # ================================================================

    @staticmethod
    def _deduplicate_entities(
        entities: Iterable[
            SemanticEntity
        ],
    ) -> list[SemanticEntity]:

        output: list[
            SemanticEntity
        ] = []

        seen = set()

        for entity in entities:

            key = (
                entity.entity_id
                or
                (
                    entity.entity_type,
                    entity.normalized,
                    entity.statement_id,
                )
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            output.append(
                entity
            )

        return output

    @staticmethod
    def _deduplicate_relations(
        relations: Iterable[
            StatementRelation
        ],
    ) -> list[StatementRelation]:

        output = []

        seen = set()

        for relation in relations:

            key = (
                relation.source_id,
                relation.relation_type,
                relation.target_id,
                relation.statement_id,
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            output.append(
                relation
            )

        return output

    @staticmethod
    def _deduplicate_dependencies(
        dependencies: Iterable[
            SemanticDependency
        ],
    ) -> list[SemanticDependency]:

        output = []

        seen = set()

        for dependency in dependencies:

            key = (
                dependency.source_id,
                dependency.dependency_type,
                dependency.target_id,
                dependency.statement_id,
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            output.append(
                dependency
            )

        return output

    # ================================================================
    # RESOLUTION DEDUPLICATION
    # ================================================================

    @staticmethod
    def _append_unique_entity(
        resolution: SemanticResolution,
        entity: SemanticEntity,
    ) -> None:

        for existing in resolution.entities:

            if (
                existing.entity_id
                == entity.entity_id
            ):

                return

        resolution.entities.append(
            entity
        )

    @staticmethod
    def _append_unique_relation(
        resolution: SemanticResolution,
        relation: StatementRelation,
    ) -> None:

        for existing in resolution.relations:

            if (
                existing.source_id
                == relation.source_id
                and
                existing.target_id
                == relation.target_id
                and
                existing.relation_type
                == relation.relation_type
                and
                existing.statement_id
                == relation.statement_id
            ):

                return

        resolution.relations.append(
            relation
        )

    @staticmethod
    def _append_unique_dependency(
        resolution: SemanticResolution,
        dependency: SemanticDependency,
    ) -> None:

        for existing in resolution.dependencies:

            if (
                existing.source_id
                == dependency.source_id
                and
                existing.target_id
                == dependency.target_id
                and
                existing.dependency_type
                == dependency.dependency_type
                and
                existing.statement_id
                == dependency.statement_id
            ):

                return

        resolution.dependencies.append(
            dependency
        )

    # ================================================================
    # RESOLUTION CONFIDENCE
    # ================================================================

    @staticmethod
    def _calculate_resolution_confidence(
        resolution: SemanticResolution,
    ) -> float:

        if not resolution.entities:

            return 0.0

        total = sum(
            entity.confidence
            for entity in resolution.entities
        )

        return (
            total
            / len(
                resolution.entities
            )
        )

    # ================================================================
    # VALUE HELPERS
    # ================================================================

    @staticmethod
    def _first_value(
        obj: Any,
        names: tuple[str, ...],
    ) -> Any:

        for name in names:

            try:

                value = getattr(
                    obj,
                    name,
                    None,
                )

            except Exception:

                value = None

            if value not in (
                None,
                "",
                [],
                {},
            ):

                return value

        return None

    @staticmethod
    def _float_value(
        obj: Any,
        name: str,
        default: float,
    ) -> float:

        value = getattr(
            obj,
            name,
            default,
        )

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return default

    @staticmethod
    def _int_value(
        obj: Any,
        name: str,
        default: int,
    ) -> int:

        value = getattr(
            obj,
            name,
            default,
        )

        try:

            return int(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return default

    @staticmethod
    def _bool_value(
        obj: Any,
        name: str,
        default: bool,
    ) -> bool:

        value = getattr(
            obj,
            name,
            default,
        )

        if isinstance(
            value,
            bool,
        ):

            return value

        if isinstance(
            value,
            str,
        ):

            return value.strip().casefold() in {
                "true",
                "1",
                "yes",
                "y",
            }

        return bool(
            value
        )

    # ================================================================
    # FACT ID
    # ================================================================

    @staticmethod
    def _fact_id(
        fact: Any,
    ) -> str:

        for field_name in (
            "fact_id",
            "id",
            "knowledge_id",
        ):

            value = getattr(
                fact,
                field_name,
                None,
            )

            if value:

                return str(
                    value
                )

        return (
            f"FACT_"
            f"{id(fact)}"
        )

    # ================================================================
    # ENTITY ID
    # ================================================================

    @staticmethod
    def _entity_id(
        item: Any,
        entity_type: str,
        canonical: str,
        fact: Any,
    ) -> str:

        existing = getattr(
            item,
            "entity_id",
            "",
        )

        if existing:

            return str(
                existing
            )

        fact_id = (
            SemanticResolver._fact_id(
                fact
            )
        )

        return (
            f"{entity_type.upper()}_"
            f"{SemanticResolver._safe_id(canonical)}_"
            f"{fact_id}"
        )

    # ================================================================
    # SAFE ID
    # ================================================================

    @staticmethod
    def _safe_id(
        value: str,
    ) -> str:

        value = str(
            value or ""
        ).strip().upper()

        output = []

        for character in value:

            if (
                character.isalnum()
                or character == "_"
            ):

                output.append(
                    character
                )

            else:

                output.append(
                    "_"
                )

        result = "".join(
            output
        )

        while "__" in result:

            result = result.replace(
                "__",
                "_",
            )

        return (
            result.strip("_")
            or "UNKNOWN"
        )


# =====================================================================
# PUBLIC EXPORT
# =====================================================================

__all__ = [
    "SemanticResolver",
]