"""
Clause Segmenter

Splits a sentence into raw semantic clauses using
detected action positions.

Responsibilities
----------------
1. Receive a sentence.
2. Receive ActionKnowledge list.
3. Split sentence at each action.
4. Return raw clause strings.

NOTE:
Cleaning and repairing clauses is handled by
ClauseRebuilder.
"""

from typing import List

from app.intelligence.utilities.knowledge.knowledge_models.clause_models import (
    Clause,
)


class ClauseSegmenter:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Public
    # ---------------------------------------------------------

    def segment(
        self,
        sentence: str,
        actions: List,
    ) -> List[Clause]:
        """
        Split sentence into raw clauses.

        Parameters
        ----------
        sentence : str

        actions : List[ActionKnowledge]

        Returns
        -------
        List[Clause]
        """

        if not sentence.strip():

            return []

        # -----------------------------------------------------
        # No actions
        # -----------------------------------------------------

        if not actions:

            return [

                Clause(

                    text=sentence.strip(),

                    index=1,

                    parent_sentence=sentence,

                    confidence=0.95,

                    is_independent=True,

                    connector="",

                )

            ]

        # -----------------------------------------------------
        # Sort actions
        # -----------------------------------------------------

        actions = sorted(

            actions,

            key=lambda x: x.start_char,

        )

        clauses = []

        # -----------------------------------------------------
        # Build clauses
        # -----------------------------------------------------

        for i, action in enumerate(actions):

            start = action.start_char

            if i == len(actions) - 1:

                end = len(sentence)

            else:

                end = actions[i + 1].start_char

            text = sentence[start:end].strip()

            if not text:

                continue

            clauses.append(

                Clause(

                    text=text,

                    index=len(clauses) + 1,

                    parent_sentence=sentence,

                    confidence=action.confidence,

                    is_independent=True,

                    connector="",

                )

            )

        return clauses