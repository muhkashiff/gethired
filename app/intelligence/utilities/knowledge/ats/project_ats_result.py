"""
Project ATS Result Contract
===========================

Enterprise project-level Phase 5 result contract.

This object is the application orchestration boundary between:

    Phase 4
        ProjectMatchResult
            ↓
    Phase 5
        ATSResumeAnalysisRequest
            ↓
        ATSResumeAnalysisResult

The complete upstream ProjectMatchResult is preserved.

Phase 5 does not reconstruct or rerun Phase 1, Phase 2,
Phase 3, or Phase 4 intelligence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.intelligence.utilities.knowledge.ats.ats_analysis_request import (
    ATSResumeAnalysisRequest,
)

from app.intelligence.utilities.knowledge.ats.ats_analysis_models import (
    ATSResumeAnalysisResult,
)

from app.intelligence.utilities.knowledge.project_pipeline.project_pipeline_result import (
    ProjectMatchResult,
)


@dataclass(frozen=True)
class ProjectATSResult:
    """
    Complete application-level Phase 5 result.

    Object In
    ---------

        ProjectMatchResult

    Internal Phase 5 input
    ----------------------

        ATSResumeAnalysisRequest

    Intelligence output
    -------------------

        ATSResumeAnalysisResult

    Object Out
    ----------

        ProjectATSResult
    """

    # ------------------------------------------------------------------
    # Complete Phase 1 -> Phase 4 project result
    # ------------------------------------------------------------------

    project_match_result: ProjectMatchResult

    # ------------------------------------------------------------------
    # Phase 5 request boundary
    # ------------------------------------------------------------------

    ats_request: ATSResumeAnalysisRequest

    # ------------------------------------------------------------------
    # Phase 5 intelligence result
    # ------------------------------------------------------------------

    ats_analysis_result: ATSResumeAnalysisResult

    # ------------------------------------------------------------------
    # Application metadata
    # ------------------------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        """
        Validate the complete Phase 4 -> Phase 5 identity chain.
        """

        # --------------------------------------------------------------
        # TYPE VALIDATION
        # --------------------------------------------------------------

        if not isinstance(
            self.project_match_result,
            ProjectMatchResult,
        ):
            raise TypeError(
                "project_match_result must be "
                "ProjectMatchResult."
            )

        if not isinstance(
            self.ats_request,
            ATSResumeAnalysisRequest,
        ):
            raise TypeError(
                "ats_request must be "
                "ATSResumeAnalysisRequest."
            )

        if not isinstance(
            self.ats_analysis_result,
            ATSResumeAnalysisResult,
        ):
            raise TypeError(
                "ats_analysis_result must be "
                "ATSResumeAnalysisResult."
            )

        # --------------------------------------------------------------
        # PHASE 4 -> PHASE 5 REQUEST IDENTITY
        # --------------------------------------------------------------

        if (
            self.ats_request.knowledge_match_profile
            is not self.project_match_result.knowledge_match_profile
        ):
            raise ValueError(
                "ats_request.knowledge_match_profile must "
                "reference the exact KnowledgeMatchProfile "
                "contained in project_match_result."
            )

        # --------------------------------------------------------------
        # RESUME PROFILE IDENTITY
        # --------------------------------------------------------------

        if (
            self.ats_request.resume_profile
            is not (
                self.project_match_result
                .resume_result
                .document_profile
            )
        ):
            raise ValueError(
                "ats_request.resume_profile must "
                "reference the exact resume DocumentKnowledgeProfile "
                "contained in project_match_result."
            )

        # --------------------------------------------------------------
        # JD REQUIREMENT PROFILE IDENTITY
        # --------------------------------------------------------------

        expected_jd_profile = (
            self.project_match_result
            .jd_result
            .jd_requirement_profile
        )

        if (
            self.ats_request.jd_requirement_profile
            is not expected_jd_profile
        ):
            raise ValueError(
                "ats_request.jd_requirement_profile must "
                "reference the exact JDRequirementProfile "
                "contained in project_match_result."
            )

        # --------------------------------------------------------------
        # RESULT -> REQUEST IDENTITY
        # --------------------------------------------------------------

        if (
            self.ats_analysis_result.request
            is not self.ats_request
        ):
            raise ValueError(
                "ats_analysis_result.request must "
                "reference the exact ats_request."
            )

        # --------------------------------------------------------------
        # METADATA NORMALIZATION
        # --------------------------------------------------------------

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )


__all__ = [
    "ProjectATSResult",
]