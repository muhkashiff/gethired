"""
Purpose Clause Detector

Detects infinitive purpose clauses that should NOT
be split into separate achievements.

Example

Led a team to improve quality.

Should remain ONE clause.

NOT

Led a team

Improve quality
"""


class PurposeClauseDetector:

    def __init__(self):

        self.purpose_phrases = {

            "to improve",
            "to increase",
            "to reduce",
            "to achieve",
            "to maintain",
            "to support",
            "to implement",
            "to ensure",
            "to establish",
            "to deliver",
            "to optimize",
            "to strengthen",
            "to enhance",
            "to maximize",
            "to minimise",
            "to minimize",
            "to eliminate",
            "to simplify",
            "to accelerate",
            "to drive",
            "to enable",
            "to create",
            "to build",
            "to develop",
            "to provide",
            "to standardize",
            "to streamline",
            "to automate"

        }

    # -----------------------------------------------------

    def is_purpose_clause(self, text: str):

        text = text.lower().strip()

        for phrase in self.purpose_phrases:

            if text.startswith(phrase):

                return True

        return False