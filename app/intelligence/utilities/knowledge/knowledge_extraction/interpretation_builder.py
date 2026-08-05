"""
Enterprise Interpretation Builder

Enterprise V12

Extraction Results
        ↓
Knowledge Interpretation

This is the bridge between
Knowledge Extraction
and
Semantic Reasoning.
"""

from app.intelligence.utilities.knowledge.knowledge_models.knowledge_models import (
    KnowledgeInterpretation,
)


class InterpretationBuilder:

    ####################################################################
    # BUILD
    ####################################################################

    def build(

        self,

        extraction_result,

    ):

        """
        Convert ExtractionResult
        →
        KnowledgeInterpretation
        """

        interpretation = KnowledgeInterpretation()

        # -------------------------------------------------------------
        # Sentence
        # -------------------------------------------------------------

        interpretation.original_text = extraction_result.sentence.text

        # -------------------------------------------------------------
        # Entities
        # -------------------------------------------------------------

        interpretation.entities = extraction_result.entities

        # -------------------------------------------------------------
        # Metadata
        # -------------------------------------------------------------

        interpretation.metadata = {

            "section": extraction_result.sentence.section,

            "sentence_id": extraction_result.sentence.sentence_id,

            "position": extraction_result.sentence.position,

        }

        # -------------------------------------------------------------
        # Confidence
        # -------------------------------------------------------------

        interpretation.confidence = extraction_result.confidence

        return interpretation