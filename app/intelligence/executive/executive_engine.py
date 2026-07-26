"""
Executive Potential Engine
"""

from .executive_detector import ExecutiveDetector
from .executive_rules import ExecutiveRules
from .executive_scorer import ExecutiveScorer
from .executive_profile_builder import ExecutiveProfileBuilder


class ExecutiveEngine:

    def __init__(self):

        self.detector = ExecutiveDetector()

        self.rules = ExecutiveRules()

        self.scorer = ExecutiveScorer(

            self.rules

        )

        self.builder = ExecutiveProfileBuilder()

    # ----------------------------------------------------

    def evaluate(

        self,

        leadership,

        promotion,

        stability,

        trajectory

    ):

        return self.builder.build(

            self.detector,

            self.scorer,

            leadership,

            promotion,

            stability,

            trajectory

        )