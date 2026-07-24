from dataclasses import dataclass, field

@dataclass
class Project:

    title: str = ""

    description: str = ""

    technologies: list = field(default_factory=list)