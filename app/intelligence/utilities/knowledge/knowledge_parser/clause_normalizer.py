"""
Clause Normalizer

Normalizes rebuilt clauses into a consistent
resume-style format.

Responsibilities
----------------
1. Convert leading gerunds to resume past tense.
2. Normalize capitalization.
3. Remove duplicate whitespace.
4. Ensure clean punctuation.

It DOES NOT perform parsing or extraction.
"""

import re
from copy import deepcopy


class ClauseNormalizer:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def normalize(
        self,
        clauses,
        actions=None,
    ):
        """
        Normalize rebuilt clauses.

        Parameters
        ----------
        clauses : List[Clause]

        actions : List[ActionKnowledge]

        Returns
        -------
        List[Clause]
        """

        normalized = []

        actions = actions or []

        for i, clause in enumerate(clauses):

            new_clause = deepcopy(clause)

            text = new_clause.text

            # ---------------------------------------------
            # Replace leading gerund
            # ---------------------------------------------

            # ---------------------------------------------
            # Replace first detected gerund after modifiers
            # ---------------------------------------------

            for action in actions:

                if not action.found:
                    continue

                pattern = rf"\b{re.escape(action.gerund)}\b"

                if re.search(pattern, text, flags=re.IGNORECASE):

                    text = re.sub(
                        pattern,
                        action.original,
                        text,
                        count=1,
                        flags=re.IGNORECASE,
                    )

                    break

            # ---------------------------------------------
            # Normalize whitespace
            # ---------------------------------------------

            text = re.sub(r"\s+", " ", text).strip()

            # ---------------------------------------------
            # Capitalize
            # ---------------------------------------------

            if text:

                text = text[0].upper() + text[1:]

            # ---------------------------------------------
            # Clean punctuation
            # ---------------------------------------------

            text = re.sub(r"\s+\.", ".", text)

            text = re.sub(r"\s+,", ",", text)

            new_clause.text = text

            normalized.append(new_clause)

        return normalized