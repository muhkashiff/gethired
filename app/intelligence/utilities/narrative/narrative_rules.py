"""
Narrative Rules

Defines writing behaviour for
the Narrative Engine.
"""


class NarrativeRules:

    def __init__(self):

        # ---------------------------------------
        # Writing Style
        # ---------------------------------------

        self.tone = "Professional"

        self.voice = "Third Person"

        self.writing_style = "Executive"

        self.language = "English"

        # ---------------------------------------
        # Confidence Thresholds
        # ---------------------------------------

        self.high_confidence = 0.90

        self.medium_confidence = 0.75

        self.low_confidence = 0.60

        # ---------------------------------------
        # Recommendation Priorities
        # ---------------------------------------

        self.priority_levels = [

            "Critical",

            "High",

            "Medium",

            "Low"

        ]

        # ---------------------------------------
        # Paragraph Order
        # ---------------------------------------

        self.section_order = [

            "Executive Summary",

            "Leadership",

            "Career Progression",

            "Career Stability",

            "Executive Potential",

            "Market Readiness",

            "Recommendations"

        ]

        # ---------------------------------------
        # Maximum Paragraph Sizes
        # ---------------------------------------

        self.max_summary_sentences = 3

        self.max_paragraph_sentences = 5

        self.max_recommendations = 5

        # ---------------------------------------
        # Evidence Limits
        # ---------------------------------------

        self.max_evidence_items = 8

        # ---------------------------------------
        # Report Formatting
        # ---------------------------------------

        self.use_bullets = True

        self.show_confidence = True

        self.show_evidence = True

        self.show_recommendations = True