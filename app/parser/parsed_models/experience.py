"""
GetHired
Enterprise V5

Experience Model
----------------
Strongly typed representation of one employment record.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Experience:

    # ============================================================
    # HEADER
    # ============================================================

    title: str = ""

    company: str = ""

    location: str = ""

    # ============================================================
    # DATES
    # ============================================================

    start_year: int = 0

    end_year: int = 0

    current_job: bool = False

    duration: float = 0.0

    # ============================================================
    # CONTENT
    # ============================================================

    responsibilities: List[str] = field(
        default_factory=list
    )

    achievements: List[str] = field(
        default_factory=list
    )

    # ============================================================
    # EXTRACTION / ENRICHMENT
    # ============================================================

    skills: List[str] = field(
        default_factory=list
    )

    technologies: List[str] = field(
        default_factory=list
    )

    keywords: List[str] = field(
        default_factory=list
    )

    # ============================================================
    # CLASSIFICATION
    # ============================================================

    industry: str = ""

    seniority: str = ""

    seniority_level: int = 0

    confidence: float = 0.0

    # ============================================================
    # TRACEABILITY
    # ============================================================

    raw_header: str = ""

    raw_lines: List[str] = field(
        default_factory=list
    )

    # ============================================================
    # REPRESENTATION
    # ============================================================

    def __repr__(self) -> str:

        return (
            "Experience("
            f"title={self.title!r}, "
            f"company={self.company!r}, "
            f"location={self.location!r}, "
            f"start_year={self.start_year!r}, "
            f"end_year={self.end_year!r}, "
            f"current_job={self.current_job!r}, "
            f"duration={self.duration!r}, "
            f"responsibilities={self.responsibilities!r}, "
            f"achievements={self.achievements!r}, "
            f"skills={self.skills!r}, "
            f"technologies={self.technologies!r}, "
            f"keywords={self.keywords!r}, "
            f"industry={self.industry!r}, "
            f"seniority={self.seniority!r}, "
            f"seniority_level={self.seniority_level!r}, "
            f"confidence={self.confidence!r}, "
            f"raw_header={self.raw_header!r}, "
            f"raw_lines={self.raw_lines!r}"
            ")"
        )