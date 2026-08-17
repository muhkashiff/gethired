"""
Enterprise Semantic Metadata Builder
Enterprise V12

Builds lightweight metadata from the current semantic result.

IMPORTANT
---------
This implementation does NOT depend on:

    SemanticMetadata
    SemanticStatistics

Those objects belong to the old semantic architecture.

Current architecture uses:

    SemanticEntity
    BusinessStatement
    StatementRelation
    SemanticResult

Metadata is represented as a normal dictionary.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


class MetadataBuilder:
    """
    Builds summary metadata from the current semantic result.

    This class is intentionally model-independent.

    It does not create a SemanticMetadata object.
    """

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def build(self, semantic_result: Any) -> dict:
        """
        Build metadata from a semantic result.

        Returns
        -------
        dict
            Plain metadata dictionary.
        """

        if semantic_result is None:
            return {
                "entities": 0,
                "dependencies": 0,
                "clusters": 0,
                "business_statements": 0,
                "actions": 0,
                "objects": 0,
                "domains": 0,
                "skills": 0,
                "technologies": 0,
                "certifications": 0,
                "standards": 0,
                "methodologies": 0,
                "metrics": 0,
                "measurements": 0,
                "kpis": 0,
                "achievement": False,
                "semantic_type": "",
                "primary_domain": "",
                "business_area": "",
            }

        entities = self._safe_list(
            getattr(
                semantic_result,
                "entities",
                [],
            )
        )

        dependencies = self._safe_list(
            getattr(
                semantic_result,
                "dependencies",
                [],
            )
        )

        clusters = self._safe_list(
            getattr(
                semantic_result,
                "clusters",
                [],
            )
        )

        statements = self._safe_list(
            getattr(
                semantic_result,
                "business_statements",
                [],
            )
        )

        # ------------------------------------------------------
        # Entity statistics
        # ------------------------------------------------------

        statistics = self._build_entity_statistics(
            entities
        )

        # ------------------------------------------------------
        # Statement metadata
        # ------------------------------------------------------

        statement_metadata = (
            self._build_statement_metadata(
                statements
            )
        )

        # ------------------------------------------------------
        # Final metadata
        # ------------------------------------------------------

        metadata = {

            "entities": len(entities),

            "dependencies": len(
                dependencies
            ),

            "clusters": len(
                clusters
            ),

            "business_statements": len(
                statements
            ),

            **statistics,

            **statement_metadata,

        }

        return metadata

    # ==========================================================
    # ENTITY STATISTICS
    # ==========================================================

    @staticmethod
    def _build_entity_statistics(
        entities: list[Any],
    ) -> dict:

        counts = Counter()

        for entity in entities:

            entity_type = str(
                getattr(
                    entity,
                    "entity_type",
                    "",
                )
                or ""
            ).strip().lower()

            if not entity_type:
                entity_type = "unknown"

            counts[
                entity_type
            ] += 1

        return {

            "actions": counts.get(
                "action",
                0,
            ),

            "objects": counts.get(
                "object",
                0,
            ),

            "targets": counts.get(
                "target",
                0,
            ),

            "domains": counts.get(
                "domain",
                0,
            ),

            "skills": counts.get(
                "skill",
                0,
            ),

            # IMPORTANT:
            # Your architecture keeps technology
            # as one entity type.
            "technologies": counts.get(
                "technologie",
                0,
            ),

            # IMPORTANT:
            # Certification remains its own entity.
            "certifications": counts.get(
                "certification",
                0,
            ),

            "standards": counts.get(
                "standard",
                0,
            ),

            # IMPORTANT:
            # methodologie is singular in the
            # entity_type value even though the
            # concept may contain many methodologies.
            "methodologies": counts.get(
                "methodologie",
                0,
            ),

            "metrics": counts.get(
                "metric",
                0,
            ),

            "measurements": counts.get(
                "measurement",
                0,
            ),

            "kpis": counts.get(
                "kpi",
                0,
            ),

            "business_kpis": counts.get(
                "business_kpi",
                0,
            ),

            "unknown": counts.get(
                "unknown",
                0,
            ),
        }

    # ==========================================================
    # STATEMENT METADATA
    # ==========================================================

    @staticmethod
    def _build_statement_metadata(
        statements: list[Any],
    ) -> dict:

        if not statements:

            return {

                "semantic_type": "",

                "primary_domain": "",

                "business_area": "",

                "achievement": False,

                "quantified": False,

                "average_confidence": 0.0,

            }

        semantic_types = []

        domains = []

        business_areas = []

        confidences = []

        achievement = False

        quantified = False

        for statement in statements:

            semantic_type = str(
                getattr(
                    statement,
                    "semantic_type",
                    "",
                )
                or ""
            ).strip()

            if semantic_type:

                semantic_types.append(
                    semantic_type
                )

            primary_domain = str(
                getattr(
                    statement,
                    "primary_domain",
                    "",
                )
                or ""
            ).strip()

            if primary_domain:

                domains.append(
                    primary_domain
                )

            business_area = str(
                getattr(
                    statement,
                    "business_area",
                    "",
                )
                or ""
            ).strip()

            if business_area:

                business_areas.append(
                    business_area
                )

            confidence = getattr(
                statement,
                "confidence",
                None,
            )

            if confidence is not None:

                try:

                    confidences.append(
                        float(confidence)
                    )

                except (
                    TypeError,
                    ValueError,
                ):

                    pass

            if bool(
                getattr(
                    statement,
                    "achievement",
                    False,
                )
            ):

                achievement = True

            if bool(
                getattr(
                    statement,
                    "quantified",
                    False,
                )
            ):

                quantified = True

        return {

            "semantic_type": (
                MetadataBuilder._most_common(
                    semantic_types
                )
            ),

            "primary_domain": (
                MetadataBuilder._most_common(
                    domains
                )
            ),

            "business_area": (
                MetadataBuilder._most_common(
                    business_areas
                )
            ),

            "achievement": achievement,

            "quantified": quantified,

            "average_confidence": (
                round(
                    sum(confidences)
                    / len(confidences),
                    2,
                )
                if confidences
                else 0.0
            ),
        }

    # ==========================================================
    # UTILITIES
    # ==========================================================

    @staticmethod
    def _most_common(
        values: list[str],
    ) -> str:

        if not values:
            return ""

        return Counter(
            values
        ).most_common(1)[0][0]

    # ----------------------------------------------------------

    @staticmethod
    def _safe_list(
        value: Any,
    ) -> list:

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

        return []