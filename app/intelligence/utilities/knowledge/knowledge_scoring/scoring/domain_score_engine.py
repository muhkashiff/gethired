from .weighted_score_engine import WeightedScoreEngine

from ..weights import DOMAIN_WEIGHTS


class DomainScoreEngine(WeightedScoreEngine):

    def __init__(self):

        super().__init__(

            category="Domain",

            weights=DOMAIN_WEIGHTS,

        )