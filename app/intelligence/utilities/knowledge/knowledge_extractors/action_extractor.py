"""
Action Extractor

Identifies actions from a sentence.
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

    def extract(self, sentence):

        sentence = sentence.lower()

        words = re.findall(r"\b[\w-]+\b", sentence)

        for word in words:

            if word in self.actions:

                data = self.actions[word]

                return ActionKnowledge(

                    found=True,

                    original=word,

                    base=data["base"],

                    gerund=data["gerund"],

                    category=data["category"],

                    confidence=0.95

                )

        return ActionKnowledge()