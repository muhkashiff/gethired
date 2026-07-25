"""
GetHired
Seniority Knowledge Loader
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent /
    "data" /
    "seniority.json"
)


class SeniorityKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:

            self.data = json.load(f)

    def lookup(self, text):

        text = text.lower()

        best = None

        longest = 0

        for record in self.data:

            for keyword in record["keywords"]:

                if keyword in text:

                    if len(keyword) > longest:

                        longest = len(keyword)

                        best = record

        return best