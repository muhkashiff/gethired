"""
Career Trajectory Engine
"""

from .trajectory_detector import TrajectoryDetector
from .trajectory_rules import TrajectoryRules
from .trajectory_scorer import TrajectoryScorer
from .trajectory_profile_builder import TrajectoryProfileBuilder


class TrajectoryEngine:

    def __init__(self):

        self.detector = TrajectoryDetector()

        self.rules = TrajectoryRules()

        self.scorer = TrajectoryScorer(self.rules)

        self.builder = TrajectoryProfileBuilder()

    # --------------------------------------------------

    def evaluate(self, experiences):

        return self.builder.build(

            self.detector,

            self.scorer,

            experiences

        )