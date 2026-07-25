"""
GetHired

Job Title Loader
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "job_titles.json"
)


class JobTitleKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:
            self.data = json.load(f)

    # --------------------------------------------------
    # Find Job Title
    # --------------------------------------------------

    def lookup(self, text):

        text = text.lower()

        best = None
        longest = 0

        for title in self.data:

            for alias in title["aliases"]:

                alias = alias.lower()

                if alias in text:

                    if len(alias) > longest:

                        longest = len(alias)
                        best = title

        return best