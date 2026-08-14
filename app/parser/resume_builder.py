# Enterprise V5 — Universal ResumeBuilder

"""
GetHired

Enterprise V5 Resume Builder
============================

Universal Resume Builder

Converts the object-oriented ResumeParser output into
the strongly typed Resume model.

Architecture
------------

DOCX
    ↓
ResumeReader
    ↓
ResumeBlock
    ↓
SectionDetector
    ↓
ResumeSection
    ↓
ResumeParser
    ↓
ResumeBuilder
    ↓
Resume
    ↓
Intelligence / Enrichment
    ↓
JD Matching


IMPORTANT ARCHITECTURAL PRINCIPLE
----------------------------------

ResumeBuilder is a structural normalization boundary.

The parser is responsible for:

    DOCX -> ResumeBlock -> ResumeSection

The builder is responsible for:

    ResumeSection
        ↓
    universal structural normalization
        ↓
    typed extractor-compatible input
        ↓
    Resume

The builder MUST NOT assume that a particular resume layout,
table structure, indentation style, or education format was used.

It must therefore handle resumes such as:

    M.Sc. Chemistry
    University of the Punjab
    2010 - 2012

or:

    M.Sc. Chemistry, University of the Punjab, Pakistan
    Four-year Bachelor's degree equivalency verified by WES.

or:

    University of the Punjab
    M.Sc. Chemistry
    Lahore, Pakistan

or:

    M.Sc. Chemistry (Organic Chemistry Major)
        University of the Punjab, Pakistan
        Four-year Bachelor's degree academic equivalency...

All of the above should become ONE education record.

Likewise, experience headers must be separated from the
previous job's responsibilities/achievements.

Example:

    QA Chemist | Coca-Cola ... 2010 - 2016

    ...

    Managing Director | Nutrain (Pvt) Ltd.
    2025 - 2026 | Lahore, Pakistan

The second header MUST NOT become an achievement belonging
to Coca-Cola.

Ontology-controlled extraction for skills, certifications,
and standards is intentionally NOT duplicated here.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .parsed_models.resume import Resume
from .parsed_models.reference import Reference

from app.parser.resume_section_adapter import (
    ResumeSectionAdapter,
)

from app.parser.normalization.resume_normalizer import (
    UniversalResumeNormalizer,
)

from app.parser.extractors import (
    ContactExtractor,
    ExperienceExtractor,
    EducationExtractor,
    LanguageExtractor,
    ProjectExtractor,
    AwardExtractor,
    ReferenceExtractor,
)


class ResumeBuilder:
    """
    Enterprise V5 Resume Builder.

    Responsibilities
    ----------------

    1. Convert ResumeSection objects into extractor-compatible text.
    2. Normalize structural record boundaries.
    3. Prevent education descriptions from becoming new records.
    4. Prevent experience headers from becoming achievements.
    5. Populate the strongly typed Resume model.
    6. Preserve raw parser information.
    7. Preserve parser -> builder traceability.
    8. Keep ontology extraction outside this builder.
    9. Remain layout-independent.
    10. Provide a stable boundary between parser and intelligence layers.

    The builder does NOT attempt to understand every semantic
    detail of a resume.

    Instead it establishes reliable structural boundaries
    before invoking the existing typed extractors.
    """

    # ========================================================
    # EXTRACTOR INPUT PREPARATION
    # ========================================================

    def _prepare_extractor_input(
        self,
        sections,
    ):
        """
        Prepare parser sections for the modular section adapter.

        ResumeBuilder is responsible only for routing data.

        It does NOT parse education or experience records.

        The SectionAdapter owns section-specific extraction.
        """

        if sections is None:
            return {}

        prepared = {}

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header_section = sections.get("header")

        if header_section is not None:
            prepared["header"] = header_section

        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        summary_section = sections.get("summary")

        if summary_section is not None:
            prepared["summary"] = summary_section

        # ----------------------------------------------------
        # SKILLS
        # ----------------------------------------------------

        skills_section = sections.get("skills")

        if skills_section is not None:
            prepared["skills"] = skills_section

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        experience_section = sections.get("experience")

        if experience_section is not None:
            prepared["experience"] = experience_section

        # ----------------------------------------------------
        # EDUCATION
        # ----------------------------------------------------

        education_section = sections.get("education")

        if education_section is not None:
            prepared["education"] = education_section

        # ----------------------------------------------------
        # CERTIFICATIONS
        # ----------------------------------------------------

        certifications_section = sections.get(
            "certifications"
        )

        if certifications_section is not None:
            prepared["certifications"] = certifications_section

        # ----------------------------------------------------
        # LANGUAGES
        # ----------------------------------------------------

        languages_section = sections.get("languages")

        if languages_section is not None:
            prepared["languages"] = languages_section

        return prepared
    # ============================================================
    # UNIVERSAL PATTERNS
    # ============================================================

    # Date ranges commonly found in resumes.
    _DATE_RANGE_RE = re.compile(
        r"""
        (?:
            \b(?:19|20)\d{2}\b
        )
        \s*
        (?:
            -
            |
            –
            |
            —
            |
            to
            |
            until
        )
        \s*
        (?:
            present
            |
            current
            |
            now
            |
            (?:19|20)\d{2}
            |
            \d{1,2}
            /
            (?:19|20)\d{2}
            |
            [A-Za-z]{3,9}
            \s+
            (?:19|20)\d{2}
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # More flexible date presence.
    _YEAR_RE = re.compile(
        r"\b(?:19|20)\d{2}\b"
    )

    
    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        # --------------------------------------------------------
        # UNIVERSAL NORMALIZER
        # --------------------------------------------------------

        self.normalizer = UniversalResumeNormalizer()

        self.section_adapter = ResumeSectionAdapter()

        # --------------------------------------------------------
        # NON-ONTOLOGY EXTRACTORS
        # --------------------------------------------------------

        self.contact_extractor = ContactExtractor()

        self.experience_extractor = ExperienceExtractor()

        self.education_extractor = EducationExtractor()

        self.language_extractor = LanguageExtractor()

        self.project_extractor = ProjectExtractor()

        self.award_extractor = AwardExtractor()

        self.reference_extractor = ReferenceExtractor()

        # --------------------------------------------------------
        # STRUCTURAL SECTION ADAPTER
        # --------------------------------------------------------

        self.section_adapter = ResumeSectionAdapter(
            education_extractor=self.education_extractor,
            experience_extractor=self.experience_extractor,
        )

    # ============================================================
    # BASIC TEXT NORMALIZATION
    # ============================================================

    @staticmethod
    def _block_text(block: Any) -> str:
        """
        Convert a ResumeBlock or compatible object into plain text.

        Supported inputs:

            ResumeBlock
            string
            objects exposing .text
            arbitrary objects with string representation
        """

        if block is None:
            return ""

        if isinstance(block, str):
            return block.strip()

        if hasattr(block, "text"):

            text = getattr(block, "text", "")

            if text is None:
                return ""

            return str(text).strip()

        return str(block).strip()

    # ============================================================

    @classmethod
    def _clean_text(cls, text: Any) -> str:
        """
        Universal text cleanup.

        This deliberately performs only safe structural cleanup.

        It does NOT aggressively rewrite resume content.
        """

        if text is None:
            return ""

        text = str(text)

        # Normalize unusual whitespace.
        text = text.replace("\xa0", " ")

        # Normalize tabs.
        text = text.replace("\t", " ")

        # Normalize line endings.
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Collapse repeated spaces but preserve line boundaries.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Remove whitespace around newlines.
        text = re.sub(
            r"[ \t]*\n[ \t]*",
            "\n",
            text,
        )

        return text.strip()

    # ============================================================
    # SECTION EXTRACTION
    # ============================================================

    @classmethod
    def _section_items(cls, section: Any) -> list[str]:
        """
        Convert a ResumeSection into a list of strings.

        This is the first compatibility boundary.
        """

        if section is None:
            return []

        # --------------------------------------------------------
        # ResumeSection
        # --------------------------------------------------------

        if hasattr(section, "items"):

            items = getattr(section, "items", None)

            if items is None:
                return []

            result = []

            for item in items:

                text = cls._clean_text(
                    cls._block_text(item)
                )

                if text:
                    result.append(text)

            return result

        # --------------------------------------------------------
        # Legacy list / tuple
        # --------------------------------------------------------

        if isinstance(section, (list, tuple)):

            result = []

            for item in section:

                text = cls._clean_text(
                    cls._block_text(item)
                )

                if text:
                    result.append(text)

            return result

        # --------------------------------------------------------
        # Single parser block
        # --------------------------------------------------------

        if hasattr(section, "text"):

            text = cls._clean_text(section)

            return [text] if text else []

        # --------------------------------------------------------
        # Single string
        # --------------------------------------------------------

        if isinstance(section, str):

            text = cls._clean_text(section)

            return [text] if text else []

        raise TypeError(
            "Unsupported resume section object: "
            f"{type(section).__name__}"
        )

    # ============================================================
    # NORMALIZE ALL SECTIONS
    # ============================================================

    @classmethod
    def _normalize_sections(
        cls,
        sections: dict[str, Any],
    ) -> dict[str, list[str]]:
        """
        Convert:

            dict[str, ResumeSection]

        into:

            dict[str, list[str]]

        while preserving the original parser objects.
        """

        if sections is None:
            return {}

        if not isinstance(sections, dict):

            raise TypeError(
                "ResumeBuilder expected sections to be dict, "
                f"received {type(sections).__name__}"
            )

        normalized: dict[str, list[str]] = {}

        for section_name, section in sections.items():

            key = str(section_name).strip().lower()

            normalized[key] = cls._section_items(section)

        return normalized

    # ============================================================
    # SECTION HEADING DETECTION
    # ============================================================

    @classmethod
    def _is_heading(cls, text: str) -> bool:
        """
        Determine whether a line is a section/subsection heading.
        """

        if not text:
            return False

        clean = text.strip()

        if cls._HEADING_RE.match(clean):
            return True

        return False

        
    # ============================================================
    # CONTACT NORMALIZATION
    # ============================================================

    @classmethod
    def _normalize_header(
        cls,
        header: list[str],
    ) -> list[str]:
        """
        Normalize header lines without destroying their structure.
        """

        if not header:
            return []

        result: list[str] = []

        for line in header:

            text = cls._clean_text(line)

            if text:
                result.append(text)

        return result

    # ============================================================
    # SUMMARY NORMALIZATION
    # ============================================================

    @classmethod
    def _normalize_summary(
        cls,
        summary: list[str],
    ) -> str:
        """
        Convert summary blocks into one clean paragraph.
        """

        if not summary:
            return ""

        parts = []

        for item in summary:

            text = cls._clean_text(item)

            if text:
                parts.append(text)

        return " ".join(parts).strip()

    # ============================================================
    # GENERAL FLAT SECTION NORMALIZATION
    # ============================================================

    @classmethod
    def _normalize_generic_lines(
        cls,
        lines: list[str],
    ) -> list[str]:
        """
        Safe normalization for sections that do not require
        specialized record-boundary reconstruction.
        """

        result: list[str] = []

        for line in lines:

            text = cls._clean_text(line)

            if text:
                result.append(text)

        return result

    # ============================================================
    # SAFE EXTRACTOR CALL
    # ============================================================

    @staticmethod
    def _safe_extract(
        extractor: Any,
        lines: list[str],
        default: Any,
    ) -> Any:
        """
        Execute an extractor without allowing a malformed optional
        section to destroy the entire resume build.

        The exception is re-raised after being annotated in a
        predictable way so debugging remains possible.
        """

        if not lines:
            return default

        try:

            result = extractor.extract(
                lines
            )

            if result is None:
                return default

            return result

        except Exception as exc:

            raise RuntimeError(
                f"{extractor.__class__.__name__} failed while "
                f"processing resume section."
            ) from exc

    # ============================================================
    # EDUCATION VALIDATION
    # ============================================================

    @classmethod
    def _education_diagnostics(
        cls,
        raw_lines: list[str],
        extracted: list[Any],
    ) -> dict[str, Any]:
        """
        Generate lightweight diagnostics.

        These diagnostics do NOT modify extraction.

        They help identify structural regressions such as:

            education input = 3 logical records
            extracted output = 4 records

        without making the builder dependent on one particular
        resume.
        """

        degree_headers = 0

        for line in raw_lines:

            if cls._is_education_degree_line(line):
                degree_headers += 1

        return {
            "input_lines": len(raw_lines),
            "degree_header_candidates": degree_headers,
            "extracted_records": len(
                extracted or []
            ),
        }

    # ============================================================
    # EXPERIENCE VALIDATION
    # ============================================================

    @classmethod
    def _experience_diagnostics(
        cls,
        raw_lines: list[str],
        extracted: list[Any],
    ) -> dict[str, Any]:
        """
        Generate lightweight experience-boundary diagnostics.
        """

        header_candidates = 0

        for line in raw_lines:

            if cls._looks_like_experience_header(line):
                header_candidates += 1

        return {
            "input_lines": len(raw_lines),
            "header_candidates": header_candidates,
            "extracted_records": len(
                extracted or []
            ),
        }

    # ============================================================
    # BUILD
    # ============================================================

    def build(
        self,
        sections: dict[str, Any],
        *,
        source_file: str = "",
        source_format: str = "docx",
        raw_blocks: list[Any] | None = None,
    ) -> Resume:
        """
        Build a strongly typed Resume object.

        Parameters
        ----------
        sections:
            Output from ResumeParser.

        source_file:
            Original resume path.

        source_format:
            Original file format.

        raw_blocks:
            Original ResumeReader blocks.

        Returns
        -------
        Resume
        """

        # ========================================================
        # 1. RAW SECTION NORMALIZATION
        # ========================================================

        normalized = self._normalize_sections(
            sections
        )

        # ========================================================
        # 2. UNIVERSAL STRUCTURAL NORMALIZATION
        # ========================================================

        prepared = self._prepare_extractor_input(
            normalized
        )

        # ========================================================
        # 3. CREATE RESUME
        # ========================================================

        resume = Resume()

        # ========================================================
        # 4. SOURCE INFORMATION
        # ========================================================

        resume.source_file = str(
            source_file or ""
        )

        resume.source_format = (
            source_format or "docx"
        )

        # Preserve original reader objects.
        if raw_blocks is not None:

            resume.raw_blocks = list(
                raw_blocks
            )

        # Preserve original parser sections.
        if sections:

            resume.sections = dict(
                sections
            )

        # ========================================================
        # 5. PERSONAL INFORMATION
        # ========================================================

        header = self._normalize_header(
            prepared.get(
                "header",
                [],
            )
        )

        if header:

            resume.personal_information.name = (
                header[0].strip()
            )

        contact = self._safe_extract(
            self.contact_extractor,
            header,
            {},
        )

        if contact is None:
            contact = {}

        resume.personal_information.email = (
            contact.get(
                "email",
                "",
            )
        )

        resume.personal_information.phone = (
            contact.get(
                "phone",
                "",
            )
        )

        resume.personal_information.linkedin = (
            contact.get(
                "linkedin",
                "",
            )
        )

        resume.personal_information.github = (
            contact.get(
                "github",
                "",
            )
        )

        resume.personal_information.address = (
            contact.get(
                "location",
                "",
            )
        )

        # ========================================================
        # 6. SUMMARY
        # ========================================================

        resume.summary = self._normalize_summary(
            prepared.get(
                "summary",
                [],
            )
        )

        # ========================================================
        # 7. EXPERIENCE
        # ========================================================

        experience_section = sections.get(
            "experience"
        )

        if experience_section is not None:

            experience_result = (
                self.section_adapter.extract_experience(
                    experience_section
                )
            )

            if experience_result.success:

                resume.experience = (
                    experience_result.records
                )

            else:

                raise RuntimeError(
                    "Experience extraction failed: "
                    f"{experience_result.error}"
                )

        else:

            resume.experience = []

        # ========================================================
        # 8. EDUCATION
        # ========================================================

        education_section = sections.get(
            "education"
        )

        if education_section is not None:

            education_result = (
                self.section_adapter.extract_education(
                    education_section
                )
            )

            if education_result.success:

                resume.education = (
                    education_result.records
                )

            else:

                raise RuntimeError(
                    "Education extraction failed: "
                    f"{education_result.error}"
                )

        else:

            resume.education = []

        # ========================================================
        # 9. PROJECTS
        # ========================================================

        project_lines = prepared.get(
            "projects",
            [],
        )

        if project_lines:

            resume.projects = self._safe_extract(
                self.project_extractor,
                project_lines,
                [],
            )

        else:

            resume.projects = []

        # ========================================================
        # 10. AWARDS
        # ========================================================

        award_lines = prepared.get(
            "awards",
            [],
        )

        if award_lines:

            resume.awards = self._safe_extract(
                self.award_extractor,
                award_lines,
                [],
            )

        else:

            resume.awards = []

        # ========================================================
        # 11. LANGUAGES
        # ========================================================

        language_lines = prepared.get(
            "languages",
            [],
        )

        if language_lines:

            resume.languages = self._safe_extract(
                self.language_extractor,
                language_lines,
                [],
            )

        else:

            resume.languages = []

        # ========================================================
        # 12. REFERENCES
        # ========================================================

        reference_lines = prepared.get(
            "references",
            [],
        )

        if reference_lines:

            resume.references = self._safe_extract(
                self.reference_extractor,
                reference_lines,
                [],
            )

        else:

            resume.references = []

        # --------------------------------------------------------
        # UNIVERSAL REFERENCE FALLBACK
        # --------------------------------------------------------

        if not resume.references:

            resume.references = [
                Reference(
                    available_on_request=True
                )
            ]

        # ========================================================
        # 13. BUILDER METADATA
        # ========================================================

        resume.metadata[
            "builder"
        ] = "ResumeBuilder"

        resume.metadata[
            "builder_version"
        ] = "Enterprise-V5-Universal"

        resume.metadata[
            "normalization"
        ] = "universal_structural"

        # --------------------------------------------------------
        # Original parser section sizes.
        # --------------------------------------------------------

        resume.metadata[
            "original_section_counts"
        ] = {
            key: len(value)
            for key, value in normalized.items()
        }

        # --------------------------------------------------------
        # Extractor input sizes.
        # --------------------------------------------------------

        resume.metadata[
            "prepared_section_counts"
        ] = {
            key: len(value)
            for key, value in prepared.items()
        }

        # --------------------------------------------------------
        # Education diagnostics.
        # --------------------------------------------------------

        # Education diagnostics are now handled by the
        # modular EducationExtractor / EducationSectionResult.
        #
        # Do not perform education parsing or classification
        # inside ResumeBuilder.

        # --------------------------------------------------------
        # Experience diagnostics.
        # --------------------------------------------------------

        # Education diagnostics are now handled by the
        # modular ExperienceExtractor / ExperienceSectionResult.
        #
        # Do not perform education parsing or classification
        # inside ResumeBuilder.

        # --------------------------------------------------------
        # Traceability.
        # --------------------------------------------------------

        resume.metadata[
            "raw_block_count"
        ] = (
            len(raw_blocks)
            if raw_blocks is not None
            else 0
        )

        resume.metadata[
            "raw_section_count"
        ] = len(
            sections or {}
        )

        return resume
    