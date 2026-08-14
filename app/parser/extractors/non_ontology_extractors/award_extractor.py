# Award Extractor


"""
GetHired
Enterprise V5

Award Extractor
"""

from __future__ import annotations

from .base_non_ontology_extractor import BaseNonOntologyExtractor


class AwardExtractor(BaseNonOntologyExtractor):

    def _extract(self, content: list[str]):

        awards = []

        for line in content:

            text = line.strip()

            if not text:
                continue

            awards.append(
                {
                    "title": self._clean(text),
                    "raw": text,
                }
            )

        return awards

    def _clean(self, text):

        return text.lstrip(
            "•▪●-* "
        ).strip()

