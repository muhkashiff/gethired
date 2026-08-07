"""
Enterprise NGram Model
Enterprise V5
"""

from dataclasses import dataclass


@dataclass(slots=True)
class NGram:
    """
    Represents one generated n-gram.
    """

    phrase: str

    normalized: str

    token_index: int

    token_count: int

    start_char: int

    end_char: int