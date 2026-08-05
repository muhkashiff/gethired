from .weighted_score_engine import WeightedScoreEngine

from ..weights import ATS_WEIGHTS


class ATSScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="ATS",

            weights=ATS_WEIGHTS,

        )