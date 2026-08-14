"""
Enterprise V5 — Universal Resume Normalizer
============================================

Purpose
-------
Convert heterogeneous ResumeBlock / ResumeSection structures into
stable, layout-independent resume records.

This layer is deliberately independent of:
    - a particular DOCX template
    - paragraph indexes
    - table indexes
    - cell positions
    - exact spacing
    - exact date formatting
    - exact section heading wording

Architecture
------------

DOCX
  ↓
ResumeReader
  ↓
ResumeBlock[]
  ↓
SectionDetector
  ↓
ResumeSection[]
  ↓
UniversalResumeNormalizer
  ↓
NormalizedResume
  ↓
ResumeBuilder
  ↓
Resume
  ↓
Intelligence / Ontology / JD Matching

Important
---------
This module NEVER invents resume content.

It only:
    - normalizes whitespace
    - identifies section boundaries
    - identifies record boundaries
    - parses dates
    - separates fields when evidence exists
    - attaches continuation paragraphs to the current record
    - preserves raw source material
"""


from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from datetime import date
import re
import unicodedata
from typing import Any, Iterable, Optional, Sequence


# =====================================================================
# NORMALIZED DOMAIN OBJECTS
# =====================================================================


@dataclass
class NormalizedExperience:
    title: str = ""
    company: str = ""
    location: str = ""

    start_date: str = ""
    end_date: str = ""

    responsibilities: list[str] = dc_field(default_factory=list)
    achievements: list[str] = dc_field(default_factory=list)

    raw_header: str = ""
    raw_content: list[str] = dc_field(default_factory=list)

    source_indexes: list[int] = dc_field(default_factory=list)


@dataclass
class NormalizedEducation:
    degree: str = ""
    institution: str = ""
    location: str = ""
    field: str = ""

    description: list[str] = dc_field(default_factory=list)

    raw_header: str = ""
    raw_content: list[str] = dc_field(default_factory=list)

    source_indexes: list[int] = dc_field(default_factory=list)


@dataclass
class NormalizedCertification:
    name: str = ""
    issuer: str = ""
    year: str = ""

    raw: str = ""
    source_index: int = -1


@dataclass
class NormalizedLanguage:
    language: str = ""
    proficiency: str = ""
    raw: str = ""
    source_index: int = -1


@dataclass
class NormalizedResume:
    name: str = ""

    email: str = ""
    phone: str = ""

    linkedin: str = ""
    github: str = ""

    address: str = ""

    headline: str = ""
    summary: str = ""

    skills: list[str] = dc_field(default_factory=list)

    experience: list[NormalizedExperience] = dc_field(
        default_factory=list
    )

    education: list[NormalizedEducation] = dc_field(
        default_factory=list
    )

    certifications: list[NormalizedCertification] = dc_field(
        default_factory=list
    )

    projects: list[str] = dc_field(
        default_factory=list
    )

    awards: list[str] = dc_field(
        default_factory=list
    )

    languages: list[NormalizedLanguage] = dc_field(
        default_factory=list
    )

    raw_blocks: list[Any] = dc_field(
        default_factory=list
    )

    section_blocks: dict[str, list[Any]] = dc_field(
        default_factory=dict
    )

    diagnostics: dict[str, Any] = dc_field(
        default_factory=dict
    )


# =====================================================================
# UNIVERSAL NORMALIZER
# =====================================================================


