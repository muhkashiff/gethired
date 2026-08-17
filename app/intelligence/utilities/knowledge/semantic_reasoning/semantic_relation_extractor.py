"""
Enterprise Semantic Relation Extractor

Enterprise V12 - NEW ARCHITECTURE

Converts resolved SemanticEntity objects into StatementRelation
objects without using the old SemanticDependency architecture.

NEW FLOW

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
SemanticEntity
        ↓
SemanticRelationExtractor
        ↓
StatementRelation
        ↓
BusinessStatementBuilder
        ↓
KnowledgeGraphBuilder

This module deliberately does NOT depend on:

    SemanticDependency
    SemanticResolution
    SemanticCluster
    SemanticMetadata

Those belong to the retired semantic architecture.
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterable

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticEntity,
    StatementRelation,
)


class SemanticRelationExtractor:
    """
    Build StatementRelation objects directly from SemanticEntity objects.

    Relations are inferred from entity types and the semantic information
    carried by the entities themselves.

    The extractor is intentionally lightweight.

    It does NOT build the knowledge graph.
    It does NOT build BusinessStatement objects.
    It does NOT perform ontology resolution.
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def extract(
        self,
        entities: list[SemanticEntity],
    ) -> list[StatementRelation]:
        """
        Convert semantic entities into statement-level relations.

        Entities belonging to different statements are never connected.
        """

        if not entities:

            return []

        valid_entities = [

            entity

            for entity in entities

            if isinstance(
                entity,
                SemanticEntity,
            )
            and entity.entity_id
        ]

        if not valid_entities:

            return []

        grouped = self._group_by_statement(
            valid_entities
        )

        relations: list[StatementRelation] = []

        for statement_id, statement_entities in grouped.items():

            self._extract_statement_relations(

                statement_id=statement_id,

                entities=statement_entities,

                relations=relations,
            )

        return relations

    # ==========================================================
    # GROUP BY STATEMENT
    # ==========================================================

    @staticmethod
    def _group_by_statement(
        entities: Iterable[SemanticEntity],
    ) -> dict[str, list[SemanticEntity]]:

        grouped: dict[
            str,
            list[SemanticEntity],
        ] = {}

        for entity in entities:

            statement_id = (

                getattr(
                    entity,
                    "statement_id",
                    "",
                )

                or getattr(
                    entity,
                    "source_statement_id",
                    "",
                )

                or "STATEMENT_1"
            )

            grouped.setdefault(
                statement_id,
                [],
            ).append(entity)

        return grouped

    # ==========================================================
    # STATEMENT RELATIONS
    # ==========================================================

    def _extract_statement_relations(
        self,
        statement_id: str,
        entities: list[SemanticEntity],
        relations: list[StatementRelation],
    ) -> None:

        actions = self._entities(
            entities,
            "action",
        )

        targets = self._entities(
            entities,
            "target",
        )

        objects = self._entities(
            entities,
            "object",
        )

        metrics = self._entities(
            entities,
            "metric",
        )

        measurements = self._entities(
            entities,
            "measurement",
        )

        skills = self._entities(
            entities,
            "skill",
        )

        standards = self._entities(
            entities,
            "standard",
        )

        methodologies = self._entities(
            entities,
            "methodology",
        )

        technologies = self._entities(
            entities,
            "technology",
        )

        certifications = self._entities(
            entities,
            "certification",
        )

        domains = self._entities(
            entities,
            "domain",
        )

        kpis = self._entities(
            entities,
            "kpi",
        )

        # ------------------------------------------------------
        # ACTION → TARGET
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            targets + objects,
            "ACTS_ON",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → METRIC
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            metrics,
            "AFFECTS",
            statement_id,
        )

        # ------------------------------------------------------
        # METRIC → MEASUREMENT
        # ------------------------------------------------------

        self._connect(

            relations,
            metrics,
            measurements,
            "MEASURED_BY",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → SKILL
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            skills,
            "REQUIRES",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → STANDARD
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            standards,
            "COMPLIES_WITH",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → METHODOLOGY
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            methodologies,
            "USES",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → TECHNOLOGY
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            technologies,
            "USES",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → CERTIFICATION
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            certifications,
            "CERTIFIES",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → DOMAIN
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            domains,
            "BELONGS_TO",
            statement_id,
        )

        # ------------------------------------------------------
        # ACTION → KPI
        # ------------------------------------------------------

        self._connect(

            relations,
            actions,
            kpis,
            "AFFECTS",
            statement_id,
        )

    # ==========================================================
    # ENTITY FILTER
    # ==========================================================

    @staticmethod
    def _entities(
        entities: list[SemanticEntity],
        entity_type: str,
    ) -> list[SemanticEntity]:

        entity_type = entity_type.casefold()

        return [

            entity

            for entity in entities

            if str(
                getattr(
                    entity,
                    "entity_type",
                    "",
                )
                or getattr(
                    entity,
                    "semantic_type",
                    "",
                )
            ).casefold()
            == entity_type

        ]

    # ==========================================================
    # CONNECT
    # ==========================================================

    def _connect(
        self,
        relations: list[StatementRelation],
        sources: list[SemanticEntity],
        targets: list[SemanticEntity],
        relation_type: str,
        statement_id: str,
    ) -> None:

        if not sources or not targets:

            return

        for source, target in combinations(
            sources + targets,
            2,
        ):

            source_type = self._type(
                source
            )

            target_type = self._type(
                target
            )

            if (
                source_type == "action"
                and target_type != "action"
            ):

                self._append(

                    relations=relations,

                    source=source,

                    target=target,

                    relation_type=relation_type,

                    statement_id=statement_id,
                )

    # ==========================================================
    # APPEND
    # ==========================================================

    @staticmethod
    def _append(
        relations: list[StatementRelation],
        source: SemanticEntity,
        target: SemanticEntity,
        relation_type: str,
        statement_id: str,
    ) -> None:

        if not source.entity_id:
            return

        if not target.entity_id:
            return

        for existing in relations:

            if (

                existing.source_id
                == source.entity_id

                and

                existing.target_id
                == target.entity_id

                and

                existing.relation_type
                == relation_type

            ):

                return

        confidence = min(

            SemanticRelationExtractor._confidence(
                source
            ),

            SemanticRelationExtractor._confidence(
                target
            ),

        )

        reasoning = (

            f"{source.canonical} "

            f"{relation_type.replace('_', ' ').lower()} "

            f"{target.canonical}"

        )

        relations.append(

            StatementRelation(

                source_id=source.entity_id,

                target_id=target.entity_id,

                relation_type=relation_type,

                confidence=confidence,

                reasoning=reasoning,

                metadata={

                    "statement_id": statement_id,

                    "source_type": (
                        SemanticRelationExtractor._type(
                            source
                        )
                    ),

                    "target_type": (
                        SemanticRelationExtractor._type(
                            target
                        )
                    ),

                    "source_canonical": (
                        source.canonical
                    ),

                    "target_canonical": (
                        target.canonical
                    ),

                },

            )

        )

    # ==========================================================
    # TYPE
    # ==========================================================

    @staticmethod
    def _type(
        entity: SemanticEntity,
    ) -> str:

        value = (

            getattr(
                entity,
                "entity_type",
                "",
            )

            or getattr(
                entity,
                "semantic_type",
                "",
            )

        )

        return str(
            value or ""
        ).strip().casefold()

    # ==========================================================
    # CONFIDENCE
    # ==========================================================

    @staticmethod
    def _confidence(
        entity: SemanticEntity,
    ) -> float:

        try:

            value = float(
                getattr(
                    entity,
                    "confidence",
                    1.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            value = 1.0

        return max(
            0.0,
            min(
                1.0,
                value,
            ),
        )