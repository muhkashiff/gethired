from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.entity_models import (
    KnowledgeEntity,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
    ExtractionCoordinator,
)


class ResumeKnowledgePipeline:

    def __init__(
        self,
        coordinator=None,
    ):

        self.coordinator = (
            coordinator
            or ExtractionCoordinator()
        )

    # =========================================================
    # PROCESS ONE RESUME LINE
    # =========================================================

    def process_sentence(
        self,
        sentence: str,
    ):

        extraction = self.coordinator.run(
            sentence
        )

        interpretation = KnowledgeInterpretation()

        entities = []

        for extracted in extraction.all_entities:

            entity = KnowledgeEntity(

                found=True,

                confidence=extracted.confidence,

                extraction_method="knowledge_v5",

                original=extracted.phrase,

                canonical=extracted.canonical,

                normalized=extracted.canonical.lower(),

                entity_id=extracted.entity_id,

                entity_type=extracted.entity_type,

                category=extracted.category,

                business_area=extracted.business_area,

                domain=extracted.domain,

                impact_weight=extracted.impact_weight,

                source="resume",

                matched_phrase=extracted.phrase,

                matched_alias=extracted.is_alias,

                start_char=extracted.start_char,

                end_char=extracted.end_char,

                token_index=extracted.token_index,

                token_count=extracted.token_count,

                metadata=extracted.metadata,

            )

            entities.append(
                entity
            )

        interpretation.entities = entities

        interpretation.confidence = (
            max(
                (
                    entity.confidence
                    for entity in entities
                ),
                default=0.0,
            )
        )

        fact = KnowledgeFact(

            text=sentence,

            interpretation=interpretation,

            source="resume",

            confidence=interpretation.confidence,

        )

        return fact

    # =========================================================
    # PROCESS MULTIPLE SENTENCES
    # =========================================================

    def process(
        self,
        sentences,
    ):

        facts = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            facts.append(
                self.process_sentence(
                    sentence
                )
            )

        return facts