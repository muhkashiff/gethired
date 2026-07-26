"""
Explanation Builder
"""

from .explanation_models import Explanation


class ExplanationBuilder:

    def build(

        self,

        title,

        summary,

        strengths,

        weaknesses,

        recommendations,

        evidence,

        confidence

    ):

        exp = Explanation()

        exp.title = title

        exp.summary = summary

        exp.strengths = strengths

        exp.weaknesses = weaknesses

        exp.recommendations = recommendations

        exp.evidence = evidence

        exp.confidence = confidence

        return exp