# Language Extractor


"""
GetHired
Enterprise V5

Language Extractor
"""

from __future__ import annotations

import re

from .base_non_ontology_extractor import BaseNonOntologyExtractor


class LanguageExtractor(BaseNonOntologyExtractor):

    def _extract(self, content: list[str]):

        results = []

        text = " ".join(content)

        parts = re.split(
            r"\s*\|\s*",
            text,
        )

        for part in parts:

            value = part.strip()

            if not value:
                continue

            match = re.match(
                r"(.+?)\s*[–—-]\s*(.+)",
                value,
            )

            if match:

                language = (
                    match.group(1).strip()
                )

                proficiency = (
                    match.group(2).strip()
                )

            else:

                language = value
                proficiency = ""

            results.append(
                {
                    "language": language,
                    "proficiency": proficiency,
                    "raw": value,
                }
            )

        return results

