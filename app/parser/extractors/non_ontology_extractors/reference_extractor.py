# Reference Extractor

"""
GetHired
Enterprise V5

Reference Extractor
"""

from __future__ import annotations

import re

from .base_non_ontology_extractor import BaseNonOntologyExtractor


class ReferenceExtractor(BaseNonOntologyExtractor):

    def _extract(self, content: list[str]):

        references = []

        for line in content:

            text = line.strip()

            if not text:
                continue

            if self._is_available_on_request(text):

                references.append(
                    {
                        "name": "",
                        "title": "",
                        "company": "",
                        "email": "",
                        "phone": "",
                        "available_on_request": True,
                        "raw": text,
                    }
                )

                continue

            references.append(
                self._parse_reference(text)
            )

        return references

    def _is_available_on_request(self, text):

        normalized = re.sub(
            r"[^a-z ]",
            " ",
            text.lower(),
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        ).strip()

        return (
            "available on request"
            in normalized
        )

    def _parse_reference(self, text):

        email_match = re.search(
            r"\b[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )

        phone_match = re.search(
            r"\+?\d[\d\s().-]{6,}\d",
            text,
        )

        return {
            "name": text,
            "title": "",
            "company": "",
            "email": (
                email_match.group(0)
                if email_match
                else ""
            ),
            "phone": (
                phone_match.group(0)
                if phone_match
                else ""
            ),
            "available_on_request": False,
            "raw": text,
        }

