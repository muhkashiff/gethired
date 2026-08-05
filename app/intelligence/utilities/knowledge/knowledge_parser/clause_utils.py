"""
Clause Utilities

Enterprise V12

Responsible for splitting raw text into
semantic business clauses.

Example

Input

Implemented FSSC22000 requirements and increased yield to 99%
using Root Cause Analysis.

Output

[
    "Implemented FSSC22000 requirements",
    "increased yield to 99% using Root Cause Analysis"
]
"""

from __future__ import annotations

import re


class ClauseUtils:

    def __init__(self):

        self.coordinators = {

            "and",
            "then",
            "while",
            "plus",

        }

    # ==========================================================
    # Normalize
    # ==========================================================

    def normalize(self, text: str) -> str:

        if not text:

            return ""

        text = text.replace("\n", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ==========================================================
    # Split Clauses
    # ==========================================================

    def split(self, text: str) -> list[str]:

        text = self.normalize(text)

        if not text:

            return []

        clauses = []

        current = []

        words = text.split()

        for word in words:

            lower = word.lower()

            if lower in self.coordinators:

                if current:

                    clauses.append(" ".join(current))

                    current = []

                continue

            current.append(word)

        if current:

            clauses.append(" ".join(current))

        return clauses

    # ==========================================================
    # Convenience
    # ==========================================================

    def first_clause(self, text: str):

        clauses = self.split(text)

        if clauses:

            return clauses[0]

        return ""

    def clause_count(self, text: str):

        return len(self.split(text))