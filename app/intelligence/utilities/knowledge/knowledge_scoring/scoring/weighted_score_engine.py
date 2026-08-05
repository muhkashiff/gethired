from .score_result import ScoreResult
from .score_engine_base import ScoreEngineBase


class WeightedScoreEngine(ScoreEngineBase):

    def __init__(

        self,

        category,

        weights=None,

        maximum_score=100,

    ):

        self.category = category

        self.weights = weights or {}

        self.maximum_score = maximum_score

    # --------------------------------------------------------

    def score(

        self,

        evidence,

    ):

        raw_score = 0.0

        details = {}

        for bucket, value in evidence.scores.items():

            weight = self.weights.get(bucket, 1.0)

            contribution = value * weight

            details[bucket] = contribution

            raw_score += contribution

        normalized = min(

            raw_score,

            self.maximum_score,

        )

        return ScoreResult(

            category=self.category,

            raw_score=raw_score,

            normalized_score=normalized,

            weight=1.0,

            confidence=1.0,

            details=details,

        )