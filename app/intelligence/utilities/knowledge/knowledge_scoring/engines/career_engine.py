"""
GetHired

Career Intelligence Engine

Central orchestrator for all career intelligence.

Everything outside the parser should use this class.
"""

from app.intelligence.leadership_engine import LeadershipEngine
from app.intelligence.seniority_engine import SeniorityEngine
from app.intelligence.business_impact_engine import BusinessImpactEngine
from app.intelligence.technical_strength_engine import TechnicalStrengthEngine
from app.intelligence.career_progression_engine import CareerProgressionEngine


class CareerEngine:

    def __init__(self):

        self.leadership_engine = LeadershipEngine()

        self.seniority_engine = SeniorityEngine()

        self.business_engine = BusinessImpactEngine()

        self.technical_engine = TechnicalStrengthEngine()

        self.progression_engine = CareerProgressionEngine()

    # =======================================================
    # Main Analysis
    # =======================================================

    def analyze(
        self,
        experiences,
        skills,
        technologies,
        achievements,
        certifications,
        education,
        industry
    ):

        leadership = self.leadership_engine.analyze(
            experiences,
            achievements
        )

        seniority = self.seniority_engine.predict(
            experiences,
            leadership
        )

        business = self.business_engine.analyze(
            achievements
        )

        technical = self.technical_engine.analyze(
            skills,
            technologies
        )

        progression = self.progression_engine.analyze(
            experiences
        )

        return {

            "leadership": leadership,

            "seniority": seniority,

            "business_impact": business,

            "technical_strength": technical,

            "career_progression": progression

        }