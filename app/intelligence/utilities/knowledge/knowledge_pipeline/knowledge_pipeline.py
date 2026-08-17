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
    ↓
KnowledgeGraph
    ↓
KnowledgeProfile
"""

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph_builder import (
    KnowledgeGraphBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.knowledge_profile_builder import (
    ProfileBuilder,
)

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
from app.intelligence.utilities.knowledge.knowledge_parser.purpose_clause_detector import (
    PurposeClauseDetector,
)
from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_connector_detector import (
    SemanticConnectorDetector,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline.pipeline_result import (
    PipelineResult,
)
from app.intelligence.utilities.knowledge.semantic_reasoning.semantic_resolver import (
    SemanticResolver,
)


class KnowledgePipeline:

    def __init__(self):

        self.connector_detector = SemanticConnectorDetector()

        self.semantic_resolver = SemanticResolver()

        self.purpose_detector = PurposeClauseDetector()

        self.clause_parser = ClauseParser()

        self.clause_rebuilder = ClauseRebuilder()

        self.clause_normalizer = ClauseNormalizer()

        self.action_segmenter = ActionSegmenter()

        self.sentence_parser = SentenceParser()

        self.graph_builder = KnowledgeGraphBuilder()

        self.profile_builder = ProfileBuilder()

    # ----------------------------------------------------------

    def process(self, sentence: str):

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

            pieces = self.action_segmenter.segment(clause)

            rebuilt = []

            for piece in pieces:

                if (

                    rebuilt

                    and (

                        self.purpose_detector.is_purpose_clause(piece.text)

                        or

                        self.connector_detector.is_connector(piece.text)

                    )

                ):

                    rebuilt[-1].text = (

                        rebuilt[-1].text.rstrip()

                        + " "

                        + piece.text.lstrip()

                    )

                else:

                    rebuilt.append(piece)

            segmented.extend(rebuilt)

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

            parsed_clause = self.sentence_parser.parse(

                clause.text

            )

            clause_obj.facts = parsed_clause.facts

            clause_obj.confidence = parsed_clause.confidence

            sentence_obj.clauses.append(clause_obj)

            all_sentence_facts.extend(

                parsed_clause.facts

            )

            clause_confidences.append(

                parsed_clause.confidence

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

            "actions": sum(

                1

                for fact in document.facts

                if fact.interpretation.action.found

            ),

            "objects": sum(

                1

                for fact in document.facts

                if fact.interpretation.object.found

            ),

            "metrics": sum(

                1

                for fact in document.facts

                if fact.interpretation.metric.found

            ),

            "measurements": sum(

                1

                for fact in document.facts

                if fact.interpretation.measurement.found

            ),

            "domains": len({

                fact.interpretation.domain.entity_id

                for fact in document.facts

                if fact.interpretation.domain.found

            }),

        }

        # --------------------------------------------------
        # Document Confidence
        # --------------------------------------------------

        if document.sentences:

            document.confidence = round(

                sum(

                    sentence.confidence

                    for sentence in document.sentences

                )

                / len(document.sentences),

                2,

            )

        # ==================================================
        # Semantic Resolution
        # ==================================================

        semantic_result = self.semantic_resolver.resolve(
            document.facts
        )

        # ==================================================
        # Build Enterprise Knowledge Graph
        # ==================================================

        from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph import (
            KnowledgeGraph,
        )

        enterprise_graph = KnowledgeGraph()

        for statement in semantic_result.business_statements:

            graph = self.graph_builder.build(statement)

            #
            # Merge nodes
            #
            if isinstance(enterprise_graph.nodes, dict):

                enterprise_graph.nodes.update(graph.nodes)

            else:

                enterprise_graph.nodes.extend(graph.nodes)

            #
            # Merge edges
            #
            enterprise_graph.nodes.update(graph.nodes)

            enterprise_graph.edges.update(graph.edges)
        #
        # Update statistics if available
        #
        if hasattr(enterprise_graph, "update_statistics"):

            enterprise_graph.update_statistics()

        # ==================================================
        # Build Knowledge Profile
        # ==================================================

        knowledge_profile = self.profile_builder.build(
            enterprise_graph
        )

        # ==================================================
        # Unified Pipeline Result
        # ==================================================

        return PipelineResult(

            knowledge_document=document,

            semantic_result=semantic_result,

            graph_document=enterprise_graph,

            knowledge_profile=knowledge_profile,

        )