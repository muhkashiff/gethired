"""
Semantic Pipeline

Converts resume text into a SemanticDocument.

Pipeline

Resume
    ↓
Sentences
    ↓
Clauses
    ↓
Knowledge Interpretation
    ↓
SemanticClause
    ↓
SemanticSentence
    ↓
SemanticDocument
"""

import re
from statistics import mean

from app.intelligence.utilities.knowledge.knowledge_parser.clause_segmenter import (
    ClauseSegmenter,
)

from app.intelligence.utilities.knowledge.knowledge_parser.sentence_parser import (
    SentenceParser,
)

from app.intelligence.utilities.knowledge.semantic_models.semantic_clause import (
    SemanticClause,
)

from app.intelligence.utilities.knowledge.semantic_models.semantic_sentence import (
    SemanticSentence,
)

from app.intelligence.utilities.knowledge.semantic_models.semantic_document import (
    SemanticDocument,
)


class SemanticPipeline:

    def __init__(self):

        self.segmenter = ClauseSegmenter()

        self.parser = SentenceParser()

    # ---------------------------------------------------------

    def process(
        self,
        text: str,
    ) -> SemanticDocument:

        sentences = self._split_sentences(text)

        semantic_sentences = []

        clause_count = 0

        confidences = []

        for sentence in sentences:

            semantic_sentence = self._process_sentence(sentence)

            semantic_sentences.append(semantic_sentence)

            clause_count += len(semantic_sentence.clauses)

            confidences.extend(
                [
                    c.confidence
                    for c in semantic_sentence.clauses
                ]
            )

        statistics = {

            "sentences": len(semantic_sentences),

            "clauses": clause_count,

        }

        document_confidence = (
            round(mean(confidences), 2)
            if confidences
            else 0.0
        )

        return SemanticDocument(

            sentences=semantic_sentences,

            statistics=statistics,

            confidence=document_confidence,

        )

    # ---------------------------------------------------------

    def _process_sentence(
        self,
        sentence,
    ):

        clauses = self.segmenter.segment(sentence)

        semantic_clauses = []

        clause_confidence = []

        for clause in clauses:

            parsed = self.parser.parse(clause.text)

            fact = parsed.facts[0]

            semantic_clause = SemanticClause(

                text=clause.text,

                normalized_text=clause.text,

                index=clause.index,

                parent_sentence=sentence,

                confidence=fact.confidence,

                action=fact.interpretation.action,

                object=fact.interpretation.object,

                domain=fact.interpretation.domain,

                metric=fact.interpretation.metric,

                measurement=fact.interpretation.measurement,

                modifiers=fact.interpretation.modifiers,

                interpretation=fact.interpretation,

                achievement=fact.achievement,

                quantified=fact.quantified,

                executive_signal=False,

                semantic_type=fact.interpretation.semantic_type,

                business_area=fact.interpretation.business_area,

                source=fact.source,

            )

            semantic_clauses.append(
                semantic_clause
            )

            clause_confidence.append(
                semantic_clause.confidence
            )

        return SemanticSentence(

            original_text=sentence,

            clauses=semantic_clauses,

            confidence=(
                round(mean(clause_confidence), 2)
                if clause_confidence
                else 0.0
            ),

        )

    # ---------------------------------------------------------

    @staticmethod
    def _split_sentences(text):

        return [

            s.strip()

            for s in re.split(

                r"(?<=[.!?])\s+",

                text.strip(),

            )

            if s.strip()

        ]