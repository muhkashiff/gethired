"""
GetHired
Skill Model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Skill:

    # ----------------------------------------
    # Display Name
    # ----------------------------------------
    name: str

    # ----------------------------------------
    # Analytics
    # Food Safety
    # Programming
    # Leadership
    # ERP
    # ----------------------------------------
    category: str = ""

    # ----------------------------------------
    # Beginner
    # Intermediate
    # Advanced
    # Expert
    # ----------------------------------------
    level: str = ""

    # ----------------------------------------
    # Years of experience
    # ----------------------------------------
    years: Optional[float] = None

    # ----------------------------------------
    # Parser confidence
    # ----------------------------------------
    confidence: float = 1.0

    # ----------------------------------------
    # ATS Matching
    # ----------------------------------------
    matched: bool = False

    score: float = 0.0

    # ----------------------------------------
    # Original resume text
    # ----------------------------------------
    raw_text: str = ""

    # ----------------------------------------
    # Canonical normalized form
    # ----------------------------------------
    normalized_name: Optional[str] = None