"""
Semantic Connector Detector

Some connectors indicate continuation of
the same achievement.

Examples

by
through
using
via
with
while
after
before

These should remain attached to
the previous clause.
"""


class SemanticConnectorDetector:

    def __init__(self):

        self.connectors = {

            "by",
            "through",
            "using",
            "via",
            "with",
            "while",
            "after",
            "before",
            "without",
            "including",
            "leveraging"

        }

    # --------------------------------------------------

    def is_connector(self, text):

        text = text.lower().strip()

        for connector in self.connectors:

            if text.startswith(connector + " "):

                return True

        return False