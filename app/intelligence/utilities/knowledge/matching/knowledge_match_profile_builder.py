"""
Knowledge Match Profile Builder
===============================

Phase 4 - Knowledge Match Profile construction.

Object In
----------

    KnowledgeMatchResult
            +
    EnrichedKnowledgeMatchResult
            +
    KnowledgeGapAnalysisResult

Object Out
-----------

    KnowledgeMatchProfile

Phase 4 is a consolidation boundary.

It does not rerun Phase 3 intelligence.
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.matching.match_models import (
    KnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    KnowledgeGapAnalysisResult,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
    build_knowledge_match_profile,
)


class KnowledgeMatchProfileBuilder:
    """
    Phase 4 Knowledge Match Profile builder.

    Responsibilities:

        Phase 3 results
            ↓
        consolidated KnowledgeMatchProfile

    It does not perform:

        - matching
        - evidence collection
        - gap analysis
        - ATS analysis
        - recommendations
    """

    def process(
        self,
        *,
        match_result: KnowledgeMatchResult,
        enriched_match_result: EnrichedKnowledgeMatchResult,
        gap_analysis_result: KnowledgeGapAnalysisResult,
    ) -> KnowledgeMatchProfile:
        """
        Build a KnowledgeMatchProfile from completed Phase 3 results.
        """

        if not isinstance(
            match_result,
            KnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfileBuilder.process() "
                "expects a KnowledgeMatchResult."
            )

        if not isinstance(
            enriched_match_result,
            EnrichedKnowledgeMatchResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfileBuilder.process() "
                "expects an EnrichedKnowledgeMatchResult."
            )

        if not isinstance(
            gap_analysis_result,
            KnowledgeGapAnalysisResult,
        ):
            raise TypeError(
                "KnowledgeMatchProfileBuilder.process() "
                "expects a KnowledgeGapAnalysisResult."
            )

        return build_knowledge_match_profile(
            match_result=match_result,
            enriched_match_result=(
                enriched_match_result
            ),
            gap_analysis_result=(
                gap_analysis_result
            ),
        )


__all__ = [
    "KnowledgeMatchProfileBuilder",
]