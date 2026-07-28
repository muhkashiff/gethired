"""
Leadership Engine

Standard Scoring API

Every scoring engine exposes

    score(graph)

The internal analyzer still performs
the actual leadership evaluation.
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.leadership.leadership_analyzer import (
    LeadershipAnalyzer,
)


class LeadershipEngine:

    def __init__(self):

        self.analyzer = LeadershipAnalyzer()

    # -----------------------------------------------------

    def score(self, graph):

        """
        Standard interface used by ProfileBuilder.
        """

        return self.analyzer.analyze(graph)

    # -----------------------------------------------------

    # Backward compatibility
    # Older modules may still call analyze()

    def analyze(self, graph):

        return self.score(graph)