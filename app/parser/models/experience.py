from dataclasses import dataclass, field

@dataclass
class Experience:

    job_title: str = ""

    company: str = ""

    location: str = ""

    start_date: str = ""

    end_date: str = ""

    duration_years: float = 0

    industry: str = ""

    management_level: bool = False

    responsibilities: list = field(default_factory=list)

    achievements: list = field(default_factory=list)

    technologies: list = field(default_factory=list)

    skills: list = field(default_factory=list)