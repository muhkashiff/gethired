"""
Clause Rebuilder

Repairs raw clauses produced by the Clause Parser.

Responsibilities
----------------
1. Remove leading connectors.
2. Remove trailing connectors.
3. Remove trailing commas.
4. Normalize whitespace.
5. Capitalize first character.

NOTE
----
The previous version attempted to reconstruct modifiers from the
original sentence.

That responsibility now belongs to the Clause Parser, therefore
the rebuilder only performs cleanup.
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
        clauses,
        modifiers=None,
    ):
        """
        Clean parser output.

        Parameters
        ----------
        clauses : list[Clause]

        modifiers : optional
            Reserved for future use.

        Returns
        -------
        list[Clause]
        """

        rebuilt = []

        for clause in clauses:

            new_clause = deepcopy(clause)

            text = new_clause.text

            # ---------------------------------------
            # Remove surrounding whitespace
            # ---------------------------------------

            text = text.strip()

            # ---------------------------------------
            # Remove trailing commas
            # ---------------------------------------

            text = re.sub(r"[,\s]+$", "", text)

            # ---------------------------------------
            # Remove leading connectors
            # ---------------------------------------

            text = self._remove_leading_connector(text)

            # ---------------------------------------
            # Remove trailing connectors
            # ---------------------------------------

            text = self._remove_trailing_connector(text)

            # ---------------------------------------
            # Normalize spaces
            # ---------------------------------------

            text = re.sub(r"\s+", " ", text).strip()

            # ---------------------------------------
            # Preserve punctuation
            # ---------------------------------------

            if (
                clause.text.endswith(".")
                and not text.endswith(".")
            ):
                text += "."

            # ---------------------------------------
            # Capitalize
            # ---------------------------------------

            if text:

                text = text[0].upper() + text[1:]

            # ---------------------------------------
            # Preserve normalized text
            # ---------------------------------------

            new_clause.text = text

            if hasattr(new_clause, "normalized_text"):

                new_clause.normalized_text = text

            rebuilt.append(new_clause)

        return rebuilt

    # ---------------------------------------------------------

    def _remove_leading_connector(
        self,
        text,
    ):

        words = text.split()

        while words:

            if words[0].lower() in self.leading_connectors:

                words.pop(0)

            else:

                break

        return " ".join(words)

    # ---------------------------------------------------------

    def _remove_trailing_connector(
        self,
        text,
    ):

        words = text.split()

        while words:

            if words[-1].lower() in self.trailing_connectors:

                words.pop()

            else:

                break

        return " ".join(words)

    # ---------------------------------------------------------

    def _prepend_modifiers(
        self,
        clause_text,
        modifiers=None,
    ):
        """
        Reserved for future versions.

        The new parser already keeps modifiers attached
        to the correct clause, so no rebuilding is required.
        """

        return clause_text