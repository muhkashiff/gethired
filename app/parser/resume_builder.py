"""
GetHired
Enterprise V5

Universal ResumeBuilder
=======================

Architecture
------------

DOCX
    |
    v
ResumeReader
    |
    v
ResumeBlock
    |
    v
SectionDetector
    |
    v
ResumeSection
    |
    v
ResumeParser
    |
    v
ResumeBuilder
    |
    v
Resume
    |
    +----------------------------+
    |                            |
    v                            v
Structural Resume          Knowledge V5
                           |
                           +--> tokenization
                           +--> normalization
                           +--> matching
                           +--> confidence
                           +--> overlap resolution
                           +--> ranking
                           +--> ontology entities


IMPORTANT ARCHITECTURAL PRINCIPLE
----------------------------------

ResumeBuilder is a STRUCTURAL boundary.

ResumeBuilder is responsible for:

    ResumeSection
        |
        v
    structural normalization
        |
        v
    typed Resume
       
ResumeBuilder is NOT responsible for:

    ontology matching
    skill extraction
    certification ontology matching
    standards ontology matching
    action ontology matching
    target ontology matching
    domain ontology matching
    metric ontology matching
    ranking ontology entities
    overlap resolution
    knowledge reasoning

Those responsibilities belong to Knowledge V5.

The builder must preserve parser structure whenever specialized
extractors need ResumeSection / ResumeBlock metadata.

"""

from __future__ import annotations

