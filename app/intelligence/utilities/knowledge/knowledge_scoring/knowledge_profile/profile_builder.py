"""
Knowledge Profile Builder

Builds the master KnowledgeProfile object.

Everything returned from this builder is object-oriented.

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

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.profile_models import (
    KnowledgeProfile,
)


class ProfileBuilder:

    def __init__(self):

        self.seniority = SeniorityPredictor()

        self.leadership = LeadershipEngine()

        self.achievement = AchievementProfileBuilder()

    # -----------------------------------------------------

    def build(self, graph_document):

        graph = graph_document.graph

        # -------------------------------------------------
        # Run Engines
        # -------------------------------------------------

        seniority_result = self.seniority.predict(graph)

        leadership_result = self.leadership.score(graph)

        achievement_result = self.achievement.build(graph)

        # -------------------------------------------------
        # Master Profile Object
        # -------------------------------------------------

        profile = KnowledgeProfile()

        # -------------------------------------------------
        # Achievement
        # -------------------------------------------------

        profile.achievement = achievement_result

        # -------------------------------------------------
        # Leadership
        # -------------------------------------------------

        profile.leadership.score = getattr(
            leadership_result,
            "overall_score",
            0,
        )

        profile.leadership.level = getattr(
            leadership_result,
            "level",
            "",
        )

        if hasattr(leadership_result, "actions"):

            profile.leadership.actions = leadership_result.actions

        if hasattr(leadership_result, "executive_actions"):

            profile.leadership.executive_actions = (
                leadership_result.executive_actions
            )

        # -------------------------------------------------
        # Seniority
        # -------------------------------------------------

        profile.seniority.score = seniority_result.get(
            "score",
            0,
        )

        profile.seniority.level = seniority_result.get(
            "level",
            "",
        )

        profile.seniority.actions = seniority_result.get(
            "actions",
            {},
        )

        profile.seniority.domains = seniority_result.get(
            "domains",
            {},
        )

        # -------------------------------------------------
        # Summary
        # -------------------------------------------------

        profile.summary.career_level = (
            profile.seniority.level
        )

        profile.summary.seniority_score = (
            profile.seniority.score
        )

        profile.summary.leadership_score = (
            profile.leadership.score
        )

        profile.summary.achievement_score = (
            profile.achievement.overall_score
        )

        profile.summary.overall_score = round(

            profile.summary.seniority_score

            + profile.summary.leadership_score

            + profile.summary.achievement_score,

            2,

        )

        return profile