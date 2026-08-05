from .weighted_score_engine import WeightedScoreEngine

from ..weights import LEADERSHIP_WEIGHTS


class LeadershipScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="Leadership",

            weights=LEADERSHIP_WEIGHTS,

        )