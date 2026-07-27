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
ClauseNormalizer
    ↓
SentenceParser
    ↓
KnowledgeDocument
"""

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeDocument,
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

    def process(
        self,
        sentence: str,
    ) -> KnowledgeDocument:

        document = KnowledgeDocument()

        # --------------------------------------------------
        # Parse clauses
        # --------------------------------------------------

        clauses = self.clause_parser.parse(sentence)

        # --------------------------------------------------
        # Cleanup
        # --------------------------------------------------

        clauses = self.clause_rebuilder.rebuild(clauses)

        clauses = self.clause_normalizer.normalize(clauses)

        # --------------------------------------------------
        # Split multiple actions
        # --------------------------------------------------

        segmented = []

        for clause in clauses:

            segmented.extend(

                self.action_segmenter.segment(clause)

            )

        # --------------------------------------------------
        # Normalize again
        # --------------------------------------------------

        segmented = self.clause_normalizer.normalize(segmented)

        # --------------------------------------------------
        # Parse every action clause
        # --------------------------------------------------

        for clause in segmented:

            parsed = self.sentence_parser.parse(clause.text)

            document.sentences.append(parsed)

            document.facts.extend(parsed.facts)

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        document.statistics = {

            "input_sentences": 1,

            "clauses": len(segmented),

            "facts": len(document.facts),

        }

        # --------------------------------------------------
        # Confidence
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