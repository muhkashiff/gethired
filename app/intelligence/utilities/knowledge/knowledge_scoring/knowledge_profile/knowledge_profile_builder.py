"""
Knowledge Profile Builder
Enterprise V14

Architecture
------------

KnowledgeGraph
      +
BusinessStatement[]
      ↓
KnowledgeProfileBuilder
      ↓
KnowledgeProfile

This class performs profile construction only.

It does NOT:

    - build the KnowledgeGraph
    - perform ontology matching
    - extract resume entities
    - perform semantic resolution
    - modify graph nodes
"""

from __future__ import annotations

from typing import Any, Iterable, Optional

from .profile_models import KnowledgeProfile

from .summary_profile_builder import (
    SummaryProfileBuilder,
)

from .entity_profile_builder import (
    EntityProfileBuilder,
)

from .achievement_profile_builder import (
    AchievementProfileBuilder,
)

from .leadership_profile_builder import (
    LeadershipProfileBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile.seniority_profile_builder import (
    SeniorityProfileBuilder,
)

from .metric_profile_builder import (
    MetricProfileBuilder,
)

from .domain_profile_builder import (
    DomainProfileBuilder,
)

from .modifier_profile_builder import (
    ModifierProfileBuilder,
)

from .impact_profile_builder import (
    ImpactProfileBuilder,
)

from .ats_profile_builder import (
    ATSProfileBuilder,
)

from .business_statement_profile_builder import (
    BusinessStatementProfileBuilder,
)


class KnowledgeProfileBuilder:
    """
    Build the complete KnowledgeProfile from the populated
    KnowledgeGraph and BusinessStatement collection.
    """

    def __init__(self) -> None:

        self.summary_builder = (
            SummaryProfileBuilder()
        )

        self.entity_builder = (
            EntityProfileBuilder()
        )

        self.achievement_builder = (
            AchievementProfileBuilder()
        )

        self.leadership_builder = (
            LeadershipProfileBuilder()
        )

        self.seniority_builder = (
            SeniorityProfileBuilder()
        )

        self.metric_builder = (
            MetricProfileBuilder()
        )

        self.domain_builder = (
            DomainProfileBuilder()
        )

        self.modifier_builder = (
            ModifierProfileBuilder()
        )

        self.impact_builder = (
            ImpactProfileBuilder()
        )

        self.ats_builder = (
            ATSProfileBuilder()
        )

        self.statement_builder = (
            BusinessStatementProfileBuilder()
        )

    # =================================================================
    # PUBLIC API
    # =================================================================

    def build(
        self,
        graph: Any = None,
        business_statements: Optional[
            Iterable[Any]
        ] = None,
    ) -> KnowledgeProfile:
        """
        Build complete KnowledgeProfile.

        Parameters
        ----------
        graph:
            Populated KnowledgeGraph.

        business_statements:
            BusinessStatement collection produced upstream.
        """

        statements = list(
            business_statements or []
        )

        profile = KnowledgeProfile()

        # -------------------------------------------------------------
        # ENTITY PROFILE
        # -------------------------------------------------------------

        profile.entities = (
            self.entity_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # METRIC PROFILE
        # -------------------------------------------------------------

        profile.metrics = (
            self.metric_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # DOMAIN PROFILE
        # -------------------------------------------------------------

        profile.domains = (
            self.domain_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # LEADERSHIP PROFILE
        # -------------------------------------------------------------

        profile.leadership = (
            self.leadership_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # SENIORITY PROFILE
        # -------------------------------------------------------------

        profile.seniority = (
            self.seniority_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # MODIFIER PROFILE
        # -------------------------------------------------------------

        profile.modifiers = (
            self.modifier_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # IMPACT PROFILE
        # -------------------------------------------------------------

        profile.impact = (
            self.impact_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # ATS PROFILE
        # -------------------------------------------------------------

        profile.ats = (
            self.ats_builder.build(
                graph
            )
        )

        # -------------------------------------------------------------
        # BUSINESS STATEMENTS
        # -------------------------------------------------------------

        profile.business_statements = (
            self.statement_builder.build(
                statements
            )
        )

        # -------------------------------------------------------------
        # ACHIEVEMENTS
        # -------------------------------------------------------------

        profile.achievements = (
            self.achievement_builder.build(
                graph=graph,
                business_statements=statements,
            )
        )

        # -------------------------------------------------------------
        # SUMMARY
        # -------------------------------------------------------------

        profile.summary = (
            self.summary_builder.build(
                achievements=profile.achievements,
                leadership=profile.leadership,
                seniority=profile.seniority,
                impact=profile.impact,
                ats=profile.ats,
            )
        )

        # -------------------------------------------------------------
        # PROFILE CONFIDENCE
        # -------------------------------------------------------------

        profile.confidence = (
            self._calculate_confidence(
                profile
            )
        )

        return profile

    # =================================================================
    # CONFIDENCE
    # =================================================================

    @staticmethod
    def _calculate_confidence(
        profile: KnowledgeProfile,
    ) -> float:

        populated = 0
        total = 10

        if profile.entities.total_entities:
            populated += 1

        if profile.metrics.total_metrics:
            populated += 1

        if profile.domains.domains:
            populated += 1

        if profile.domains.business_areas:
            populated += 1

        if profile.leadership.entity_count:
            populated += 1

        if profile.seniority.score:
            populated += 1

        if profile.impact.entity_count:
            populated += 1

        if profile.ats.entity_count:
            populated += 1

        if profile.achievements.achievement_count:
            populated += 1

        if (
            profile.business_statements
            .total_statements
        ):
            populated += 1

        return round(
            populated / total,
            4,
        )


# =====================================================================
# CONVENIENCE FUNCTION
# =====================================================================

def build_knowledge_profile(
    graph: Any = None,
    business_statements: Optional[
        Iterable[Any]
    ] = None,
) -> KnowledgeProfile:

    builder = (
        KnowledgeProfileBuilder()
    )

    return builder.build(
        graph=graph,
        business_statements=business_statements,
    )


__all__ = [
    "KnowledgeProfileBuilder",
    "build_knowledge_profile",
]