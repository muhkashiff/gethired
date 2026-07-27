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

        # longest phrases first
        self.sorted_objects = sorted(
            self.objects.keys(),
            key=len,
            reverse=True,
        )

    # -----------------------------------------------------

    def extract(self, sentence):

        sentence_lower = sentence.lower()

        for phrase in self.sorted_objects:

            if phrase in sentence_lower:

                data = self.objects[phrase]

                return ObjectKnowledge(

                    found=True,

                    original=phrase,

                    canonical=data["canonical"],

                    category=data["category"],

                    confidence=0.95

                )

        return ObjectKnowledge()