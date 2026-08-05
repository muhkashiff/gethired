"""
Enterprise Fact Builder

Enterprise V12

KnowledgeInterpretation
        ↓
KnowledgeFact
"""

from app.intelligence.utilities.knowledge.knowledge_models.knowledge_models import (
    KnowledgeFact,
)


class FactBuilder:

    ####################################################################
    # BUILD
    ####################################################################

    def build(

        self,

        interpretation,

    ):

        fact = KnowledgeFact(

            text=interpretation.original_text,

            interpretation=interpretation,

            confidence=interpretation.confidence,

            source="resume",

        )

        return fact

    ####################################################################
    # BUILD MANY
    ####################################################################

    def build_many(

        self,

        interpretations,

    ):

        return [

            self.build(i)

            for i in interpretations

        ]