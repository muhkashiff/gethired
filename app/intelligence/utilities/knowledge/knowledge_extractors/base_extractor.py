"""
Enterprise Base Extractor
Enterprise V5

Only responsibility:

MatchResult  ---> Knowledge Object

Pipeline is completely independent.
"""

from abc import ABC
from abc import abstractmethod

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import MatchResult


class BaseExtractor(ABC):

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        pipeline,

    ):

        self.pipeline = pipeline

    ####################################################################
    # PARSER CONTEXT
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
    # POPULATE SHARED FIELDS
    ####################################################################

    def populate_entity(

        self,

        model,

        match: MatchResult,

    ):

        entity = match.entity

        model.found = True

        model.confidence = match.confidence

        model.original = match.phrase

        model.matched_phrase = match.phrase

        model.canonical = entity.canonical

        model.normalized = entity.normalized

        model.entity_id = entity.entity_id

        model.entity_type = entity.entity_type

        model.category = entity.category

        model.business_area = entity.business_area

        model.domain = entity.domain

        model.description = entity.description

        model.impact_weight = entity.impact_weight

        model.source = entity.source

        model.metadata = entity.metadata

        model.matched_alias = match.matched_alias

        model.is_alias = match.is_alias

        model.start_char = match.start_char

        model.end_char = match.end_char

        model.token_index = match.token_index

        model.token_count = match.token_count

        model.sentence_index = 0

        return model

    ####################################################################
    # ABSTRACT
    ####################################################################

    @abstractmethod
    def extract(

        self,

        sentence,

    ):

        pass