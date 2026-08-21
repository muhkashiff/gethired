"""
Document Knowledge Profile
==========================

Enterprise V14 document-aware wrapper around the existing
KnowledgeProfile.

IMPORTANT
---------
The existing KnowledgeProfile is NOT modified.

This object adds document identity to the existing profile.

Object In
---------
KnowledgePipelineResponse

Object Out
----------
DocumentKnowledgeProfile
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.intelligence.utilities.knowledge.documents.document_types import (
    DocumentType,
)

from app.intelligence.utilities.knowledge.knowledge_scoring.knowledge_profile import (
    KnowledgeProfile,
)


@dataclass(frozen=True)
class DocumentKnowledgeProfile:
    """
    Document-aware KnowledgeProfile.

    This is a wrapper around the existing enterprise
    KnowledgeProfile.

    Attributes
    ----------
    document_type:
        Type of source document.

    profile:
        Existing Enterprise KnowledgeProfile.

    source_result:
        Optional original KnowledgePipeline result.

    Object In
        KnowledgeProfile + DocumentType

    Object Out
        DocumentKnowledgeProfile
    """

    document_type: DocumentType
    profile: KnowledgeProfile
    source_result: Any = None

    def __post_init__(self) -> None:
        """Validate the profile object."""

        if not isinstance(
            self.document_type,
            DocumentType,
        ):
            raise TypeError(
                "DocumentKnowledgeProfile.document_type "
                "must be a DocumentType."
            )

        if not isinstance(
            self.profile,
            KnowledgeProfile,
        ):
            raise TypeError(
                "DocumentKnowledgeProfile.profile "
                "must be a KnowledgeProfile."
            )

    @property
    def summary(self):
        """Return the existing SummaryProfile."""

        return self.profile.summary

    @property
    def entities(self):
        """Return the existing EntityProfile."""

        return self.profile.entities

    @property
    def achievements(self):
        """Return the existing AchievementProfile."""

        return self.profile.achievements

    @property
    def leadership(self):
        """Return the existing LeadershipProfile."""

        return self.profile.leadership

    @property
    def seniority(self):
        """Return the existing SeniorityProfile."""

        return self.profile.seniority

    @property
    def metrics(self):
        """Return the existing MetricProfile."""

        return self.profile.metrics

    @property
    def domains(self):
        """Return the existing DomainProfile."""

        return self.profile.domains

    @property
    def modifiers(self):
        """Return the existing ModifierProfile."""

        return self.profile.modifiers

    @property
    def impact(self):
        """Return the existing ImpactProfile."""

        return self.profile.impact

    @property
    def ats(self):
        """Return the existing ATSProfile."""

        return self.profile.ats

    @property
    def business_statements(self):
        """Return the existing BusinessStatementProfile."""

        return self.profile.business_statements

    @property
    def confidence(self) -> float:
        """Return the existing profile confidence."""

        return self.profile.confidence

    @property
    def is_resume(self) -> bool:
        """Return True when the profile represents a resume."""

        return self.document_type == DocumentType.RESUME

    @property
    def is_jd(self) -> bool:
        """Return True when the profile represents a job description."""

        return self.document_type == DocumentType.JD


__all__ = [
    "DocumentKnowledgeProfile",
]