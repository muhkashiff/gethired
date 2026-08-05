"""
Enterprise Clause Segmenter

Enterprise V12

Responsibilities
----------------
1. Split text into semantic clauses
2. Normalize clauses
3. Return clean clause list

NO ontology
NO extractors
NO reasoners
NO interpretations
NO sentence parsing

Pipeline

Raw Text
    ↓
Clause Splitter
    ↓
Clause Normalizer
    ↓
list[str]
"""

from __future__ import annotations

import re

from .clause_normalizer import ClauseNormalizer


class ClauseSegmenter:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.normalizer = ClauseNormalizer()

    ####################################################################
    # MAIN
    ####################################################################

    def segment(
        self,
        text: str,
    ) -> list[str]:

        if not text:
            return []

        # ------------------------------------------------------------
        # Standard cleanup
        # ------------------------------------------------------------

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        # ------------------------------------------------------------
        # Initial clause split
        # ------------------------------------------------------------

        clauses = self._split(text)

        # ------------------------------------------------------------
        # Normalize
        # ------------------------------------------------------------

        clauses = self.normalizer.normalize(clauses)

        # ------------------------------------------------------------
        # Remove empty clauses
        # ------------------------------------------------------------

        clauses = [

            clause.strip()

            for clause in clauses

            if clause.strip()

        ]

        return clauses

    ####################################################################
    # SPLITTER
    ####################################################################

    def _split(
        self,
        text: str,
    ) -> list[str]:

        """
        Enterprise clause splitter.

        Splits on

            .
            ;
            :
            and
            but
            while

        while preserving meaningful business phrases.
        """

        if not text:
            return []

        clauses = re.split(

            r"""
            \s*;\s*
            |
            \.\s+
            |
            \s+\band\b\s+
            |
            \s+\bbut\b\s+
            |
            \s+\bwhile\b\s+
            """,

            text,

            flags=re.IGNORECASE | re.VERBOSE,

        )

        return [

            clause.strip()

            for clause in clauses

            if clause.strip()

        ]