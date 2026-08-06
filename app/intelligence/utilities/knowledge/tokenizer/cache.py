"""
Enterprise Tokenization Cache
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class TokenizationCache:

    sentence: str = ""

    tokens: List[str] = field(default_factory=list)

    matches: list = field(default_factory=list)

    ngrams: List[Tuple[str, int, int]] = field(default_factory=list)

    normalized: Dict[str, str] = field(default_factory=dict)

    token_positions: Dict[int, Tuple[int, int]] = field(default_factory=dict)

    def clear(self):

        self.sentence = ""

        self.tokens.clear()

        self.matches.clear()

        self.ngrams.clear()

        self.normalized.clear()

        self.token_positions.clear()