import re
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
    Enterprise V5 Universal Resume Builder.

    Responsibilities
    ----------------

    1. Preserve parser -> builder traceability.
    2. Normalize ResumeSection content safely.
    3. Populate personal/contact information.
    4. Preserve ResumeSection objects for specialized extractors.
    5. Populate experience and education structurally.
    6. Populate languages/projects/awards/references.
    7. Preserve raw blocks.
    8. Preserve original parser sections.
    9. Keep ontology extraction outside ResumeBuilder.
    10. Provide a stable structural boundary before Knowledge V5.

    IMPORTANT
    ---------

    Skills and certifications are intentionally NOT populated
    by ontology matching here.

    They remain available through the parser sections and raw
    text so KnowledgeV5Pipeline can process them.

    This keeps:

        ResumeBuilder
            =
        structural parsing

    separate from:

        KnowledgeV5Pipeline
            =
        semantic / ontology knowledge extraction
    """

    # ============================================================
    # UNIVERSAL PATTERNS
    # ============================================================

    _YEAR_RE = re.compile(
        r"\b(?:19|20)\d{2}\b"
    )

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
            \d{1,2}/(?:19|20)\d{2}
            |
            [A-Za-z]{3,9}\s+(?:19|20)\d{2}
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ------------------------------------------------------------
    # Safe contact patterns
    #
    # These are deliberately simple and syntactically conservative.
    # Do not use a giant phone regex.
    # ------------------------------------------------------------

    _EMAIL_RE = re.compile(
        r"""
        (?<![\w.+-])
        [A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+
        @
        [A-Za-z0-9-]+
        (?:\.[A-Za-z0-9-]+)+
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _PHONE_RE = re.compile(
        r"""
        (?<!\d)
        (?:\+?\d[\d\s().-]{6,}\d)
        (?!\d)
        """,
        re.VERBOSE,
    )

    _LINKEDIN_RE = re.compile(
        r"""
        (?:
            https?://
        )?
        (?:
            www\.
        )?
        linkedin\.com/in/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _GITHUB_RE = re.compile(
        r"""
        (?:
            https?://
        )?
        (?:
            www\.
        )?
        github\.com/[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _LOCATION_LABEL_RE = re.compile(
        r"""
        \b
        (?:location|address)
        \s*[:\-]\s*
        ([^|\n]+)
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ------------------------------------------------------------
    # Generic heading detection.
    # ------------------------------------------------------------

    _HEADING_RE = re.compile(
        r"""
        ^\s*
        (?:
            summary
            |
            profile
            |
            professional\s+summary
            |
            objective
            |
            skills?
            |
            core\s+skills?
            |
            core\s+leadership\s+competencies
            |
            professional\s+experience
            |
            work\s+experience
            |
            experience
            |
            education
            |
            certifications?
            |
            professional\s+certifications?
            |
            languages?
            |
            projects?
            |
            awards?
            |
            references?
            |
            technology
            |
            technologies
        )
        \s*
        $
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self):

        # --------------------------------------------------------
        # UNIVERSAL NORMALIZER
        # --------------------------------------------------------

        self.normalizer = UniversalResumeNormalizer()

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
    # BASIC BLOCK TEXT
    # ============================================================

    @staticmethod
    def _block_text(
        block: Any,
    ) -> str:
        """
        Safely convert a ResumeBlock-compatible object to text.
        """

        if block is None:
            return ""

        if isinstance(block, str):
            return block.strip()

        if hasattr(block, "text"):

            value = getattr(
                block,
                "text",
                "",
            )

            if value is None:
                return ""

            return str(value).strip()

        return str(block).strip()

    # ============================================================
    # TEXT CLEANING
    # ============================================================

    @classmethod
    def _clean_text(
        cls,
        text: Any,
    ) -> str:
        """
        Safe structural text cleanup.

        Does NOT perform semantic rewriting.
        """

        if text is None:
            return ""

        text = str(text)

        # Non-breaking spaces.
        text = text.replace(
            "\xa0",
            " ",
        )

        # Tabs.
        text = text.replace(
            "\t",
            " ",
        )

        # Windows / old Mac line endings.
        text = text.replace(
            "\r\n",
            "\n",
        )

        text = text.replace(
            "\r",
            "\n",
        )

        # Collapse spaces without destroying line boundaries.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Remove spaces around line breaks.
        text = re.sub(
            r"[ \t]*\n[ \t]*",
            "\n",
            text,
        )

        return text.strip()

    # ============================================================
    # SECTION ITEMS
    # ============================================================

    @classmethod
    def _section_items(
        cls,
        section: Any,
    ) -> list[str]:
        """
        Convert a ResumeSection / list / tuple / block into text.

        IMPORTANT:

        This method is used only for flat structural normalization.

        Specialized extractors receive the ORIGINAL ResumeSection.
        """

        if section is None:
            return []

        # --------------------------------------------------------
        # ResumeSection
        # --------------------------------------------------------

        if hasattr(
            section,
            "items",
        ):

            items = getattr(
                section,
                "items",
                None,
            )

            if not items:
                return []

            result: list[str] = []

            for item in items:

                text = cls._clean_text(
                    cls._block_text(item)
                )

                if text:
                    result.append(text)

            return result

        # --------------------------------------------------------
        # list / tuple
        # --------------------------------------------------------

        if isinstance(
            section,
            (list, tuple),
        ):

            result: list[str] = []

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

        if hasattr(
            section,
            "text",
        ):

            text = cls._clean_text(
                cls._block_text(section)
            )

            return (
                [text]
                if text
                else []
            )

        # --------------------------------------------------------
        # Single string
        # --------------------------------------------------------

        if isinstance(
            section,
            str,
        ):

            text = cls._clean_text(
                section
            )

            return (
                [text]
                if text
                else []
            )

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
        Normalize parser sections into flat text collections.

        The ORIGINAL sections remain untouched and are preserved
        separately on the Resume object.
        """

        if sections is None:
            return {}

        if not isinstance(
            sections,
            dict,
        ):
            raise TypeError(
                "ResumeBuilder expected sections to be dict, "
                f"received {type(sections).__name__}"
            )

        normalized: dict[str, list[str]] = {}

        for section_name, section in sections.items():

            key = str(
                section_name
            ).strip().lower()

            normalized[key] = (
                cls._section_items(section)
            )

        return normalized

    # ============================================================
    # HEADING DETECTION
    # ============================================================

    @classmethod
    def _is_heading(
        cls,
        text: str,
    ) -> bool:

        if not text:
            return False

        clean = text.strip()

        return bool(
            cls._HEADING_RE.match(
                clean
            )
        )

    # ============================================================
    # HEADER NORMALIZATION
    # ============================================================

    @classmethod
    def _normalize_header(
        cls,
        header: list[str],
    ) -> list[str]:
        """
        Normalize header content while preserving embedded lines.

        A single ResumeBlock can contain:

            Phone...
            LinkedIn...

        so embedded newline characters are expanded into
        independent header lines.
        """

        if not header:
            return []

        result: list[str] = []

        for item in header:

            clean = cls._clean_text(
                item
            )

            if not clean:
                continue

            # ----------------------------------------------------
            # Split embedded lines.
            # ----------------------------------------------------

            for line in clean.split("\n"):

                line = line.strip()

                if line:
                    result.append(line)

        return result

    # ============================================================
    # SUMMARY
    # ============================================================

    @classmethod
    def _normalize_summary(
        cls,
        summary: list[str],
    ) -> str:

        if not summary:
            return ""

        parts: list[str] = []

        for item in summary:

            text = cls._clean_text(
                item
            )

            if text:
                parts.append(text)

        return " ".join(
            parts
        ).strip()

    # ============================================================
    # GENERIC SECTION
    # ============================================================

    @classmethod
    def _normalize_generic_lines(
        cls,
        lines: list[str],
    ) -> list[str]:

        result: list[str] = []

        for line in lines:

            text = cls._clean_text(
                line
            )

            if text:
                result.append(text)

        return result

    # ============================================================
    # EXTRACTOR INPUT
    # ============================================================

    @classmethod
    def _prepare_extractor_input(
        cls,
        normalized: dict[str, list[str]],
    ) -> dict[str, list[str]]:
        """
        Prepare flat inputs for extractors.

        Specialized education and experience extraction DOES NOT
        use these flat values. It uses the original ResumeSection
        objects in build().

        This prevents loss of ResumeBlock metadata.
        """

        prepared: dict[str, list[str]] = {}

        for key, lines in normalized.items():

            prepared[key] = (
                cls._normalize_generic_lines(
                    lines
                )
            )

        return prepared

    # ============================================================
    # CONTACT EXTRACTION
    # ============================================================

    @classmethod
    def _extract_contact(
        cls,
        header: list[str],
    ) -> dict[str, str]:
        """
        Robust contact extraction.

        This is intentionally performed at the structural boundary
        because the parser may provide contact information inside
        one or more ResumeBlocks.

        Example input:

            Phone: +923334940827 | Email: muhkashiff@gmail.com
            | Location: Lahore, Punjab, Pakistan
            LinkedIn: linkedin.com/in/muhkashiff |
            GitHub: github.com/muhkashiff
        """

        result = {
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "location": "",
        }

        if not header:
            return result

        # --------------------------------------------------------
        # Join header lines for contact scanning.
        # --------------------------------------------------------

        text = "\n".join(
            line
            for line in header
            if line
        )

        # --------------------------------------------------------
        # EMAIL
        # --------------------------------------------------------

        email_match = cls._EMAIL_RE.search(
            text
        )

        if email_match:
            result["email"] = (
                email_match.group(0)
                .strip()
                .rstrip(".,;")
            )

        # --------------------------------------------------------
        # PHONE
        # --------------------------------------------------------

        phone_match = cls._PHONE_RE.search(
            text
        )

        if phone_match:

            phone = (
                phone_match.group(0)
                .strip()
            )

            # Remove accidental trailing punctuation.
            phone = phone.rstrip(
                ".,;|"
            )

            result["phone"] = phone

        # --------------------------------------------------------
        # LINKEDIN
        # --------------------------------------------------------

        linkedin_match = (
            cls._LINKEDIN_RE.search(
                text
            )
        )

        if linkedin_match:

            result["linkedin"] = (
                linkedin_match.group(0)
                .strip()
                .rstrip(".,;|")
            )

        # --------------------------------------------------------
        # GITHUB
        # --------------------------------------------------------

        github_match = (
            cls._GITHUB_RE.search(
                text
            )
        )

        if github_match:

            result["github"] = (
                github_match.group(0)
                .strip()
                .rstrip(".,;|")
            )

        # --------------------------------------------------------
        # LOCATION
        # --------------------------------------------------------

        location_match = (
            cls._LOCATION_LABEL_RE.search(
                text
            )
        )

        if location_match:

            location = (
                location_match.group(1)
                .strip()
                .rstrip(".,;|")
            )

            result["location"] = location

        # --------------------------------------------------------
        # Fallback location extraction
        #
        # If Location: was not detected, inspect the header lines.
        # --------------------------------------------------------

        if not result["location"]:

            for line in header:

                clean = line.strip()

                if (
                    "location:" in clean.lower()
                ):

                    parts = re.split(
                        r"location\s*:\s*",
                        clean,
                        maxsplit=1,
                        flags=re.IGNORECASE,
                    )

                    if len(parts) == 2:

                        location = (
                            parts[1]
                            .split("|")[0]
                            .strip()
                            .rstrip(".,;")
                        )

                        if location:
                            result["location"] = (
                                location
                            )

                        break

        return result

    # ============================================================
    # SAFE EXTRACTOR
    # ============================================================

    @staticmethod
    def _safe_extract(
        extractor: Any,
        lines: Any,
        default: Any,
    ) -> Any:
        """
        Safely call a legacy/simple extractor.

        This method is intended for flat text extractors only.

        Education and experience use ResumeSectionAdapter.
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
                "processing resume section."
            ) from exc

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
        Build strongly typed Resume.

        Parameters
        ----------

        sections:
            Exact output of ResumeParser.parse(file_path).

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
        # 1. VALIDATE INPUT
        # ========================================================

        if sections is None:
            sections = {}

        if not isinstance(
            sections,
            dict,
        ):
            raise TypeError(
                "ResumeBuilder.build expected parser sections "
                "as dict, received "
                f"{type(sections).__name__}"
            )

        # ========================================================
        # 2. FLAT NORMALIZATION
        # ========================================================

        normalized = (
            self._normalize_sections(
                sections
            )
        )

        prepared = (
            self._prepare_extractor_input(
                normalized
            )
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

        # ========================================================
        # 5. RAW BLOCK TRACEABILITY
        # ========================================================

        if raw_blocks is not None:

            resume.raw_blocks = list(
                raw_blocks
            )

        # ========================================================
        # 6. ORIGINAL SECTION TRACEABILITY
        # ========================================================

        resume.sections = dict(
            sections
        )

        # ========================================================
        # 7. PERSONAL INFORMATION
        # ========================================================

        header = self._normalize_header(
            normalized.get(
                "header",
                [],
            )
        )

        # --------------------------------------------------------
        # NAME
        # --------------------------------------------------------

        if header:

            resume.personal_information.name = (
                header[0].strip()
            )

        # --------------------------------------------------------
        # CONTACT
        #
        # IMPORTANT:
        #
        # Do NOT depend exclusively on ContactExtractor here.
        #
        # The current parser can place multiple contact fields
        # inside one ResumeBlock.
        # --------------------------------------------------------

        contact = self._extract_contact(
            header
        )

        # --------------------------------------------------------
        # Optional ContactExtractor enrichment
        #
        # We try it, but do not allow an empty/malformed result
        # to erase the robust structural extraction above.
        # --------------------------------------------------------

        try:

            extracted_contact = (
                self.contact_extractor.extract(
                    header
                )
            )

            if isinstance(
                extracted_contact,
                dict,
            ):

                for key in (
                    "email",
                    "phone",
                    "linkedin",
                    "github",
                    "location",
                ):

                    value = (
                        extracted_contact.get(
                            key,
                            "",
                        )
                    )

                    if value:

                        contact[key] = (
                            str(value).strip()
                        )

        except Exception:
            # Contact extraction is optional because the builder
            # already performed robust structural extraction.
            pass

        # --------------------------------------------------------
        # Assign personal information.
        # --------------------------------------------------------

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
        # 8. SUMMARY
        # ========================================================

        resume.summary = (
            self._normalize_summary(
                normalized.get(
                    "summary",
                    [],
                )
            )
        )

        # ========================================================
        # 9. EXPERIENCE
        # ========================================================

        experience_section = (
            sections.get(
                "experience"
            )
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
        # 10. EDUCATION
        # ========================================================

        education_section = (
            sections.get(
                "education"
            )
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
        # 11. PROJECTS
        # ========================================================

        project_lines = prepared.get(
            "projects",
            [],
        )

        if project_lines:

            resume.projects = (
                self._safe_extract(
                    self.project_extractor,
                    project_lines,
                    [],
                )
            )

        else:

            resume.projects = []

        # ========================================================
        # 12. AWARDS
        # ========================================================

        award_lines = prepared.get(
            "awards",
            [],
        )

        if award_lines:

            resume.awards = (
                self._safe_extract(
                    self.award_extractor,
                    award_lines,
                    [],
                )
            )

        else:

            resume.awards = []

        # ========================================================
        # 13. LANGUAGES
        # ========================================================

        language_lines = prepared.get(
            "languages",
            [],
        )

        if language_lines:

            resume.languages = (
                self._safe_extract(
                    self.language_extractor,
                    language_lines,
                    [],
                )
            )

        else:

            resume.languages = []

        # ========================================================
        # 14. REFERENCES
        # ========================================================

        reference_lines = prepared.get(
            "references",
            [],
        )

        if reference_lines:

            resume.references = (
                self._safe_extract(
                    self.reference_extractor,
                    reference_lines,
                    [],
                )
            )

        else:

            resume.references = []

        # --------------------------------------------------------
        # Default reference fallback.
        # --------------------------------------------------------

        if not resume.references:

            resume.references = [
                Reference(
                    available_on_request=True
                )
            ]

        # ========================================================
        # 15. KNOWLEDGE V5 BOUNDARY
        # ========================================================

        # --------------------------------------------------------
        # IMPORTANT
        #
        # Do NOT populate:
        #
        #     resume.skills
        #     resume.certifications
        #
        # through ontology extraction here.
        #
        # KnowledgeV5Pipeline is responsible for:
        #
        #     tokenization
        #     normalization
        #     matching
        #     confidence
        #     overlap resolution
        #     ranking
        #     ontology entity extraction
        #
        # Therefore skills/certifications remain available in:
        #
        #     resume.sections["skills"]
        #     resume.sections["certifications"]
        #
        # and in raw blocks/full resume text.
        #
        # This is intentional.
        # --------------------------------------------------------

        # ========================================================
        # 16. BUILDER METADATA
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

        resume.metadata[
            "knowledge_boundary"
        ] = "KnowledgeV5Pipeline"

        resume.metadata[
            "ontology_extraction"
        ] = "deferred_to_knowledge_v5"

        # --------------------------------------------------------
        # Original section counts.
        # --------------------------------------------------------

        resume.metadata[
            "original_section_counts"
        ] = {
            key: len(value)
            for key, value in normalized.items()
        }

        # --------------------------------------------------------
        # Prepared section counts.
        # --------------------------------------------------------

        resume.metadata[
            "prepared_section_counts"
        ] = {
            key: len(value)
            for key, value in prepared.items()
        }

        # --------------------------------------------------------
        # Raw block count.
        # --------------------------------------------------------

        resume.metadata[
            "raw_block_count"
        ] = (
            len(raw_blocks)
            if raw_blocks is not None
            else 0
        )

        # --------------------------------------------------------
        # Raw section count.
        # --------------------------------------------------------

        resume.metadata[
            "raw_section_count"
        ] = len(
            sections
        )

        # --------------------------------------------------------
        # Structural content diagnostics.
        # --------------------------------------------------------

        resume.metadata[
            "contact_extraction"
        ] = {
            "name": bool(
                resume.personal_information.name
            ),
            "email": bool(
                resume.personal_information.email
            ),
            "phone": bool(
                resume.personal_information.phone
            ),
            "linkedin": bool(
                resume.personal_information.linkedin
            ),
            "github": bool(
                resume.personal_information.github
            ),
            "address": bool(
                resume.personal_information.address
            ),
        }

        # ========================================================
        # 17. RETURN
        # ========================================================

        return resume