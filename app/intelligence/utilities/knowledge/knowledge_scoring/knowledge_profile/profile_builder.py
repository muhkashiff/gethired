"""
Knowledge Profile Builder

Builds the master knowledge profile from the
Knowledge Graph.

This is the single object consumed by the rest
of the intelligence platform.

Current Modules

    • Seniority
    • Leadership
    • Achievement

Future Modules

    • Business Value
    • Executive Readiness
    • Domain Expertise
    • Technical Expertise
    • ATS Profile
    • Resume Score
"""

from app.intelligence.utilities.knowledge.knowledge_scoring.seniority.seniority_predictor import (
    SeniorityPredictor,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.engines.leadership_engine import (
    LeadershipEngine,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.achievement.achievement_profile_builder import (
    AchievementProfileBuilder,
)


class ProfileBuilder:

    def __init__(self):

        self.seniority = SeniorityPredictor()

        self.leadership = LeadershipEngine()

        self.achievement = AchievementProfileBuilder()

    # -----------------------------------------------------

    def build(self, graph_document):

        graph = graph_document.graph

        seniority = self.seniority.predict(graph)

        leadership = self.leadership.score(graph)

        achievement = self.achievement.build(graph)

        profile = {

            "summary": {},

            "seniority": seniority,

            "leadership": leadership,

            "achievement": achievement,

        }

        profile["summary"] = self._build_summary(profile)

        return profile

    # -----------------------------------------------------

    def _build_summary(self, profile):

        seniority = profile["seniority"]

        leadership = profile["leadership"]

        achievement = profile["achievement"]

        seniority_level = seniority.get("level", "Unknown")
        seniority_score = seniority.get("score", 0)

        leadership_score = getattr(
            leadership,
            "overall_score",
            0,
        )

        achievement_score = achievement.get(
            "overall_score",
            0,
        )

        overall = round(

            seniority_score

            + leadership_score

            + achievement_score,

            2,

        )

        return {

            "career_level": seniority_level,

            "seniority_score": seniority_score,

            "leadership_score": leadership_score,

            "achievement_score": achievement_score,

            "overall_score": overall,

        }