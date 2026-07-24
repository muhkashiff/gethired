"""
resume_model.py

Production Grade Resume Model
"""

from dataclasses import dataclass, field
from typing import List


# ======================================================
# PERSONAL INFORMATION
# ======================================================

@dataclass
class PersonalInformation:

    name: str = ""

    email: str = ""

    phone: str = ""

    linkedin: str = ""

    github: str = ""

    address: str = ""


# ======================================================
# EXPERIENCE
# ======================================================

@dataclass
class Experience:

    job_title: str = ""

    company: str = ""

    location: str = ""

    start_date: str = ""

    end_date: str = ""

    duration_years: float = 0

    employment_type: str = ""

    bullets: List[str] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)


# ======================================================
# EDUCATION
# ======================================================

@dataclass
class Education:

    degree: str = ""

    institution: str = ""

    location: str = ""

    graduation_year: str = ""

    description: List[str] = field(default_factory=list)


# ======================================================
# CERTIFICATION
# ======================================================

@dataclass
class Certification:

    name: str = ""

    organization: str = ""

    year: str = ""


# ======================================================
# PROJECT
# ======================================================

@dataclass
class Project:

    name: str = ""

    description: str = ""

    technologies: List[str] = field(default_factory=list)


# ======================================================
# LANGUAGE
# ======================================================

@dataclass
class Language:

    language: str = ""

    proficiency: str = ""


# ======================================================
# AWARD
# ======================================================

@dataclass
class Award:

    title: str = ""

    organization: str = ""

    year: str = ""


# ======================================================
# RESUME
# ======================================================

@dataclass
class Resume:

    personal_information: PersonalInformation = field(
        default_factory=PersonalInformation
    )

    summary: str = ""

    skills: List[str] = field(default_factory=list)

    experience: List[Experience] = field(default_factory=list)

    education: List[Education] = field(default_factory=list)

    certifications: List[Certification] = field(default_factory=list)

    projects: List[Project] = field(default_factory=list)

    languages: List[Language] = field(default_factory=list)

    achievements: List[str] = field(default_factory=list)

    awards: List[Award] = field(default_factory=list)