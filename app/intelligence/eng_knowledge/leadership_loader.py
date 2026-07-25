"""
Leadership Knowledge Loader
"""

import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "leadership_patterns.json"
)


class LeadershipKnowledge:

    def __init__(self):

        with open(DATA_FILE, encoding="utf8") as f:

            self.patterns = json.load(f)

    def get_patterns(self):

        return self.patterns