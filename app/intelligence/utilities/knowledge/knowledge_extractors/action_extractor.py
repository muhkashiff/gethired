"""
Action Extractor

Identifies one or more actions from a sentence.

extract()
    Returns the first detected action (backward compatible).

extract_all()
    Returns every detected action with positional metadata.
"""

import json
import re
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.action_models import (
    ActionKnowledge,
)


class ActionExtractor:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "data"
            / "actions.json"
        )

        with open(path, encoding="utf8") as f:
            self.actions = json.load(f)

    # ----------------------------------------------------------
    # Backward compatible API
    # ----------------------------------------------------------

    def extract(self, sentence: str) -> ActionKnowledge:
        """
        Returns the first action found.

        Existing parser code can continue calling this
        without any modification.
        """

        actions = self.extract_all(sentence)

        if actions:
            return actions[0]

        return ActionKnowledge()

    # ----------------------------------------------------------
    # New API
    # ----------------------------------------------------------

    def extract_all(self, sentence: str):
        """
        Returns every detected action in the sentence.

        Each ActionKnowledge contains positional information
        that will later be used by the Clause Parser.
        """

        results = []

        sentence_lower = sentence.lower()

        token_index = 0

        pattern = re.compile(r"\b[\w-]+\b")

        for match in pattern.finditer(sentence_lower):

            word = match.group()

            if word not in self.actions:
                token_index += 1
                continue

            data = self.actions[word]

            results.append(

                ActionKnowledge(

                    found=True,

                    original=word,

                    base=data["base"],

                    gerund=data["gerund"],

                    category=data["category"],

                    confidence=0.95,

                    start_char=match.start(),

                    end_char=match.end(),

                    token_index=token_index,

                    sentence_index=0,

                    clause_candidate=True,

                )

            )

            token_index += 1

        return results