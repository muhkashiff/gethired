import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).parent /
    "data" /
    "certifications.json"
)


class CertificationKnowledge:

    def __init__(self):

        with open(DATA_FILE,
                  encoding="utf8") as f:

            self.data = json.load(f)

    def lookup(self, text):

        text = text.lower()

        for record in self.data:

            for keyword in record["keywords"]:

                if keyword in text:

                    return record

        return {
            "category": "Other",
            "level": ""
        }