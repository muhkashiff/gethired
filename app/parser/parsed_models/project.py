from dataclasses import dataclass, field
from typing import List


@dataclass
class Project:
    name: str = ""
    description: str = ""
    technologies: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    url: str = ""
    role: str = ""