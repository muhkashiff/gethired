
"""
GetHired

Enterprise V5 Resume Model
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Any

from .personal_information import PersonalInformation
from .resume_section import ResumeSection


@dataclass
class Resume:

    # ============================================================
    # PERSONAL INFORMATION
    # ============================================================

    personal_information: PersonalInformation = dc_field(
        default_factory=PersonalInformation
    )

    # ============================================================
    # SUMMARY
    # ============================================================

    summary: str = ""

    # ============================================================
    # STRUCTURED SECTIONS
    # ============================================================

    skills: list[Any] = dc_field(
        default_factory=list
    )

    experience: list[Any] = dc_field(
        default_factory=list
    )

    education: list[Any] = dc_field(
        default_factory=list
    )

    certifications: list[Any] = dc_field(
        default_factory=list
    )

    projects: list[Any] = dc_field(
        default_factory=list
    )

    awards: list[Any] = dc_field(
        default_factory=list
    )

    languages: list[Any] = dc_field(
        default_factory=list
    )

    references: list[Any] = dc_field(
        default_factory=list
    )

    # ============================================================
    # SOURCE
    # ============================================================

    source_file: str = ""

    source_format: str = "docx"

    raw_blocks: list[Any] = dc_field(
        default_factory=list
    )

    # ============================================================
    # PARSER SECTIONS
    # ============================================================

    sections: dict[str, ResumeSection] = dc_field(
        default_factory=dict
    )

    # ============================================================
    # METADATA
    # ============================================================

    metadata: dict[str, Any] = dc_field(
        default_factory=dict
    )

    # ============================================================
    # CONVENIENCE
    # ============================================================

    @property
    def full_text(self) -> str:

        return "\n".join(

            block.text
            if hasattr(block, "text")
            else str(block)

            for block in self.raw_blocks
        )

    # ============================================================
    # SECTION ACCESS
    # ============================================================

    def get_section(
        self,
        name: str,
    ) -> ResumeSection | None:

        return self.sections.get(
            name
        )

