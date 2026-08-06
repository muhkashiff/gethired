"""
Enterprise Tokenizer
Enterprise V5
"""

from .cache import TokenizationCache
from .normalizer import Normalizer
from .ngrams import NGramGenerator
from .tokenizer_rules import TOKEN_PATTERN


class Tokenizer:

    def __init__(self, max_ngram=5):

        self.cache = TokenizationCache()

        self.normalizer = Normalizer()

        self.ngram_generator = NGramGenerator(max_ngram)

    # -----------------------------------------------------

    def tokenize(self, sentence):

        if sentence == self.cache.sentence:

            return self.cache.tokens

        matches = list(TOKEN_PATTERN.finditer(sentence))

        tokens = [m.group() for m in matches]

        self.cache.clear()

        self.cache.sentence = sentence

        self.cache.tokens = tokens

        self.cache.matches = matches

        for index, match in enumerate(matches):

            self.cache.token_positions[index] = (

                match.start(),

                match.end(),

            )

        return tokens

    # -----------------------------------------------------

    def normalize(self, phrase):

        if phrase in self.cache.normalized:

            return self.cache.normalized[phrase]

        normalized = self.normalizer.normalize(phrase)

        self.cache.normalized[phrase] = normalized

        return normalized

    # -----------------------------------------------------

    def generate_ngrams(self, sentence):

        if (
            sentence == self.cache.sentence
            and self.cache.ngrams
        ):
            return self.cache.ngrams

        tokens = self.tokenize(sentence)

        self.cache.ngrams = self.ngram_generator.generate(tokens)

        return self.cache.ngrams

    # -----------------------------------------------------

    def get_char_position(self, token_index, token_count):

        start = self.cache.token_positions[token_index][0]

        end = self.cache.token_positions[
            token_index + token_count - 1
        ][1]

        return start, end

    # -----------------------------------------------------

    def clear_cache(self):

        self.cache.clear()