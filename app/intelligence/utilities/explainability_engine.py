"""
Shared Explainability Engine
"""

from .explanation_templates import ExplanationTemplates
from .explanation_builder import ExplanationBuilder


class ExplainabilityEngine:

    def __init__(self):

        self.templates = ExplanationTemplates()

        self.builder = ExplanationBuilder()

    def explain_career(

        self,

        career_profile

    ):

        # ----------------------------------

        if career_profile.leadership_index >= 85:

            leadership = self.templates.get(

                "leadership",

                "high"

            )

        elif career_profile.leadership_index >= 70:

            leadership = self.templates.get(

                "leadership",

                "medium"

            )

        else:

            leadership = self.templates.get(

                "leadership",

                "low"

            )

        # ----------------------------------

        if career_profile.career_health_index >= 85:

            health = self.templates.get(

                "career_health",

                "high"

            )

        elif career_profile.career_health_index >= 70:

            health = self.templates.get(

                "career_health",

                "medium"

            )

        else:

            health = self.templates.get(

                "career_health",

                "low"

            )

        # ----------------------------------

        if career_profile.market_readiness_index >= 85:

            market = self.templates.get(

                "market",

                "high"

            )

        elif career_profile.market_readiness_index >= 70:

            market = self.templates.get(

                "market",

                "medium"

            )

        else:

            market = self.templates.get(

                "market",

                "low"

            )

        summary = (

            leadership

            + " "

            + health

            + " "

            + market

        )

        return self.builder.build(

            title="Career Intelligence Summary",

            summary=summary,

            strengths=career_profile.strengths,

            weaknesses=career_profile.development_areas,

            recommendations=[

                "Strengthen promotion readiness.",

                "Continue building leadership experience.",

                "Maintain long-term career stability."

            ],

            evidence=career_profile.evidence,

            confidence=career_profile.confidence

        )