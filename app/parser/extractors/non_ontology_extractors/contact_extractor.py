# Contact Extractor

"""
GetHired
Enterprise V5

Contact Extractor

Extracts:
    email
    phone
    linkedin
    github
    location
"""

from __future__ import annotations

import re

from .base_non_ontology_extractor import BaseNonOntologyExtractor


class ContactExtractor(BaseNonOntologyExtractor):

    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    PHONE_PATTERN = re.compile(
        r"""
        (?:
            \+\d{1,3}[\s.-]?
        )?
        (?:
            \(\d{2,4}\)[\s.-]?
        )?
        \d{3,4}
        [\s.-]?
        \d{3,4}
        [\s.-]?
        \d{0,4}
        """,
        re.VERBOSE,
    )

    LINKEDIN_PATTERN = re.compile(
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/[^\s|]+",
        re.IGNORECASE,
    )

    GITHUB_PATTERN = re.compile(
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/[^\s|]+",
        re.IGNORECASE,
    )

    LOCATION_PATTERN = re.compile(
        r"(?:Location|Address)\s*:\s*([^|\n]+)",
        re.IGNORECASE,
    )

    def _extract(self, content: list[str]):

        text = "\n".join(content)

        email = self._first_match(
            self.EMAIL_PATTERN,
            text,
        )

        phone = self._extract_phone(text)

        linkedin = self._first_match(
            self.LINKEDIN_PATTERN,
            text,
        )

        github = self._first_match(
            self.GITHUB_PATTERN,
            text,
        )

        location_match = self.LOCATION_PATTERN.search(
            text
        )

        location = (
            location_match.group(1).strip()
            if location_match
            else ""
        )

        return {
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "location": location,
        }

    def _first_match(self, pattern, text):

        match = pattern.search(text)

        if not match:
            return ""

        return match.group(0).strip()

    def _extract_phone(self, text):

        for match in self.PHONE_PATTERN.finditer(text):

            value = match.group(0).strip()

            digits = re.sub(
                r"\D",
                "",
                value,
            )

            if len(digits) >= 7:
                return value

        return ""

