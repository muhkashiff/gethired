"""
GetHired
Enterprise V5

Experience Section Result
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.parser.parsed_models.experience import Experience


@dataclass
class ExperienceSectionResult:

    # ============================================================
    # SECTION IDENTITY
    # ============================================================

    section_name: str = "experience"

    # ============================================================
    # EXTRACTED RECORDS
    # ============================================================

    records: List[Experience] = field(
        default_factory=list
    )

    # ============================================================
    # SOURCE
    # ============================================================

    source_section: Optional[object] = None

    # ============================================================
    # STATUS
    # ============================================================

    success: bool = True

    confidence: float = 0.0

    error: str = ""

    # ============================================================
    # CONVENIENCE
    # ============================================================

    @property
    def count(self) -> int:
        return len(self.records)

    @property
    def is_empty(self) -> bool:
        return not bool(self.records)

    def add(self, experience: Experience) -> None:

        if experience is not None:
            self.records.append(experience)

    def __iter__(self):

        return iter(self.records)

    def __len__(self):

        return len(self.records)

    def __repr__(self):

        return (
            "ExperienceSectionResult("
            f"section_name={self.section_name!r}, "
            f"records={len(self.records)!r}, "
            f"success={self.success!r}, "
            f"confidence={self.confidence!r}"
            ")"
        )