"""
GetHired
Enterprise V5

Resume Section Extraction Adapter
=================================

Structural boundary between ResumeBuilder and section extractors.

Architecture
------------

ResumeSection
      ↓
ResumeSectionAdapter
      ↓
EducationExtractor / ExperienceExtractor
      ↓
Typed Section Result

The adapter does NOT perform semantic extraction.

It does NOT contain:
    - university databases
    - company databases
    - industry databases
    - hard-coded resume layouts
    - ontology logic

It only routes a ResumeSection to the appropriate
structural extractor.
"""

from __future__ import annotations

from typing import Any

from app.parser.parsed_models.resume_section import ResumeSection

from app.parser.extractors.non_ontology_extractors.education_extractor import (
    EducationExtractor,
)

from app.parser.extractors.non_ontology_extractors.experience_extractor import (
    ExperienceExtractor,
)


class ResumeSectionAdapter:
    """
    Enterprise V5 section extraction adapter.

    One adapter instance owns the structural extractors.

    Input:
        ResumeSection

    Output:
        EducationSectionResult
        ExperienceSectionResult
    """

    def __init__(
        self,
        education_extractor: EducationExtractor | None = None,
        experience_extractor: ExperienceExtractor | None = None,
    ) -> None:

        self.education_extractor = (
            education_extractor
            if education_extractor is not None
            else EducationExtractor()
        )

        self.experience_extractor = (
            experience_extractor
            if experience_extractor is not None
            else ExperienceExtractor()
        )

    # ============================================================
    # EDUCATION
    # ============================================================

    def extract_education(
        self,
        section: ResumeSection,
    ) -> Any:
        """
        Extract education from one ResumeSection.

        The EducationExtractor remains responsible for
        all education parsing.
        """

        self._validate_section(
            section,
            expected_name="education",
        )

        return self.education_extractor.extract(
            section
        )

    # ============================================================
    # EXPERIENCE
    # ============================================================

    def extract_experience(
        self,
        section: ResumeSection,
    ) -> Any:
        """
        Extract experience from one ResumeSection.

        The ExperienceExtractor remains responsible for
        all experience parsing.
        """

        self._validate_section(
            section,
            expected_name="experience",
        )

        return self.experience_extractor.extract(
            section
        )

    # ============================================================
    # GENERIC ROUTING
    # ============================================================

    def extract(
        self,
        section: ResumeSection,
    ) -> Any:
        """
        Route a ResumeSection to its correct extractor.
        """

        self._validate_section(
            section
        )

        name = (
            section.name
            or section.title
            or ""
        ).strip().lower()

        if name in {
            "education",
            "academic background",
            "academic",
            "qualifications",
        }:

            return self.extract_education(
                section
            )

        if name in {
            "experience",
            "professional experience",
            "work experience",
            "employment",
            "employment history",
        }:

            return self.extract_experience(
                section
            )

        raise ValueError(
            "Unsupported section for structural extraction: "
            f"{section.name!r}"
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    @staticmethod
    def _validate_section(
        section: ResumeSection,
        expected_name: str | None = None,
    ) -> None:

        if section is None:

            raise ValueError(
                "ResumeSection cannot be None."
            )

        if not isinstance(
            section,
            ResumeSection,
        ):

            raise TypeError(
                "ResumeSectionAdapter expected ResumeSection, "
                f"received {type(section).__name__}"
            )

        if expected_name is None:
            return

        actual = (
            section.name
            or section.title
            or ""
        ).strip().lower()

        if expected_name not in {
            actual,
            actual.replace("_", " "),
        }:

            raise ValueError(
                "Incorrect section supplied. "
                f"Expected {expected_name!r}, "
                f"received {actual!r}."
            )