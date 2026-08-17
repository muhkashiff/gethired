"""
Enterprise Business Statement Builder
Enterprise V14

Purpose
-------

Convert SemanticResolver output into BusinessStatement objects.

Architecture
------------

SemanticEntity[]
SemanticDependency[]
        ↓
BusinessStatementBuilder
        ↓
BusinessStatement[]
        ↓
KnowledgeGraphBuilder
        ↓
KnowledgeGraph
        ↓
Knowledge Profile

Design Principles
-----------------

1. BusinessStatement is the single source of truth for statement-level
   semantic information.

2. Every resolved entity is preserved.

3. Technologies remain entity_type="technology".

4. Methodologies remain entity_type="methodology".

5. Certifications remain entity_type="certification".

6. Standards remain entity_type="standard".

7. Entity metadata is preserved.

8. impact_weight is preserved exactly from the entity.

9. ATS-related information is preserved in metadata.

10. No scoring is performed here.

11. No ontology matching is performed here.

12. No graph construction is performed here.

13. No information is silently discarded.

14. The builder is deliberately tolerant of small differences between
    SemanticEntity / SemanticDependency implementations.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


# ============================================================================
# MODEL IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
)

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticEntity,
    StatementRelation,
)


# ============================================================================
# BUSINESS STATEMENT BUILDER
# ============================================================================


class BusinessStatementBuilder:
    """
    Convert semantic resolver output into BusinessStatement objects.

    Input
    -----

        semantic_resolution

    or, where required:

        semantic_entities
        semantic_dependencies

    Output
    ------

        list[BusinessStatement]

    The builder preserves the complete semantic information needed by
    KnowledgeGraphBuilder and the downstream Knowledge Profile layer.
    """

    # ========================================================================
    # INITIALIZATION
    # ========================================================================

    def __init__(self) -> None:

        pass

    # ========================================================================
    # PUBLIC API
    # ========================================================================

    def build(
        self,
        semantic_resolution: Any = None,
        entities: Optional[Iterable[Any]] = None,
        dependencies: Optional[Iterable[Any]] = None,
    ) -> list[BusinessStatement]:
        """
        Build BusinessStatement objects.

        Preferred usage:

            builder.build(
                semantic_resolution
            )

        Compatibility usage:

            builder.build(
                entities=entities,
                dependencies=dependencies,
            )

        Parameters
        ----------
        semantic_resolution:
            Result returned by SemanticResolver.

        entities:
            Optional explicit SemanticEntity collection.

        dependencies:
            Optional explicit SemanticDependency / relation collection.

        Returns
        -------
        list[BusinessStatement]
        """

        semantic_entities = self._extract_entities(
            semantic_resolution=semantic_resolution,
            entities=entities,
        )

        semantic_dependencies = self._extract_dependencies(
            semantic_resolution=semantic_resolution,
            dependencies=dependencies,
        )

        if not semantic_entities:
            return []

        # --------------------------------------------------------------------
        # Build entity lookup.
        # --------------------------------------------------------------------

        entity_map = self._build_entity_map(
            semantic_entities
        )

        # --------------------------------------------------------------------
        # Group entities into statements.
        #
        # Statement grouping is intentionally conservative.
        #
        # If an entity carries a statement_id, sentence_index or fact
        # reference, that information is used.
        #
        # Otherwise entities are grouped by sentence / source context.
        # --------------------------------------------------------------------

        groups = self._group_entities(
            semantic_entities
        )

        statements: list[BusinessStatement] = []

        for statement_id, statement_entities in groups.items():

            statement_dependencies = (
                self._dependencies_for_statement(
                    statement_id=statement_id,
                    statement_entities=statement_entities,
                    dependencies=semantic_dependencies,
                    entity_map=entity_map,
                )
            )

            statement = self._build_statement(
                statement_id=statement_id,
                entities=statement_entities,
                dependencies=statement_dependencies,
            )

            statements.append(
                statement
            )

        return statements

    # ========================================================================
    # ENTITY EXTRACTION
    # ========================================================================

    @staticmethod
    def _extract_entities(
        semantic_resolution: Any = None,
        entities: Optional[Iterable[Any]] = None,
    ) -> list[Any]:
        """
        Extract SemanticEntity objects from the semantic resolution.

        Supports:

            resolution.entities
            resolution.semantic_entities
            explicit entities argument
        """

        if entities is not None:

            return list(
                entities
            )

        if semantic_resolution is None:

            return []

        candidates = getattr(
            semantic_resolution,
            "entities",
            None,
        )

        if candidates is None:

            candidates = getattr(
                semantic_resolution,
                "semantic_entities",
                None,
            )

        if candidates is None:

            return []

        return list(
            candidates
        )

    # ========================================================================
    # DEPENDENCY EXTRACTION
    # ========================================================================

    @staticmethod
    def _extract_dependencies(
        semantic_resolution: Any = None,
        dependencies: Optional[Iterable[Any]] = None,
    ) -> list[Any]:
        """
        Extract semantic dependencies / relations.
        """

        if dependencies is not None:

            return list(
                dependencies
            )

        if semantic_resolution is None:

            return []

        candidates = getattr(
            semantic_resolution,
            "dependencies",
            None,
        )

        if candidates is None:

            candidates = getattr(
                semantic_resolution,
                "semantic_dependencies",
                None,
            )

        if candidates is None:

            return []

        return list(
            candidates
        )

    # ========================================================================
    # ENTITY MAP
    # ========================================================================

    @staticmethod
    def _build_entity_map(
        entities: list[Any],
    ) -> dict[str, Any]:
        """
        Build entity_id → SemanticEntity map.
        """

        result: dict[str, Any] = {}

        for entity in entities:

            entity_id = str(
                getattr(
                    entity,
                    "entity_id",
                    "",
                )
                or ""
            ).strip()

            if not entity_id:
                continue

            result[entity_id] = entity

        return result

    # ========================================================================
    # ENTITY GROUPING
    # ========================================================================

    def _group_entities(
        self,
        entities: list[Any],
    ) -> dict[str, list[Any]]:
        """
        Group entities into BusinessStatements.

        Priority:

            1. statement_id
            2. sentence_index
            3. fact/source grouping
            4. deterministic fallback

        This prevents unrelated entities from being merged simply because
        they have the same entity type.
        """

        groups: dict[str, list[Any]] = {}

        fallback_counter = 0

        for entity in entities:

            statement_id = self._entity_statement_id(
                entity
            )

            if not statement_id:

                sentence_index = getattr(
                    entity,
                    "sentence_index",
                    -1,
                )

                try:

                    sentence_index = int(
                        sentence_index
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    sentence_index = -1

                if sentence_index >= 0:

                    statement_id = (
                        f"sentence_{sentence_index}"
                    )

                else:

                    fallback_counter += 1

                    statement_id = (
                        f"statement_{fallback_counter}"
                    )

            groups.setdefault(
                statement_id,
                [],
            ).append(
                entity
            )

        return groups

    # ========================================================================
    # STATEMENT ID
    # ========================================================================

    @staticmethod
    def _entity_statement_id(
        entity: Any,
    ) -> str:
        """
        Obtain an existing statement identifier from an entity.
        """

        for attribute in (
            "statement_id",
            "business_statement_id",
            "source_statement_id",
            "fact_id",
            "source_fact_id",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                )

        return ""

    # ========================================================================
    # DEPENDENCIES FOR STATEMENT
    # ========================================================================

    def _dependencies_for_statement(
        self,
        statement_id: str,
        statement_entities: list[Any],
        dependencies: list[Any],
        entity_map: dict[str, Any],
    ) -> list[Any]:
        """
        Select relations belonging to the current statement.

        A relation is retained when:

        • it explicitly references an entity in the statement
        • both endpoints belong to the statement
        • it carries the same statement_id
        """

        entity_ids = {
            str(
                getattr(
                    entity,
                    "entity_id",
                    "",
                )
                or ""
            )
            for entity in statement_entities
        }

        entity_ids.discard("")

        selected: list[Any] = []

        for dependency in dependencies:

            dependency_statement_id = self._dependency_statement_id(
                dependency
            )

            if (
                dependency_statement_id
                and dependency_statement_id == statement_id
            ):

                selected.append(
                    dependency
                )

                continue

            source_id = self._dependency_source_id(
                dependency
            )

            target_id = self._dependency_target_id(
                dependency
            )

            if (
                source_id in entity_ids
                or target_id in entity_ids
            ):

                selected.append(
                    dependency
                )

        return self._deduplicate_dependencies(
            selected
        )

    # ========================================================================
    # DEPENDENCY HELPERS
    # ========================================================================

    @staticmethod
    def _dependency_statement_id(
        dependency: Any,
    ) -> str:

        for attribute in (
            "statement_id",
            "business_statement_id",
        ):

            value = getattr(
                dependency,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                )

        return ""

    # ------------------------------------------------------------------------

    @staticmethod
    def _dependency_source_id(
        dependency: Any,
    ) -> str:

        for attribute in (
            "source_id",
            "source_entity_id",
            "from_id",
        ):

            value = getattr(
                dependency,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                )

        return ""

    # ------------------------------------------------------------------------

    @staticmethod
    def _dependency_target_id(
        dependency: Any,
    ) -> str:

        for attribute in (
            "target_id",
            "target_entity_id",
            "to_id",
        ):

            value = getattr(
                dependency,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                )

        return ""

    # ========================================================================
    # BUILD SINGLE STATEMENT
    # ========================================================================

    def _build_statement(
        self,
        statement_id: str,
        entities: list[Any],
        dependencies: list[Any],
    ) -> BusinessStatement:
        """
        Convert one entity group into BusinessStatement.
        """

        statement_label = self._build_label(
            entities
        )

        confidence = self._statement_confidence(
            entities
        )

        semantic_type = self._statement_semantic_type(
            entities
        )

        primary_domain = self._primary_value(
            entities,
            "primary_domain",
            "domain",
        )

        business_area = self._primary_value(
            entities,
            "business_area",
        )

        achievement = any(
            bool(
                getattr(
                    entity,
                    "achievement",
                    False,
                )
            )
            for entity in entities
        )

        statement_entities = []

        for entity in entities:

            normalized_entity = (
                self._normalize_entity(
                    entity
                )
            )

            statement_entities.append(
                normalized_entity
            )

        statement_relations = []

        for dependency in dependencies:

            relation = (
                self._normalize_relation(
                    dependency
                )
            )

            if relation is not None:

                statement_relations.append(
                    relation
                )

        technologies = [
            entity
            for entity in statement_entities
            if self._entity_type(
                entity
            ) == "technologie"
        ]

        methodologies = [
            entity
            for entity in statement_entities
            if self._entity_type(
                entity
            ) == "methodologie"
        ]

        metadata = self._build_statement_metadata(
            entities=statement_entities,
            relations=statement_relations,
        )

        # Preserve technology and methodology as explicit single entity
        # categories while also making them available through statement
        # compatibility fields.
        metadata["technologie_count"] = len(
            technologies
        )

        metadata["methodologie_count"] = len(
            methodologies
        )

        metadata["certification_count"] = len(
            [
                entity
                for entity in statement_entities
                if self._entity_type(entity)
                == "certification"
            ]
        )

        metadata["standard_count"] = len(
            [
                entity
                for entity in statement_entities
                if self._entity_type(entity)
                == "standard"
            ]
        )

        return BusinessStatement(

            statement_id=statement_id,

            label=statement_label,

            confidence=confidence,

            semantic_type=semantic_type,

            primary_domain=primary_domain,

            business_area=business_area,

            achievement=achievement,

            metadata=metadata,

            technologies=technologies,

            entities=statement_entities,

            relations=statement_relations,
        )

    # ========================================================================
    # ENTITY NORMALIZATION
    # ========================================================================

    @staticmethod
    def _normalize_entity(
        entity: Any,
    ) -> Any:
        """
        Preserve the original SemanticEntity object.

        We intentionally do not rebuild the entity into a smaller object.

        This is critical because the entity may contain:

            impact_weight
            ATS score information
            ontology information
            metadata
            confidence
            business meaning
            direction
            unit
            aliases
            repository object

        Returning the original object prevents information loss.
        """

        return entity

    # ========================================================================
    # RELATION NORMALIZATION
    # ========================================================================

    @staticmethod
    def _normalize_relation(
        dependency: Any,
    ) -> Optional[Any]:
        """
        Convert a semantic dependency into StatementRelation.

        If dependency is already a StatementRelation, preserve it.

        Otherwise construct a StatementRelation using the fields that
        are available.
        """

        if dependency is None:

            return None

        if isinstance(
            dependency,
            StatementRelation,
        ):

            return dependency

        relation_type = ""

        for attribute in (
            "relation_type",
            "relation",
            "type",
        ):

            value = getattr(
                dependency,
                attribute,
                None,
            )

            if value:

                relation_type = str(
                    value
                ).upper()

                break

        source_id = (
            BusinessStatementBuilder
            ._dependency_source_id(
                dependency
            )
        )

        target_id = (
            BusinessStatementBuilder
            ._dependency_target_id(
                dependency
            )
        )

        if not relation_type:

            relation_type = "RELATED_TO"

        try:

            return StatementRelation(

                source_id=source_id,

                target_id=target_id,

                relation_type=relation_type,

            )

        except TypeError:

            # Some versions may contain additional required fields.
            # If the object cannot be constructed safely, preserve the
            # dependency itself rather than silently losing it.
            return dependency

    # ========================================================================
    # LABEL
    # ========================================================================

    @staticmethod
    def _build_label(
        entities: list[Any],
    ) -> str:
        """
        Generate a human-readable statement label.
        """

        if not entities:

            return ""

        action = next(
            (
                entity
                for entity in entities
                if BusinessStatementBuilder._entity_type(
                    entity
                ) == "action"
            ),
            None,
        )

        target = next(
            (
                entity
                for entity in entities
                if BusinessStatementBuilder._entity_type(
                    entity
                ) in {
                    "target",
                    "object",
                }
            ),
            None,
        )

        if action is not None:

            action_name = (
                BusinessStatementBuilder
                ._entity_display_name(
                    action
                )
            )

            if target is not None:

                target_name = (
                    BusinessStatementBuilder
                    ._entity_display_name(
                        target
                    )
                )

                if target_name:

                    return (
                        f"{action_name} "
                        f"{target_name}"
                    )

            if action_name:

                return action_name

        names = []

        for entity in entities:

            name = (
                BusinessStatementBuilder
                ._entity_display_name(
                    entity
                )
            )

            if name and name not in names:

                names.append(
                    name
                )

        return " | ".join(
            names[:8]
        )

    # ========================================================================
    # DISPLAY NAME
    # ========================================================================

    @staticmethod
    def _entity_display_name(
        entity: Any,
    ) -> str:

        for attribute in (
            "canonical",
            "name",
            "normalized",
            "original",
            "label",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            if value:

                return str(
                    value
                ).strip()

        return ""

    # ========================================================================
    # ENTITY TYPE
    # ========================================================================

    @staticmethod
    def _entity_type(
        entity: Any,
    ) -> str:

        return str(
            getattr(
                entity,
                "entity_type",
                "",
            )
            or ""
        ).strip().casefold()

    # ========================================================================
    # STATEMENT SEMANTIC TYPE
    # ========================================================================

    @staticmethod
    def _statement_semantic_type(
        entities: list[Any],
    ) -> str:
        """
        Determine the dominant semantic type.

        Achievement takes priority because it is important for downstream
        business-value scoring.
        """

        if any(
            bool(
                getattr(
                    entity,
                    "achievement",
                    False,
                )
            )
            for entity in entities
        ):

            return "achievement"

        entity_types = [
            BusinessStatementBuilder._entity_type(
                entity
            )
            for entity in entities
        ]

        if "action" in entity_types:

            return "action_statement"

        if "kpi" in entity_types:

            return "kpi_statement"

        if "metric" in entity_types:

            return "metric_statement"

        if "technologie" in entity_types:

            return "technologie_statement"

        if "certification" in entity_types:

            return "certification_statement"

        if "standard" in entity_types:

            return "standard_statement"

        return (
            entity_types[0]
            if entity_types
            else ""
        )

    # ========================================================================
    # PRIMARY VALUE
    # ========================================================================

    @staticmethod
    def _primary_value(
        entities: list[Any],
        *attributes: str,
    ) -> str:
        """
        Find the first useful value across candidate attributes.
        """

        for entity in entities:

            for attribute in attributes:

                value = getattr(
                    entity,
                    attribute,
                    None,
                )

                if value:

                    return str(
                        value
                    ).strip()

        return ""

    # ========================================================================
    # CONFIDENCE
    # ========================================================================

    @classmethod
    def _statement_confidence(
        cls,
        entities: list[Any],
    ) -> float:
        """
        Calculate statement confidence from entity confidence.

        This does NOT use impact_weight as confidence.

        impact_weight is a business importance value and must remain
        independent from extraction confidence.
        """

        values = []

        for entity in entities:

            value = getattr(
                entity,
                "confidence",
                None,
            )

            try:

                if value is not None:

                    values.append(
                        float(value)
                    )

            except (
                TypeError,
                ValueError,
            ):

                continue

        if not values:

            return 1.0

        return round(
            sum(values) / len(values),
            4,
        )

    # ========================================================================
    # STATEMENT METADATA
    # ========================================================================

    @classmethod
    def _build_statement_metadata(
        cls,
        entities: list[Any],
        relations: list[Any],
    ) -> dict:
        """
        Preserve important information at statement level.

        Entity-level information remains on each SemanticEntity.
        This metadata provides an aggregated view for downstream systems.
        """

        metadata = {}

        # --------------------------------------------------------------------
        # Impact
        # --------------------------------------------------------------------

        impact_weights = []

        for entity in entities:

            value = getattr(
                entity,
                "impact_weight",
                None,
            )

            try:

                if value is not None:

                    impact_weights.append(
                        float(value)
                    )

            except (
                TypeError,
                ValueError,
            ):

                continue

        if impact_weights:

            metadata[
                "impact_weight"
            ] = round(
                max(
                    impact_weights
                ),
                4,
            )

            metadata[
                "impact_weight_sum"
            ] = round(
                sum(
                    impact_weights
                ),
                4,
            )

            metadata[
                "impact_weight_average"
            ] = round(
                sum(
                    impact_weights
                )
                / len(
                    impact_weights
                ),
                4,
            )

        # --------------------------------------------------------------------
        # ATS
        # --------------------------------------------------------------------

        ats_values = []

        for entity in entities:

            value = cls._extract_ats_value(
                entity
            )

            if value is not None:

                ats_values.append(
                    value
                )

        if ats_values:

            metadata[
                "ats_score"
            ] = round(
                max(
                    ats_values
                ),
                4,
            )

            metadata[
                "ats_score_average"
            ] = round(
                sum(
                    ats_values
                )
                / len(
                    ats_values
                ),
                4,
            )

        # --------------------------------------------------------------------
        # Entity type inventory
        # --------------------------------------------------------------------

        type_counts = {}

        for entity in entities:

            entity_type = cls._entity_type(
                entity
            )

            if not entity_type:

                continue

            type_counts[
                entity_type
            ] = (
                type_counts.get(
                    entity_type,
                    0,
                )
                + 1
            )

        metadata[
            "entity_type_counts"
        ] = type_counts

        # --------------------------------------------------------------------
        # Relations
        # --------------------------------------------------------------------

        metadata[
            "relation_count"
        ] = len(
            relations
        )

        metadata[
            "relation_types"
        ] = sorted(
            {
                str(
                    getattr(
                        relation,
                        "relation_type",
                        getattr(
                            relation,
                            "relation",
                            "",
                        ),
                    )
                    or ""
                ).upper()
                for relation in relations
                if getattr(
                    relation,
                    "relation_type",
                    getattr(
                        relation,
                        "relation",
                        "",
                    ),
                )
            }
        )

        # --------------------------------------------------------------------
        # Technologies
        # --------------------------------------------------------------------

        metadata[
            "technologies"
        ] = [
            cls._entity_display_name(
                entity
            )
            for entity in entities
            if cls._entity_type(
                entity
            ) == "technologie"
        ]

        # --------------------------------------------------------------------
        # Methodologies
        # --------------------------------------------------------------------

        metadata[
            "methodologies"
        ] = [
            cls._entity_display_name(
                entity
            )
            for entity in entities
            if cls._entity_type(
                entity
            ) == "methodologie"
        ]

        # --------------------------------------------------------------------
        # Certifications
        # --------------------------------------------------------------------

        metadata[
            "certifications"
        ] = [
            cls._entity_display_name(
                entity
            )
            for entity in entities
            if cls._entity_type(
                entity
            ) == "certification"
        ]

        # --------------------------------------------------------------------
        # Standards
        # --------------------------------------------------------------------

        metadata[
            "standards"
        ] = [
            cls._entity_display_name(
                entity
            )
            for entity in entities
            if cls._entity_type(
                entity
            ) == "standard"
        ]

        return metadata

    # ========================================================================
    # ATS EXTRACTION
    # ========================================================================

    @staticmethod
    def _extract_ats_value(
        entity: Any,
    ) -> Optional[float]:
        """
        Extract an entity ATS score without assuming one exact model layout.

        Supported examples:

            entity.ats_score
            entity.ats_weight
            entity.metadata["ats_score"]
            entity.metadata["ats_weight"]
            entity.metadata["ats"]["score"]
        """

        for attribute in (
            "ats_score",
            "ats_weight",
        ):

            value = getattr(
                entity,
                attribute,
                None,
            )

            if value is not None:

                try:

                    return float(
                        value
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        metadata = getattr(
            entity,
            "metadata",
            None,
        )

        if not isinstance(
            metadata,
            dict,
        ):

            return None

        for key in (
            "ats_score",
            "ats_weight",
        ):

            value = metadata.get(
                key
            )

            if value is not None:

                try:

                    return float(
                        value
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

        ats = metadata.get(
            "ats"
        )

        if isinstance(
            ats,
            dict,
        ):

            for key in (
                "score",
                "weight",
            ):

                value = ats.get(
                    key
                )

                if value is not None:

                    try:

                        return float(
                            value
                        )

                    except (
                        TypeError,
                        ValueError,
                    ):

                        pass

        return None

    # ========================================================================
    # DEPENDENCY DEDUPLICATION
    # ========================================================================

    @classmethod
    def _deduplicate_dependencies(
        cls,
        dependencies: list[Any],
    ) -> list[Any]:
        """
        Deduplicate semantic relations.
        """

        result = []

        seen = set()

        for dependency in dependencies:

            source_id = cls._dependency_source_id(
                dependency
            )

            target_id = cls._dependency_target_id(
                dependency
            )

            relation_type = str(
                getattr(
                    dependency,
                    "relation_type",
                    getattr(
                        dependency,
                        "relation",
                        "",
                    ),
                )
                or ""
            ).upper()

            key = (
                source_id,
                target_id,
                relation_type,
            )

            if key in seen:

                continue

            seen.add(
                key
            )

            result.append(
                dependency
            )

        return result


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================


def build_business_statements(
    semantic_resolution: Any = None,
    entities: Optional[Iterable[Any]] = None,
    dependencies: Optional[Iterable[Any]] = None,
) -> list[BusinessStatement]:
    """
    Convenience API.

    Example
    -------

        statements = build_business_statements(
            semantic_resolution
        )
    """

    builder = (
        BusinessStatementBuilder()
    )

    return builder.build(
        semantic_resolution=semantic_resolution,
        entities=entities,
        dependencies=dependencies,
    )


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "BusinessStatementBuilder",
    "build_business_statements",
]