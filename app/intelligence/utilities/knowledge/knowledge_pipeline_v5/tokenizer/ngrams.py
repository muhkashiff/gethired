"""
Enterprise NGram Generator
Enterprise V5
"""


class NGramGenerator:

    def __init__(self, max_ngram=5):

        self.max_ngram = max_ngram

    def generate(self, tokens):

        results = []

        length = len(tokens)

        for size in range(self.max_ngram, 0, -1):

            for i in range(length - size + 1):

                phrase = " ".join(tokens[i:i+size])

                results.append(
                    (
                        phrase,
                        i,
                        size,
                    )
                )

        return results