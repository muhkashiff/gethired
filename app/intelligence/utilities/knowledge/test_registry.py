"""
Tests for DocumentKnowledgeProfile
===================================

Milestone 1.4
"""

import pytest

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile import (
    KnowledgeProfile,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.documents.document_profile_builder import (
    DocumentProfileBuilder,
)


class TestDocumentKnowledgeProfile:

    def test_resume_profile_is_document_aware(self):

        profile = KnowledgeProfile()

        document_profile = DocumentKnowledgeProfile(
            document_type=DocumentType.RESUME,
            profile=profile,
        )

        assert (
            document_profile.document_type
            == DocumentType.RESUME
        )

        assert (
            document_profile.profile
            is profile
        )

        assert (
            document_profile.is_resume
            is True
        )

        assert (
            document_profile.is_jd
            is False
        )

    def test_jd_profile_is_document_aware(self):

        profile = KnowledgeProfile()

        document_profile = DocumentKnowledgeProfile(
            document_type=DocumentType.JD,
            profile=profile,
        )

        assert (
            document_profile.document_type
            == DocumentType.JD
        )

        assert (
            document_profile.profile
            is profile
        )

        assert (
            document_profile.is_resume
            is False
        )

        assert (
            document_profile.is_jd
            is True
        )

    def test_existing_profile_is_preserved(self):

        profile = KnowledgeProfile()

        profile.summary.overall_score = 82.5
        profile.entities.total_entities = 25
        profile.confidence = 0.91

        document_profile = DocumentKnowledgeProfile(
            document_type=DocumentType.RESUME,
            profile=profile,
        )

        assert (
            document_profile.summary.overall_score
            == 82.5
        )

        assert (
            document_profile.entities.total_entities
            == 25
        )

        assert (
            document_profile.confidence
            == 0.91
        )

    def test_invalid_document_type_is_rejected(self):

        profile = KnowledgeProfile()

        with pytest.raises(TypeError):

            DocumentKnowledgeProfile(
                document_type="resume",
                profile=profile,
            )

    def test_invalid_profile_is_rejected(self):

        with pytest.raises(TypeError):

            DocumentKnowledgeProfile(
                document_type=DocumentType.RESUME,
                profile="not a KnowledgeProfile",
            )


class TestDocumentProfileBuilder:

    def test_builder_creates_resume_profile(self):

        profile = KnowledgeProfile()

        response = KnowledgePipelineResponse(
            success=True,
            document_type=DocumentType.RESUME,
            result="PIPELINE_RESULT",
        )

        # Replace the response's result with an object that
        # exposes the KnowledgeProfile expected by the response.

        class FakeResult:

            knowledge_profile = profile

        response = KnowledgePipelineResponse(
            success=True,
            document_type=DocumentType.RESUME,
            result=FakeResult(),
        )

        builder = DocumentProfileBuilder()

        result = builder.build(
            response
        )

        assert isinstance(
            result,
            DocumentKnowledgeProfile,
        )

        assert (
            result.document_type
            == DocumentType.RESUME
        )

        assert (
            result.profile
            is profile
        )

    def test_builder_creates_jd_profile(self):

        profile = KnowledgeProfile()

        class FakeResult:

            knowledge_profile = profile

        response = KnowledgePipelineResponse(
            success=True,
            document_type=DocumentType.JD,
            result=FakeResult(),
        )

        builder = DocumentProfileBuilder()

        result = builder.build(
            response
        )

        assert isinstance(
            result,
            DocumentKnowledgeProfile,
        )

        assert (
            result.document_type
            == DocumentType.JD
        )

        assert (
            result.profile
            is profile
        )

    def test_builder_rejects_invalid_response(self):

        builder = DocumentProfileBuilder()

        with pytest.raises(TypeError):

            builder.build(
                "invalid response"
            )

    def test_builder_rejects_failed_response(self):

        response = KnowledgePipelineResponse(
            success=False,
            document_type=DocumentType.RESUME,
            result=None,
            error="Pipeline failed",
        )

        builder = DocumentProfileBuilder()

        with pytest.raises(ValueError):

            builder.build(
                response
            )

    def test_builder_rejects_missing_profile(self):

        class FakeResult:
            knowledge_profile = None

        response = KnowledgePipelineResponse(
            success=True,
            document_type=DocumentType.RESUME,
            result=FakeResult(),
        )

        builder = DocumentProfileBuilder()

        with pytest.raises(ValueError):

            builder.build(
                response
            )