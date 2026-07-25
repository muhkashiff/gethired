"""
GetHired
Certification Knowledge Base

Loads certification knowledge from JSON and
returns the best matching certification.
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "certifications.json"
)


class CertificationKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

    # ==========================================================
    # Lookup
    # ==========================================================

    def lookup(self, text):

        text = text.lower().strip()

        best_match = None
        best_score = -1

        for record in self.data:

            for keyword in record.get("keywords", []):

                keyword = keyword.lower()

                if keyword in text:

                    # longer keyword = better match
                    score = len(keyword)

                    if score > best_score:

                        best_score = score
                        best_match = record

        if best_match:

            return best_match

        return {

            "category": "Other",

            "level": "",

            "canonical_name": "",

            "issuer": ""

        }