from __future__ import annotations

"""
Enterprise Interpretation Builder
Enterprise V14

Purpose
-------

Bridge the Knowledge Extraction layer and Semantic Reasoning layer.

Actual architecture
--------------------

KnowledgeDocument
        ↓
KnowledgeFact
        ↓
KnowledgeInterpretation
        ↓
InterpretationBuilder
        ↓
KnowledgeInterpretation
        ↓
SemanticResolver
        ↓
SemanticResolution

Important
---------

This builder accepts either:

1. KnowledgeFact
2. an extraction-result object
3. an existing KnowledgeInterpretation

When a KnowledgeFact already contains an interpretation, that
interpretation is preserved.

The builder does NOT create SemanticEntity objects.

It only preserves the knowledge objects produced by extraction.
"""


from typing import Any


from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


class InterpretationBuilder:
    """
    Normalize extraction output into KnowledgeInterpretation.

    Supported input
    ---------------

    KnowledgeFact
        fact.interpretation

    ExtractionResult
        extraction_result.interpretation

    Generic extraction object
        extraction_result.entities
        extraction_result.action
        extraction_result.target
        ...

    Existing KnowledgeInterpretation
        returned unchanged after normalization.
    """

    # ================================================================
    # PUBLIC API
    # ================================================================

    def build(
        self,
        source: Any,
    ) -> KnowledgeInterpretation:

        # ------------------------------------------------------------
        # Empty input
        # ------------------------------------------------------------

        if source is None:

            return KnowledgeInterpretation()

        # ------------------------------------------------------------
        # Already KnowledgeInterpretation
        # ------------------------------------------------------------

        if isinstance(
            source,
            KnowledgeInterpretation,
        ):

            self._normalize_interpretation(
                source
            )

            return source

        # ------------------------------------------------------------
        # KnowledgeFact
        # ------------------------------------------------------------
        #
        # THIS IS THE IMPORTANT FIX.
        #
        # KnowledgeFact already contains the interpretation.
        #
        # Do not try to find "action", "entities", "skills", etc.
        # directly on KnowledgeFact.
        #
        # ------------------------------------------------------------

        existing_interpretation = getattr(
            source,
            "interpretation",
            None,
        )

        if isinstance(
            existing_interpretation,
            KnowledgeInterpretation,
        ):

            self._normalize_interpretation(
                existing_interpretation
            )

            return existing_interpretation

        # ------------------------------------------------------------
        # Extraction result containing nested interpretation
        # ------------------------------------------------------------

        nested_interpretation = getattr(
            source,
            "interpretation",
            None,
        )

        if nested_interpretation is not None:

            interpretation = (
                self._convert_nested_interpretation(
                    nested_interpretation
                )
            )

            self._normalize_interpretation(
                interpretation
            )

            return interpretation

        # ------------------------------------------------------------
        # Generic extraction result
        # ------------------------------------------------------------

        interpretation = (
            KnowledgeInterpretation()
        )

        self._copy_extraction_fields(
            source,
            interpretation,
        )

        self._normalize_interpretation(
            interpretation
        )

        return interpretation

    # ================================================================
    # NORMALIZE EXISTING INTERPRETATION
    # ================================================================

    def _normalize_interpretation(
        self,
        interpretation: KnowledgeInterpretation,
    ) -> None:

        if interpretation is None:

            return

        # ------------------------------------------------------------
        # Make sure entities exists
        # ------------------------------------------------------------

        entities = getattr(
            interpretation,
            "entities",
            None,
        )

        if entities is None:

            try:

                interpretation.entities = []

            except Exception:

                pass

        # ------------------------------------------------------------
        # Normalize entity collection
        # ------------------------------------------------------------

        entities = getattr(
            interpretation,
            "entities",
            [],
        )

        entities = self._list_value(
            entities
        )

        entities = (
            self._deduplicate_entities(
                entities
            )
        )

        try:

            interpretation.entities = entities

        except Exception:

            pass

        # ------------------------------------------------------------
        # Compatibility:
        #
        # Some current KnowledgeFact code expects
        #
        #     interpretation.semantic_entities
        #
        # but semantic entities should actually be produced by
        # SemanticResolver.
        #
        # Therefore we DO NOT manufacture SemanticEntity here.
        #
        # We only make sure an existing field is not accidentally
        # destroyed.
        # ------------------------------------------------------------

        if not hasattr(
            interpretation,
            "semantic_entities",
        ):

            try:

                interpretation.semantic_entities = []

            except Exception:

                pass

    # ================================================================
    # NESTED INTERPRETATION
    # ================================================================

    def _convert_nested_interpretation(
        self,
        nested: Any,
    ) -> KnowledgeInterpretation:

        if isinstance(
            nested,
            KnowledgeInterpretation,
        ):

            return nested

        interpretation = (
            KnowledgeInterpretation()
        )

        self._copy_extraction_fields(
            nested,
            interpretation,
        )

        return interpretation

    # ================================================================
    # COPY EXTRACTION FIELDS
    # ================================================================

    def _copy_extraction_fields(
        self,
        source: Any,
        interpretation: KnowledgeInterpretation,
    ) -> None:

        if source is None:

            return

        # ------------------------------------------------------------
        # CORE KNOWLEDGE
        # ------------------------------------------------------------

        self._copy_if_present(
            source,
            interpretation,
            "action",
        )

        self._copy_if_present(
            source,
            interpretation,
            "target",
        )

        self._copy_if_present(
            source,
            interpretation,
            "domain",
        )

        self._copy_if_present(
            source,
            interpretation,
            "metric",
        )

        self._copy_if_present(
            source,
            interpretation,
            "measurement",
        )

        self._copy_if_present(
            source,
            interpretation,
            "practice",
        )

        self._copy_if_present(
            source,
            interpretation,
            "modifiers",
            list_value=True,
        )

        # ------------------------------------------------------------
        # ENTITY COLLECTION
        # ------------------------------------------------------------

        entities = self._get(
            source,
            "entities",
        )

        if entities:

            try:

                interpretation.entities = (
                    self._list_value(
                        entities
                    )
                )

            except Exception:

                pass

        # ------------------------------------------------------------
        # TYPED ENTITY FALLBACK
        # ------------------------------------------------------------

        if not getattr(
            interpretation,
            "entities",
            None,
        ):

            interpretation.entities = (
                self._collect_typed_entities(
                    source
                )
            )

        # ------------------------------------------------------------
        # BUSINESS FLAGS
        # ------------------------------------------------------------

        self._copy_if_present(
            source,
            interpretation,
            "achievement",
        )

        self._copy_if_present(
            source,
            interpretation,
            "quantified",
        )

        self._copy_if_present(
            source,
            interpretation,
            "semantic_type",
        )

        self._copy_if_present(
            source,
            interpretation,
            "business_area",
        )

        # ------------------------------------------------------------
        # CONFIDENCE
        # ------------------------------------------------------------

        self._copy_if_present(
            source,
            interpretation,
            "confidence",
        )

        self._copy_if_present(
            source,
            interpretation,
            "overall_impact_weight",
        )

        # ------------------------------------------------------------
        # EXPLANATION
        # ------------------------------------------------------------

        self._copy_if_present(
            source,
            interpretation,
            "explanation",
        )

    # ================================================================
    # TYPED ENTITY COLLECTION
    # ================================================================

    def _collect_typed_entities(
        self,
        source: Any,
    ) -> list[Any]:

        output: list[Any] = []

        # ------------------------------------------------------------
        # Single-value entities
        # ------------------------------------------------------------

        for name in (
            "action",
            "target",
            "domain",
            "metric",
            "measurement",
            "practice",
            "technology",
            "certification",
            "standard",
            "methodology",
            "skill",
            "kpi",
            "business_kpi",
            "object",
        ):

            value = self._get(
                source,
                name,
            )

            self._append_if_present(
                output,
                value,
            )

        # ------------------------------------------------------------
        # Collection entities
        # ------------------------------------------------------------

        for name in (
            "actions",
            "targets",
            "domains",
            "metrics",
            "measurements",
            "technologies",
            "certifications",
            "standards",
            "methodologies",
            "skills",
            "kpis",
            "business_kpis",
            "objects",
            "modifiers",
            "practices",
        ):

            values = self._get(
                source,
                name,
            )

            if not values:

                continue

            for value in self._list_value(
                values
            ):

                self._append_if_present(
                    output,
                    value,
                )

        return output

    # ================================================================
    # COPY HELPER
    # ================================================================

    @staticmethod
    def _copy_if_present(
        source: Any,
        destination: Any,
        name: str,
        list_value: bool = False,
    ) -> None:

        value = getattr(
            source,
            name,
            None,
        )

        if value is None:

            return

        if list_value:

            value = (
                InterpretationBuilder._list_value(
                    value
                )
            )

        try:

            setattr(
                destination,
                name,
                value,
            )

        except Exception:

            pass

    # ================================================================
    # GET
    # ================================================================

    @staticmethod
    def _get(
        obj: Any,
        name: str,
        default: Any = None,
    ) -> Any:

        if obj is None:

            return default

        return getattr(
            obj,
            name,
            default,
        )

    # ================================================================
    # LIST NORMALIZATION
    # ================================================================

    @staticmethod
    def _list_value(
        value: Any,
    ) -> list[Any]:

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
            set,
        ):

            return list(value)

        return [value]

    # ================================================================
    # DEDUPLICATION
    # ================================================================

    @staticmethod
    def _deduplicate_entities(
        entities: list[Any],
    ) -> list[Any]:

        output: list[Any] = []

        seen: set[str] = set()

        for entity in entities:

            if entity is None:

                continue

            entity_id = getattr(
                entity,
                "entity_id",
                "",
            )

            canonical = getattr(
                entity,
                "canonical",
                "",
            )

            normalized = getattr(
                entity,
                "normalized",
                "",
            )

            original = getattr(
                entity,
                "original",
                "",
            )

            entity_type = getattr(
                entity,
                "entity_type",
                "",
            )

            key = (
                str(entity_id).strip()
                if entity_id
                else (
                    f"{entity_type}:"
                    f"{canonical or normalized or original}"
                )
                .strip()
                .casefold()
            )

            if not key:

                key = (
                    f"object:{id(entity)}"
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

    # ================================================================
    # APPEND HELPER
    # ================================================================

    @staticmethod
    def _append_if_present(
        output: list[Any],
        value: Any,
    ) -> None:

        if value is None:

            return

        if isinstance(
            value,
            (list, tuple, set),
        ):

            for item in value:

                if item is not None:

                    output.append(
                        item
                    )

            return

        output.append(
            value
        )