"""
Enterprise Tokenization Rules
"""

import re

TOKEN_PATTERN = re.compile(
    r"[A-Za-z0-9]+(?:[:./&+_-][A-Za-z0-9]+)*",
    re.UNICODE,
)

MULTI_SPACE = re.compile(

    r"\s+"

)

PUNCTUATION = re.compile(

    r"[^\w\s:+./&%-]"

)