from dataclasses import dataclass, field
from typing import List


@dataclass
class JobDescription:

    title: str = ""

    company: str = ""

    summary: str = ""

    skills: List[str] = field(default_factory=list)

    technologies: List[str] = field(default_factory=list)

    certifications: List[str] = field(default_factory=list)

    education: List[str] = field(default_factory=list)

    experience_required: int = 0

    job_titles: List[str] = field(default_factory=list)

    industries: List[str] = field(default_factory=list)

    responsibilities: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)