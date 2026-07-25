"""
Leadership Engine

Public API
"""

from .leadership_analyzer import LeadershipAnalyzer


class LeadershipEngine:

    def __init__(self):

        self.analyzer = LeadershipAnalyzer()

    def analyze(self, experiences):

        return self.analyzer.analyze(
            experiences
        )