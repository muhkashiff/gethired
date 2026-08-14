
"""
GetHired
Enterprise V5

Section Extraction Adapter
--------------------------

Purpose
-------

This module is the integration boundary between:

    ResumeSection
        ↓
    Section Extractors
        ↓
    Typed Section Results

IMPORTANT
---------

EducationExtractor and ExperienceExtractor are already independently
tested and must NOT be duplicated or modified here.

This adapter only:

    1. Accepts ResumeSection objects.
    2. Routes education sections to EducationExtractor.
    3. Routes experience sections to ExperienceExtractor.
    4. Returns the extractor result objects unchanged.

Architecture
------------

ResumeParser
    ↓
ResumeSection
    ↓
SectionExtractionAdapter
    ├── EducationExtractor
    │       ↓
    │   EducationSectionResult
    │
    └── ExperienceExtractor
            ↓
        ExperienceSectionResult

No ontology logic belongs here.
No university database belongs here.
No resume layout assumptions belong here.
"""

from __future__ import annotations

from typing import Optional

from app.parser.parsed_models.resume_section import ResumeSection

from app.parser.extractors.non_ontology_extractors.education_extractor import (
    EducationExtractor,
)

from app.parser.extractors.non_ontology_extractors.experience_extractor import (
    ExperienceExtractor,
)

from app.parser.education.education_section_result import (
    EducationSectionResult,
)

# IMPORTANT:
# Change this import ONLY if your existing experience result model
# lives at a different path.
from app.parser.experience.experience_section_result import (
    ExperienceSectionResult,
)


class SectionExtractionAdapter:
    """
    Small integration layer for structural resume sections.

    The adapter deliberately keeps education and experience separate.

    It does not convert:

        EducationSectionResult -> list
        ExperienceSectionResult -> list

    The extractor result objects remain intact.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        education_extractor: Optional[EducationExtractor] = None,
        experience_extractor: Optional[ExperienceExtractor] = None,
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
    ) -> EducationSectionResult:
        """
        Extract education from one ResumeSection.

        The EducationExtractor owns all education-specific logic.
        """

        if section is None:

            return self.education_extractor.extract(
                section
            )

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
    ) -> ExperienceSectionResult:
        """
        Extract experience from one ResumeSection.

        The ExperienceExtractor owns all experience-specific logic.
        """

        if section is None:

            return self.experience_extractor.extract(
                section
            )

        self._validate_section(
            section,
            expected_name="experience",
        )

        return self.experience_extractor.extract(
            section
        )

    # ============================================================
    # BOTH SECTIONS
    # ============================================================

    def extract_sections(
        self,
        education_section: Optional[ResumeSection] = None,
        experience_section: Optional[ResumeSection] = None,
    ) -> tuple[
        Optional[EducationSectionResult],
        Optional[ExperienceSectionResult],
    ]:
        """
        Extract education and experience independently.

        Returns
        -------

        (
            education_result,
            experience_result,
        )

        The two result objects remain completely independent.
        """

        education_result = None
        experience_result = None

        if education_section is not None:

            education_result = self.extract_education(
                education_section
            )

        if experience_section is not None:

            experience_result = self.extract_experience(
                experience_section
            )

        return (
            education_result,
            experience_result,
        )

    # ============================================================
    # VALIDATION
    # ============================================================

    @staticmethod
    def _validate_section(
        section: ResumeSection,
        expected_name: str,
    ) -> None:
        """
        Validate that the supplied object is a ResumeSection.

        We intentionally do NOT reject a section merely because its
        name differs slightly from the expected name.

        The parser may use:

            education
            academic background
            qualifications

        etc.

        Therefore structural extraction remains permissive.
        """

        if not isinstance(
            section,
            ResumeSection,
        ):

            raise TypeError(
                f"SectionExtractionAdapter expected "
                f"ResumeSection for {expected_name}, "
                f"received {type(section).__name__}"
            )


__all__ = [
    "SectionExtractionAdapter",
]

