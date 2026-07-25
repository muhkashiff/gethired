from dataclasses import dataclass, field

from .personal_information import PersonalInformation
from .experience import Experience
from .education import Education
from .certification import Certification
from .project import Project
from .language import Language
from .award import Award
from .publication import Publication
from .achievement import Achievement
from .membership import Membership
from .reference import Reference
from .skill import Skill


@dataclass
class Resume:

    personal_information: PersonalInformation = field(default_factory=PersonalInformation)

    summary: str = ""

    skills: list[Skill] = field(default_factory=list)

    experience: list[Experience] = field(default_factory=list)

    education: list[Education] = field(default_factory=list)

    certifications: list[Certification] = field(default_factory=list)

    projects: list[Project] = field(default_factory=list)

    awards: list[Award] = field(default_factory=list)

    achievements: list[Achievement] = field(default_factory=list)

    memberships: list[Membership] = field(default_factory=list)

    publications: list[Publication] = field(default_factory=list)

    languages: list[Language] = field(default_factory=list)

    references: list[Reference] = field(default_factory=list)