class UniversalResumeNormalizer:
    """
    Universal structural normalizer.

    Designed to work with existing ResumeBlock objects without
    requiring the exact ResumeBlock implementation.
    """

    # -----------------------------------------------------------------
    # SECTION ALIASES
    # -----------------------------------------------------------------

    SECTION_ALIASES = {
        "summary": {
            "summary",
            "professional summary",
            "executive summary",
            "profile",
            "professional profile",
            "career profile",
            "objective",
            "career objective",
            "professional objective",
            "about me",
            "executive profile",
        },

        "skills": {
            "skills",
            "technical skills",
            "core skills",
            "key skills",
            "professional skills",
            "competencies",
            "core competencies",
            "core leadership competencies",
            "leadership competencies",
            "areas of expertise",
            "expertise",
            "technical expertise",
            "key competencies",
            "skills & competencies",
            "skills and competencies",
        },

        "experience": {
            "experience",
            "work experience",
            "professional experience",
            "employment",
            "employment history",
            "career history",
            "work history",
            "professional history",
            "career experience",
        },

        "education": {
            "education",
            "academic background",
            "academic history",
            "educational background",
            "education & training",
            "education and training",
            "academic qualifications",
            "qualifications",
        },

        "certifications": {
            "certifications",
            "certification",
            "professional certifications",
            "professional certification",
            "certifications & accreditations",
            "professional certifications & accreditations",
            "licenses & certifications",
            "licenses and certifications",
            "credentials",
            "professional credentials",
        },

        "projects": {
            "projects",
            "key projects",
            "selected projects",
            "professional projects",
            "technology projects",
            "technical projects",
            "data analytics projects",
            "data analytics & machine learning projects",
            "portfolio",
            "selected portfolio",
        },

        "awards": {
            "awards",
            "honors",
            "honours",
            "achievements",
            "recognition",
            "awards & honors",
            "awards and honors",
        },

        "languages": {
            "languages",
            "language",
            "language skills",
            "languages spoken",
        },

        "references": {
            "references",
            "professional references",
            "referees",
        },
    }

    # -----------------------------------------------------------------
    # GENERIC HEADING WORDS
    # -----------------------------------------------------------------

    HEADING_WORDS = {
        "summary",
        "profile",
        "objective",
        "skills",
        "competencies",
        "experience",
        "employment",
        "education",
        "certifications",
        "certification",
        "projects",
        "portfolio",
        "awards",
        "honors",
        "languages",
        "references",
    }

    # -----------------------------------------------------------------
    # DEGREE SIGNALS
    # -----------------------------------------------------------------

    DEGREE_PATTERNS = [
        r"\bph\.?d\.?\b",
        r"\bdoctor(?:ate)?\b",
        r"\bm\.?sc\.?\b",
        r"\bm\.?s\.?\b",
        r"\bm\.?a\.?\b",
        r"\bm\.?ba\b",
        r"\bm\.?eng\b",
        r"\bm\.?phil\b",
        r"\bmba\b",
        r"\bmaster(?:'s)?\b",
        r"\bb\.?sc\.?\b",
        r"\bb\.?a\.?\b",
        r"\bb\.?ba\b",
        r"\bb\.?eng\b",
        r"\bbs\b",
        r"\bbachelor(?:'s)?\b",
        r"\bassociate(?:'s)?\b",
        r"\bcollege diploma\b",
        r"\bdiploma\b",
        r"\bpost[- ]?graduate diploma\b",
        r"\bpost[- ]?graduation diploma\b",
        r"\bcertificate\b",
        r"\bcertification\b",
        r"\bboot ?camp\b",
        r"\bhigh school\b",
        r"\bsecondary school\b",
    ]

    # -----------------------------------------------------------------
    # INSTITUTION SIGNALS
    # -----------------------------------------------------------------

    INSTITUTION_TERMS = {
        "university",
        "college",
        "institute",
        "school",
        "academy",
        "polytechnic",
        "conservatory",
    }

    # -----------------------------------------------------------------
    # EXPERIENCE TITLE SIGNALS
    # -----------------------------------------------------------------

    TITLE_TERMS = {
        "manager",
        "director",
        "president",
        "vice president",
        "vp",
        "chief",
        "officer",
        "engineer",
        "chemist",
        "analyst",
        "specialist",
        "supervisor",
        "coordinator",
        "administrator",
        "consultant",
        "developer",
        "designer",
        "technician",
        "scientist",
        "lead",
        "head",
        "executive",
        "associate",
        "assistant",
        "operator",
        "accountant",
        "buyer",
        "planner",
        "auditor",
        "quality assurance",
        "quality control",
    }

    # -----------------------------------------------------------------
    # MONTHS
    # -----------------------------------------------------------------

    MONTH_PATTERN = (
        r"(?:"
        r"jan(?:uary)?|"
        r"feb(?:ruary)?|"
        r"mar(?:ch)?|"
        r"apr(?:il)?|"
        r"may|"
        r"jun(?:e)?|"
        r"jul(?:y)?|"
        r"aug(?:ust)?|"
        r"sep(?:t(?:ember)?)?|"
        r"oct(?:ober)?|"
        r"nov(?:ember)?|"
        r"dec(?:ember)?"
        r")"
    )

    DATE_TOKEN = (
        rf"(?:"
        rf"{MONTH_PATTERN}\s+\d{{4}}|"
        rf"\d{{1,2}}\s+{MONTH_PATTERN}\s+\d{{4}}|"
        rf"\d{{4}}"
        rf")"
    )

    DATE_RANGE_PATTERN = re.compile(
        rf"(?P<start>{DATE_TOKEN})"
        rf"\s*(?:-|–|—|to|until|through)\s*"
        rf"(?P<end>{DATE_TOKEN}|present|current|now)",
        re.IGNORECASE,
    )

    SINGLE_DATE_PATTERN = re.compile(
        rf"\b{DATE_TOKEN}\b",
        re.IGNORECASE,
    )

    YEAR_RANGE_PATTERN = re.compile(
        r"\b(?P<start>19\d{2}|20\d{2})"
        r"\s*(?:-|–|—|to|until|through)"
        r"\s*(?P<end>19\d{2}|20\d{2}|present|current|now)\b",
        re.IGNORECASE,
    )

    # -----------------------------------------------------------------
    # EMAIL / PHONE / SOCIAL
    # -----------------------------------------------------------------

    EMAIL_PATTERN = re.compile(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        re.IGNORECASE,
    )

    PHONE_PATTERN = re.compile(
        r"(?<!\d)"
        r"(?:\+?\d[\d\s().\-]{7,}\d)"
        r"(?!\d)"
    )

    LINKEDIN_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"linkedin\.com/[^\s|,;]+",
        re.IGNORECASE,
    )

    GITHUB_PATTERN = re.compile(
        r"(?:https?://)?(?:www\.)?"
        r"github\.com/[^\s|,;]+",
        re.IGNORECASE,
    )

    # -----------------------------------------------------------------
    # BULLET / LABEL CLEANING
    # -----------------------------------------------------------------

    BULLET_CHARS = (
        "•",
        "",
        "▪",
        "‣",
        "◦",
        "●",
        "○",
        "■",
        "□",
        "➢",
        "➤",
        "–",
        "-",
        "*",
    )

    ACHIEVEMENT_LABELS = {
        "key accomplishments",
        "key achievements",
        "selected achievements",
        "major achievements",
        "achievements",
        "accomplishments",
        "highlights",
        "key results",
        "results",
    }

    # =================================================================
    # PUBLIC API
    # =================================================================

    def normalize(
        self,
        blocks: Sequence[Any],
    ) -> NormalizedResume:

        blocks = list(blocks)

        result = NormalizedResume(
            raw_blocks=blocks
        )

        # -------------------------------------------------------------
        # 1. CLEAN BLOCKS
        # -------------------------------------------------------------

        cleaned = [
            self._clean_block(block)
            for block in blocks
        ]

        # -------------------------------------------------------------
        # 2. REBUILD SECTIONS FROM RAW TEXT + STRUCTURE
        # -------------------------------------------------------------

        sections = self._detect_sections(
            cleaned
        )

        result.section_blocks = sections

        # -------------------------------------------------------------
        # 3. CONTACT / HEADER
        # -------------------------------------------------------------

        self._extract_header(
            cleaned,
            result,
        )

        # -------------------------------------------------------------
        # 4. SUMMARY
        # -------------------------------------------------------------

        result.summary = self._extract_summary(
            sections.get("summary", [])
        )

        # -------------------------------------------------------------
        # 5. SKILLS
        # -------------------------------------------------------------

        result.skills = self._extract_skills(
            sections.get("skills", [])
        )

        # -------------------------------------------------------------
        # 6. EXPERIENCE
        # -------------------------------------------------------------

        result.experience = (
            self._extract_experience(
                sections.get("experience", [])
            )
        )

        # -------------------------------------------------------------
        # 7. EDUCATION
        # -------------------------------------------------------------

        result.education = (
            self._extract_education(
                sections.get("education", [])
            )
        )

        # -------------------------------------------------------------
        # 8. CERTIFICATIONS
        # -------------------------------------------------------------

        result.certifications = (
            self._extract_certifications(
                sections.get("certifications", [])
            )
        )

        # -------------------------------------------------------------
        # 9. PROJECTS
        # -------------------------------------------------------------

        result.projects = (
            self._extract_simple_records(
                sections.get("projects", [])
            )
        )

        # -------------------------------------------------------------
        # 10. AWARDS
        # -------------------------------------------------------------

        result.awards = (
            self._extract_simple_records(
                sections.get("awards", [])
            )
        )

        # -------------------------------------------------------------
        # 11. LANGUAGES
        # -------------------------------------------------------------

        result.languages = (
            self._extract_languages(
                sections.get("languages", [])
            )
        )

        # -------------------------------------------------------------
        # 12. DIAGNOSTICS
        # -------------------------------------------------------------

        result.diagnostics = (
            self._diagnostics(result)
        )

        return result

    # =================================================================
    # TEXT NORMALIZATION
    # =================================================================

    def _clean_text(
        self,
        value: Any,
    ) -> str:

        if value is None:
            return ""

        text = str(value)

        text = unicodedata.normalize(
            "NFKC",
            text,
        )

        text = (
            text.replace("\u00a0", " ")
                .replace("\u200b", "")
                .replace("\ufeff", "")
                .replace("\r\n", "\n")
                .replace("\r", "\n")
        )

        # Replace tabs with spaces.
        text = re.sub(
            r"\t+",
            "    ",
            text,
        )

        # Collapse excessive spaces but preserve newlines.
        text = re.sub(
            r"[ ]{2,}",
            " ",
            text,
        )

        return text.strip()

    def _clean_block(
        self,
        block: Any,
    ) -> dict[str, Any]:

        if isinstance(block, dict):
            text = block.get(
                "text",
                block.get("value", ""),
            )

            index = block.get(
                "index",
                -1,
            )

            block_type = block.get(
                "block_type",
                "",
            )

            table_index = block.get(
                "table_index",
                -1,
            )

            row_index = block.get(
                "row_index",
                -1,
            )

            cell_index = block.get(
                "cell_index",
                -1,
            )

            section = block.get(
                "section",
                "",
            )

        else:
            text = getattr(
                block,
                "text",
                "",
            )

            index = getattr(
                block,
                "index",
                -1,
            )

            block_type = getattr(
                block,
                "block_type",
                "",
            )

            table_index = getattr(
                block,
                "table_index",
                -1,
            )

            row_index = getattr(
                block,
                "row_index",
                -1,
            )

            cell_index = getattr(
                block,
                "cell_index",
                -1,
            )

            section = getattr(
                block,
                "section",
                "",
            )

        text = self._clean_text(text)

        return {
            "object": block,
            "index": index,
            "text": text,
            "block_type": block_type,
            "table_index": table_index,
            "row_index": row_index,
            "cell_index": cell_index,
            "section": self._normalize_section_name(
                section
            ),
        }

    # =================================================================
    # SECTION DETECTION
    # =================================================================

    def _detect_sections(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> dict[str, list[Any]]:

        sections: dict[str, list[Any]] = {
            key: []
            for key in self.SECTION_ALIASES
        }

        current = "header"

        for item in blocks:

            text = item["text"]

            if not text:
                continue

            detected = self._section_from_heading(
                text
            )

            if detected:
                current = detected
                continue

            if current == "header":
                # Header material before the first known section.
                continue

            sections.setdefault(
                current,
                []
            ).append(item)

        # -------------------------------------------------------------
        # FALLBACK RECLASSIFICATION
        #
        # Some DOCX files put competencies/certifications in tables
        # where the detector does not assign a useful section.
        # -------------------------------------------------------------

        if not sections["skills"]:
            sections["skills"] = self._infer_skills(
                blocks
            )

        if not sections["certifications"]:
            sections["certifications"] = (
                self._infer_certifications(
                    blocks
                )
            )

        return sections

    def _section_from_heading(
        self,
        text: str,
    ) -> Optional[str]:

        normalized = self._normalize_heading(
            text
        )

        if not normalized:
            return None

        for section, aliases in self.SECTION_ALIASES.items():

            if normalized in aliases:
                return section

        # Remove punctuation and retry.
        simplified = re.sub(
            r"[^a-z0-9& ]",
            "",
            normalized,
        )

        for section, aliases in self.SECTION_ALIASES.items():

            for alias in aliases:

                alias_simple = re.sub(
                    r"[^a-z0-9& ]",
                    "",
                    alias,
                )

                if simplified == alias_simple:
                    return section

        return None

    def _normalize_heading(
        self,
        text: str,
    ) -> str:

        text = self._clean_text(
            text
        ).lower()

        text = text.strip(
            " :|-–—"
        )

        return text

    def _normalize_section_name(
        self,
        value: str,
    ) -> str:

        normalized = self._normalize_heading(
            value
        )

        detected = self._section_from_heading(
            normalized
        )

        return detected or normalized

    # =================================================================
    # HEADER
    # =================================================================

    def _extract_header(
        self,
        blocks: Sequence[dict[str, Any]],
        result: NormalizedResume,
    ) -> None:

        header_candidates = []

        for item in blocks:

            text = item["text"]

            if not text:
                continue

            if self._section_from_heading(text):
                break

            header_candidates.append(
                text
            )

        if not header_candidates:
            return

        # -------------------------------------------------------------
        # NAME
        # -------------------------------------------------------------

        for text in header_candidates:

            if self._looks_like_name(text):

                result.name = (
                    self._clean_name(text)
                )

                break

        # -------------------------------------------------------------
        # HEADLINE
        # -------------------------------------------------------------

        for text in header_candidates:

            if text == result.name:
                continue

            if self.EMAIL_PATTERN.search(text):
                continue

            if self.PHONE_PATTERN.search(text):
                continue

            if self.LINKEDIN_PATTERN.search(text):
                continue

            if self.GITHUB_PATTERN.search(text):
                continue

            if self._looks_like_heading(text):
                continue

            if len(text) < 150:

                result.headline = text

                break

        # -------------------------------------------------------------
        # CONTACT FIELDS
        # -------------------------------------------------------------

        all_header = " | ".join(
            header_candidates
        )

        email = self.EMAIL_PATTERN.search(
            all_header
        )

        if email:
            result.email = email.group(0)

        phone = self.PHONE_PATTERN.search(
            all_header
        )

        if phone:
            result.phone = self._clean_phone(
                phone.group(0)
            )

        linkedin = self.LINKEDIN_PATTERN.search(
            all_header
        )

        if linkedin:
            result.linkedin = (
                linkedin.group(0)
            )

        github = self.GITHUB_PATTERN.search(
            all_header
        )

        if github:
            result.github = (
                github.group(0)
            )

        result.address = self._extract_address(
            header_candidates
        )

    def _looks_like_name(
        self,
        text: str,
    ) -> bool:

        if not text:
            return False

        if len(text) > 80:
            return False

        if self.EMAIL_PATTERN.search(text):
            return False

        if self.PHONE_PATTERN.search(text):
            return False

        words = re.findall(
            r"[A-Za-zÀ-ÿ'-]+",
            text,
        )

        if not 1 <= len(words) <= 5:
            return False

        uppercase_ratio = sum(
            1
            for c in text
            if c.isalpha() and c.isupper()
        ) / max(
            1,
            sum(
                1
                for c in text
                if c.isalpha()
            ),
        )

        return uppercase_ratio >= 0.65

    def _clean_name(
        self,
        text: str,
    ) -> str:

        return re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

    def _clean_phone(
        self,
        text: str,
    ) -> str:

        text = text.strip()

        return re.sub(
            r"\s+",
            " ",
            text,
        )

    def _extract_address(
        self,
        candidates: list[str],
    ) -> str:

        for text in candidates:

            if any(
                token in text.lower()
                for token in (
                    "location:",
                    "address:",
                    "based in",
                    "ontario",
                    "canada",
                    "pakistan",
                    "lahore",
                    "brampton",
                    "toronto",
                )
            ):

                # Remove known contact labels.
                value = re.sub(
                    r"\b(?:location|address)\s*:\s*",
                    "",
                    text,
                    flags=re.IGNORECASE,
                )

                # If line contains multiple contact fields,
                # keep only likely location portion.
                parts = re.split(
                    r"\s*\|\s*",
                    value,
                )

                for part in parts:

                    low = part.lower()

                    if (
                        "email" not in low
                        and "phone" not in low
                        and "linkedin" not in low
                        and "github" not in low
                        and (
                            "canada" in low
                            or "pakistan" in low
                            or "ontario" in low
                            or "lahore" in low
                            or "brampton" in low
                            or "toronto" in low
                        )
                    ):
                        return part.strip()

        return ""

    # =================================================================
    # SUMMARY
    # =================================================================

    def _extract_summary(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> str:

        return " ".join(
            item["text"]
            for item in blocks
            if item["text"]
        ).strip()

    # =================================================================
    # SKILLS
    # =================================================================

    def _extract_skills(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[str]:

        values = []

        for item in blocks:

            text = self._strip_bullet(
                item["text"]
            )

            if not text:
                continue

            # Ignore labels.
            if self._is_achievement_label(text):
                continue

            # Split pipe-separated skills.
            pieces = re.split(
                r"\s*\|\s*",
                text,
            )

            for piece in pieces:

                piece = self._clean_text(
                    piece
                )

                if not piece:
                    continue

                # Split semicolon-separated skills.
                if ";" in piece:
                    subparts = piece.split(";")
                else:
                    subparts = [piece]

                for subpart in subparts:

                    value = self._clean_text(
                        subpart
                    )

                    if value:
                        values.append(
                            value
                        )

        return self._dedupe(
            values
        )

    def _infer_skills(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        candidates = []

        for item in blocks:

            text = item["text"]

            if not text:
                continue

            if len(text) > 100:
                continue

            if self._looks_like_skill_line(
                text
            ):
                candidates.append(item)

        return candidates

    def _looks_like_skill_line(
        self,
        text: str,
    ) -> bool:

        if len(text) > 120:
            return False

        low = text.lower()

        skill_terms = (
            "python",
            "sql",
            "excel",
            "power bi",
            "tableau",
            "minitab",
            "machine learning",
            "data analytics",
            "quality",
            "food safety",
            "supply chain",
            "inventory",
            "procurement",
            "audit",
            "leadership",
            "management",
            "six sigma",
            "haccp",
            "fssc",
            "iso 9001",
            "capability",
            "control charts",
        )

        return any(
            term in low
            for term in skill_terms
        )

    # =================================================================
    # EXPERIENCE
    # =================================================================

    def _extract_experience(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[NormalizedExperience]:

        records: list[NormalizedExperience] = []

        current: Optional[
            NormalizedExperience
        ] = None

        achievement_mode = False

        for item in blocks:

            text = item["text"]

            if not text:
                continue

            clean = self._strip_bullet(
                text
            )

            # ---------------------------------------------------------
            # NEW EXPERIENCE HEADER
            # ---------------------------------------------------------

            parsed_header = (
                self._parse_experience_header(
                    clean
                )
            )

            if parsed_header is not None:

                if current is not None:
                    self._finalize_experience(
                        current
                    )
                    records.append(
                        current
                    )

                current = parsed_header
                current.source_indexes.append(
                    item["index"]
                )

                achievement_mode = False

                continue

            if current is None:
                continue

            # ---------------------------------------------------------
            # ACHIEVEMENT LABEL
            # ---------------------------------------------------------

            if self._is_achievement_label(
                clean
            ):

                achievement_mode = True
                continue

            # ---------------------------------------------------------
            # CONTENT
            # ---------------------------------------------------------

            current.source_indexes.append(
                item["index"]
            )

            current.raw_content.append(
                clean
            )

            if achievement_mode:
                current.achievements.append(
                    clean
                )
            else:
                current.responsibilities.append(
                    clean
                )

        if current is not None:
            self._finalize_experience(
                current
            )
            records.append(
                current
            )

        return records

    def _parse_experience_header(
        self,
        text: str,
    ) -> Optional[NormalizedExperience]:

        if not text:
            return None

        # Must have a date signal.
        date_match = (
            self.DATE_RANGE_PATTERN.search(text)
            or self.YEAR_RANGE_PATTERN.search(text)
        )

        if not date_match:
            return None

        # Do not classify ordinary achievement sentences
        # containing a year as employment headers.
        if self._looks_like_achievement_sentence(
            text
        ):
            return None

        start, end = self._extract_date_range(
            text
        )

        without_dates = self._remove_dates(
            text
        )

        # -------------------------------------------------------------
        # Normalize separators.
        # -------------------------------------------------------------

        parts = [
            self._clean_text(p)
            for p in re.split(
                r"\s*\|\s*",
                without_dates,
            )
            if self._clean_text(p)
        ]

        title = ""
        company = ""
        location = ""

        if len(parts) >= 3:

            # Common canonical format:
            #
            # title | company | location
            #
            # This is intentionally preferred.
            title = parts[0]
            company = parts[1]
            location = " | ".join(
                parts[2:]
            )

        elif len(parts) == 2:

            first = parts[0]
            second = parts[1]

            # Decide which is company/title using signals.
            if self._looks_like_title(first):

                title = first

                if self._looks_like_location(
                    second
                ):
                    location = second
                else:
                    company = second

            elif self._looks_like_title(second):

                company = first
                title = second

            else:

                title = first
                company = second

        elif len(parts) == 1:

            # Handle resumes where pipes are absent.
            title, company, location = (
                self._parse_unstructured_experience_header(
                    parts[0]
                )
            )

        # -------------------------------------------------------------
        # Handle cases like:
        #
        # Managing Director | Nutrain
        # 2025 – 2026 | Lahore
        #
        # after date removal.
        # -------------------------------------------------------------

        if not location:

            tokens = re.split(
                r"\s*\|\s*",
                text,
            )

            for token in tokens:

                token_clean = self._clean_text(
                    self._remove_dates(token)
                )

                if self._looks_like_location(
                    token_clean
                ):

                    location = token_clean

                    if token_clean in parts:
                        parts.remove(
                            token_clean
                        )

                    break

        # -------------------------------------------------------------
        # Last validation.
        # -------------------------------------------------------------

        if not title:

            return None

        # A bare location must NEVER become a title.
        if self._looks_like_location(
            title
        ) and not self._looks_like_title(
            title
        ):
            return None

        return NormalizedExperience(
            title=title,
            company=company,
            location=location,
            start_date=start,
            end_date=end,
            raw_header=text,
        )

    def _parse_unstructured_experience_header(
        self,
        text: str,
    ) -> tuple[str, str, str]:

        # Try to identify location after a date-like separator.
        location = ""

        location_match = re.search(
            r"\b(?:in|at)\s+"
            r"(.+)$",
            text,
            re.IGNORECASE,
        )

        if location_match:
            candidate = (
                location_match.group(1)
            )

            if self._looks_like_location(
                candidate
            ):
                location = candidate

        # Title is generally the initial segment.
        title = text

        if location:
            title = text[
                :location_match.start()
            ].strip(
                " |-–—"
            )

        company = ""

        # Try common "Title, Company" / "Title at Company".
        match = re.match(
            r"(.+?)\s+(?:at|@)\s+(.+)$",
            title,
            re.IGNORECASE,
        )

        if match:
            title = match.group(1).strip()
            company = match.group(2).strip()

        return (
            title,
            company,
            location,
        )

    def _extract_date_range(
        self,
        text: str,
    ) -> tuple[str, str]:

        match = (
            self.DATE_RANGE_PATTERN.search(text)
            or self.YEAR_RANGE_PATTERN.search(text)
        )

        if not match:
            return "", ""

        start = self._normalize_date(
            match.group("start")
        )

        end = self._normalize_date(
            match.group("end")
        )

        return start, end

    def _normalize_date(
        self,
        value: str,
    ) -> str:

        value = self._clean_text(
            value
        ).lower()

        if value in {
            "present",
            "current",
            "now",
        }:
            return "present"

        return value

    def _remove_dates(
        self,
        text: str,
    ) -> str:

        text = self.DATE_RANGE_PATTERN.sub(
            " ",
            text,
        )

        text = self.YEAR_RANGE_PATTERN.sub(
            " ",
            text,
        )

        return self._clean_text(
            text
        ).strip(
            " |-–—"
        )

    def _looks_like_title(
        self,
        text: str,
    ) -> bool:

        low = text.lower()

        return any(
            term in low
            for term in self.TITLE_TERMS
        )

    def _looks_like_location(
        self,
        text: str,
    ) -> bool:

        if not text:
            return False

        low = text.lower()

        location_terms = (
            "canada",
            "pakistan",
            "usa",
            "united states",
            "ontario",
            "british columbia",
            "bc",
            "alberta",
            "quebec",
            "lahore",
            "brampton",
            "toronto",
            "vancouver",
            "montreal",
            "calgary",
            "new york",
            "london",
            "india",
            "punjab",
        )

        return any(
            term in low
            for term in location_terms
        )

    def _looks_like_achievement_sentence(
        self,
        text: str,
    ) -> bool:

        low = text.lower()

        signals = (
            "achieved",
            "increased",
            "improved",
            "reduced",
            "delivered",
            "obtained",
            "maintained",
            "generated",
            "saved",
            "grew",
            "%",
        )

        return (
            len(text) > 100
            and any(
                signal in low
                for signal in signals
            )
        )

    def _finalize_experience(
        self,
        record: NormalizedExperience,
    ) -> None:

        record.responsibilities = (
            self._dedupe(
                record.responsibilities
            )
        )

        record.achievements = (
            self._dedupe(
                record.achievements
            )
        )

        record.raw_content = (
            self._dedupe(
                record.raw_content
            )
        )

    # =================================================================
    # EDUCATION
    # =================================================================

    def _extract_education(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[NormalizedEducation]:

        records: list[NormalizedEducation] = []

        current: Optional[
            NormalizedEducation
        ] = None

        for item in blocks:

            text = item["text"]

            if not text:
                continue

            clean = self._strip_bullet(
                text
            )

            parsed = (
                self._parse_education_header(
                    clean
                )
            )

            if parsed is not None:

                if current is not None:
                    self._finalize_education(
                        current
                    )
                    records.append(
                        current
                    )

                current = parsed

                current.source_indexes.append(
                    item["index"]
                )

                continue

            # ---------------------------------------------------------
            # CONTINUATION PARAGRAPH
            #
            # IMPORTANT:
            # A description does NOT create a new education record.
            # ---------------------------------------------------------

            if current is not None:

                current.description.append(
                    clean
                )

                current.raw_content.append(
                    clean
                )

                current.source_indexes.append(
                    item["index"]
                )

        if current is not None:

            self._finalize_education(
                current
            )

            records.append(
                current
            )

        return records

    def _parse_education_header(
        self,
        text: str,
    ) -> Optional[NormalizedEducation]:

        if not text:
            return None

        low = text.lower()

        degree_signal = any(
            re.search(
                pattern,
                low,
            )
            for pattern in self.DEGREE_PATTERNS
        )

        institution_signal = any(
            term in low
            for term in self.INSTITUTION_TERMS
        )

        if not (
            degree_signal
            or institution_signal
        ):
            return None

        # -------------------------------------------------------------
        # TAB / PIPE / MULTI-SPACE layouts
        # -------------------------------------------------------------

        parts = self._split_structured_line(
            text
        )

        degree = ""
        institution = ""
        location = ""
        field = ""

        if len(parts) >= 2:

            # Determine which side contains institution.
            institution_index = None

            for idx, part in enumerate(parts):

                if self._looks_like_institution(
                    part
                ):
                    institution_index = idx
                    break

            if institution_index is not None:

                institution = parts[
                    institution_index
                ]

                before = parts[
                    :institution_index
                ]

                after = parts[
                    institution_index + 1:
                ]

                degree = " ".join(
                    before
                ).strip()

                if after:
                    location = " ".join(
                        after
                    ).strip()

            else:

                degree = parts[0]
                institution = parts[1]

                if len(parts) > 2:
                    location = " ".join(
                        parts[2:]
                    )

        else:

            degree, institution, location = (
                self._parse_unstructured_education(
                    text
                )
            )

        # -------------------------------------------------------------
        # Institution embedded in degree because DOCX tabs were
        # flattened.
        # -------------------------------------------------------------

        if not institution:

            match = re.search(
                r"\b("
                r"(?:University|College|Institute|"
                r"School|Academy|Polytechnic)"
                r"[^,|]+"
                r"(?:,\s*[^|]+)?"
                r")$",
                text,
                re.IGNORECASE,
            )

            if match:

                institution = (
                    match.group(1).strip()
                )

                degree = (
                    text[
                        :match.start()
                    ]
                    .strip(
                        " ,-–—"
                    )
                )

        if not degree:
            return None

        # -------------------------------------------------------------
        # Extract field from parentheses.
        # -------------------------------------------------------------

        field_match = re.search(
            r"\(([^)]*(?:major|field|speciali[sz]ation|"
            r"concentration|studies)[^)]*)\)",
            degree,
            re.IGNORECASE,
        )

        if field_match:

            field = field_match.group(1).strip()

        return NormalizedEducation(
            degree=degree,
            institution=institution,
            location=location,
            field=field,
            raw_header=text,
        )

    def _split_structured_line(
        self,
        text: str,
    ) -> list[str]:

        # Pipes are strong separators.
        if "|" in text:

            return [
                self._clean_text(p)
                for p in text.split("|")
                if self._clean_text(p)
            ]

        # Tabs have already been normalized to spaces.
        # Detect long spacing that originated from tabs.
        parts = re.split(
            r"\s{4,}",
            text,
        )

        if len(parts) > 1:

            return [
                self._clean_text(p)
                for p in parts
                if self._clean_text(p)
            ]

        return [text]

    def _looks_like_institution(
        self,
        text: str,
    ) -> bool:

        low = text.lower()

        return any(
            term in low
            for term in self.INSTITUTION_TERMS
        )

    def _parse_unstructured_education(
        self,
        text: str,
    ) -> tuple[str, str, str]:

        # Find institution anywhere in line.
        pattern = re.compile(
            r"\b("
            r"(?:University|College|Institute|"
            r"School|Academy|Polytechnic)"
            r"[^,|]*"
            r"(?:,\s*[^|]+)?"
            r")",
            re.IGNORECASE,
        )

        match = pattern.search(
            text
        )

        if not match:

            return (
                text,
                "",
                "",
            )

        degree = text[
            :match.start()
        ].strip(
            " ,-–—"
        )

        institution = match.group(
            1
        ).strip()

        location = ""

        return (
            degree,
            institution,
            location,
        )

    def _finalize_education(
        self,
        record: NormalizedEducation,
    ) -> None:

        record.description = (
            self._dedupe(
                record.description
            )
        )

        record.raw_content = (
            self._dedupe(
                record.raw_content
            )
        )

        # -------------------------------------------------------------
        # Remove accidental duplicate institution from degree.
        # -------------------------------------------------------------

        if record.institution:

            degree_low = (
                record.degree.lower()
            )

            institution_low = (
                record.institution.lower()
            )

            if institution_low in degree_low:

                record.degree = re.sub(
                    re.escape(
                        record.institution
                    ),
                    "",
                    record.degree,
                    flags=re.IGNORECASE,
                ).strip(
                    " ,-–—"
                )

    # =================================================================
    # CERTIFICATIONS
    # =================================================================

    def _extract_certifications(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[NormalizedCertification]:

        results = []

        for item in blocks:

            text = self._strip_bullet(
                item["text"]
            )

            if not text:
                continue

            if self._is_achievement_label(
                text
            ):
                continue

            issuer = ""

            # Common issuer patterns.
            match = re.search(
                r"\(([^)]*(?:CQI|IRCA|BRCGS|FSPCA|"
                r"Highfield|Simplilearn|University|"
                r"College)[^)]*)\)",
                text,
                re.IGNORECASE,
            )

            if match:
                issuer = match.group(
                    1
                )

            results.append(
                NormalizedCertification(
                    name=text,
                    issuer=issuer,
                    raw=text,
                    source_index=item["index"],
                )
            )

        return results

    def _infer_certifications(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[dict[str, Any]]:

        candidates = []

        signals = (
            "certified",
            "certification",
            "lead auditor",
            "haccp",
            "pcqi",
            "six sigma",
            "iso 9001",
            "brcgs",
            "fssc",
            "highfield",
        )

        for item in blocks:

            low = item["text"].lower()

            if any(
                signal in low
                for signal in signals
            ):
                candidates.append(item)

        return candidates

    # =================================================================
    # LANGUAGES
    # =================================================================

    def _extract_languages(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[NormalizedLanguage]:

        results = []

        for item in blocks:

            text = self._strip_bullet(
                item["text"]
            )

            if not text:
                continue

            pieces = re.split(
                r"\s*\|\s*",
                text,
            )

            for piece in pieces:

                piece = self._clean_text(
                    piece
                )

                if not piece:
                    continue

                match = re.match(
                    r"(.+?)\s*[–-]\s*(.+)$",
                    piece,
                )

                if match:

                    language = (
                        match.group(1).strip()
                    )

                    proficiency = (
                        match.group(2).strip()
                    )

                else:

                    language = piece
                    proficiency = ""

                results.append(
                    NormalizedLanguage(
                        language=language,
                        proficiency=proficiency,
                        raw=piece,
                        source_index=item["index"],
                    )
                )

        return results

    # =================================================================
    # SIMPLE RECORDS
    # =================================================================

    def _extract_simple_records(
        self,
        blocks: Sequence[dict[str, Any]],
    ) -> list[str]:

        values = []

        for item in blocks:

            text = self._strip_bullet(
                item["text"]
            )

            if text:
                values.append(
                    text
                )

        return self._dedupe(
            values
        )

    # =================================================================
    # HELPERS
    # =================================================================

    def _strip_bullet(
        self,
        text: str,
    ) -> str:

        text = self._clean_text(
            text
        )

        while text and text[0] in self.BULLET_CHARS:

            text = text[1:].strip()

        return text

    def _is_achievement_label(
        self,
        text: str,
    ) -> bool:

        normalized = self._normalize_heading(
            text
        )

        return normalized in (
            self.ACHIEVEMENT_LABELS
        )

    def _looks_like_heading(
        self,
        text: str,
    ) -> bool:

        normalized = self._normalize_heading(
            text
        )

        if normalized in self.HEADING_WORDS:
            return True

        return False

    def _looks_like_institution(
        self,
        text: str,
    ) -> bool:

        low = text.lower()

        return any(
            term in low
            for term in self.INSTITUTION_TERMS
        )

    def _dedupe(
        self,
        values: Iterable[str],
    ) -> list[str]:

        result = []

        seen = set()

        for value in values:

            normalized = self._normalize_compare(
                value
            )

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            result.append(
                value.strip()
            )

        return result

    def _normalize_compare(
        self,
        value: str,
    ) -> str:

        value = self._clean_text(
            value
        ).lower()

        value = re.sub(
            r"\s+",
            " ",
            value,
        )

        return value

    # =================================================================
    # DIAGNOSTICS
    # =================================================================

    def _diagnostics(
        self,
        resume: NormalizedResume,
    ) -> dict[str, Any]:

        problems = []

        for idx, record in enumerate(
            resume.experience
        ):

            if (
                not record.title
                or self._looks_like_location(
                    record.title
                )
            ):
                problems.append(
                    f"experience[{idx}] invalid title"
                )

            if not record.start_date:
                problems.append(
                    f"experience[{idx}] missing start date"
                )

        for idx, record in enumerate(
            resume.education
        ):

            if not record.degree:
                problems.append(
                    f"education[{idx}] missing degree"
                )

        return {
            "experience_count": len(
                resume.experience
            ),
            "education_count": len(
                resume.education
            ),
            "skills_count": len(
                resume.skills
            ),
            "certification_count": len(
                resume.certifications
            ),
            "language_count": len(
                resume.languages
            ),
            "problems": problems,
            "valid": not problems,
        }