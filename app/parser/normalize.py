"""
GetHired

Text Normalizer
"""


import re


def normalize_heading(text):

    if not text:
        return ""

    text = text.upper().strip()

    # Remove common trailing punctuation
    text = re.sub(r"[:\-|]+$", "", text)

    # Remove decorative characters
    text = re.sub(r"[*_=.#•]+", "", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()