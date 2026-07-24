from dataclasses import dataclass, field
from typing import List


@dataclass
class Experience:

    title: str = ""

    company: str = ""

    location: str = ""

    start_year: int = 0

    end_year: int = 0

    duration: float = 0

    responsibilities: List[str] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)

    skills: List[str] = field(default_factory=list)

    technologies: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)

    industry: str = ""

    seniority: str = ""