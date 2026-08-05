"""
Enterprise Achievement Reasoner

Enterprise V6

Purpose
-------
Builds enterprise achievement intelligence.

Pipeline

Graph

↓

Achievement Extractor

↓

Impact Analyzer

↓

Quantified Achievement Analyzer

↓

Leadership Signal Detector

↓

Achievement Pattern Analyzer

↓

AchievementReasoningResult
"""

from collections import Counter

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.achievement_models import (
    AchievementReasoningResult,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.achievement_extractor import (
    AchievementExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.impact_analyzer import (
    ImpactAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.quantified_achievement_analyzer import (
    QuantifiedAchievementAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.leadership_signal_detector import (
    LeadershipSignalDetector,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.achievement_pattern_analyzer import (
    AchievementPatternAnalyzer,
)


class AchievementReasoner:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.extractor = AchievementExtractor()

        self.impact_analyzer = ImpactAnalyzer()

        self.quantified_analyzer = (

            QuantifiedAchievementAnalyzer()

        )

        self.leadership_detector = (

            LeadershipSignalDetector()

        )

        self.pattern_analyzer = (

            AchievementPatternAnalyzer()

        )

    ####################################################################
    # MAIN ENTRY
    ####################################################################

    def analyze(

        self,

        graph,

        dependency_reasoning,

        ontology_reasoning,

        reasoning,

    ):

        """
        Enterprise achievement reasoning.
        """

        result = AchievementReasoningResult()

        ###############################################################
        # STEP 1
        # Extract achievement evidence
        ###############################################################

        result.achievements = (

            self.extractor.extract(

                graph,

                dependency_reasoning,

                ontology_reasoning,

            )

        )

        ###############################################################
        # STEP 2
        # Business impact
        ###############################################################

        result.business_impacts = (

            self.impact_analyzer.analyze(

                result.achievements

            )

        )

        ###############################################################
        # STEP 3
        # Quantified achievements
        ###############################################################

        result.quantified_results = (

            self.quantified_analyzer.analyze(

                result.achievements

            )

        )

        ###############################################################
        # STEP 4
        # Leadership signals
        ###############################################################

        result.leadership_signals = (

            self.leadership_detector.analyze(

                result.achievements

            )

        )

        ###############################################################
        # STEP 5
        # Achievement patterns
        ###############################################################

        result.achievement_patterns = (

            self.pattern_analyzer.analyze(

                result.achievements

            )
        )