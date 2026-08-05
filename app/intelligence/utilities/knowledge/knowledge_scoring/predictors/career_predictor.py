"""
Enterprise Career Predictor

Enterprise V12
"""

from .prediction_models import CareerPrediction


class CareerPredictor:

    def predict(

        self,

        domain_score,

        technical_score,

        leadership_score,

        executive_score,

        business_score,

    ) -> CareerPrediction:

        score = (

            domain_score.normalized_score * 0.25 +

            technical_score.normalized_score * 0.20 +

            leadership_score.normalized_score * 0.20 +

            executive_score.normalized_score * 0.15 +

            business_score.normalized_score * 0.20

        )

        if score >= 90:
            level = "Chief Executive"

        elif score >= 80:
            level = "Vice President"

        elif score >= 70:
            level = "Director"

        elif score >= 60:
            level = "Senior Manager"

        elif score >= 45:
            level = "Manager"

        elif score >= 30:
            level = "Professional"

        else:
            level = "Associate"

        return CareerPrediction(

            career_level=level,

            score=round(score, 2),

            confidence=1.0,

            reasoning=[

                f"Domain: {domain_score.normalized_score:.1f}",

                f"Technical: {technical_score.normalized_score:.1f}",

                f"Leadership: {leadership_score.normalized_score:.1f}",

                f"Executive: {executive_score.normalized_score:.1f}",

                f"Business: {business_score.normalized_score:.1f}",

            ]

        )