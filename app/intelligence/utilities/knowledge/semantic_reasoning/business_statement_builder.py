"""
Enterprise Business Statement Builder
=====================================

Enterprise V18 - Object-Oriented Boundary

Purpose
-------

Convert semantic resolver output into BusinessStatement objects.

Architecture
------------

    SemanticResolution
            |
            v
    BusinessStatementBuilder
            |
            v
    list[BusinessStatement]

Important
---------

This builder creates BusinessStatement objects.

It does NOT create dictionaries as its primary output.

Clusters are the primary grouping mechanism.

Relations/dependencies are the fallback grouping mechanism.

Individual entities are the final fallback.

Source evidence is preserved whenever it is available on the semantic
entities. The builder never intentionally replaces source evidence with
classifier-generated text when actual source text exists.
"""

from __future__ import annotations

from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Set,
)

import logging
import uuid

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    BusinessStatement,
    SemanticEntity,
    StatementRelation,
    SemanticDependency,
    SemanticCluster,
    SemanticResolution,
)


logger = logging.getLogger(__name__)


# ============================================================================
# BUILDER
# ============================================================================


class BusinessStatementBuilder:
    """
    Convert semantic resolver output into BusinessStatement objects.

    Primary grouping:

        SemanticCluster

    Fallback:

        SemanticDependency / relation

    Final fallback:

        Individual semantic entities
    """

    def __init__(
        self,
    ) -> None:

        self.statements: List[
            BusinessStatement
        ] = []

        self.logger = logger

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def build(
        self,
        semantic_resolution: Any = None,
        entities: Optional[
            Iterable[Any]
        ] = None,
        dependencies: Optional[
            Iterable[Any]
        ] = None,
        clusters: Optional[
            Iterable[Any]
        ] = None,
        source: str = "",
    ) -> list[BusinessStatement]:
        """
        Build BusinessStatement objects.

        Object In
            SemanticResolution / semantic objects

        Object Out
            list[BusinessStatement]

        Parameters
        ----------
        source:
            Optional source label such as:

                "resume"
                "jd"

            If omitted, the builder attempts to recover source metadata
            from the semantic resolution/entities.
        """

        self.logger.info(
            "Starting BusinessStatementBuilder.build()"
        )

        semantic_entities = (
            self._extract_entities(
                semantic_resolution,
                entities,
            )
        )

        self.logger.info(
            "Extracted %s semantic entities",
            len(semantic_entities),
        )

        if not semantic_entities:

            self.logger.warning(
                "No semantic entities found"
            )

            self.statements = []

            return []

        semantic_dependencies = (
            self._extract_dependencies(
                semantic_resolution,
                dependencies,
            )
        )

        self.logger.info(
            "Extracted %s semantic dependencies",
            len(semantic_dependencies),
        )

        semantic_clusters = (
            self._extract_clusters(
                semantic_resolution,
                clusters,
            )
        )

        self.logger.info(
            "Extracted %s semantic clusters",
            len(semantic_clusters),
        )

        entity_map = (
            self._build_entity_map(
                semantic_entities
            )
        )

        # ---------------------------------------------------------------------
        # Resolve source once.
        # ---------------------------------------------------------------------

        resolved_source = (
            self._resolve_source(
                source,
                semantic_resolution,
                semantic_entities,
            )
        )

        # ---------------------------------------------------------------------
        # PRIMARY GROUPING
        # ---------------------------------------------------------------------

        groups = (
            self._group_by_clusters(
                semantic_clusters,
                entity_map,
            )
        )

        if groups:

            self.logger.info(
                "Created %s groups from clusters",
                len(groups),
            )

        else:

            self.logger.warning(
                "No groups from clusters - "
                "trying fallback grouping"
            )

            groups = (
                self._group_by_relations(
                    semantic_entities,
                    semantic_dependencies,
                )
            )

        # ---------------------------------------------------------------------
        # FINAL GROUPING FALLBACK
        # ---------------------------------------------------------------------

        if not groups:

            self.logger.warning(
                "No groups from relations - "
                "creating individual statements"
            )

            groups = (
                self._group_individual_entities(
                    semantic_entities
                )
            )

        # ---------------------------------------------------------------------
        # BUILD BUSINESS STATEMENTS
        # ---------------------------------------------------------------------

        statements: list[
            BusinessStatement
        ] = []

        for group_id, group_entities in groups.items():

            if not group_entities:
                continue

            group_deps = (
                self._find_dependencies_for_group(
                    group_entities,
                    semantic_dependencies,
                    entity_map,
                )
            )

            statement = (
                self._create_statement(
                    group_id=group_id,
                    entities=group_entities,
                    dependencies=group_deps,
                    entity_map=entity_map,
                    source=resolved_source,
                )
            )

            if (
                statement is not None
                and statement.is_valid
            ):

                statements.append(
                    statement
                )

        self.statements = statements

        self.logger.info(
            "Generated %s business statements",
            len(statements),
        )

        return statements

    # =========================================================================
    # EXTRACTION
    # =========================================================================

    @staticmethod
    def _extract_entities(
        resolution: Any,
        entities: Optional[
            Iterable[Any]
        ],
    ) -> list[Any]:
        """
        Extract semantic entities from the resolution or direct input.
        """

        if entities is not None:
            return list(
                entities
            )

        if resolution is None:
            return []

        for field in (
            "entities",
            "semantic_entities",
        ):

            value = getattr(
                resolution,
                field,
                None,
            )

            if value is not None:

                try:
                    return list(
                        value
                    )
                except TypeError:
                    return []

        return []

    @staticmethod
    def _extract_dependencies(
        resolution: Any,
        dependencies: Optional[
            Iterable[Any]
        ],
    ) -> list[Any]:
        """
        Extract semantic dependencies.
        """

        if dependencies is not None:
            return list(
                dependencies
            )

        if resolution is None:
            return []

        result: list[Any] = []

        for field in (
            "dependencies",
            "semantic_dependencies",
            "relations",
            "semantic_relations",
        ):

            value = getattr(
                resolution,
                field,
                None,
            )

            if value is None:
                continue

            try:

                result.extend(
                    list(value)
                )

            except TypeError:
                continue

        return result

    @staticmethod
    def _extract_clusters(
        resolution: Any,
        clusters: Optional[
            Iterable[Any]
        ],
    ) -> list[Any]:
        """
        Extract semantic clusters.
        """

        if clusters is not None:
            return list(
                clusters
            )

        if resolution is None:
            return []

        value = getattr(
            resolution,
            "clusters",
            None,
        )

        if value is None:
            return []

        try:
            return list(
                value
            )
        except TypeError:
            return []

    # =========================================================================
    # SOURCE RESOLUTION
    # =========================================================================

    @classmethod
    def _resolve_source(
        cls,
        explicit_source: str,
        resolution: Any,
        entities: list[Any],
    ) -> str:
        """
        Resolve the document source without inventing one.

        Priority:

            explicit source
            resolution.source
            resolution.metadata.source
            entity.source
            entity.metadata.source

        Empty string is returned when no source is available.
        """

        if explicit_source:
            return str(
                explicit_source
            ).strip()

        source = getattr(
            resolution,
            "source",
            "",
        )

        if source:
            return str(
                source
            ).strip()

        metadata = getattr(
            resolution,
            "metadata",
            None,
        )

        if isinstance(
            metadata,
            dict,
        ):

            value = metadata.get(
                "source"
            )

            if value:
                return str(
                    value
                ).strip()

        for entity in entities:

            value = getattr(
                entity,
                "source",
                "",
            )

            if value:
                return str(
                    value
                ).strip()

            metadata = getattr(
                entity,
                "metadata",
                None,
            )

            if isinstance(
                metadata,
                dict,
            ):

                value = metadata.get(
                    "source"
                )

                if value:
                    return str(
                        value
                    ).strip()

        return ""

    # =========================================================================
    # ENTITY MAP
    # =========================================================================

    @staticmethod
    def _build_entity_map(
        entities: list[Any],
    ) -> Dict[str, Any]:
        """
        Build entity_id -> entity.
        """

        result: Dict[
            str,
            Any,
        ] = {}

        for entity in entities:

            entity_id = (
                BusinessStatementBuilder
                ._get_entity_id(
                    entity
                )
            )

            if entity_id:
                result[
                    entity_id
                ] = entity

        return result

    # =========================================================================
    # CLUSTER GROUPING
    # =========================================================================

    def _group_by_clusters(
        self,
        clusters: list[Any],
        entity_map: Dict[str, Any],
    ) -> Dict[
        str,
        List[Any],
    ]:
        """
        PRIMARY STRATEGY.

        Group entities using SemanticCluster.
        """

        groups: Dict[
            str,
            List[Any],
        ] = {}

        for cluster in clusters:

            cluster_id = getattr(
                cluster,
                "cluster_id",
                None,
            )

            if not cluster_id:

                cluster_id = getattr(
                    cluster,
                    "id",
                    None,
                )

            if not cluster_id:

                cluster_id = (
                    f"cluster_"
                    f"{uuid.uuid4().hex[:8]}"
                )

            entity_ids = getattr(
                cluster,
                "entity_ids",
                None,
            )

            if not entity_ids:

                entity_ids = getattr(
                    cluster,
                    "members",
                    None,
                )

            if not entity_ids:

                entity_ids = getattr(
                    cluster,
                    "entities",
                    None,
                )

            if not entity_ids:
                continue

            try:

                entity_ids = list(
                    entity_ids
                )

            except TypeError:

                continue

            group_key = (
                f"cluster_{cluster_id}"
            )

            group: list[Any] = []

            for entity_id in entity_ids:

                if entity_id in entity_map:

                    group.append(
                        entity_map[
                            entity_id
                        ]
                    )

            if group:

                groups[
                    group_key
                ] = group

                self.logger.debug(
                    "Cluster %s: %s entities",
                    cluster_id,
                    len(group),
                )

        total_grouped = sum(
            len(group)
            for group
            in groups.values()
        )

        self.logger.info(
            "Grouped %s entities across %s clusters",
            total_grouped,
            len(groups),
        )

        return groups

    # =========================================================================
    # RELATION GROUPING
    # =========================================================================

    def _group_by_relations(
        self,
        entities: list[Any],
        dependencies: list[Any],
    ) -> Dict[
        str,
        List[Any],
    ]:
        """
        FALLBACK STRATEGY.

        Group around action entities and their targets.
        """

        groups: Dict[
            str,
            List[Any],
        ] = {}

        entity_map = (
            self._build_entity_map(
                entities
            )
        )

        source_map: Dict[
            str,
            List[tuple],
        ] = {}

        for dependency in dependencies:

            source_id = (
                self._get_dependency_source(
                    dependency
                )
            )

            target_id = (
                self._get_dependency_target(
                    dependency
                )
            )

            relation_type = (
                self._get_relation_type(
                    dependency
                )
            )

            if (
                source_id
                and target_id
            ):

                source_map.setdefault(
                    source_id,
                    [],
                ).append(
                    (
                        target_id,
                        relation_type,
                    )
                )

        for entity in entities:

            entity_id = (
                self._get_entity_id(
                    entity
                )
            )

            entity_type = (
                self._get_entity_type(
                    entity
                )
            )

            if (
                entity_type
                in {
                    "action",
                    "act",
                }
                and entity_id
                in source_map
            ):

                group_key = (
                    f"action_{entity_id}"
                )

                group = [
                    entity
                ]

                for target_id, _ in (
                    source_map[
                        entity_id
                    ]
                ):

                    target = (
                        entity_map.get(
                            target_id
                        )
                    )

                    if (
                        target is not None
                        and target not in group
                    ):
                        group.append(
                            target
                        )

                groups[
                    group_key
                ] = group

        return groups

    # =========================================================================
    # INDIVIDUAL ENTITY FALLBACK
    # =========================================================================

    def _group_individual_entities(
        self,
        entities: list[Any],
    ) -> Dict[
        str,
        List[Any],
    ]:
        """
        FINAL FALLBACK.

        Important semantic entities receive their own statement.
        """

        groups: Dict[
            str,
            List[Any],
        ] = {}

        for entity in entities:

            entity_id = (
                self._get_entity_id(
                    entity
                )
            )

            entity_type = (
                self._get_entity_type(
                    entity
                )
            )

            if entity_type in {
                "action",
                "act",
                "target",
                "skill",
                "standard",
                "certification",
                "technology",
                "methodology",
                "domain",
                "metric",
                "kpi",
            }:

                group_key = (
                    f"single_"
                    f"{entity_id or uuid.uuid4().hex[:8]}"
                )

                groups[
                    group_key
                ] = [
                    entity
                ]

        if (
            not groups
            and entities
        ):

            groups[
                "all_entities"
            ] = list(
                entities
            )

        return groups

    # =========================================================================
    # DEPENDENCY HELPERS
    # =========================================================================

    def _find_dependencies_for_group(
        self,
        group_entities: list[Any],
        all_dependencies: list[Any],
        entity_map: Dict[str, Any],
    ) -> list[Any]:
        """
        Find dependencies touching any entity in the group.
        """

        del entity_map

        entity_ids = {
            self._get_entity_id(
                entity
            )
            for entity
            in group_entities
        }

        entity_ids.discard(
            ""
        )

        result: list[Any] = []

        for dependency in all_dependencies:

            source = (
                self._get_dependency_source(
                    dependency
                )
            )

            target = (
                self._get_dependency_target(
                    dependency
                )
            )

            if (
                source in entity_ids
                or target in entity_ids
            ):

                result.append(
                    dependency
                )

        return result

    # =========================================================================
    # STATEMENT CREATION
    # =========================================================================

    def _create_statement(
        self,
        group_id: str,
        entities: list[Any],
        dependencies: list[Any],
        entity_map: Dict[str, Any],
        source: str,
    ) -> Optional[
        BusinessStatement
    ]:
        """
        Create one BusinessStatement object.

        No semantic objects are duplicated.
        """

        del entity_map

        if not entities:
            return None

        # ---------------------------------------------------------------------
        # Remove duplicate semantic entities while preserving object identity.
        # ---------------------------------------------------------------------

        seen: Set[str] = set()

        unique_entities: list[
            Any
        ] = []

        for entity in entities:

            entity_id = (
                self._get_entity_id(
                    entity
                )
            )

            if (
                entity_id
                and entity_id not in seen
            ):

                seen.add(
                    entity_id
                )

                unique_entities.append(
                    entity
                )

            elif not entity_id:

                unique_entities.append(
                    entity
                )

        if not unique_entities:
            return None

        # ---------------------------------------------------------------------
        # Semantic components.
        # ---------------------------------------------------------------------

        action = (
            self._find_entity_by_type(
                unique_entities,
                {
                    "action",
                    "act",
                },
            )
        )

        target = (
            self._find_entity_by_type(
                unique_entities,
                {
                    "target",
                    "skill",
                    "technology",
                    "certification",
                    "standard",
                    "methodology",
                },
            )
        )

        domain = (
            self._find_entity_by_type(
                unique_entities,
                {
                    "domain",
                    "business_area",
                },
            )
        )

        metric = (
            self._find_entity_by_type(
                unique_entities,
                {
                    "metric",
                    "kpi",
                    "business_kpi",
                },
            )
        )

        # ---------------------------------------------------------------------
        # Generated semantic statement text.
        # ---------------------------------------------------------------------

        text = (
            self._build_statement_text(
                action=action,
                target=target,
                domain=domain,
                metric=metric,
                entities=unique_entities,
            )
        )

        # ---------------------------------------------------------------------
        # IMPORTANT:
        #
        # source_text is actual evidence from semantic entities whenever
        # available.
        #
        # It is NOT automatically replaced with generated `text`.
        # ---------------------------------------------------------------------

        source_text = (
            self._get_source_text(
                unique_entities
            )
        )

        if not source_text:
            source_text = text

        statement_source = (
            source
            or self._get_entity_source(
                unique_entities
            )
        )

        # ---------------------------------------------------------------------
        # Build object.
        # ---------------------------------------------------------------------

        try:

            statement = BusinessStatement(
                statement_id=(
                    f"BS-"
                    f"{uuid.uuid4().hex[:8]}"
                ),

                canonical=text,

                text=text,

                normalized=(
                    text.casefold()
                    if text
                    else ""
                ),

                fact_id=(
                    self._get_fact_id(
                        unique_entities
                    )
                ),

                sentence_index=(
                    self._get_sentence_index(
                        unique_entities
                    )
                ),

                source_text=source_text,

                source=statement_source,

                action=action,

                target=target,

                domain=domain,

                metric=metric,

                entities=unique_entities,

                relations=[
                    dependency
                    for dependency
                    in dependencies
                    if isinstance(
                        dependency,
                        StatementRelation,
                    )
                ],

                dependencies=dependencies,

                achievement=(
                    self._check_achievement(
                        unique_entities
                    )
                ),

                quantified=(
                    self._check_quantified(
                        unique_entities
                    )
                ),

                impact=(
                    self._get_impact(
                        metric,
                        unique_entities,
                    )
                ),

                business_value=(
                    self._get_business_value(
                        unique_entities
                    )
                ),

                category=(
                    self._get_category(
                        action,
                        target,
                        domain,
                        metric,
                    )
                ),

                business_area=(
                    self._get_business_area(
                        domain,
                        unique_entities,
                    )
                ),

                confidence=(
                    self._calculate_confidence(
                        unique_entities
                    )
                ),

                impact_weight=(
                    self._calculate_impact_weight(
                        unique_entities
                    )
                ),

                metadata={
                    "group_id": group_id,

                    "entity_count": (
                        len(
                            unique_entities
                        )
                    ),

                    "entity_ids": [
                        self._get_entity_id(
                            entity
                        )
                        for entity
                        in unique_entities
                    ],

                    "entity_types": [
                        self._get_entity_type(
                            entity
                        )
                        for entity
                        in unique_entities
                    ],
                },
            )

            return statement

        except Exception as exc:

            self.logger.error(
                "Failed to create BusinessStatement: %s",
                exc,
                exc_info=True,
            )

            return None

    # =========================================================================
    # SOURCE EVIDENCE
    # =========================================================================

    @classmethod
    def _get_source_text(
        cls,
        entities: list[Any],
    ) -> str:
        """
        Recover actual source evidence from semantic entities.
        """

        for entity in entities:

            for field in (
                "source_text",
                "matched_phrase",
                "evidence",
                "text",
                "original",
            ):

                value = getattr(
                    entity,
                    field,
                    None,
                )

                if (
                    value is not None
                    and str(value).strip()
                ):

                    return str(
                        value
                    ).strip()

        return ""

    @classmethod
    def _get_entity_source(
        cls,
        entities: list[Any],
    ) -> str:

        for entity in entities:

            value = getattr(
                entity,
                "source",
                None,
            )

            if (
                value is not None
                and str(value).strip()
            ):

                return str(
                    value
                ).strip()

            metadata = getattr(
                entity,
                "metadata",
                None,
            )

            if isinstance(
                metadata,
                dict,
            ):

                value = metadata.get(
                    "source"
                )

                if (
                    value is not None
                    and str(value).strip()
                ):

                    return str(
                        value
                    ).strip()

        return ""

    # =========================================================================
    # ENTITY HELPERS
    # =========================================================================

    @staticmethod
    def _get_entity_id(
        entity: Any,
    ) -> str:

        for attr in (
            "entity_id",
            "id",
            "canonical_id",
        ):

            value = getattr(
                entity,
                attr,
                None,
            )

            if value:
                return str(
                    value
                ).strip()

        return ""

    @staticmethod
    def _get_entity_type(
        entity: Any,
    ) -> str:

        return (
            str(
                getattr(
                    entity,
                    "entity_type",
                    "",
                )
                or ""
            )
            .strip()
            .casefold()
        )

    @staticmethod
    def _get_entity_name(
        entity: Any,
    ) -> str:

        for attr in (
            "canonical",
            "name",
            "normalized",
            "original",
            "label",
            "text",
        ):

            value = getattr(
                entity,
                attr,
                None,
            )

            if value:
                return str(
                    value
                ).strip()

        return ""

    # =========================================================================
    # DEPENDENCY HELPERS
    # =========================================================================

    @staticmethod
    def _get_dependency_source(
        dependency: Any,
    ) -> str:

        for attr in (
            "source_id",
            "source_entity_id",
            "from_id",
            "source",
        ):

            value = getattr(
                dependency,
                attr,
                None,
            )

            if value:

                if not isinstance(
                    value,
                    (
                        str,
                        int,
                        float,
                    ),
                ):

                    nested = getattr(
                        value,
                        "entity_id",
                        None,
                    )

                    if nested:
                        return str(
                            nested
                        ).strip()

                return str(
                    value
                ).strip()

        return ""

    @staticmethod
    def _get_dependency_target(
        dependency: Any,
    ) -> str:

        for attr in (
            "target_id",
            "target_entity_id",
            "to_id",
            "target",
        ):

            value = getattr(
                dependency,
                attr,
                None,
            )

            if value:

                if not isinstance(
                    value,
                    (
                        str,
                        int,
                        float,
                    ),
                ):

                    nested = getattr(
                        value,
                        "entity_id",
                        None,
                    )

                    if nested:
                        return str(
                            nested
                        ).strip()

                return str(
                    value
                ).strip()

        return ""

    @staticmethod
    def _get_relation_type(
        dependency: Any,
    ) -> str:

        for attr in (
            "relation_type",
            "relation",
            "type",
        ):

            value = getattr(
                dependency,
                attr,
                None,
            )

            if value:

                return str(
                    value
                ).upper().strip()

        return "RELATED_TO"

    # =========================================================================
    # FACT / SENTENCE HELPERS
    # =========================================================================

    @staticmethod
    def _get_fact_id(
        entities: list[Any],
    ) -> str:

        for entity in entities:

            value = (
                getattr(
                    entity,
                    "fact_id",
                    None,
                )
                or getattr(
                    entity,
                    "source_fact_id",
                    None,
                )
            )

            if value:

                return str(
                    value
                ).strip()

        return ""

    @staticmethod
    def _get_sentence_index(
        entities: list[Any],
    ) -> int:

        for entity in entities:

            value = getattr(
                entity,
                "sentence_index",
                -1,
            )

            try:

                value = int(
                    value
                )

                if value >= 0:
                    return value

            except (
                TypeError,
                ValueError,
            ):
                continue

        return -1

    # =========================================================================
    # ENTITY TYPE SEARCH
    # =========================================================================

    @staticmethod
    def _find_entity_by_type(
        entities: list[Any],
        types: set[str],
    ) -> Optional[Any]:

        for entity in entities:

            entity_type = (
                BusinessStatementBuilder
                ._get_entity_type(
                    entity
                )
            )

            if entity_type in types:
                return entity

        return None

    # =========================================================================
    # STATEMENT TEXT
    # =========================================================================

    @staticmethod
    def _build_statement_text(
        action: Optional[Any],
        target: Optional[Any],
        domain: Optional[Any],
        metric: Optional[Any],
        entities: list[Any],
    ) -> str:

        parts: list[str] = []

        if action:

            action_name = (
                BusinessStatementBuilder
                ._get_entity_name(
                    action
                )
            )

            if action_name:
                parts.append(
                    action_name
                )

        if target:

            target_name = (
                BusinessStatementBuilder
                ._get_entity_name(
                    target
                )
            )

            if target_name:
                parts.append(
                    target_name
                )

        if (
            not parts
            and domain
        ):

            domain_name = (
                BusinessStatementBuilder
                ._get_entity_name(
                    domain
                )
            )

            if domain_name:
                parts.append(
                    domain_name
                )

        if (
            not parts
            and entities
        ):

            fallback = (
                BusinessStatementBuilder
                ._get_entity_name(
                    entities[0]
                )
            )

            if fallback:
                parts.append(
                    fallback
                )

        if (
            metric
            and BusinessStatementBuilder
            ._check_quantified(
                [metric]
            )
        ):

            metric_name = (
                BusinessStatementBuilder
                ._get_entity_name(
                    metric
                )
            )

            if metric_name:

                parts.append(
                    f"resulting in "
                    f"{metric_name}"
                )

        if parts:
            return " ".join(
                parts
            )

        return "Professional Achievement"

    # =========================================================================
    # SEMANTIC FLAGS
    # =========================================================================

    @staticmethod
    def _check_achievement(
        entities: list[Any],
    ) -> bool:

        for entity in entities:

            if getattr(
                entity,
                "achievement",
                False,
            ):

                return True

        return False

    @staticmethod
    def _check_quantified(
        entities: list[Any],
    ) -> bool:

        for entity in entities:

            if getattr(
                entity,
                "quantified",
                False,
            ):

                return True

        return False

    # =========================================================================
    # BUSINESS MEANING
    # =========================================================================

    @staticmethod
    def _get_impact(
        metric: Optional[Any],
        entities: list[Any],
    ) -> str:

        if metric:

            return (
                BusinessStatementBuilder
                ._get_entity_name(
                    metric
                )
            )

        for entity in entities:

            impact = getattr(
                entity,
                "impact",
                None,
            )

            if impact:

                return str(
                    impact
                )

        return ""

    @staticmethod
    def _get_business_value(
        entities: list[Any],
    ) -> str:

        for entity in entities:

            value = (
                getattr(
                    entity,
                    "business_value",
                    None,
                )
                or getattr(
                    entity,
                    "business_meaning",
                    None,
                )
            )

            if value:

                return str(
                    value
                )

        return ""

    # =========================================================================
    # CATEGORY
    # =========================================================================

    @staticmethod
    def _get_category(
        action: Optional[Any],
        target: Optional[Any],
        domain: Optional[Any],
        metric: Optional[Any],
    ) -> str:

        if (
            action
            and target
        ):
            return "achievement"

        if action:
            return "action_statement"

        if metric:
            return "metric_statement"

        if domain:
            return "domain_statement"

        return "professional_statement"

    # =========================================================================
    # BUSINESS AREA
    # =========================================================================

    @staticmethod
    def _get_business_area(
        domain: Optional[Any],
        entities: list[Any],
    ) -> str:

        if domain:

            area = (
                getattr(
                    domain,
                    "business_area",
                    None,
                )
                or BusinessStatementBuilder
                ._get_entity_name(
                    domain
                )
            )

            if area:
                return str(
                    area
                )

        for entity in entities:

            area = getattr(
                entity,
                "business_area",
                None,
            )

            if area:
                return str(
                    area
                )

        return ""

    # =========================================================================
    # CONFIDENCE
    # =========================================================================

    @staticmethod
    def _calculate_confidence(
        entities: list[Any],
    ) -> float:

        confidences: list[
            float
        ] = []

        for entity in entities:

            value = getattr(
                entity,
                "confidence",
                None,
            )

            if value is None:
                continue

            try:

                confidences.append(
                    float(value)
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

        if not confidences:
            return 0.5

        return round(
            sum(confidences)
            / len(confidences),
            4,
        )

    # =========================================================================
    # IMPACT WEIGHT
    # =========================================================================

    @staticmethod
    def _calculate_impact_weight(
        entities: list[Any],
    ) -> float:

        weights: list[
            float
        ] = []

        for entity in entities:

            value = getattr(
                entity,
                "impact_weight",
                None,
            )

            if value is None:
                continue

            try:

                weights.append(
                    float(value)
                )

            except (
                TypeError,
                ValueError,
            ):
                continue

        if not weights:
            return 1.0

        return round(
            max(weights),
            4,
        )


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================


def build_business_statements(
    semantic_resolution: Any = None,
    entities: Optional[
        Iterable[Any]
    ] = None,
    dependencies: Optional[
        Iterable[Any]
    ] = None,
    clusters: Optional[
        Iterable[Any]
    ] = None,
    source: str = "",
) -> list[BusinessStatement]:
    """
    Convenience API.

    Object In
        SemanticResolution / semantic objects

    Object Out
        list[BusinessStatement]
    """

    builder = (
        BusinessStatementBuilder()
    )

    return builder.build(
        semantic_resolution=semantic_resolution,
        entities=entities,
        dependencies=dependencies,
        clusters=clusters,
        source=source,
    )


__all__ = [
    "BusinessStatementBuilder",
    "build_business_statements",
]