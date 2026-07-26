"""
Clause Parser

Splits complex resume sentences into
independent semantic clauses.
"""

import json
import re
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_models.clause_models import Clause


class ClauseParser:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "data"
            / "clause_patterns.json"
        )

        with open(path, encoding="utf8") as f:
            self.rules = json.load(f)

    # -------------------------------------------------------

    def parse(self, sentence):

        sentence = sentence.strip()

        clauses = self._split(sentence)

        results = []

        for i, clause in enumerate(clauses):

            results.append(

                Clause(

                    text=clause.strip(),

                    index=i + 1,

                    parent_sentence=sentence,

                    confidence=0.95,

                    is_independent=True

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