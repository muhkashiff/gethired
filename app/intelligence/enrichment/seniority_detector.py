"""
Enterprise V5
Seniority Detection Intelligence

Responsibility
--------------
Determine the most likely career seniority level from an
already-built Resume object.

This component does NOT parse the DOCX.
This component does NOT modify ResumeBuilder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SeniorityResult:
    """
    Result returned by SeniorityDetector.
    """

    seniority: str = ""

    seniority_level: int = 0

    confidence: float = 0.0

    matched_titles: list[str] = field(
        default_factory=list
    )

    signals: list[str] = field(
        default_factory=list
    )


class SeniorityDetector:
    """
    Determines career seniority from Resume experience.

    Seniority levels
    ----------------
    1 = Entry
    2 = Junior
    3 = Mid
    4 = Senior
    5 = Lead
    6 = Manager
    7 = Director
    8 = Executive
    """

    TITLE_RULES = {
        "executive": [
            "chief",
            "ceo",
            "cfo",
            "coo",
            "cto",
            "president",
            "owner",
            "founder",
            "managing director",
        ],
        "director": [
            "director",
            "regional director",
            "operations director",
            "quality director",
            "plant director",
        ],
        "manager": [
            "manager",
            "store manager",
            "quality manager",
            "qa manager",
            "food safety manager",
            "operations manager",
            "plant manager",
            "production manager",
        ],
        "lead": [
            "lead",
            "team lead",
            "technical lead",
            "qa lead",
            "quality lead",
            "food safety lead",
        ],
        "senior": [
            "senior",
            "sr.",
            "sr ",
            "specialist",
            "senior specialist",
            "senior analyst",
        ],
        "mid": [
            "analyst",
            "engineer",
            "chemist",
            "coordinator",
            "administrator",
            "supervisor",
        ],
        "junior": [
            "junior",
            "jr.",
            "jr ",
            "associate",
            "assistant",
        ],
        "entry": [
            "intern",
            "internship",
            "trainee",
            "student",
        ],
    }

    LEVELS = {
        "entry": 1,
        "junior": 2,
        "mid": 3,
        "senior": 4,
        "lead": 5,
        "manager": 6,
        "director": 7,
        "executive": 8,
    }

    def detect(
        self,
        resume: Any,
    ) -> SeniorityResult:
        """
        Detect seniority from Resume.experience.
        """

        experiences = getattr(
            resume,
            "experience",
            [],
        ) or []

        if not experiences:
            return SeniorityResult(
                seniority="",
                seniority_level=0,
                confidence=0.0,
                signals=["No experience records available."],
            )

        scores: dict[str, float] = {
            level: 0.0
            for level in self.LEVELS
        }

        matched_titles: list[str] = []
        signals: list[str] = []

        for experience in experiences:

            title = str(
                getattr(
                    experience,
                    "title",
                    "",
                )
                or ""
            ).strip()

            if not title:
                continue

            normalized = title.lower()

            for level, keywords in self.TITLE_RULES.items():

                for keyword in keywords:

                    if keyword in normalized:

                        scores[level] += self._title_weight(
                            level
                        )

                        matched_titles.append(title)

                        signals.append(
                            f"Title '{title}' matched "
                            f"{level} signal '{keyword}'."
                        )

                        break

        # ------------------------------------------------------------
        # Additional experience signals
        # ------------------------------------------------------------

        total_duration = 0.0

        for experience in experiences:

            duration = getattr(
                experience,
                "duration",
                0,
            )

            try:
                total_duration += float(duration or 0)
            except (
                TypeError,
                ValueError,
            ):
                pass

        if total_duration >= 10:
            scores["senior"] += 1.5
            scores["lead"] += 1.5
            scores["manager"] += 1.5
            scores["director"] += 1.0

            signals.append(
                "10+ years of cumulative experience."
            )

        elif total_duration >= 5:
            scores["senior"] += 1.0
            scores["lead"] += 1.0

            signals.append(
                "5+ years of cumulative experience."
            )

        # ------------------------------------------------------------
        # Leadership signals
        # ------------------------------------------------------------

        leadership_terms = [
            "led",
            "managed",
            "directed",
            "governed",
            "spearheaded",
            "oversaw",
            "strategic",
            "cross-functional",
        ]

        leadership_count = 0

        for experience in experiences:

            responsibilities = getattr(
                experience,
                "responsibilities",
                [],
            ) or []

            achievements = getattr(
                experience,
                "achievements",
                [],
            ) or []

            text = " ".join(
                responsibilities + achievements
            ).lower()

            for term in leadership_terms:

                if term in text:
                    leadership_count += 1

        if leadership_count >= 5:

            scores["lead"] += 1.5
            scores["manager"] += 1.5
            scores["director"] += 0.5

            signals.append(
                "Strong leadership responsibility signals detected."
            )

        # ------------------------------------------------------------
        # Select highest score
        # ------------------------------------------------------------

        best_level = max(
            scores,
            key=scores.get,
        )

        best_score = scores[best_level]

        total_score = sum(
            scores.values()
        )

        if total_score <= 0:

            confidence = 0.0

        else:

            confidence = min(
                best_score / total_score,
                1.0,
            )

        return SeniorityResult(
            seniority=best_level,
            seniority_level=self.LEVELS[
                best_level
            ],
            confidence=round(
                confidence,
                3,
            ),
            matched_titles=list(
                dict.fromkeys(
                    matched_titles
                )
            ),
            signals=signals,
        )

    @staticmethod
    def _title_weight(
        level: str,
    ) -> float:

        weights = {
            "executive": 10.0,
            "director": 8.0,
            "manager": 6.0,
            "lead": 5.0,
            "senior": 4.0,
            "mid": 3.0,
            "junior": 2.0,
            "entry": 1.0,
        }

        return weights.get(
            level,
            1.0,
        )