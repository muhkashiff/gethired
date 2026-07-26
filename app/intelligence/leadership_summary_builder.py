"""
Leadership Summary Builder

Converts leadership dimensions into
an executive summary.
"""

import json
from pathlib import Path

from app.intelligence.eng_models.leadership_summary import LeadershipSummary


class LeadershipSummaryBuilder:

    def __init__(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "intelligence"
            / "eng_knowledge"
            / "data"
            / "leadership_strength_thresholds.json"
        )

        with open(path, "r", encoding="utf8") as f:
            self.thresholds = json.load(f)

    # -----------------------------------------

    def build(self, profile):

        summary = LeadershipSummary()

        scores = profile["scores"]

        evidence = profile["evidence"]

        summary.dimension_scores = scores

        summary.evidence = evidence

        # -----------------------------
        # Normalize score
        # -----------------------------

        max_possible = 100

        overall = sum(scores.values()) / max(len(scores), 1)

        overall = min(overall, max_possible)

        summary.overall_score = round(overall, 1)

        # -----------------------------
        # Rank dimensions
        # -----------------------------

        ordered = sorted(

            scores.items(),

            key=lambda x: x[1],

            reverse=True

        )

        summary.strongest_dimensions = [

            x[0] for x in ordered[:3]

        ]

        summary.weakest_dimensions = [

            x[0] for x in ordered[-3:]

        ]

        # -----------------------------
        # Executive Readiness
        # -----------------------------

        if overall >= self.thresholds["excellent"]:

            summary.executive_level = "Executive"

            summary.readiness = "Ready"

        elif overall >= self.thresholds["strong"]:

            summary.executive_level = "Senior Leader"

            summary.readiness = "High"

        elif overall >= self.thresholds["good"]:

            summary.executive_level = "Manager"

            summary.readiness = "Moderate"

        else:

            summary.executive_level = "Professional"

            summary.readiness = "Developing"

        # -----------------------------
        # Confidence
        # -----------------------------

        conf = profile["confidence"]

        if conf:

            summary.confidence = round(

                sum(conf.values()) / len(conf),

                2

            )

        # -----------------------------
        # Narrative
        # -----------------------------

        summary.summary = (

            f"Demonstrates strongest capability in "

            f"{', '.join(summary.strongest_dimensions)} "

            f"with an overall leadership score of "

            f"{summary.overall_score:.1f}. "

            f"Current executive readiness is "

            f"{summary.readiness}."

        )

        return summary