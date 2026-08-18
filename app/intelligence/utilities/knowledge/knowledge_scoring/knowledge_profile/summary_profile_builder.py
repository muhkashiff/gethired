"""
Summary Profile Builder
Enterprise V14
"""

from __future__ import annotations

from typing import Any

from .profile_models import SummaryProfile


class SummaryProfileBuilder:

    def build(
        self,
        achievements,
        leadership,
        seniority,
        impact,
        ats,
    ) -> SummaryProfile:

        profile = SummaryProfile()

        profile.impact_score = round(
            impact.average_impact,
            4,
        )

        profile.ats_score = round(
            ats.score,
            4,
        )

        profile.achievement_score = round(
            achievements.overall_score,
            4,
        )

        profile.leadership_score = round(
            leadership.score,
            4,
        )

        profile.seniority_score = round(
            seniority.score,
            4,
        )

        profile.career_level = (
            seniority.level
        )

        # -------------------------------------------------------------
        # Aggregate score
        # -------------------------------------------------------------

        components = [
            profile.impact_score,
            profile.ats_score,
            profile.achievement_score,
            profile.leadership_score,
            profile.seniority_score,
        ]

        components = [
            value
            for value in components
            if value is not None
        ]

        if components:

            profile.overall_score = round(
                sum(components)
                / len(components),
                4,
            )

        return profile