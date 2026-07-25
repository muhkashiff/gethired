"""
GetHired

Company Knowledge Loader
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "companies.json"
)


class CompanyKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

    # --------------------------------------------------
    # Find Company
    # --------------------------------------------------

    def lookup(self, text):

        text = text.lower()

        best = None
        longest = 0

        for company in self.data:

            for alias in company["aliases"]:

                alias = alias.lower()

                if alias in text:

                    if len(alias) > longest:

                        longest = len(alias)
                        best = company

        return best