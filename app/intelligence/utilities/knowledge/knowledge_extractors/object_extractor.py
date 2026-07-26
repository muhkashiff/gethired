"""
Object Extractor

Finds business objects
mentioned in a sentence.
"""

import json
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.object_models import (
    ObjectKnowledge,
)


class ObjectExtractor:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent.parent

            / "knowledge_knowledge"

            / "data"

            / "objects.json"

        )

        with open(path, encoding="utf8") as f:

            self.objects = json.load(f)

    # ---------------------------------------------------------

    def extract(self, sentence):

        sentence_lower = sentence.lower()

        best_match = ""

        category = ""

        # longest match wins

        for obj, cat in self.objects.items():

            if obj.lower() in sentence_lower:

                if len(obj) > len(best_match):

                    best_match = obj

                    category = cat

        if best_match == "":

            return ObjectKnowledge()

        return ObjectKnowledge(

            found=True,

            original=best_match,

            canonical=best_match.lower(),

            category=category,

            confidence=0.95

        )