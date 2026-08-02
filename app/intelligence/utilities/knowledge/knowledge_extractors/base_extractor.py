"""
Enterprise Base Extractor

Shared functionality for every ontology extractor.

Responsibilities
----------------
✓ Repository dependency injection
✓ Confidence calculator injection
✓ Text cleaning
✓ Tokenization
✓ N-Gram generation
✓ N-Gram caching

Version : Enterprise V4
"""

from __future__ import annotations

import re

from typing import List, Tuple

from app.intelligence.utilities.knowledge.repository.repository import Repository

from app.intelligence.utilities.knowledge.knowledge_extractors.confidence_calculator import (
    ConfidenceCalculator,
)


class BaseExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        repository=None,

        confidence=None,

    ):

        self.repository = repository or Repository()

        self.confidence = (

            confidence

            or ConfidenceCalculator(

                self.repository

            )

        )

        # Maximum phrase length searched
        self.max_ngram = 5

        # NGram cache
        self._cached_sentence = None

        self._cached_ngrams = None

    ####################################################################
    # CLEAN
    ####################################################################

    def clean(

        self,

        text,

    ):

        """
        Standard cleaning before extraction.
        """

        if text is None:

            return ""

        if isinstance(text, list):

            text = " ".join(text)

        text = str(text)

        text = text.replace(

            "\n",

            " "

        )

        text = re.sub(

            r"\s+",

            " ",

            text,

        )

        return text.strip()

    ####################################################################
    # TOKENIZER
    ####################################################################

    def tokenize(

        self,

        sentence,

    ):

        """
        Enterprise tokenizer.

        Supports:

        ISO 9001:2015

        FSSC22000

        GMP

        5S

        C++

        AI/ML

        ERP-SAP
        """

        matches = list(

            re.finditer(

                r"[A-Za-z0-9:+./&_-]+",

                sentence,

            )

        )

        words = [

            m.group()

            for m in matches

        ]

        return words, matches

    ####################################################################
    # NGRAM GENERATION
    ####################################################################

    def generate_ngrams(

        self,

        sentence,

    ) -> List[Tuple[str, int, int]]:

        """
        Cached NGram generator.

        Returns

        (phrase,

         token_index,

         token_count)
        """

        if (

            self._cached_sentence

            == sentence

        ):

            return self._cached_ngrams

        words, _ = self.tokenize(sentence)

        results = []

        for n in range(

            self.max_ngram,

            0,

            -1,

        ):

            for i in range(

                len(words)

                - n

                + 1

            ):

                phrase = " ".join(

                    words[i:i+n]

                )

                results.append(

                    (

                        phrase,

                        i,

                        n,

                    )

                )

        self._cached_sentence = sentence

        self._cached_ngrams = results

        return results
    ####################################################################
    # POSITION DETECTION
    ####################################################################

    def get_position(

        self,

        sentence,

        phrase,

    ):

        """
        Returns

        start_char,
        end_char,
        token_index
        """

        match = re.search(

            r"\b"

            + re.escape(phrase)

            + r"\b",

            sentence,

            flags=re.IGNORECASE,

        )

        if not match:

            return -1, -1, -1

        token_index = len(

            sentence[: match.start()].split()

        )

        return (

            match.start(),

            match.end(),

            token_index,

        )

    ####################################################################
    # DUPLICATE DETECTION
    ####################################################################

    def already_seen(

        self,

        entity,

        seen,

    ):

        """
        Prevent duplicate ontology entities.
        """

        if entity.entity_id in seen:

            return True

        seen.add(

            entity.entity_id

        )

        return False

    ####################################################################
    # PARSER CONTEXT BUILDER
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

        """
        Shared parser context used by
        Confidence Calculator.
        """

        return {

            "verb_found": verb,

            "object_found": obj,

            "metric_found": metric,

            "modifier_found": modifier,

            "numeric_value": numeric,

            "domain_found": domain,

        }

    ####################################################################
    # ENTITY LOOKUP
    ####################################################################

    def lookup_entity(

        self,

        ontology,

        phrase,

    ):

        """
        Generic repository lookup.
        """

        return self.repository.find_entity(

            ontology,

            phrase,

        )

    ####################################################################
    # ENTITY LOOKUP (EXACT)
    ####################################################################

    def lookup_exact(

        self,

        ontology,

        phrase,

    ):

        """
        Optional exact lookup.
        Useful for IDs and Standards.
        """

        return self.repository.find_entity_exact(

            ontology,

            phrase,

        )

    ####################################################################
    # LOOKUP MULTIPLE
    ####################################################################

    def lookup_all(

        self,

        ontology,

        sentence,

    ):

        """
        Returns every ontology candidate
        found inside a sentence.

        Output

        [

            {

                entity,

                phrase,

                confidence,

                start_char,

                end_char,

                token_index,

                token_count,

                matched_alias

            }

        ]
        """

        candidates = []

        seen = set()

        for (

            phrase,

            token_index,

            token_count,

        ) in self.generate_ngrams(sentence):

            entity = self.lookup_entity(

                ontology,

                phrase,

            )

            if entity is None:

                continue

            if self.already_seen(

                entity,

                seen,

            ):

                continue

            start_char, end_char, _ = self.get_position(

                sentence,

                phrase,

            )

            parser_context = self.build_parser_context()

            confidence = self.confidence.calculate(

                phrase=phrase,

                entity=entity,

                sentence=sentence,

                parser_context=parser_context,

            )

            candidates.append(

                {
                    "entity": entity,
                    "phrase": phrase,

                    "matched_alias":
                    (
                        phrase.lower()
                        != entity.canonical.lower()
                    ),

                    "confidence": self.confidence.calculate(
                        phrase,
                        entity
                    ),

                    "start_char": start_char,

                    "end_char": end_char,

                    "token_index": token_index,

                    "token_count": token_count,
                }

            )

        return candidates
    ####################################################################
    # REMOVE OVERLAPPING MATCHES
    ####################################################################

    def remove_overlaps(

        self,

        candidates,

    ):

        """
        Keep the longest match when two ontology
        candidates overlap.

        Example

        Food Safety
        Food Safety Management

        keeps only

        Food Safety Management
        """

        candidates = sorted(

            candidates,

            key=lambda c: (

                c["token_count"],

                c["confidence"],

            ),

            reverse=True,

        )

        accepted = []

        occupied = set()

        for candidate in candidates:

            token_range = set(

                range(

                    candidate["token_index"],

                    candidate["token_index"]

                    + candidate["token_count"],

                )

            )

            if occupied.intersection(token_range):

                continue

            accepted.append(candidate)

            occupied.update(token_range)

        return sorted(

            accepted,

            key=lambda x: x["token_index"]

        )

    ####################################################################
    # SORT CANDIDATES
    ####################################################################

    def rank_candidates(

        self,

        candidates,

    ):

        """
        Highest confidence first.

        Longest phrase preferred.

        Highest impact preferred.
        """

        return sorted(

            candidates,

            key=lambda x: (

                x["confidence"],

                x["token_count"],

                x["entity"].impact_weight,

            ),

            reverse=True,

        )

    ####################################################################
    # ENTITY TO MODEL
    ####################################################################

    def populate_entity(

        self,

        model,

        candidate,

    ):

        """
        Copies every shared ontology field into
        KnowledgeEntity-derived models.
        """

        entity = candidate["entity"]

        model.found = True

        model.confidence = candidate["confidence"]

        model.original = candidate["phrase"]

        model.canonical = entity.canonical

        model.normalized = entity.normalized

        model.entity_id = entity.entity_id

        model.entity_type = entity.entity_type

        model.category = entity.category

        model.business_area = entity.business_area

        model.domain = entity.domain

        model.impact_weight = entity.impact_weight

        model.source = entity.source

        model.matched_phrase = candidate["phrase"]

        model.matched_alias = candidate["matched_alias"]

        model.metadata = entity.metadata

        model.start_char = candidate["start_char"]

        model.end_char = candidate["end_char"]

        model.token_index = candidate["token_index"]

        model.token_count = candidate["token_count"]

        model.sentence_index = 0

        return model

    ####################################################################
    # COMPLETE EXTRACTION PIPELINE
    ####################################################################

    def extract_candidates(

        self,

        ontology,

        sentence,

    ):

        """
        Complete enterprise pipeline.

        sentence

             ↓

        lookup_all()

             ↓

        remove_overlaps()

             ↓

        rank_candidates()

        """

        candidates = self.lookup_all(

            ontology,

            sentence,

        )

        candidates = self.remove_overlaps(

            candidates,

        )

        candidates = self.rank_candidates(

            candidates,

        )

        return candidates