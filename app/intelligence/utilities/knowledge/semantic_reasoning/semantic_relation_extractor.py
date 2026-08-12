"""
Enterprise Relation Extractor
Enterprise V12

Converts semantic dependencies into higher-level
StatementRelation objects.

Pipeline

SemanticEntity[]
        +
SemanticDependency[]
        ↓
RelationExtractor
        ↓
StatementRelation[]

Responsibilities
----------------
• Convert dependencies into semantic relations
• Preserve source/target entity IDs
• Preserve confidence
• Preserve entity types
• Preserve statement boundaries
• Prevent duplicate relations
• Keep KPI and BKPI distinctions
• Remain independent from KnowledgeGraphBuilder

This class does NOT build the knowledge graph.
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_models import (
    SemanticDependency,
    SemanticEntity,
    StatementRelation,
)


class SemanticRelationExtractor:
    """
    Extracts higher-level semantic relations from
    already-resolved SemanticDependency objects.

    DependencyResolver determines that a relationship exists.

    RelationExtractor determines how that dependency should
    be represented as a StatementRelation.
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def extract(
        self,
        entities: list[SemanticEntity],
        dependencies: list[SemanticDependency],
    ) -> list[StatementRelation]:
        """
        Convert semantic dependencies into StatementRelation objects.
        """

        if not entities or not dependencies:
            return []

        entity_lookup = {
            entity.entity_id: entity
            for entity in entities
            if isinstance(entity, SemanticEntity)
            and entity.entity_id
        }

        relations: list[StatementRelation] = []

        for dependency in dependencies:

            source = entity_lookup.get(
                dependency.source_entity
            )

            target = entity_lookup.get(
                dependency.target_entity
            )

            if source is None or target is None:
                continue

            if not self._same_statement(
                source,
                target,
            ):
                continue

            relation_type = self._map_relation(
                dependency.relation
            )

            if relation_type is None:
                continue

            self._append_relation(
                relations=relations,
                source=source,
                target=target,
                relation_type=relation_type,
                confidence=dependency.confidence,
                dependency=dependency,
            )

        return relations

    # ==========================================================
    # RELATION MAPPING
    # ==========================================================

    @staticmethod
    def _map_relation(
        relation: str | None,
    ) -> str | None:
        """
        Convert DependencyResolver relation names into
        standardized StatementRelation names.
        """

        if not relation:
            return None

        mapping = {

            # ----------------------------------------------
            # TARGET RELATIONS
            # ----------------------------------------------

            "targets": "ACTS_ON",
            "creates": "CREATES",
            "manages": "MANAGES",
            "monitors": "MONITORS",
            "maintains": "MAINTAINS",
            "optimizes": "OPTIMIZES",
            "improves": "IMPROVES",
            "controls": "CONTROLS",
            "executes": "EXECUTES",
            "certifies": "CERTIFIES",

            # ----------------------------------------------
            # STANDARD
            # ----------------------------------------------

            "complies_with": "COMPLIES_WITH",
            "certified_against": "CERTIFIED_AGAINST",
            "audited_against": "AUDITED_AGAINST",

            # ----------------------------------------------
            # METHODOLOGY
            # ----------------------------------------------

            "performed_using": "USES",

            # ----------------------------------------------
            # SKILL
            # ----------------------------------------------

            "requires": "REQUIRES",

            # ----------------------------------------------
            # KPI / METRIC
            # ----------------------------------------------

            "improved": "AFFECTS",
            "reduced": "AFFECTS",
            "increased": "AFFECTS",
            "optimized": "AFFECTS",
            "measures": "MEASURES",
            "measured_by": "MEASURED_BY",

            # ----------------------------------------------
            # BKPI
            # ----------------------------------------------

            "contributes_to": "CONTRIBUTES_TO",
            "supports": "SUPPORTS",

            # ----------------------------------------------
            # DOMAIN
            # ----------------------------------------------

            "belongs_to": "BELONGS_TO",
        }

        return mapping.get(
            relation
        )

    # ==========================================================
    # STATEMENT BOUNDARY
    # ==========================================================

    @staticmethod
    def _same_statement(
        source: SemanticEntity,
        target: SemanticEntity,
    ) -> bool:
        """
        Prevent relations from crossing statements.
        """

        source_statement = (
            getattr(
                source,
                "statement_id",
                "",
            )
            or "STATEMENT_1"
        )

        target_statement = (
            getattr(
                target,
                "statement_id",
                "",
            )
            or "STATEMENT_1"
        )

        return source_statement == target_statement

    # ==========================================================
    # DUPLICATE PROTECTION
    # ==========================================================

    @staticmethod
    def _append_relation(
        relations: list[StatementRelation],
        source: SemanticEntity,
        target: SemanticEntity,
        relation_type: str,
        confidence: float,
        dependency: SemanticDependency,
    ) -> None:
        """
        Add a StatementRelation unless the exact relation
        already exists.
        """

        for existing in relations:

            if (
                existing.source_id
                == source.entity_id
                and existing.target_id
                == target.entity_id
                and existing.relation_type
                == relation_type
            ):
                return

        effective_confidence = min(
            source.confidence,
            target.confidence,
            confidence,
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
                confidence=effective_confidence,
                reasoning=reasoning,
                metadata={
                    "source_type": source.entity_type,
                    "target_type": target.entity_type,
                    "dependency_relation": dependency.relation,
                    "statement_id": (
                        getattr(
                            source,
                            "statement_id",
                            "",
                        )
                        or "STATEMENT_1"
                    ),
                },
            )
        )