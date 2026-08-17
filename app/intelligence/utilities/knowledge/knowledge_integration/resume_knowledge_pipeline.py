from __future__ import annotations

"""
Enterprise Resume Knowledge Pipeline
Enterprise V5

Architecture
------------

Sentence
    ↓
ExtractionCoordinator
    ↓
KnowledgeV5Pipeline
    ↓
ExtractedEntity
    ↓
KnowledgeEntity
    ↓
KnowledgeInterpretation
    ↓
KnowledgeFact
"""

from typing import Iterable

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
    ExtractionCoordinator,
)


class ResumeKnowledgePipeline:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        coordinator=None,
    ) -> None:

        self.coordinator = (
            coordinator
            or ExtractionCoordinator()
        )

    # =========================================================
    # PROCESS ONE SENTENCE
    # =========================================================

    def process_sentence(
        self,
        sentence: str,
    ) -> KnowledgeFact | None:

        if not isinstance(
            sentence,
            str,
        ):
            raise TypeError(
                "sentence must be a string."
            )

        sentence = sentence.strip()

        if not sentence:
            return None

        # =====================================================
        # EXTRACTION
        # =====================================================

        extraction = self.coordinator.run(
            sentence
        )

        # =====================================================
        # CREATE INTERPRETATION
        # =====================================================

        interpretation = (
            KnowledgeInterpretation()
        )

        # =====================================================
        # CONVERT EXTRACTED ENTITIES
        # =====================================================

        knowledge_entities = []

        for extracted in (
            extraction.all_entities
        ):

            if extracted is None:
                continue

            knowledge_entity = (
                KnowledgeEntity(

                    found=True,

                    confidence=float(
                        extracted.confidence
                    ),

                    extraction_method=(
                        "knowledge_v5"
                    ),

                    original=(
                        extracted.phrase
                    ),

                    canonical=(
                        extracted.canonical
                    ),

                    normalized=(
                        extracted.canonical
                        .strip()
                        .casefold()
                    ),

                    entity_id=(
                        extracted.entity_id
                    ),

                    entity_type=(
                        extracted.entity_type
                    ),

                    category=(
                        extracted.category
                    ),

                    ontology_name=(
                        extracted.ontology
                    ),

                    business_area=(
                        extracted.business_area
                    ),

                    domain=(
                        extracted.domain
                    ),

                    impact_weight=float(
                        extracted.impact_weight
                    ),

                    source="resume",

                    matched_phrase=(
                        extracted.phrase
                    ),

                    matched_alias=(
                        extracted.is_alias
                    ),

                    start_char=int(
                        extracted.start_char
                    ),

                    end_char=int(
                        extracted.end_char
                    ),

                    token_index=int(
                        extracted.token_index
                    ),

                    token_count=int(
                        extracted.token_count
                    ),

                    metadata=dict(
                        extracted.metadata
                        or {}
                    ),
                )
            )

            knowledge_entities.append(
                knowledge_entity
            )

        # =====================================================
        # INTERPRETATION ENTITY HANDOFF
        # =====================================================

        interpretation.entities = (
            knowledge_entities
        )

        # =====================================================
        # CONFIDENCE
        # =====================================================

        interpretation.confidence = max(
            (
                entity.confidence
                for entity in knowledge_entities
            ),
            default=0.0,
        )

        # =====================================================
        # QUANTIFICATION
        # =====================================================

        interpretation.quantified = any(
            bool(
                getattr(
                    entity,
                    "metadata",
                    {},
                ).get(
                    "quantified",
                    False,
                )
            )
            for entity in knowledge_entities
        )

        # =====================================================
        # FACT
        # =====================================================

        fact = KnowledgeFact(

            text=sentence,

            interpretation=(
                interpretation
            ),

            source="resume",

            confidence=(
                interpretation.confidence
            ),
        )

        return fact

    # =========================================================
    # PROCESS MANY SENTENCES
    # =========================================================

    def process(
        self,
        sentences: Iterable[str],
    ) -> list[KnowledgeFact]:

        facts = []

        for sentence in sentences:

            if not isinstance(
                sentence,
                str,
            ):
                continue

            fact = (
                self.process_sentence(
                    sentence
                )
            )

            if fact is not None:

                facts.append(
                    fact
                )

        return facts