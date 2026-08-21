"""
Knowledge Matching
==================

Phase 3 matching and Phase 4 knowledge-match-profile layer.

Public objects:

    KnowledgeMatchRequest
    KnowledgeMatchResult
    RequirementMatch
    MatchStatus
    MatchBasis
    KnowledgeMatcher

    KnowledgeMatchEnricher
    EnrichedKnowledgeMatchResult

    KnowledgeGapAnalyzer
    GapStatus
    GapSeverity
    RequirementGap
    KnowledgeGapAnalysisResult

    KnowledgeRequirementProfile
    KnowledgeMatchProfile
    KnowledgeMatchProfileBuilder
"""

from app.intelligence.utilities.knowledge.matching.match_models import (
    MatchBasis,
    MatchStatus,
    KnowledgeMatchRequest,
    KnowledgeMatchResult,
    RequirementMatch,
)

from app.intelligence.utilities.knowledge.matching.knowledge_matcher import (
    KnowledgeMatcher,
)

from app.intelligence.utilities.knowledge.matching.match_enricher import (
    KnowledgeMatchEnricher,
)

from app.intelligence.utilities.knowledge.matching.enrichment_models import (
    EnrichedKnowledgeMatchResult,
)

from app.intelligence.utilities.knowledge.matching.gap_models import (
    GapStatus,
    GapSeverity,
    RequirementGap,
    KnowledgeGapAnalysisResult,
)

from app.intelligence.utilities.knowledge.matching.gap_analyzer import (
    KnowledgeGapAnalyzer,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeRequirementProfile,
    KnowledgeMatchProfile,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_builder import (
    KnowledgeMatchProfileBuilder,
)


__all__ = [
    "MatchBasis",
    "MatchStatus",
    "KnowledgeMatchRequest",
    "KnowledgeMatchResult",
    "RequirementMatch",
    "KnowledgeMatcher",
    "KnowledgeMatchEnricher",
    "EnrichedKnowledgeMatchResult",
    "KnowledgeGapAnalyzer",
    "GapStatus",
    "GapSeverity",
    "RequirementGap",
    "KnowledgeGapAnalysisResult",
    "KnowledgeRequirementProfile",
    "KnowledgeMatchProfile",
    "KnowledgeMatchProfileBuilder",
]