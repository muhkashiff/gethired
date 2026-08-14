"""
GetHired
Enterprise V5

Education Extractor
===================

Input
-----
ResumeSection

Output
------
EducationSectionResult

Architecture
------------
ResumeSection
    ↓
EducationExtractor
    ↓
Education records
    ↓
EducationSectionResult

Important design principle
--------------------------
Education records are STRUCTURALLY identified.

A new education record normally begins with a
qualification/degree header.

Continuation lines such as:

    Completed a Data Analytics Certificate...
    A comprehensive 2-year...
    Four-year Bachelor's degree academic equivalency...
    coursework...
    thesis...
    curriculum...

are treated as DESCRIPTION lines belonging to
the preceding education record.

The extractor does NOT use a hard-coded university
or college database.

It uses structural and linguistic signals instead.
"""

from __future__ import annotations

import re
from typing import Any

from app.parser.parsed_models.education import Education
from app.parser.parsed_models.resume_section import ResumeSection

from app.parser.education.education_section_result import (
    EducationSectionResult,
)


class EducationExtractor:
    """
    Extract structured Education objects from one ResumeSection.

    Expected input structure:

        ResumeSection(
            name="education",
            title="Education",
            items=[
                "Degree ........ Institution, Location",
                "Description...",
                "Degree ........ Institution, Location",
                "Description...",
            ],
        )

    The extractor returns one Education object per
    actual qualification.
    """

    # ============================================================
    # DEGREE / QUALIFICATION PATTERNS
    # ============================================================

    _DEGREE_RE = re.compile(
        r"""
        (?:
            \bPh\.?\s*D\.?\b
            |
            \bD\.?\s*Phil\.?\b
            |
            \bDoctorate\b
            |
            \bDoctor\b
            |
            \bM\.?\s*Sc\.?\b
            |
            \bM\.?\s*S\.?\b
            |
            \bM\.?\s*A\.?\b
            |
            \bM\.?\s*B\.?\s*A\.?\b
            |
            \bM\.?\s*Eng\.?\b
            |
            \bM\.?\s*Tech\.?\b
            |
            \bB\.?\s*Sc\.?\b
            |
            \bB\.?\s*S\.?\b
            |
            \bB\.?\s*A\.?\b
            |
            \bB\.?\s*Eng\.?\b
            |
            \bB\.?\s*Tech\.?\b
            |
            \bDiploma\b
            |
            \bCertificate\b
            |
            \bCertification\b
            |
            \bPostgraduate\b
            |
            \bPost[-\s]?graduate\b
            |
            \bUndergraduate\b
            |
            \bBachelor'?s?\b
            |
            \bMaster'?s?\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # DEGREE HEADER START PATTERNS
    #
    # These are intentionally stricter than _DEGREE_RE.
    #
    # _DEGREE_RE answers:
    #
    #     "Does this text contain a degree word?"
    #
    # _DEGREE_HEADER_RE answers:
    #
    #     "Does this line START like an education header?"
    #
    # This distinction is critical.
    #
    # Example:
    #
    #     Completed a Data Analytics Certificate...
    #
    # contains "Certificate", but is NOT a new record.
    # ============================================================

    _DEGREE_HEADER_RE = re.compile(
        r"""
        ^\s*
        (?:
            Ph\.?\s*D\.?
            |
            D\.?\s*Phil\.?
            |
            Doctorate
            |
            Doctor
            |
            M\.?\s*Sc\.?
            |
            M\.?\s*S\.?
            |
            M\.?\s*A\.?
            |
            M\.?\s*B\.?\s*A\.?
            |
            M\.?\s*Eng\.?
            |
            M\.?\s*Tech\.?
            |
            B\.?\s*Sc\.?
            |
            B\.?\s*S\.?
            |
            B\.?\s*A\.?
            |
            B\.?\s*Eng\.?
            |
            B\.?\s*Tech\.?
            |
            Diploma
            |
            Certificate
            |
            Certification
            |
            Postgraduate
            |
            Post[-\s]?graduate
            |
            Undergraduate
            |
            Bachelor'?s?
            |
            Master'?s?
        )
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # COMMON QUALIFICATION PHRASES
    #
    # Needed for titles such as:
    #
    # Post Graduation Diploma: Business Administration
    #
    # where "Post Graduation Diploma" is the actual
    # qualification.
    # ============================================================

    _QUALIFICATION_START_RE = re.compile(
        r"""
        ^\s*
        (?:
            post\s+graduation\s+diploma
            |
            post[-\s]?graduate\s+diploma
            |
            postgraduate\s+diploma
            |
            advanced\s+diploma
            |
            higher\s+diploma
            |
            associate\s+degree
            |
            bachelor's?\s+degree
            |
            master's?\s+degree
            |
            doctoral\s+degree
            |
            professional\s+certificate
            |
            graduate\s+certificate
        )
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # INSTITUTION
    # ============================================================

    _INSTITUTION_RE = re.compile(
        r"""
        \b(
            University
            |
            College
            |
            Institute
            |
            School
            |
            Academy
            |
            Polytechnic
        )
        \b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # MAJOR
    # ============================================================

    _MAJOR_PAREN_RE = re.compile(
        r"""
        \(
            \s*
            ([^)]*?)
            \s*
            major
            \s*
        \)
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _MAJOR_TEXT_RE = re.compile(
        r"""
        \bmajor
        \s*
        (?:in|:|-)
        \s*
        ([A-Za-z][A-Za-z &/\-]+)
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # YEAR
    # ============================================================

    _YEAR_RE = re.compile(
        r"\b(?:19|20)\d{2}\b"
    )

    # ============================================================
    # LOCATION
    #
    # We mainly parse the common:
    #
    #     University of Toronto, ON, Canada
    #
    #     Selkirk College, BC, Canada
    #
    #     University of the Punjab, Pakistan
    #
    # Institution parsing happens BEFORE location parsing.
    # ============================================================

    _PROVINCE_RE = re.compile(
        r"""
        \b(
            AB |
            BC |
            MB |
            NB |
            NL |
            NS |
            NT |
            NU |
            ON |
            PE |
            QC |
            SK |
            YT
        )\b
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # DESCRIPTION START SIGNALS
    #
    # IMPORTANT:
    #
    # These are used to classify a continuation line.
    # They are NEVER sufficient by themselves to create
    # a new education record.
    # ============================================================

    _DESCRIPTION_START_RE = re.compile(
        r"""
        ^\s*
        (?:
            completed\b
            |
            a\s+comprehensive\b
            |
            comprehensive\b
            |
            this\s+program\b
            |
            the\s+program\b
            |
            coursework\b
            |
            curriculum\b
            |
            thesis\b
            |
            dissertation\b
            |
            four[-\s]?year\b
            |
            three[-\s]?year\b
            |
            two[-\s]?year\b
            |
            one[-\s]?year\b
            |
            academic\b
            |
            equivalent\b
            |
            equivalency\b
            |
            verified\b
            |
            accredited\b
            |
            gained\b
            |
            gained\s+practical\b
            |
            practical\s+experience\b
            |
            focused\b
            |
            focusing\b
            |
            studied\b
            |
            covering\b
            |
            included\b
            |
            designed\b
            |
            provided\b
            |
            developed\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # NARRATIVE STARTS
    #
    # Additional protection against treating prose as a new
    # education header.
    # ============================================================

    _NARRATIVE_START_RE = re.compile(
        r"""
        ^\s*
        (?:
            completed\b
            |
            achieved\b
            |
            successfully\b
            |
            gained\b
            |
            developed\b
            |
            provided\b
            |
            included\b
            |
            focused\b
            |
            focusing\b
            |
            studied\b
            |
            managed\b
            |
            led\b
            |
            worked\b
            |
            responsible\b
            |
            extensive\b
            |
            four[-\s]?year\b
            |
            three[-\s]?year\b
            |
            two[-\s]?year\b
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # ============================================================
    # LEVEL
    # ============================================================

    _LEVEL_PATTERNS = (
        (
            re.compile(
                r"\b(?:ph\.?\s*d\.?|d\.?\s*phil\.?|doctorate|doctoral)\b",
                re.IGNORECASE,
            ),
            "phd",
        ),
        (
            re.compile(
                r"\b(?:m\.?\s*sc\.?|m\.?\s*s\.?|m\.?\s*a\.?|m\.?\s*b\.?\s*a\.?|m\.?\s*eng\.?|m\.?\s*tech\.?|master'?s?)\b",
                re.IGNORECASE,
            ),
            "master",
        ),
        (
            re.compile(
                r"\b(?:b\.?\s*sc\.?|b\.?\s*s\.?|b\.?\s*a\.?|b\.?\s*eng\.?|b\.?\s*tech\.?|bachelor'?s?)\b",
                re.IGNORECASE,
            ),
            "bachelor",
        ),
        (
            re.compile(
                r"\b(?:post\s+graduation\s+diploma|post[-\s]?graduate\s+diploma|postgraduate\s+diploma|diploma)\b",
                re.IGNORECASE,
            ),
            "diploma",
        ),
        (
            re.compile(
                r"\b(?:certificate|certification)\b",
                re.IGNORECASE,
            ),
            "certificate",
        ),
    )

    # ============================================================
    # PUBLIC API
    # ============================================================

    def extract(
        self,
        section: ResumeSection,
    ) -> EducationSectionResult:
        """
        Extract education records from one ResumeSection.

        The extractor operates directly on section.items.

        It does NOT flatten the entire section into one string.
        """

        result = EducationSectionResult(
            source_section=section
        )

        if section is None:

            result.success = False
            result.error = "Education section is None"

            return result

        if not isinstance(section, ResumeSection):

            result.success = False
            result.error = (
                "EducationExtractor expected ResumeSection, "
                f"received {type(section).__name__}"
            )

            return result

        try:

            blocks = self._get_blocks(section)

            records = self._build_records(
                blocks
            )

            for record in records:

                education = self._parse_record(
                    record
                )

                if education is not None:

                    result.add(
                        education
                    )

            result.confidence = (
                self._calculate_confidence(
                    result
                )
            )

            result.success = True

            return result

        except Exception as exc:

            result.success = False
            result.error = str(exc)

            return result

    # ============================================================
    # BLOCK EXTRACTION
    # ============================================================

    @staticmethod
    def _get_blocks(
        section: ResumeSection,
    ) -> list[Any]:
        """
        Preserve ResumeSection.items as individual blocks.

        Do NOT flatten the section here.
        """

        return list(
            section.items
        )

    # ============================================================
    # BLOCK TEXT
    # ============================================================

    @staticmethod
    def _block_text(
        block: Any,
    ) -> str:
        """
        Extract text from a ResumeBlock or string.
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
    # CLEAN TEXT
    # ============================================================

    @staticmethod
    def _clean_text(
        text: str,
    ) -> str:
        """
        Safe structural cleanup.

        Tabs are preserved temporarily because tabs are useful
        for detecting:

            degree <TAB> institution

        """

        if not text:
            return ""

        text = text.replace(
            "\xa0",
            " ",
        )

        text = text.replace(
            "\r\n",
            "\n",
        )

        text = text.replace(
            "\r",
            "\n",
        )

        # Preserve tabs because they may represent
        # the original two-column resume structure.
        text = re.sub(
            r"[ ]{2,}",
            " ",
            text,
        )

        text = re.sub(
            r"\t+",
            "\t",
            text,
        )

        return text.strip()

    # ============================================================
    # RECORD BUILDING
    # ============================================================

    @classmethod
    def _build_records(
        cls,
        blocks: list[Any],
    ) -> list[list[str]]:
        """
        Convert ResumeSection blocks into logical education records.

        THIS is the most important part of the extractor.

        Given:

            Degree 1
            Description 1
            Degree 2
            Description 2
            Degree 3
            Description 3

        return:

            [
                [Degree 1, Description 1],
                [Degree 2, Description 2],
                [Degree 3, Description 3],
            ]

        Crucially:

            "Completed a Data Analytics Certificate..."

        does NOT become a new record merely because it contains
        the word "Certificate".

        Likewise:

            "Four-year Bachelor's degree..."

        does NOT become a new record.
        """

        records: list[list[str]] = []

        current: list[str] = []

        for block in blocks:

            text = cls._clean_text(
                cls._block_text(block)
            )

            if not text:
                continue

            # ----------------------------------------------------
            # New qualification header
            # ----------------------------------------------------

            if cls._is_new_education_header(
                text,
                has_current=bool(current),
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
            # First non-header line.
            #
            # We still need somewhere to put it.
            # It belongs to the current logical record.
            # ----------------------------------------------------

            if not current:

                current = [
                    text
                ]

                continue

            # ----------------------------------------------------
            # Continuation / description
            # ----------------------------------------------------

            current.append(
                text
            )

        if current:

            records.append(
                current
            )

        return records

    # ============================================================
    # NEW EDUCATION HEADER
    # ============================================================

    @classmethod
    def _is_new_education_header(
        cls,
        text: str,
        has_current: bool = False,
    ) -> bool:
        """
        Determine whether a line starts a NEW education record.

        Rules:

        1. A degree at the START of the line is strong evidence.
        2. A qualification phrase at the START is strong evidence.
        3. Narrative lines are never new records.
        4. A line containing a degree word somewhere in the
           sentence is NOT enough.
        """

        clean = text.strip()

        if not clean:
            return False

        # --------------------------------------------------------
        # Narrative protection comes FIRST.
        #
        # This is what prevents:
        #
        # Completed a Data Analytics Certificate...
        #
        # from becoming a new education record.
        # --------------------------------------------------------

        if cls._looks_like_narrative(
            clean
        ):

            return False

        # --------------------------------------------------------
        # Strong degree header.
        # --------------------------------------------------------

        if cls._DEGREE_HEADER_RE.match(
            clean
        ):

            return True

        # --------------------------------------------------------
        # Explicit qualification phrase.
        # --------------------------------------------------------

        if cls._QUALIFICATION_START_RE.match(
            clean
        ):

            return True

        # --------------------------------------------------------
        # Degree + institution on same line.
        #
        # Useful for unusual formats where the qualification
        # begins with a descriptive word but still clearly has
        # institution structure.
        # --------------------------------------------------------

        if (
            cls._DEGREE_RE.search(clean)
            and cls._INSTITUTION_RE.search(clean)
            and not cls._looks_like_narrative(clean)
        ):

            # If there is a strong qualification near the
            # beginning, treat it as a header.
            prefix = clean[:80]

            if cls._DEGREE_RE.search(
                prefix
            ):

                return True

        return False

    # ============================================================
    # NARRATIVE DETECTION
    # ============================================================

    @classmethod
    def _looks_like_narrative(
        cls,
        text: str,
    ) -> bool:
        """
        Detect prose describing an education.

        Narrative wins over degree-word detection.

        Examples:

            Completed a Data Analytics Certificate...
            Four-year Bachelor's degree academic equivalency...
            A comprehensive 2-year business management program...

        are descriptions, not new education records.
        """

        clean = text.strip()

        if not clean:
            return False

        # --------------------------------------------------------
        # Explicit narrative starters.
        # --------------------------------------------------------

        if cls._NARRATIVE_START_RE.match(
            clean
        ):

            return True

        # --------------------------------------------------------
        # Description phrases.
        # --------------------------------------------------------

        if cls._DESCRIPTION_START_RE.match(
            clean
        ):

            return True

        # --------------------------------------------------------
        # Sentence punctuation is a strong prose signal.
        #
        # Do not apply this to short degree headers.
        # --------------------------------------------------------

        words = clean.split()

        if (
            len(words) >= 12
            and (
                "." in clean
                or "," in clean
            )
        ):

            return True

        return False

    # ============================================================
    # PARSE ONE RECORD
    # ============================================================

    @classmethod
    def _parse_record(
        cls,
        lines: list[str],
    ) -> Education | None:
        """
        Parse one logical education record.

        Example:

            [
                "M.Sc. Chemistry (Organic Chemistry Major)
                 University of the Punjab, Pakistan",
                "Four-year Bachelor's degree academic equivalency
                 verified by WES."
            ]

        """

        if not lines:
            return None

        header = lines[0].strip()

        if not header:
            return None

        education = Education()

        education.description = ""

        # --------------------------------------------------------
        # Parse header
        # --------------------------------------------------------

        cls._parse_header(
            header,
            education,
        )

        # --------------------------------------------------------
        # Remaining lines = description
        # --------------------------------------------------------

        descriptions = []

        for line in lines[1:]:

            clean = line.strip()

            if not clean:
                continue

            descriptions.append(
                clean
            )

        if descriptions:

            education.description = " ".join(
                descriptions
            ).strip()

        # --------------------------------------------------------
        # Infer level
        # --------------------------------------------------------

        education.level = (
            cls._detect_level(
                header
            )
        )

        # --------------------------------------------------------
        # Keywords
        # --------------------------------------------------------

        education.keywords = (
            cls._extract_keywords(
                education
            )
        )

        return education

    # ============================================================
    # HEADER PARSING
    # ============================================================

    @classmethod
    def _parse_header(
        cls,
        header: str,
        education: Education,
    ) -> None:
        """
        Parse:

            Degree    Institution, Location

        The parser first separates the qualification from the
        institution.

        It does NOT need to know the university name beforehand.
        """

        clean = header.strip()

        # --------------------------------------------------------
        # TAB STRUCTURE
        #
        # Example:
        #
        # Bootcamp Certificate: Data Analytics
        #     University of Toronto, ON, Canada
        # --------------------------------------------------------

        if "\t" in clean:

            parts = [
                part.strip()
                for part in clean.split("\t")
                if part.strip()
            ]

            if len(parts) >= 2:

                degree_part = parts[0]

                institution_part = " ".join(
                    parts[1:]
                )

                cls._set_degree(
                    education,
                    degree_part,
                )

                cls._set_institution_location(
                    education,
                    institution_part,
                )

                cls._set_major(
                    education,
                    degree_part,
                )

                return

        # --------------------------------------------------------
        # If no tab exists, attempt to locate institution.
        # --------------------------------------------------------

        institution_match = (
            cls._INSTITUTION_RE.search(
                clean
            )
        )

        if institution_match:

            # Institution begins at the matched word.
            start = institution_match.start()

            degree_part = clean[
                :start
            ].strip(
                " ,|-–—"
            )

            institution_part = clean[
                start:
            ].strip()

            if degree_part:

                cls._set_degree(
                    education,
                    degree_part,
                )

            cls._set_institution_location(
                education,
                institution_part,
            )

            cls._set_major(
                education,
                degree_part,
            )

            return

        # --------------------------------------------------------
        # No institution found.
        #
        # Preserve the whole line as degree.
        # --------------------------------------------------------

        cls._set_degree(
            education,
            clean,
        )

        cls._set_major(
            education,
            clean,
        )

    # ============================================================
    # SET DEGREE
    # ============================================================

    @classmethod
    def _set_degree(
        cls,
        education: Education,
        text: str,
    ) -> None:
        """
        Store the qualification/title.

        Special handling:

            M.Sc. Chemistry (Organic Chemistry Major)

        becomes:

            degree = "M.Sc. Chemistry"
            major  = "Organic Chemistry"
        """

        clean = text.strip()

        # Remove trailing separators.
        clean = clean.strip(
            " ,|-–—"
        )

        # Remove parenthesized major from degree.
        major_match = cls._MAJOR_PAREN_RE.search(
            clean
        )

        if major_match:

            major = major_match.group(
                1
            ).strip()

            if major:

                education.major = (
                    cls._normalize_major(
                        major
                    )
                )

            clean = (
                clean[
                    :major_match.start()
                ]
                +
                clean[
                    major_match.end():
                ]
            ).strip()

        education.degree = clean

    # ============================================================
    # MAJOR
    # ============================================================

    @classmethod
    def _set_major(
        cls,
        education: Education,
        text: str,
    ) -> None:
        """
        Extract major from the degree text if it was not
        already extracted.
        """

        if education.major:
            return

        match = cls._MAJOR_TEXT_RE.search(
            text
        )

        if match:

            education.major = (
                cls._normalize_major(
                    match.group(1)
                )
            )

    # ============================================================
    # NORMALIZE MAJOR
    # ============================================================

    @staticmethod
    def _normalize_major(
        major: str,
    ) -> str:

        major = major.strip()

        major = re.sub(
            r"\s+",
            " ",
            major,
        )

        return major.strip(
            " ,.-"
        )

    # ============================================================
    # INSTITUTION + LOCATION
    # ============================================================

    @classmethod
    def _set_institution_location(
        cls,
        education: Education,
        text: str,
    ) -> None:
        """
        Parse:

            University of Toronto, ON, Canada

        into:

            institution = University of Toronto
            location    = ON, Canada
        """

        clean = text.strip()

        clean = re.sub(
            r"\s+",
            " ",
            clean,
        )

        # --------------------------------------------------------
        # Canadian province + country
        # --------------------------------------------------------

        match = re.search(
            r"""
            ,
            \s*
            (
                AB|BC|MB|NB|NL|NS|NT|NU|ON|PE|QC|SK|YT
            )
            \s*
            ,
            \s*
            (
                Canada
            )
            \s*$
            """,
            clean,
            re.IGNORECASE | re.VERBOSE,
        )

        if match:

            education.institution = (
                clean[
                    :match.start()
                ].strip(
                    " ,"
                )
            )

            education.location = (
                f"{match.group(1).upper()}, "
                f"{match.group(2)}"
            )

            return

        # --------------------------------------------------------
        # Institution + country
        #
        # University of the Punjab, Pakistan
        # --------------------------------------------------------

        match = re.search(
            r"""
            ,
            \s*
            (
                Pakistan
                |
                Canada
                |
                USA
                |
                UK
                |
                United\s+Kingdom
                |
                United\s+States
            )
            \s*$
            """,
            clean,
            re.IGNORECASE | re.VERBOSE,
        )

        if match:

            education.institution = (
                clean[
                    :match.start()
                ].strip(
                    " ,"
                )
            )

            education.location = (
                match.group(1)
                .strip()
            )

            return

        # --------------------------------------------------------
        # Generic final comma-separated location.
        #
        # We do not require a university database.
        # --------------------------------------------------------

        parts = [
            part.strip()
            for part in clean.split(",")
            if part.strip()
        ]

        if len(parts) >= 2:

            # If the last part is short, it is likely a
            # country/state code or location.
            if (
                len(parts) == 2
                or len(parts[-1]) <= 20
            ):

                education.institution = (
                    ", ".join(
                        parts[:-1]
                    )
                )

                education.location = (
                    parts[-1]
                )

                return

        # --------------------------------------------------------
        # Fallback
        # --------------------------------------------------------

        education.institution = clean

    # ============================================================
    # LEVEL DETECTION
    # ============================================================

    @classmethod
    def _detect_level(
        cls,
        text: str,
    ) -> str:
        """
        Determine education level from the qualification header.

        Order matters: more specific qualifications are checked
        before generic ones.
        """

        clean = text.lower()

        for pattern, level in cls._LEVEL_PATTERNS:

            if pattern.search(clean):

                return level

        return ""

    # ============================================================
    # KEYWORD EXTRACTION
    # ============================================================

    @classmethod
    def _extract_keywords(
        cls,
        education: Education,
    ) -> list[str]:
        """
        Generate lightweight education keywords.

        This is NOT ontology extraction.

        It only captures obvious semantic terms from the
        degree/major.
        """

        text = " ".join(
            value
            for value in (
                education.degree,
                education.major,
            )
            if value
        ).lower()

        keywords: list[str] = []

        known_terms = (
            "data analytics",
            "business administration",
            "chemistry",
            "organic chemistry",
            "computer science",
            "engineering",
            "food science",
            "food technology",
            "quality assurance",
            "food safety",
            "management",
            "accounting",
            "economics",
            "marketing",
            "finance",
        )

        for term in known_terms:

            if term in text:

                keywords.append(
                    term
                )

        return keywords

    # ============================================================
    # CONFIDENCE
    # ============================================================

    @staticmethod
    def _calculate_confidence(
        result: EducationSectionResult,
    ) -> float:
        """
        Calculate a simple structural confidence score.

        This intentionally does not pretend to be an ML probability.
        """

        if not result.records:

            return 0.0

        scores = []

        for education in result.records:

            score = 0.0

            if education.degree:
                score += 0.30

            if education.institution:
                score += 0.30

            if education.level:
                score += 0.15

            if education.description:
                score += 0.10

            if education.location:
                score += 0.10

            if education.major:
                score += 0.05

            scores.append(
                min(score, 1.0)
            )

        if not scores:

            return 0.0

        return round(
            sum(scores) / len(scores),
            3,
        )