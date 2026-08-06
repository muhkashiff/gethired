"""
Enterprise Tokenizer

Enterprise V5

Responsibilities
----------------
• Tokenization
• Normalization
• NGram Generation
• Character Position Tracking
• Cache Management

Everything in the system starts here.
"""

from __future__ import annotations

from typing import List
from typing import Tuple

from .cache import TokenizationCache
from .normalizer import Normalizer
from .ngrams import NGramGenerator
from .tokenizer_rules import TOKEN_PATTERN


class Tokenizer:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(

        self,

        max_ngram: int = 5,

    ):

        self.cache = TokenizationCache()

        self.normalizer = Normalizer()

        self.ngram_generator = NGramGenerator(

            max_ngram=max_ngram

        )

    ####################################################################
    # TOKENIZE
    ####################################################################

    def tokenize(

        self,

        sentence: str,

    ) -> Tuple[List[str], list]:

        """
        Enterprise tokenizer.

        Supports

        ISO 9001
        ISO 9001:2015
        FSSC22000
        GMP
        5S
        AI/ML
        ERP-SAP
        C++
        """

        ############################################################

        if sentence == self.cache.sentence:

            return (

                self.cache.tokens,

                self.cache.matches,

            )

        ############################################################

        matches = list(

            TOKEN_PATTERN.finditer(

                sentence

            )

        )

        tokens = [

            m.group()

            for m in matches

        ]

        ############################################################

        self.cache.clear()

        self.cache.sentence = sentence

        self.cache.tokens = tokens

        self.cache.matches = matches

        ############################################################

        for index, match in enumerate(matches):

            self.cache.token_positions[index] = (

                match.start(),

                match.end(),

            )

        ############################################################

        return tokens, matches

    ####################################################################
    # NORMALIZE
    ####################################################################

    def normalize(

        self,

        phrase: str,

    ) -> str:

        if phrase in self.cache.normalized:

            return self.cache.normalized[phrase]

        normalized = self.normalizer.normalize(

            phrase

        )

        self.cache.normalized[phrase] = normalized

        return normalized

    ####################################################################
    # NGRAMS
    ####################################################################

    def generate_ngrams(

        self,

        sentence: str,

    ):

        """
        Returns

        (

            phrase,

            token_index,

            token_count

        )
        """

        ############################################################

        if (

            sentence == self.cache.sentence

            and

            self.cache.ngrams

        ):

            return self.cache.ngrams

        ############################################################

        tokens, _ = self.tokenize(

            sentence

        )

        ngrams = self.ngram_generator.generate(

            tokens

        )

        self.cache.ngrams = ngrams

        return ngrams

    ####################################################################
    # POSITION
    ####################################################################

    def get_char_position(

        self,

        token_index: int,

        token_count: int,

    ):

        """
        Convert token positions
        into character positions.
        """

        start = self.cache.token_positions[

            token_index

        ][0]

        end = self.cache.token_positions[

            token_index +

            token_count -

            1

        ][1]

        return start, end

    ####################################################################
    # TOKEN COUNT
    ####################################################################

    def token_count(

        self,

        sentence,

    ):

        tokens, _ = self.tokenize(

            sentence

        )

        return len(tokens)

    ####################################################################
    # RESET
    ####################################################################

    def clear_cache(

        self,

    ):

        self.cache.clear()