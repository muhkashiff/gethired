"""
Knowledge Pipeline

Master orchestration layer for the GetHired Intelligence Engine.

Pipeline

Sentence
    ↓
ClauseParser
    ↓
ClauseRebuilder
    ↓
ClauseNormalizer
    ↓
ActionSegmenter
    ↓
SentenceParser
    ↓
KnowledgeDocument
"""

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
    KnowledgeSentence,
    KnowledgeClause,
)

from app.intelligence.utilities.knowledge.knowledge_parser.clause_parser import (
    ClauseParser,
)

from app.intelligence.utilities.knowledge.knowledge_parser.clause_rebuilder import (
    ClauseRebuilder,
)

from app.intelligence.utilities.knowledge.knowledge_parser.clause_normalizer import (
    ClauseNormalizer,
)

from app.intelligence.utilities.knowledge.knowledge_parser.action_segmenter import (
    ActionSegmenter,
)

from app.intelligence.utilities.knowledge.knowledge_parser.sentence_parser import (
    SentenceParser,
)


class KnowledgePipeline:

    def __init__(self):

        self.clause_parser = ClauseParser()

        self.clause_rebuilder = ClauseRebuilder()

        self.clause_normalizer = ClauseNormalizer()

        self.action_segmenter = ActionSegmenter()

        self.sentence_parser = SentenceParser()

    # ----------------------------------------------------------

    def process(self, sentence: str) -> KnowledgeDocument:

        document = KnowledgeDocument()

        # --------------------------------------------------
        # Parse Clauses
        # --------------------------------------------------

        clauses = self.clause_parser.parse(sentence)

        clauses = self.clause_rebuilder.rebuild(clauses)

        clauses = self.clause_normalizer.normalize(clauses)

        # --------------------------------------------------
        # Split Multiple Actions
        # --------------------------------------------------

        segmented = []

        for clause in clauses:

            segmented.extend(

                self.action_segmenter.segment(clause)

            )

        segmented = self.clause_normalizer.normalize(segmented)

        # --------------------------------------------------
        # Build Sentence Object
        # --------------------------------------------------

        sentence_obj = KnowledgeSentence(

            original_text=sentence

        )

        # --------------------------------------------------
        # Parse Every Clause
        # --------------------------------------------------

        all_sentence_facts = []

        clause_confidences = []

        for clause in segmented:

            clause_obj = KnowledgeClause(

                original_text=clause.text

            )

            parsed_sentence = self.sentence_parser.parse(

                clause.text

            )

            clause_obj.facts = parsed_sentence.facts

            clause_obj.confidence = parsed_sentence.confidence

            sentence_obj.clauses.append(clause_obj)

            all_sentence_facts.extend(

                parsed_sentence.facts

            )

            clause_confidences.append(

                parsed_sentence.confidence

            )

        # --------------------------------------------------
        # Sentence Summary
        # --------------------------------------------------

        sentence_obj.facts = all_sentence_facts

        if clause_confidences:

            sentence_obj.confidence = round(

                sum(clause_confidences)

                / len(clause_confidences),

                2,

            )

        # --------------------------------------------------
        # Document
        # --------------------------------------------------

        document.sentences.append(

            sentence_obj

        )

        document.facts.extend(

            all_sentence_facts

        )

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        document.statistics = {

            "input_sentences": 1,

            "clauses": len(sentence_obj.clauses),

            "facts": len(document.facts),

        }

        # --------------------------------------------------
        # Document Confidence
        # --------------------------------------------------

        if document.sentences:

            document.confidence = round(

                sum(

                    s.confidence

                    for s in document.sentences

                )

                / len(document.sentences),

                2,

            )

        return document