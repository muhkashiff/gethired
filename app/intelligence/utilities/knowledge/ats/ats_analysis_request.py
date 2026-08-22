from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.intelligence.utilities.knowledge.matching.knowledge_match_profile_models import (
        KnowledgeMatchProfile,
    )
    from app.intelligence.utilities.knowledge.documents.document_input import (
        DocumentInput,
    )

@dataclass
class ATSResumeAnalysisRequest:
    resume_text: str = ""
    knowledge_match_profile: Optional["KnowledgeMatchProfile"] = None
    resume_document: Optional["DocumentInput"] = None
    resume_profile: Any = None
    jd_requirement_profile: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.resume_document is not None:
            text = getattr(self.resume_document, "text", "")
            if text is None or not str(text).strip():
                raise ValueError(
                    "ATSResumeAnalysisRequest.resume_document must contain "
                    "non-empty text."
                )
            self.resume_text = str(text)
        elif not str(self.resume_text or "").strip():
            raise ValueError(
                "ATSResumeAnalysisRequest requires non-empty resume_text "
                "or a resume_document with non-empty text."
            )

        if self.knowledge_match_profile is None:
            raise ValueError(
                "ATSResumeAnalysisRequest requires a KnowledgeMatchProfile."
            )

        if self.resume_profile is None:
            self.resume_profile = getattr(
                self.knowledge_match_profile, "resume_profile", None
            )
        if self.jd_requirement_profile is None:
            self.jd_requirement_profile = getattr(
                self.knowledge_match_profile, "jd_requirement_profile", None
            )

    @property
    def has_resume_source(self) -> bool:
        return bool(str(self.resume_text or "").strip())

    @property
    def has_phase4_profile(self) -> bool:
        return self.knowledge_match_profile is not None

    @property
    def source_text(self) -> str:
        return self.resume_text

    def validate(self) -> None:
        self.__post_init__()

__all__ = ["ATSResumeAnalysisRequest"]