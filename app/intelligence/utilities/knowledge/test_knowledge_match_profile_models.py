"""
Tests for Phase 4 Knowledge Match Profile Models
================================================

Tests the pure Phase 4 contracts independently of ProjectPipeline.
"""

from __future__ import annotations

import pytest

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
    KnowledgeRequirementProfile,
    KnowledgeMatchProfile,
    build_knowledge_match_profile,
)


# ============================================================================
# HELPERS
# ============================================================================


def _build_phase3_chain(
    *,
    monkeypatch,
):
    """
    Build a minimal Phase 3 chain using the project's existing models.

    This test intentionally obtains the actual objects from the existing
    matcher/enricher/gap-analysis pipeline rather than constructing fake
    dataclass internals.
    """

    from app.intelligence.utilities.knowledge.matching.knowledge_matcher import (
        KnowledgeMatcher,
    )

    from app.intelligence.utilities.knowledge.matching.match_enricher import (
        KnowledgeMatchEnricher,
    )

    from app.intelligence.utilities.knowledge.matching.gap_analyzer import (
        GapAnalyzer,
    )

    # The actual project test suite may already provide fixtures/helpers
    # for constructing these objects. This helper is intentionally kept
    # isolated so it can be replaced by those fixtures if available.
    pytest.skip(
        "Use the project's existing Phase 3 chain fixture here."
    )


# ============================================================================
# CONTRACT TESTS
# ============================================================================


def test_knowledge_requirement_profile_requires_enriched_match_and_gap():
    with pytest.raises(TypeError):

        KnowledgeRequirementProfile(
            enriched_match=None,
            gap=None,
        )


def test_knowledge_match_profile_requires_match_result():
    with pytest.raises(TypeError):

        KnowledgeMatchProfile(
            match_result=None,
            enriched_match_result=None,
            gap_analysis_result=None,
        )


def test_profile_builder_function_is_importable():
    assert callable(
        build_knowledge_match_profile
    )


def test_knowledge_match_profile_class_is_importable():
    assert KnowledgeMatchProfile is not None


def test_knowledge_requirement_profile_class_is_importable():
    assert KnowledgeRequirementProfile is not None