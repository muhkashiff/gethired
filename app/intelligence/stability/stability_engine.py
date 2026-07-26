"""
Career Stability Engine
"""

from .stability_detector import StabilityDetector
from .stability_rules import StabilityRules
from .stability_scorer import StabilityScorer
from .stability_profile_builder import StabilityProfileBuilder


class StabilityEngine:

    def __init__(self):

        self.detector = StabilityDetector()

        self.rules = StabilityRules()

        self.scorer = StabilityScorer(self.rules)

        self.builder = StabilityProfileBuilder()

    # -------------------------------------

    def evaluate(self, experiences):

        return self.builder.build(

            self.detector,

            self.scorer,

            experiences

        )