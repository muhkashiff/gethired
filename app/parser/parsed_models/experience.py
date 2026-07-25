from dataclasses import dataclass, field
from typing import List


@dataclass
class Experience:

    # ==========================================
    # Header Information
    # ==========================================

    title: str = ""

    company: str = ""

    location: str = ""

    # ==========================================
    # Employment Dates
    # ==========================================

    start_year: int = 0

    end_year: int = 0

    current_job: bool = False

    duration: float = 0.0

    # ==========================================
    # Experience Content
    # ==========================================

    responsibilities: List[str] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)

    technologies: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)

    # ==========================================
    # Classification
    # ==========================================

    industry: str = ""

    seniority: str = ""

    confidence: float = 0.0

    raw_header: str = ""

    raw_lines: List[str] = field(default_factory=list)