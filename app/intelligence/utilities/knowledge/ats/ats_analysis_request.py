"""
ATS Resume Analysis Request
============================

Phase 5 input contract.

Object In
---------

    KnowledgeMatchProfile
    +
    Resume DocumentKnowledgeProfile
    +
    JDRequirementProfile

Object Out
-----------

    ATSResumeAnalysisRequest

The request is an immutable object-in contract.

The request contains references to the authoritative Phase 4 and
source document objects. Phase 5 must not reconstruct those objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.utilities.knowledge.documents.document_knowledge_profile import (
    DocumentKnowledgeProfile,
)

from app.intelligence.utilities.knowledge.jd_requirements.requirement_models import (
    JDRequirementProfile,
)

from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
    KnowledgeMatchProfile,
)


@dataclass(frozen=True)
class ATSResumeAnalysisRequest:
    """
    Immutable Phase 5 analysis request.

    The exact Phase 4 KnowledgeMatchProfile is preserved for traceability.

    The resume and JD profiles are retained separately because ATS analysis
    may require document-side information that is not represented directly
    by the consolidated Phase 4 profile.
    """

    knowledge_match_profile: KnowledgeMatchProfile

    resume_profile: DocumentKnowledgeProfile

    jd_requirement_profile: JDRequirementProfile

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """
        Validate the structural Phase 5 request boundary.

        This layer validates object contracts only.

        It intentionally does NOT validate whether resume_profile is actually
        a RESUME. That semantic boundary belongs to ATSResumeAnalyzer, where
        the request is consumed.
        """

        if not isinstance(
            self.knowledge_match_profile,
            KnowledgeMatchProfile,
        ):
            raise TypeError(
                "knowledge_match_profile must be "
                "KnowledgeMatchProfile."
            )

        if not isinstance(
            self.resume_profile,
            DocumentKnowledgeProfile,
        ):
            raise TypeError(
                "resume_profile must be "
                "DocumentKnowledgeProfile."
            )

        if not isinstance(
            self.jd_requirement_profile,
            JDRequirementProfile,
        ):
            raise TypeError(
                "jd_requirement_profile must be "
                "JDRequirementProfile."
            )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )


__all__ = [
    "ATSResumeAnalysisRequest",
]