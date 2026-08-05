from .weighted_score_engine import WeightedScoreEngine

from ..weights import EXECUTIVE_WEIGHTS


class ExecutiveScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="Executive",

            weights=EXECUTIVE_WEIGHTS,

        )