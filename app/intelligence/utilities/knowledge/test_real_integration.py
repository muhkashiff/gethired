"""
Milestone 1.4
Document Knowledge Profile Integration Test
"""

import pytest

from app.intelligence.utilities.knowledge.documents.document_input import (
    DocumentInput,
)

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.documents.document_processing.document_processing_service import (
    DocumentProcessingService,
)

from app.intelligence.utilities.knowledge.documents.document_profile_builder import (
    DocumentProfileBuilder,
)

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)


class TestDocumentKnowledgeProfileIntegration:

    @pytest.mark.integration
    def test_real_resume_profile_boundary(self):

        resume_text = """
        MUHAMMAD KASHIF

        Quality Assurance & Food Safety Professional

        Led implementation of FSSC 22000 requirements.

        Increased production yield from 70% to 99%
        through data-based decision making.

        Conducted HACCP development and root cause analysis.
        """

        # ------------------------------------------------------
        # 1. DOCUMENT INPUT
        # ------------------------------------------------------

        document = DocumentInput(
            text=resume_text,
            document_type=DocumentType.RESUME,
        )

        # ------------------------------------------------------
        # 2. REAL DOCUMENT PROCESSING
        # ------------------------------------------------------

        processing_service = (
            DocumentProcessingService()
        )

        response = processing_service.process(
            document
        )

        assert response.success is True

        # ------------------------------------------------------
        # 3. BUILD DOCUMENT-AWARE PROFILE
        # ------------------------------------------------------

        profile_builder = (
            DocumentProfileBuilder()
        )

        document_profile = (
            profile_builder.build(
                response
            )
        )

        # ------------------------------------------------------
        # 4. OUTPUT CONTRACT
        # ------------------------------------------------------

        assert isinstance(
            document_profile,
            DocumentKnowledgeProfile,
        )

        # ------------------------------------------------------
        # 5. DOCUMENT TYPE
        # ------------------------------------------------------

        assert (
            document_profile.document_type
            == DocumentType.RESUME
        )

        assert (
            document_profile.is_resume
            is True
        )

        assert (
            document_profile.is_jd
            is False
        )

        # ------------------------------------------------------
        # 6. REAL KNOWLEDGE PROFILE
        # ------------------------------------------------------

        assert (
            document_profile.profile
            is not None
        )

        # ------------------------------------------------------
        # 7. PROFILE COMPONENTS
        # ------------------------------------------------------

        assert (
            document_profile.summary
            is not None
        )

        assert (
            document_profile.entities
            is not None
        )

        assert (
            document_profile.achievements
            is not None
        )

        assert (
            document_profile.leadership
            is not None
        )

        assert (
            document_profile.seniority
            is not None
        )

        assert (
            document_profile.metrics
            is not None
        )

        assert (
            document_profile.domains
            is not None
        )

        assert (
            document_profile.impact
            is not None
        )

        assert (
            document_profile.ats
            is not None
        )

        assert (
            document_profile.business_statements
            is not None
        )

        # ------------------------------------------------------
        # 8. VERIFY REAL PROFILE DATA
        # ------------------------------------------------------

        assert (
            document_profile.entities.total_entities
            >= 0
        )

        assert (
            document_profile.achievements.achievement_count
            >= 0
        )

        assert (
            document_profile.metrics.total_metrics
            >= 0
        )

        assert (
            document_profile.confidence
            >= 0.0
        )