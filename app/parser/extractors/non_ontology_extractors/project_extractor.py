# Project Extractor


"""
GetHired
Enterprise V5

Project Extractor
"""

from __future__ import annotations

from .base_non_ontology_extractor import BaseNonOntologyExtractor


class ProjectExtractor(BaseNonOntologyExtractor):

    def _extract(self, content: list[str]):

        projects = []

        current = None

        for line in content:

            text = line.strip()

            if not text:
                continue

            if self._looks_like_project_header(text):

                if current:
                    projects.append(current)

                current = {
                    "title": text,
                    "description": [],
                    "technologies": [],
                    "achievements": [],
                    "raw": [],
                }

            elif current:

                current["raw"].append(text)

                if self._is_achievement(text):

                    current["achievements"].append(
                        self._clean(text)
                    )

                else:

                    current["description"].append(
                        self._clean(text)
                    )

            else:

                current = {
                    "title": "",
                    "description": [
                        self._clean(text)
                    ],
                    "technologies": [],
                    "achievements": [],
                    "raw": [text],
                }

        if current:
            projects.append(current)

        return projects

    def _looks_like_project_header(self, text):

        return (
            text.lower().startswith(
                (
                    "project:",
                    "project -",
                    "project –",
                    "project —",
                )
            )
        )

    def _is_achievement(self, text):

        return text.lower().startswith(
            (
                "achievement",
                "result",
                "successfully",
            )
        )

    def _clean(self, text):

        return text.lstrip(
            "•▪●-* "
        ).strip()

