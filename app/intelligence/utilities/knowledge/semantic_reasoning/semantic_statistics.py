"""
Enterprise Semantic Statistics

Enterprise V12

Builds statistics directly from the NEW semantic
resolution result.

NEW ARCHITECTURE

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
SemanticEntity
        ↓
BusinessStatementBuilder
"""

from __future__ import annotations

from typing import Any


class SemanticStatistics:
    """
    Statistics for the new semantic architecture.

    This class deliberately does NOT depend on:

        SemanticDependency
        SemanticResolution
        SemanticCluster

    Those belong to the old semantic architecture.
    """

    def build(
        self,
        semantic_result: Any,
    ) -> dict[str, Any]:

        if semantic_result is None:

            return self._empty()

        entities = self._get_collection(
            semantic_result,
            "entities",
        )

        statements = self._get_collection(
            semantic_result,
            "business_statements",
        )

        facts = self._get_collection(
            semantic_result,
            "facts",
        )

        stats = self._empty()

        stats["entities"] = len(
            entities
        )

        stats["business_statements"] = len(
            statements
        )

        stats["facts"] = len(
            facts
        )

        for entity in entities:

            self._count_entity(
                stats,
                entity,
            )

        stats["total_entity_types"] = sum(
            stats[key]
            for key in (
                "actions",
                "targets",
                "objects",
                "domains",
                "metrics",
                "measurements",
                "methodologies",
                "technologies",
                "standards",
                "certifications",
                "skills",
                "kpis",
            )
        )

        return stats

    # ==========================================================
    # EMPTY
    # ==========================================================

    @staticmethod
    def _empty() -> dict[str, Any]:

        return {

            "entities": 0,

            "facts": 0,

            "business_statements": 0,

            "actions": 0,

            "targets": 0,

            "objects": 0,

            "domains": 0,

            "metrics": 0,

            "measurements": 0,

            "methodologies": 0,

            "technologies": 0,

            "standards": 0,

            "certifications": 0,

            "skills": 0,

            "kpis": 0,

            "total_entity_types": 0,

        }

    # ==========================================================
    # ENTITY COUNT
    # ==========================================================

    @classmethod
    def _count_entity(
        cls,
        stats: dict[str, Any],
        entity: Any,
    ) -> None:

        if entity is None:

            return

        entity_type = cls._entity_type(
            entity
        )

        if not entity_type:

            return

        mapping = {

            "action": "actions",

            "target": "targets",

            "object": "objects",

            "domain": "domains",

            "metric": "metrics",

            "measurement": "measurements",

            "methodology": "methodologies",

            "technology": "technologies",

            "standard": "standards",

            "certification": "certifications",

            "skill": "skills",

            "kpi": "kpis",

            "business_kpi": "kpis",

        }

        key = mapping.get(
            entity_type
        )

        if key is not None:

            stats[key] += 1

    # ==========================================================
    # ENTITY TYPE
    # ==========================================================

    @staticmethod
    def _entity_type(
        entity: Any,
    ) -> str:

        value = getattr(
            entity,
            "entity_type",
            "",
        )

        if not value:

            value = getattr(
                entity,
                "semantic_type",
                "",
            )

        return str(
            value or ""
        ).strip().casefold()

    # ==========================================================
    # COLLECTION
    # ==========================================================

    @staticmethod
    def _get_collection(
        obj: Any,
        name: str,
    ) -> list:

        value = getattr(
            obj,
            name,
            None,
        )

        if value is None:

            return []

        if isinstance(
            value,
            list,
        ):

            return value

        if isinstance(
            value,
            tuple,
        ):

            return list(value)

        if isinstance(
            value,
            dict,
        ):

            return list(
                value.values()
            )

        try:

            return list(value)

        except TypeError:

            return []