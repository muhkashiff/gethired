"""
GetHired

Leadership Dimension Scorer

Distributes leadership weight across
all detected leadership dimensions.
"""

from collections import defaultdict


class LeadershipDimensionScorer:

    def score(self, patterns):

        dimensions = defaultdict(float)

        evidence = defaultdict(list)

        confidence = defaultdict(list)

        for pattern in patterns:

            if not pattern.dimensions:
                continue

            # ------------------------------
            # Split weight evenly
            # ------------------------------

            portion = pattern.weight / len(pattern.dimensions)

            for dim in pattern.dimensions:

                dimensions[dim] += portion

                evidence[dim].append(pattern.text)

                confidence[dim].append(pattern.confidence)

        return {

            "scores": dict(dimensions),

            "evidence": dict(evidence),

            "confidence": {

                d: round(

                    sum(c) / len(c),

                    2

                )

                for d, c in confidence.items()

            }

        }