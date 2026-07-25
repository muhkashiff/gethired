"""
GetHired
Technology Knowledge Loader
"""

import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "technologies.json"
)


class TechnologyKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

    def lookup_all(self, text):

        text = text.lower()

        matches = []

        seen = set()

        for record in self.data:

            for keyword in record["keywords"]:

                keyword = keyword.lower()

                if keyword in text:

                    if record["canonical_name"] not in seen:

                        seen.add(record["canonical_name"])

                        matches.append(record)

        return matches