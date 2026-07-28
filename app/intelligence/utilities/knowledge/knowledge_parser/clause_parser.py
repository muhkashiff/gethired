"""
Clause Parser

Splits complex resume sentences into
independent semantic clauses.
"""

import json
import re
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_models.clause_models import Clause
from app.intelligence.utilities.knowledge.repository.repository import Repository


class ClauseParser:

    def __init__(self):

        self.repository = Repository()

        self.rules = self.repository.get_clause_patterns()
    # -------------------------------------------------------

    def parse(self, sentence):

        sentence = sentence.strip()

        clauses = self._split(sentence)

        results = []

        for i, clause in enumerate(clauses):

            results.append(

                Clause(

                    text=clause,

                    index=i + 1,

                    parent_sentence=sentence,

                    confidence=1.0,

                    is_independent=True,

                    clause_type="semantic",

                    source="rule"

                )

            )

        return results

    # -------------------------------------------------------

    def _split(self, sentence):

        text = sentence

        # protect phrases that should never split
        protected = {}

        for i, phrase in enumerate(self.rules["preserve_phrases"]):

            token = f"__PHRASE{i}__"

            protected[token] = phrase

            text = re.sub(
                phrase,
                token,
                text,
                flags=re.IGNORECASE
            )

        separators = []

        for word in self.rules["split_words"]:

            separators.append(rf"\b{re.escape(word)}\b")

        regex = "|".join(separators)

        pieces = re.split(regex, text)

        final = []

        for piece in pieces:

            piece = piece.strip()

            if not piece:
                continue

            for token, phrase in protected.items():

                piece = piece.replace(token, phrase)

            final.append(piece)

        return final