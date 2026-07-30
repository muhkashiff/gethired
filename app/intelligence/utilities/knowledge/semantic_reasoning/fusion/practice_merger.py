"""
Practice Merger

Groups methodologies together.

Example

Lean

Kaizen

Six Sigma

↓

Continuous Improvement

Example

Fishbone

5 Why

↓

Root Cause Analysis
"""


class PracticeMerger:

    """
    Adds semantic grouping for methodologies.
    """

    def __init__(self):

        self.groups = {

            "continuous_improvement": {

                "Lean Manufacturing",

                "Lean",

                "Kaizen",

                "Six Sigma",

                "DMAIC",

            },

            "problem_solving": {

                "Fishbone Analysis",

                "Fishbone",

                "5 Why",

                "5 Whys",

                "Root Cause Analysis",

            },

        }

    # -----------------------------------------------------

    def merge(self, resolution):

        methodologies = [

            entity

            for entity in resolution.entities

            if entity.entity_type.lower() == "methodology"

        ]

        for method in methodologies:

            for group, members in self.groups.items():

                if method.canonical in members:

                    method.metadata["practice_group"] = group

                    break

        return resolution