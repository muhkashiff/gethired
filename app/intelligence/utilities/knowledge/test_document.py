"""
Tests for DocumentProcessingService
===================================

Milestone 1.3

DocumentInput
      ↓
DocumentProcessingService
      ↓
DocumentRouter
      ↓
KnowledgePipelineRequest
      ↓
KnowledgePipelineAdapter
      ↓
KnowledgePipelineResponse
"""

from dataclasses import dataclass

import pytest

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.documents.routed_document import (
    RoutedDocument,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_request import (
    KnowledgePipelineRequest,
)

from app.intelligence.utilities.knowledge.pipeline_request.knowledge_pipeline_response import (
    KnowledgePipelineResponse,
)

from app.intelligence.utilities.knowledge.documents.document_processing.document_processing_service import (
    DocumentProcessingService,
)


# ==============================================================
# TEST DOUBLES
# ==============================================================

class FakeRouter:
    """
    Fake DocumentRouter used to test orchestration.
    """

    def __init__(self):
        self.received_document = None

    def process(
        self,
        document,
    ):
        self.received_document = document

        return RoutedDocument(
            text=document.text.strip(),
            document_type=document.document_type,
        )


class FakePipelineAdapter:
    """
    Fake KnowledgePipelineAdapter used to test the service
    without running the real Enterprise Pipeline.
    """

    def __init__(self):
        self.received_request = None

    def process(
        self,
        request,
    ):
        self.received_request = request

        return KnowledgePipelineResponse(
            success=True,
            document_type=request.document_type,
            result="FAKE_PIPELINE_RESULT",
        )


# ==============================================================
# TESTS
# ==============================================================

class TestDocumentProcessingService:

    # ----------------------------------------------------------
    # RESUME
    # ----------------------------------------------------------

    def test_resume_flows_through_service(self):

        router = FakeRouter()
        adapter = FakePipelineAdapter()

        service = DocumentProcessingService(
            router=router,
            pipeline_adapter=adapter,
        )

        document = DocumentInput(
            text="Muhammad Kashif QA Professional",
            document_type=DocumentType.RESUME,
        )

        response = service.process(
            document
        )

        # Output contract

        assert isinstance(
            response,
            KnowledgePipelineResponse,
        )

        assert response.success is True

        assert (
            response.document_type
            == DocumentType.RESUME
        )

        # Router received original object

        assert (
            router.received_document
            is document
        )

        # Adapter received correct request

        assert isinstance(
            adapter.received_request,
            KnowledgePipelineRequest,
        )

        assert (
            adapter.received_request.document_text
            == "Muhammad Kashif QA Professional"
        )

        assert (
            adapter.received_request.document_type
            == DocumentType.RESUME
        )

    # ----------------------------------------------------------
    # JOB DESCRIPTION
    # ----------------------------------------------------------

    def test_jd_flows_through_service(self):

        router = FakeRouter()
        adapter = FakePipelineAdapter()

        service = DocumentProcessingService(
            router=router,
            pipeline_adapter=adapter,
        )

        document = DocumentInput(
            text=(
                "Quality Assurance Manager "
                "with HACCP experience."
            ),
            document_type=DocumentType.JD,
        )

        response = service.process(
            document
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
            adapter.received_request.document_type
            == DocumentType.JD
        )

        assert (
            adapter.received_request.document_text
            == (
                "Quality Assurance Manager "
                "with HACCP experience."
            )
        )

    # ----------------------------------------------------------
    # OBJECT CONTRACT
    # ----------------------------------------------------------

    def test_service_rejects_wrong_input_type(self):

        service = DocumentProcessingService(
            router=FakeRouter(),
            pipeline_adapter=FakePipelineAdapter(),
        )

        with pytest.raises(TypeError):

            service.process(
                "This is not a DocumentInput"
            )

    # ----------------------------------------------------------
    # PIPELINE RESPONSE PRESERVED
    # ----------------------------------------------------------

    def test_pipeline_response_is_returned_unchanged(self):

        router = FakeRouter()
        adapter = FakePipelineAdapter()

        service = DocumentProcessingService(
            router=router,
            pipeline_adapter=adapter,
        )

        document = DocumentInput(
            text="Resume",
            document_type=DocumentType.RESUME,
        )

        response = service.process(
            document
        )

        assert (
            response.result
            == "FAKE_PIPELINE_RESULT"
        )

        assert response.success is True

    # ----------------------------------------------------------
    # DEPENDENCY INJECTION
    # ----------------------------------------------------------

    def test_dependencies_can_be_injected(self):

        router = FakeRouter()
        adapter = FakePipelineAdapter()

        service = DocumentProcessingService(
            router=router,
            pipeline_adapter=adapter,
        )

        assert service.router is router

        assert (
            service.pipeline_adapter
            is adapter
        )