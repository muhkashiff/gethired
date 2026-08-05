from .weighted_score_engine import WeightedScoreEngine

from ..weights import TECHNICAL_WEIGHTS


class TechnicalScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="Technical",

            weights=TECHNICAL_WEIGHTS,

        )