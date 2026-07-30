"""
Semantic Validator

Removes impossible semantic interpretations.

This module is executed AFTER extraction
and BEFORE graph creation.
"""


class SemanticValidator:

    def validate(self, interpretation):

        # ------------------------------------------
        # Certification numbers
        # ------------------------------------------

        if interpretation.metric.found:

            if interpretation.metric.entity_id.startswith("STD_"):

                interpretation.metric.found = False

        if interpretation.measurement.found:

            if interpretation.measurement.entity_id.startswith("STD_"):

                interpretation.measurement.found = False

        # ------------------------------------------
        # FSSC 22000
        # ISO 9001
        # ISO 45001
        # etc.
        # ------------------------------------------

        if interpretation.measurement.found:

            if interpretation.action.category == "implementation":

                if interpretation.measurement.numeric_value > 1000:

                    interpretation.measurement.found = False

        return interpretation