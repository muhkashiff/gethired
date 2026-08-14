"""
GetHired
Enterprise V5

Education Section Result
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from app.parser.parsed_models.education import Education


@dataclass
class EducationSectionResult:

    # ============================================================
    # SECTION IDENTITY
    # ============================================================

    section_name: str = "education"

    # ============================================================
    # EXTRACTED RECORDS
    # ============================================================

    records: List[Education] = field(
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

    def add(self, education: Education) -> None:

        if education is not None:
            self.records.append(education)

    def __iter__(self):

        return iter(self.records)

    def __len__(self):

        return len(self.records)

    def __repr__(self):

        return (
            "EducationSectionResult("
            f"section_name={self.section_name!r}, "
            f"records={len(self.records)!r}, "
            f"success={self.success!r}, "
            f"confidence={self.confidence!r}"
            ")"
        )