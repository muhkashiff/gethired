"""
GetHired
Enterprise V5

Education Model
---------------
Strongly typed representation of one education record.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Education:
    """
    Represents one education record.

    Example
    -------
    Education(
        degree="M.Sc. Chemistry",
        major="Organic Chemistry",
        institution="University of the Punjab",
        location="Lahore, Pakistan",
        graduation_year=2010,
        level="master"
    )
    """

    # ============================================================
    # QUALIFICATION
    # ============================================================

    degree: str = ""

    major: str = ""

    # ============================================================
    # INSTITUTION
    # ============================================================

    institution: str = ""

    location: str = ""

    # ============================================================
    # DESCRIPTION
    # ============================================================

    description: str = ""

    # ============================================================
    # DATE
    # ============================================================

    graduation_year: int = 0

    # ============================================================
    # CLASSIFICATION
    # ============================================================

    level: str = ""

    keywords: List[str] = field(
        default_factory=list
    )

    # ============================================================
    # REPRESENTATION
    # ============================================================

    def __repr__(self) -> str:

        return (
            "Education("
            f"degree={self.degree!r}, "
            f"major={self.major!r}, "
            f"institution={self.institution!r}, "
            f"description={self.description!r}, "
            f"location={self.location!r}, "
            f"graduation_year={self.graduation_year!r}, "
            f"level={self.level!r}, "
            f"keywords={self.keywords!r}"
            ")"
        )