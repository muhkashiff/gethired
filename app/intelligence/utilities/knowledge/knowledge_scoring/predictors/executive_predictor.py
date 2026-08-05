"""
Enterprise Executive Readiness Predictor

Enterprise V12
"""

from .prediction_models import ExecutivePrediction


class ExecutivePredictor:

    def predict(

        self,

        executive_score,

        leadership_score,

        business_score,

    ) -> ExecutivePrediction:

        score = (

            executive_score.normalized_score * 0.50 +

            leadership_score.normalized_score * 0.30 +

            business_score.normalized_score * 0.20

        )

        ready = score >= 75

        return ExecutivePrediction(

            ready=ready,

            score=round(score, 2),

            confidence=1.0,

            reasoning=[

                f"Executive Score: {executive_score.normalized_score:.1f}",

                f"Leadership Score: {leadership_score.normalized_score:.1f}",

                f"Business Score: {business_score.normalized_score:.1f}",

            ]

        )