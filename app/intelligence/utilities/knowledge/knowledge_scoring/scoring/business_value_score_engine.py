from .weighted_score_engine import WeightedScoreEngine

from ..weights import BUSINESS_VALUE_WEIGHTS


class BusinessValueScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="Business Value",

            weights=BUSINESS_VALUE_WEIGHTS,

        )