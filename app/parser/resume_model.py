from dataclasses import dataclass, field
from typing import List


@dataclass
class PersonalInformation:
    name: str = ""
    email: str = ""
    phone: str = ""
    linkedin: str = ""
    github: str = ""
    address: str = ""


@dataclass
class Resume:

    personal_information: PersonalInformation = field(default_factory=PersonalInformation)

    summary: str = ""

    skills: List[str] = field(default_factory=list)

    experience: List[str] = field(default_factory=list)

    education: List[str] = field(default_factory=list)

    certifications: List[str] = field(default_factory=list)

    projects: List[str] = field(default_factory=list)

    languages: List[str] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)