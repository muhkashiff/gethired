"""
Promotion Intelligence Engine
"""

from .promotion_detector import PromotionDetector
from .promotion_rules import PromotionRules
from .promotion_scorer import PromotionScorer
from .promotion_profile_builder import PromotionProfileBuilder


class PromotionEngine:

    def __init__(self):

        self.detector = PromotionDetector()

        self.rules = PromotionRules()

        self.scorer = PromotionScorer(self.rules)

        self.builder = PromotionProfileBuilder()

    # -----------------------------------

    def evaluate(self, experiences):

        return self.builder.build(

            self.detector,

            self.scorer,

            experiences

        )