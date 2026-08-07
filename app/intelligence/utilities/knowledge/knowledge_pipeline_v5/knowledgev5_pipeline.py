"""
Enterprise Knowledge Pipeline
Enterprise V5

Single responsibility:

Sentence
    ↓
Tokenizer
    ↓
Repository
    ↓
Matcher
    ↓
Confidence
    ↓
Overlap Resolver
    ↓
Ranker
    ↓
List[MatchResult]
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository

from .tokenizer.tokenizer import Tokenizer

from .matcher.matcher import Matcher

from .overlap.overlap_resolver import OverlapResolver

from .ranker.ranker import Ranker

from .confidence.confidence_calculator import ConfidenceCalculator


class KnowledgeV5Pipeline:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository_instance=None,

        tokenizer=None,

        matcher=None,

        confidence=None,

        overlap=None,

        ranker=None,

    ):

        ############################################################

        self.repository = repository_instance or repository 

        ############################################################

        self.tokenizer = tokenizer or Tokenizer()

        ############################################################

        self.matcher = matcher or Matcher(

            repository=self.repository,

            tokenizer=self.tokenizer,

        )

        ############################################################

        self.confidence = confidence or ConfidenceCalculator(
            repository=self.repository
        )

        ############################################################

        self.overlap = overlap or OverlapResolver()

        ############################################################

        self.ranker = ranker or Ranker()

    ####################################################################
    # BUILD PARSER CONTEXT
    ####################################################################

    def build_parser_context(

        self,

        verb=False,

        obj=False,

        metric=False,

        modifier=False,

        numeric=False,

        domain=False,

    ):

        return {

            "verb_found": verb,

            "object_found": obj,

            "metric_found": metric,

            "modifier_found": modifier,

            "numeric_value": numeric,

            "domain_found": domain,

        }

    ####################################################################
    # RUN PIPELINE
    ####################################################################

    def run(

        self,

        ontology,

        sentence,

    ):

        ############################################################
        # Stage 1
        ############################################################

        matches = self.matcher.match(

            ontology,

            sentence,

        )

        ############################################################
        # Stage 2
        ############################################################

        ############################################################
        # Confidence
        ############################################################

        matches = self.confidence.score_all(matches)
        ############################################################
        # Stage 3
        ############################################################

        matches = self.overlap.clean(

            matches,

        )

        ############################################################
        # Stage 4
        ############################################################

        matches = self.ranker.rank(

            matches,

        )

        ############################################################

        return matches

    ####################################################################
    # BEST MATCH
    ####################################################################

    def best(

        self,

        ontology,

        sentence,

    ):

        matches = self.run(

            ontology,

            sentence,

        )

        if matches:

            return matches[0]

        return None