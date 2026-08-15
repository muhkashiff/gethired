"""
Enterprise Resume Knowledge Pipeline
Enterprise V5

Responsibility:

Resume
    ↓
Resume textual units
    ↓
ExtractionCoordinator
    ↓
KnowledgeV5Pipeline
    ↓
Ontology knowledge entities
    ↓
KnowledgeEntity
    ↓
KnowledgeFact

This layer does NOT:

- tokenize
- match
- calculate confidence
- resolve overlaps
- rank ontology matches
- perform reasoning
- build the knowledge graph

Those responsibilities remain in their existing layers.
"""

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
    ):

        self.coordinator = (
            coordinator
            or ExtractionCoordinator()
        )

    # =========================================================
    # PROCESS ONE TEXT UNIT
    # =========================================================

    def process_sentence(
        self,
        sentence: str,
    ):

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

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # ExtractionCoordinator internally invokes:
        #
        # ExtractionCoordinator
        #       ↓
        # KnowledgeV5Pipeline
        #       ↓
        # Tokenizer
        #       ↓
        # Matcher
        #       ↓
        # Confidence
        #       ↓
        # Overlap
        #       ↓
        # Ranker
        # -----------------------------------------------------

        extraction = self.coordinator.run(
            sentence
        )

        interpretation = (
            KnowledgeInterpretation()
        )

        entities = []

        # =====================================================
        # CONVERT ExtractedEntity
        # → KnowledgeEntity
        # =====================================================

        for extracted in (
            extraction.all_entities
        ):

            entity = KnowledgeEntity(

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
                    .lower()
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

            entities.append(
                entity
            )

        # =====================================================
        # INTERPRETATION
        # =====================================================

        interpretation.entities = (
            entities
        )

        interpretation.confidence = max(
            (
                entity.confidence
                for entity in entities
            ),
            default=0.0,
        )

        # =====================================================
        # FACT
        # =====================================================

        return KnowledgeFact(

            text=sentence,

            interpretation=(
                interpretation
            ),

            source="resume",

            confidence=(
                interpretation.confidence
            ),
        )

    # =========================================================
    # PROCESS MULTIPLE TEXT UNITS
    # =========================================================

    def process(
        self,
        sentences,
    ):

        facts = []

        for sentence in sentences:

            if not isinstance(
                sentence,
                str,
            ):

                continue

            sentence = sentence.strip()

            if not sentence:

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