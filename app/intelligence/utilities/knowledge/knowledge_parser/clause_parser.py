"""
Clause Parser

Splits complex resume sentences into
independent semantic clauses.
"""

import re

from app.intelligence.utilities.knowledge.knowledge_models.clause_models import Clause
from app.intelligence.utilities.knowledge.repository.repository import Repository


class ClauseParser:

    def __init__(self):

        self.repository = Repository()
        self.rules = self.repository.get_clause_patterns()

        # -------------------------------
        # Schema Compatibility Layer
        # -------------------------------

        self.split_tokens = (
            self.rules.get("split_tokens")
            or self.rules.get("split_words")
            or []
        )

        self.protected_phrases = (
            self.rules.get("protected_phrases")
            or self.rules.get("preserve_phrases")
            or []
        )

        self.protected_phrases.extend(
            self.rules.get("compound_entities", [])
        )

        self.protected_phrases.extend(
            self.rules.get("keep_together", [])
        )

        # remove duplicates while preserving order
        self.protected_phrases = list(
            dict.fromkeys(self.protected_phrases)
        )

        # compile split regex once
        if self.split_tokens:

            escaped = [
                rf"\b{re.escape(token)}\b"
                for token in self.split_tokens
            ]

            self.split_regex = re.compile(
                "|".join(escaped),
                flags=re.IGNORECASE
            )

        else:

            self.split_regex = None

    # -------------------------------------------------------

    def parse(self, sentence):

        sentence = sentence.strip()

        clauses = self._split(sentence)

        return [

            Clause(

                text=clause,

                index=i + 1,

                parent_sentence=sentence,

                confidence=1.0,

                is_independent=True,

                clause_type="semantic",

                source="rule"

            )

            for i, clause in enumerate(clauses)

        ]

    # -------------------------------------------------------

    def _split(self, sentence):

        text = sentence

        protected = {}

        # -----------------------------------------
        # Protect multi-word phrases
        # -----------------------------------------

        for i, phrase in enumerate(self.protected_phrases):

            token = f"__PHRASE_{i}__"

            protected[token] = phrase

            pattern = re.escape(phrase)

            text = re.sub(

                pattern,

                token,

                text,

                flags=re.IGNORECASE

            )

        # -----------------------------------------
        # Split
        # -----------------------------------------

        if self.split_regex:

            pieces = self.split_regex.split(text)

        else:

            pieces = [text]

        # -----------------------------------------
        # Restore protected phrases
        # -----------------------------------------

        clauses = []

        for piece in pieces:

            piece = piece.strip()

            if not piece:
                continue

            for token, phrase in protected.items():

                piece = piece.replace(token, phrase)

            clauses.append(piece)

        return clauses