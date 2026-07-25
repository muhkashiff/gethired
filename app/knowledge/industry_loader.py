"""
GetHired
Industry Knowledge Loader
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "industries.json"
)


class IndustryKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

    # ==========================================================
    # Detect Industry
    # ==========================================================

    def detect(self, text):

        text = text.lower()

        scores = {}

        for record in self.data:

            score = 0

            for keyword in record["keywords"]:

                if keyword.lower() in text:

                    score += len(keyword)

            if score:

                scores[record["industry"]] = score

        if not scores:
            return "Other"

        return max(scores, key=scores.get)