from dataclasses import dataclass, field

from .personal_information import PersonalInformation
from .experience import Experience
from .education import Education
from .certification import Certification
from .project import Project


@dataclass
class Resume:

    personal_information: PersonalInformation = field(default_factory=PersonalInformation)

    summary: str = ""

    skills: list = field(default_factory=list)

    experiences: list[Experience] = field(default_factory=list)

    education: list[Education] = field(default_factory=list)

    certifications: list[Certification] = field(default_factory=list)

    projects: list[Project] = field(default_factory=list)

    languages: list = field(default_factory=list)