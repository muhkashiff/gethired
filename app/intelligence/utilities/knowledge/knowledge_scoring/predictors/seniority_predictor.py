"""
Enterprise Seniority Predictor

Enterprise V12
"""

from .prediction_models import SeniorityPrediction


class SeniorityPredictor:

    def predict(

        self,

        leadership_score,

        executive_score,

        business_score,

    ) -> SeniorityPrediction:

        score = (

            leadership_score.normalized_score * 0.45 +

            executive_score.normalized_score * 0.35 +

            business_score.normalized_score * 0.20

        )

        if score >= 85:
            level = "Executive"

        elif score >= 70:
            level = "Director"

        elif score >= 55:
            level = "Manager"

        elif score >= 40:
            level = "Senior Professional"

        elif score >= 25:
            level = "Professional"

        else:
            level = "Entry"

        return SeniorityPrediction(

            level=level,

            score=round(score, 2),

            confidence=1.0,

            reasoning=[

                f"Leadership Score: {leadership_score.normalized_score:.1f}",

                f"Executive Score: {executive_score.normalized_score:.1f}",

                f"Business Value: {business_score.normalized_score:.1f}",

            ]

        )