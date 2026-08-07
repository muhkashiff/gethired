"""
Enterprise NGram Generator
Enterprise V5
"""

from .ngram import NGram


class NGramGenerator:

    def __init__(self, max_ngram=5):

        self.max_ngram = max_ngram

    ############################################################

    def generate(self, tokens):

        results = []

        length = len(tokens)

        for size in range(self.max_ngram, 0, -1):

            for i in range(length - size + 1):

                phrase = " ".join(tokens[i:i + size])

                results.append(

                    NGram(

                        phrase=phrase,

                        normalized="",

                        token_index=i,

                        token_count=size,

                        start_char=0,

                        end_char=0,

                    )

                )

        return results