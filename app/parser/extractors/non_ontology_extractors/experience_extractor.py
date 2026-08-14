"""
GetHired
Enterprise V5

Experience Extractor
--------------------

Input:
    ResumeSection

Output:
    ExperienceSectionResult

The extractor is completely independent from ResumeBuilder.
"""

from __future__ import annotations

import re
from typing import Any

from app.parser.parsed_models.experience import Experience
from app.parser.parsed_models.resume_section import ResumeSection

from app.parser.experience.experience_section_result import ExperienceSectionResult


class ExperienceExtractor:

    # ============================================================
    # DATE
    # ============================================================

    _DATE_RANGE_RE = re.compile(
        r"""
        (?:
            (19|20)\d{2}
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
            (19|20)\d{2}
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _YEAR_RE = re.compile(
        r"\b(?:19|20)\d{2}\b"
    )

    # ============================================================
    # JOB TITLE
    # ============================================================

    _TITLE_RE = re.compile(
        r"""
        \b(
            manager |
            director |
            engineer |
            chemist |
            analyst |
            specialist |
            supervisor |
            coordinator |
            officer |
            consultant |
            executive |
            administrator |
            technician |
            operator |
            scientist |
            developer |
            designer |
            auditor |
            accountant |
            associate |
            assistant |
            lead |
            head |
            president |
            owner |
            founder |
            partner |
            trainee |
            intern |
            representative |
            pharmacist |
            teacher |
            professor |
            researcher |
            architect |
            inspector |
            controller |
            marketer |
            buyer |
            planner |
            technician
        )\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # NARRATIVE
    # ============================================================

    _NARRATIVE_STARTS = (
        "achieved ",
        "successfully ",
        "managed ",
        "led ",
        "developed ",
        "implemented ",
        "improved ",
        "oversaw ",
        "directed ",
        "maintained ",
        "responsible for ",
        "ensured ",
        "supported ",
        "utilized ",
        "utilised ",
        "coordinated ",
        "performed ",
        "conducted ",
        "worked ",
        "assisted ",
        "spearheaded ",
        "governed ",
        "drove ",
        "fostered ",
        "strengthened ",
        "enhanced ",
    )

    # ============================================================
    # PUBLIC API
    # ============================================================

    def extract(
        self,
        section: ResumeSection,
    ) -> ExperienceSectionResult:

        result = ExperienceSectionResult(
            source_section=section
        )

        if section is None:

            result.success = False
            result.error = (
                "Experience section is None"
            )

            return result

        if not isinstance(
            section,
            ResumeSection
        ):

            result.success = False
            result.error = (
                "ExperienceExtractor expected "
                f"ResumeSection, received "
                f"{type(section).__name__}"
            )

            return result

        try:

            blocks = self._get_blocks(
                section
            )

            records = self._split_records(
                blocks
            )

            for record in records:

                experience = (
                    self._parse_record(
                        record
                    )
                )

                if experience:

                    result.add(
                        experience
                    )

            result.confidence = (
                self._calculate_confidence(
                    result
                )
            )

            return result

        except Exception as exc:

            result.success = False
            result.error = str(exc)

            return result

    # ============================================================
    # BLOCKS
    # ============================================================

    @staticmethod
    def _get_blocks(
        section: ResumeSection,
    ) -> list[Any]:

        return list(
            section.items
        )

    # ============================================================
    # TEXT
    # ============================================================

    @staticmethod
    def _block_text(
        block: Any,
    ) -> str:

        if block is None:

            return ""

        if isinstance(
            block,
            str
        ):

            return block.strip()

        if hasattr(
            block,
            "text"
        ):

            value = getattr(
                block,
                "text",
                ""
            )

            return (
                str(value).strip()
                if value is not None
                else ""
            )

        return str(block).strip()

    # ============================================================
    # JOB HEADER DETECTION
    # ============================================================

    @classmethod
    def _is_job_header(
        cls,
        text: str,
    ) -> bool:

        if not text:

            return False

        clean = " ".join(
            text.split()
        )

        lower = clean.lower()

        # --------------------------------------------------------
        # Narrative is never a header.
        # --------------------------------------------------------

        if lower.startswith(
            cls._NARRATIVE_STARTS
        ):

            return False

        # --------------------------------------------------------
        # Explicit job separator.
        # --------------------------------------------------------

        has_separator = any(
            token in clean
            for token in (
                "|",
                " @ ",
                " — ",
                " – ",
            )
        )

        # --------------------------------------------------------
        # Date range.
        # --------------------------------------------------------

        has_date_range = bool(
            cls._DATE_RANGE_RE.search(
                clean
            )
        )

        # --------------------------------------------------------
        # Job title.
        # --------------------------------------------------------

        has_title = bool(
            cls._TITLE_RE.search(
                clean
            )
        )

        # --------------------------------------------------------
        # Strongest case:
        #
        # Title + company separator + dates
        # --------------------------------------------------------

        if (
            has_title
            and has_separator
            and has_date_range
        ):

            return True

        # --------------------------------------------------------
        # Title + separator
        # --------------------------------------------------------

        if (
            has_title
            and has_separator
        ):

            return True

        # --------------------------------------------------------
        # Date + title
        # --------------------------------------------------------

        if (
            has_date_range
            and has_title
        ):

            return True

        return False

    # ============================================================
    # SPLIT EXPERIENCE RECORDS
    # ============================================================

    @classmethod
    def _split_records(
        cls,
        blocks: list[Any],
    ) -> list[list[str]]:

        records: list[list[str]] = []

        current: list[str] = []

        for block in blocks:

            text = cls._block_text(
                block
            )

            if not text:

                continue

            # ----------------------------------------------------
            # New job
            # ----------------------------------------------------

            if cls._is_job_header(
                text
            ):

                if current:

                    records.append(
                        current
                    )

                current = [
                    text
                ]

                continue

            # ----------------------------------------------------
            # Content belonging to current job
            # ----------------------------------------------------

            if current:

                current.append(
                    text
                )

        if current:

            records.append(
                current
            )

        return records

    # ============================================================
    # PARSE RECORD
    # ============================================================

    @classmethod
    def _parse_record(
        cls,
        lines: list[str],
    ) -> Experience | None:

        if not lines:

            return None

        header = lines[0]

        experience = Experience()

        experience.raw_header = header

        experience.raw_lines = list(
            lines
        )

        # --------------------------------------------------------
        # Header
        # --------------------------------------------------------

        cls._parse_header(
            header,
            experience
        )

        # --------------------------------------------------------
        # Remaining content
        # --------------------------------------------------------

        content = lines[1:]

        mode = "responsibility"

        for line in content:

            clean = line.strip()

            if not clean:

                continue

            lower = clean.lower()

            # ----------------------------------------------------
            # Achievement heading
            # ----------------------------------------------------

            if (
                "key accomplishment" in lower
                or "key achievement" in lower
                or lower in (
                    "achievements",
                    "accomplishments",
                    "selected achievements",
                )
            ):

                mode = "achievement"

                continue

            # ----------------------------------------------------
            # Responsibility heading
            # ----------------------------------------------------

            if lower in (
                "responsibilities",
                "duties",
                "job responsibilities",
            ):

                mode = "responsibility"

                continue

            # ----------------------------------------------------
            # Content
            # ----------------------------------------------------

            if mode == "achievement":

                experience.achievements.append(
                    clean
                )

            else:

                experience.responsibilities.append(
                    clean
                )

        return experience

    # ============================================================
    # HEADER PARSER
    # ============================================================

    @classmethod
    def _parse_header(
        cls,
        text: str,
        experience: Experience,
    ) -> None:

        clean = " ".join(
            text.split()
        )

        experience.raw_header = clean

        # --------------------------------------------------------
        # Years
        # --------------------------------------------------------

        years = [
            int(value)
            for value in cls._YEAR_RE.findall(
                clean
            )
        ]

        if years:

            experience.start_year = years[0]

            if len(years) >= 2:

                experience.end_year = years[1]

            else:

                experience.current_job = True

        # --------------------------------------------------------
        # Remove dates
        # --------------------------------------------------------

        without_dates = cls._DATE_RANGE_RE.sub(
            "",
            clean
        )

        without_dates = re.sub(
            r"\b(?:19|20)\d{2}\b",
            "",
            without_dates
        )

        without_dates = re.sub(
            r"\s+",
            " ",
            without_dates
        ).strip(
            " |,-–—"
        )

        # --------------------------------------------------------
        # Split title/company
        # --------------------------------------------------------

        if "|" in without_dates:

            parts = [
                part.strip()
                for part in without_dates.split(
                    "|"
                )
                if part.strip()
            ]

            if parts:

                experience.title = parts[0]

            if len(parts) >= 2:

                experience.company = parts[1]

            if len(parts) >= 3:

                experience.location = (
                    " | ".join(
                        parts[2:]
                    )
                )

        else:

            # ----------------------------------------------------
            # Fallback title detection
            # ----------------------------------------------------

            match = cls._TITLE_RE.search(
                without_dates
            )

            if match:

                experience.title = (
                    without_dates
                    .strip()
                )

            else:

                experience.title = (
                    without_dates
                )

        # --------------------------------------------------------
        # Location
        # --------------------------------------------------------

        location = cls._extract_location(
            clean
        )

        if location:

            experience.location = location

        # --------------------------------------------------------
        # Duration
        # --------------------------------------------------------

        if (
            experience.start_year
            and experience.end_year
        ):

            experience.duration = (
                experience.end_year
                - experience.start_year
            )

        elif (
            experience.start_year
            and experience.current_job
        ):

            from datetime import datetime

            experience.duration = (
                datetime.now().year
                - experience.start_year
            )

    # ============================================================
    # LOCATION
    # ============================================================

    @staticmethod
    def _extract_location(
        text: str,
    ) -> str:

        # Common resume location forms:
        #
        # Lahore, Pakistan
        # Canada
        # Lahore, Pakistan | ...
        #

        parts = [
            part.strip()
            for part in text.split("|")
        ]

        if len(parts) >= 3:

            return parts[-1]

        # Detect final "Country" style value.
        countries = (
            "Canada",
            "Pakistan",
            "United States",
            "USA",
            "UK",
            "United Kingdom",
        )

        for country in countries:

            if re.search(
                rf"\b{re.escape(country)}\s*$",
                text,
                re.IGNORECASE,
            ):

                return country

        return ""

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def _calculate_confidence(
        result: ExperienceSectionResult,
    ) -> float:

        if not result.records:

            return 0.0

        score = 0.0

        for record in result.records:

            if record.title:

                score += 0.25

            if record.company:

                score += 0.25

            if record.start_year:

                score += 0.15

            if (
                record.responsibilities
                or record.achievements
            ):

                score += 0.20

        maximum = len(
            result.records
        ) * 0.85

        return min(
            1.0,
            score / maximum
            if maximum
            else 0.0
        )