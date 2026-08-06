"""
Enterprise Tokenization Cache
Enterprise V5
"""

from dataclasses import dataclass, field


@dataclass
class TokenizationCache:

    sentence: str = ""

    tokens: list = field(default_factory=list)

    matches: list = field(default_factory=list)

    token_positions: dict = field(default_factory=dict)

    normalized: dict = field(default_factory=dict)

    ngrams: list = field(default_factory=list)

    def clear(self):

        self.sentence = ""

        self.tokens.clear()

        self.matches.clear()

        self.token_positions.clear()

        self.normalized.clear()

        self.ngrams.clear()