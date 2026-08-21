"""
Tests for KnowledgePipelineAdapter
==================================

Milestone 1.2

KnowledgePipelineRequest
        ↓
KnowledgePipelineAdapter
        ↓
KnowledgePipelineResponse
"""

from dataclasses import dataclass

import pytest

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_adapter import (
    KnowledgePipelineAdapter,
)


# ==============================================================
# TEST DOUBLE
# ==============================================================

@dataclass
class FakePipelineResult:
    """
    Minimal fake result used to test the adapter.

    This prevents the unit test from executing the full
    Enterprise Knowledge Pipeline.
    """

    success: bool = True
    error: str = None
    knowledge_profile: object = None
    knowledge_document: object = None
    business_statements: list = None
    semantic_entities: list = None
    knowledge_graph: object = None


class FakeEnterprisePipeline:
    """
    Test double for EnterpriseResumePipeline.
    """

    def __init__(self):
        self.received_text = None

    def run(self, text):
        self.received_text = text

        return FakePipelineResult(
            success=True,
            knowledge_profile="PROFILE",
            knowledge_document="DOCUMENT",
            business_statements=["STATEMENT"],
            semantic_entities=["ENTITY"],
            knowledge_graph="GRAPH",
        )


class FailingPipeline:
    """
    Test double representing a pipeline failure.
    """

    def run(self, text):
        raise RuntimeError(
            "Simulated pipeline failure"
        )


# ==============================================================
# TESTS
# ==============================================================

class TestKnowledgePipelineAdapter:

    def test_resume_request_produces_response(self):

        request = KnowledgePipelineRequest(
            document_text="Resume content",
            document_type=DocumentType.RESUME,
        )

        pipeline = FakeEnterprisePipeline()

        adapter = KnowledgePipelineAdapter(
            pipeline=pipeline
        )

        response = adapter.process(
            request
        )

        assert isinstance(
            response,
            KnowledgePipelineResponse,
        )

        assert response.success is True

        assert (
            response.document_type
            == DocumentType.RESUME
        )

        assert (
            pipeline.received_text
            == "Resume content"
        )

    def test_jd_request_produces_response(self):

        request = KnowledgePipelineRequest(
            document_text=(
                "Quality Assurance Manager "
                "with HACCP experience."
            ),
            document_type=DocumentType.JD,
        )

        pipeline = FakeEnterprisePipeline()

        adapter = KnowledgePipelineAdapter(
            pipeline=pipeline
        )

        response = adapter.process(
            request
        )

        assert isinstance(
            response,
            KnowledgePipelineResponse,
        )

        assert response.success is True

        assert (
            response.document_type
            == DocumentType.JD
        )

        assert (
            pipeline.received_text
            == (
                "Quality Assurance Manager "
                "with HACCP experience."
            )
        )

    def test_response_exposes_knowledge_profile(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        response = adapter.process(
            request
        )

        assert (
            response.knowledge_profile
            == "PROFILE"
        )

    def test_response_exposes_knowledge_document(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        response = adapter.process(
            request
        )

        assert (
            response.knowledge_document
            == "DOCUMENT"
        )

    def test_response_exposes_business_statements(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        response = adapter.process(
            request
        )

        assert (
            response.business_statements
            == ["STATEMENT"]
        )

    def test_response_exposes_semantic_entities(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        response = adapter.process(
            request
        )

        assert (
            response.semantic_entities
            == ["ENTITY"]
        )

    def test_response_exposes_knowledge_graph(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        response = adapter.process(
            request
        )

        assert (
            response.knowledge_graph
            == "GRAPH"
        )

    def test_adapter_rejects_wrong_input_type(self):

        adapter = KnowledgePipelineAdapter(
            pipeline=FakeEnterprisePipeline()
        )

        with pytest.raises(TypeError):

            adapter.process(
                "invalid request"
            )

    def test_pipeline_exception_becomes_failed_response(self):

        request = KnowledgePipelineRequest(
            document_text="Resume",
            document_type=DocumentType.RESUME,
        )

        adapter = KnowledgePipelineAdapter(
            pipeline=FailingPipeline()
        )

        response = adapter.process(
            request
        )

        assert isinstance(
            response,
            KnowledgePipelineResponse,
        )

        assert response.success is False

        assert (
            response.document_type
            == DocumentType.RESUME
        )

        assert (
            "RuntimeError"
            in response.error
        )

        assert response.result is None