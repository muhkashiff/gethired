"""
ATS Analysis Policy
===================

Phase 5 policy contract.

The policy contains deterministic configuration for ATS analysis.

The policy is owned by ATSResumeAnalyzer and is NOT part of
ATSResumeAnalysisRequest.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ATSAnalysisPolicy:
    """
    Immutable configuration for Phase 5 ATS analysis.
    """

    required_sections: tuple[str, ...] = (
        "Professional Summary",
        "Experience",
        "Education",
        "Skills",
    )

    max_line_length: int = 180

    minimum_quantifications: int = 3

    score_weights: Mapping[str, float] = field(
        default_factory=lambda: {
            "keyword": 0.25,
            "section": 0.15,
            "formatting": 0.10,
            "readability": 0.10,
            "terminology": 0.15,
            "quantification": 0.10,
            "parseability": 0.15,
        }
    )

    def __post_init__(self) -> None:
        sections = tuple(
            str(section).strip()
            for section in self.required_sections
            if str(section).strip()
        )

        object.__setattr__(
            self,
            "required_sections",
            sections,
        )

        if self.max_line_length <= 0:
            raise ValueError(
                "max_line_length must be greater than zero."
            )

        if self.minimum_quantifications < 0:
            raise ValueError(
                "minimum_quantifications cannot be negative."
            )

        raw_weights = dict(
            self.score_weights
        )

        expected_keys = {
            "keyword",
            "section",
            "formatting",
            "readability",
            "terminology",
            "quantification",
            "parseability",
        }

        if set(raw_weights) != expected_keys:
            raise ValueError(
                "score_weights must contain exactly: "
                "keyword, section, formatting, readability, "
                "terminology, quantification, parseability."
            )

        normalized_weights = {}

        for name, value in raw_weights.items():

            try:
                numeric = float(value)
            except (
                TypeError,
                ValueError,
            ) as exc:
                raise ValueError(
                    f"score weight {name!r} must be numeric."
                ) from exc

            if numeric < 0.0:
                raise ValueError(
                    f"score weight {name!r} cannot be negative."
                )

            normalized_weights[name] = numeric

        total = sum(
            normalized_weights.values()
        )

        if total <= 0.0:
            raise ValueError(
                "score_weights must contain a positive total weight."
            )

        if abs(total - 1.0) > 1e-9:
            raise ValueError(
                "score_weights must sum to 1.0."
            )

        object.__setattr__(
            self,
            "score_weights",
            MappingProxyType(
                normalized_weights
            ),
        )


__all__ = [
    "ATSAnalysisPolicy",
]