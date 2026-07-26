"""
Clause Rebuilder

Repairs raw clauses produced by ClauseSegmenter.

Responsibilities
----------------
1. Remove leading/trailing connectors.
2. Remove trailing commas and punctuation.
3. Restore modifiers that appear before the first action.
4. Normalize whitespace.
5. Capitalize first character.
"""

import re
from copy import deepcopy


class ClauseRebuilder:

    def __init__(self):

        self.leading_connectors = {
            "and",
            "while",
            "with",
            "then",
            "also",
            "including",
            "including the",
            "using",
            "via",
            "through",
        }

        self.trailing_connectors = {
            "and",
            "while",
            "with",
            "then",
        }

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def rebuild(
        self,
        sentence,
        clauses,
        modifiers=None,
    ):
        """
        Rebuild raw clauses.

        Parameters
        ----------
        sentence : str

        clauses : List[Clause]

        modifiers : List[ModifierKnowledge]

        Returns
        -------
        List[Clause]
        """

        rebuilt = []

        for i, clause in enumerate(clauses):

            new_clause = deepcopy(clause)

            text = new_clause.text

            # --------------------------------------------
            # Remove commas
            # --------------------------------------------

            text = text.strip()

            text = re.sub(r"[,\s]+$", "", text)

            # --------------------------------------------
            # Remove leading connectors
            # --------------------------------------------

            text = self._remove_leading_connector(text)

            # --------------------------------------------
            # Remove trailing connectors
            # --------------------------------------------

            text = self._remove_trailing_connector(text)

            # --------------------------------------------
            # Normalize whitespace
            # --------------------------------------------

            text = re.sub(r"\s+", " ", text).strip()

            # --------------------------------------------
            # Recover leading modifiers
            # Only first clause
            # --------------------------------------------

            if i == 0:

                text = self._prepend_modifiers(
                    sentence,
                    text,
                    modifiers,
                )

            # --------------------------------------------
            # Capitalize
            # --------------------------------------------

            if text:

                text = text[0].upper() + text[1:]

            new_clause.text = text

            rebuilt.append(new_clause)

        return rebuilt

    # ---------------------------------------------------------

    def _remove_leading_connector(self, text):

        words = text.split()

        while words:

            first = words[0].lower()

            if first in self.leading_connectors:

                words.pop(0)

            else:

                break

        return " ".join(words)

    # ---------------------------------------------------------

    def _remove_trailing_connector(self, text):

        words = text.split()

        while words:

            last = words[-1].lower()

            if last in self.trailing_connectors:

                words.pop()

            else:

                break

        return " ".join(words)

    # ---------------------------------------------------------

    def _prepend_modifiers(
        self,
        sentence,
        clause,
        modifiers,
    ):
        """
        Recover modifiers before first action.

        Example

        Successfully implemented...

        ↓

        Successfully implemented...
        """

        if not modifiers:

            return clause

        sentence_lower = sentence.lower()

        clause_lower = clause.lower()

        clause_pos = sentence_lower.find(clause_lower)

        if clause_pos <= 0:

            return clause

        prefix = sentence[:clause_pos].strip()

        if not prefix:

            return clause

        prefix = prefix.rstrip(", ")

        if prefix:

            return f"{prefix} {clause}"

        return clause