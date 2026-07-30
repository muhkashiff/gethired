"""
Semantic Connector Detector

Detects semantic connectors between entities.

Example

Implemented ISO 9001 using Lean Manufacturing.

Connector:
using

Relation:
achieved_using
"""

import re


class SemanticConnectorDetector:

    def __init__(self):

        self.rules = {

            "using": "achieved_using",

            "through": "achieved_through",

            "via": "achieved_using",

            "by": "performed_by",

            "with": "performed_with",

            "to": "resulting_in",

            "for": "supports",

            "into": "transformed_into",

            "from": "derived_from",

            "across": "applies_to",

            "within": "belongs_to",

            "under": "governed_by",

        }

    # ----------------------------------------------------------

    def detect(self, sentence):

        sentence = sentence.lower()

        found = []

        for connector, relation in self.rules.items():

            pattern = r"\b" + re.escape(connector) + r"\b"

            if re.search(pattern, sentence):

                found.append(

                    {

                        "connector": connector,

                        "relation": relation,

                    }

                )

        return found