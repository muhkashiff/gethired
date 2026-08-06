"""
Enterprise Tokenizer Rules
Enterprise V5
"""

import re

# ---------------------------------------------------------
# Enterprise token pattern
# ---------------------------------------------------------

TOKEN_PATTERN = re.compile(
    r"""
    [A-Za-z][A-Za-z0-9]*(?:[-/][A-Za-z0-9+]+)*\+?
    |
    [0-9]+(?:\.[0-9]+)?%?
    |
    \+\+
    """,
    re.VERBOSE,
)
# ---------------------------------------------------------
# Cleanup Rules
# ---------------------------------------------------------

MULTI_SPACE = re.compile(r"\s+")

PUNCTUATION = re.compile(r"[^\w\s:/.+%-]")