from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Skill:

    # Canonical skill name
    name: str

    # Food Safety, Programming, Analytics...
    category: str = ""

    # ATS weight
    importance: int = 1

    # Estimated years
    years: float = 0.0

    # Beginner / Intermediate / Advanced / Expert
    level: str = ""

    # Skills / Experience / Certification / Project
    source: str = ""

    # Parser confidence
    confidence: float = 1.0

    # ATS Matching
    matched: bool = False

    score: float = 0.0

    # Knowledge Base
    aliases: List[str] = field(default_factory=list)

    found_in_jobs: List[str] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    normalized_name: Optional[str] = None