"""
Action Segmenter

Splits one clause into multiple action-centric clauses.

Example

Implemented ISO 9001, trained staff and improved productivity.

↓

Implemented ISO 9001

Trained staff

Improved productivity
"""

from copy import deepcopy

from app.intelligence.utilities.knowledge.knowledge_models.clause_models import (
    Clause,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import (
    ActionExtractor,
)


class ActionSegmenter:

    def __init__(self):

        self.action_extractor = ActionExtractor()

    # ---------------------------------------------------------

    def segment(
        self,
        clause: Clause,
    ):
        """
        Split one clause into one clause per action.

        Returns
        -------
        list[Clause]
        """

        actions = self.action_extractor.extract_all(
            clause.text
        )

        # -------------------------------------------------
        # Only one action
        # -------------------------------------------------

        if len(actions) <= 1:

            clause.action = actions[0] if actions else clause.action

            return [clause]

        # -------------------------------------------------
        # Multiple actions
        # -------------------------------------------------

        results = []

        text = clause.text

        actions = sorted(
            actions,
            key=lambda x: x.start_char,
        )

        for i, action in enumerate(actions):

            start = action.start_char

            if i < len(actions) - 1:

                end = actions[i + 1].start_char

            else:

                end = len(text)

            piece = text[start:end].strip()

            # ---------------------------------------------
            # Remove trailing connectors
            # ---------------------------------------------

            piece = piece.rstrip(",")

            words = piece.split()

            while words:

                if words[-1].lower() in {

                    "and",
                    "while",
                    "with",
                    "then",

                }:

                    words.pop()

                else:

                    break

            piece = " ".join(words).strip()

            new_clause = deepcopy(clause)

            new_clause.text = piece

            new_clause.normalized_text = piece

            new_clause.action = action

            results.append(new_clause)

        return results