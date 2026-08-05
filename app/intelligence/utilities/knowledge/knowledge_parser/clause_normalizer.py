"""
Enterprise Clause Normalizer

Enterprise V12

Responsibilities
----------------
1. Normalize whitespace
2. Normalize punctuation
3. Normalize capitalization
4. Remove duplicate clauses

Input
-----
list[str]

Output
------
list[str]
"""

from __future__ import annotations

import re


class ClauseNormalizer:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):
        pass

    ####################################################################
    # PUBLIC
    ####################################################################

    def normalize(
        self,
        clauses: list[str],
    ) -> list[str]:

        normalized = []

        seen = set()

        for clause in clauses:

            text = self._normalize_text(clause)

            if not text:
                continue

            key = text.lower()

            if key in seen:
                continue

            seen.add(key)

            normalized.append(text)

        return normalized

    ####################################################################
    # PRIVATE
    ####################################################################

    def _normalize_text(
        self,
        text: str,
    ) -> str:

        if not text:
            return ""

        # ---------------------------------------------
        # Whitespace
        # ---------------------------------------------

        text = re.sub(r"\s+", " ", text).strip()

        # ---------------------------------------------
        # Remove spaces before punctuation
        # ---------------------------------------------

        text = re.sub(r"\s+([.,;:])", r"\1", text)

        # ---------------------------------------------
        # Remove repeated punctuation
        # ---------------------------------------------

        text = re.sub(r"[.]{2,}", ".", text)
        text = re.sub(r"[,]{2,}", ",", text)

        # ---------------------------------------------
        # Capitalize first letter
        # ---------------------------------------------

        if text:

            text = text[0].upper() + text[1:]

        return text