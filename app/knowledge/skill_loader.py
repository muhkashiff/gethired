"""
GetHired
Skill Knowledge Loader

Loads the skills knowledge base from JSON
and performs intelligent keyword lookup.
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "skills.json"
)


class SkillKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

        # --------------------------------------------------
        # Sort records once
        # Longest keywords first
        # Prevents "food safety" matching before
        # "food safety management"
        # --------------------------------------------------

        self.data = sorted(

            self.data,

            key=lambda record: max(

                len(keyword)

                for keyword in record.get("keywords", [])

            ),

            reverse=True

        )

    # ==========================================================
    # Lookup ALL Matching Skills
    # ==========================================================

    def lookup_all(self, text):
        """
        Returns ALL matching skills found in a line.

        Example

        Input:
            "QMS Implementation & Food Safety Governance"

        Returns

            [
                QMS Implementation,
                Food Safety Governance
            ]

        Duplicate matches are automatically removed.
        """

        text = text.lower().strip()

        matches = []

        seen = set()

        for record in self.data:

            keywords = record.get("keywords", [])

            for keyword in keywords:

                keyword = keyword.lower().strip()

                if keyword in text:

                    canonical = record.get(
                        "canonical_name",
                        ""
                    )

                    if canonical.lower() not in seen:

                        matches.append(record)

                        seen.add(
                            canonical.lower()
                        )

                    # Don't check remaining aliases
                    break

        return matches

    # ==========================================================
    # Backward Compatibility
    # ==========================================================

    def lookup(self, text):
        """
        Returns only the first match.

        Older code can continue using lookup()
        while new parser uses lookup_all().
        """

        matches = self.lookup_all(text)

        if matches:
            return matches[0]

        return {

            "canonical_name": "",

            "category": "Other",

            "level": "",

            "aliases": []

        }