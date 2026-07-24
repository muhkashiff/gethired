"""
GetHired
Resume Builder

Converts detected resume sections into a Resume object.
"""

from .resume_model import Resume

from .extractors import (
    ContactExtractor,
    SkillsExtractor,
    ExperienceExtractor,
    EducationExtractor,
    CertificationExtractor,
    LanguageExtractor,
    ProjectExtractor,
    AwardExtractor,
)


class ResumeBuilder:

    def __init__(self):

        self.contact_extractor = ContactExtractor()
        self.skills_extractor = SkillsExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.education_extractor = EducationExtractor()
        self.certification_extractor = CertificationExtractor()
        self.language_extractor = LanguageExtractor()
        self.project_extractor = ProjectExtractor()
        self.award_extractor = AwardExtractor()

    def build(self, sections):

        resume = Resume()

        # =====================================================
        # HEADER / PERSONAL INFORMATION
        # =====================================================

        header = sections.get("header", [])

        if header:
            resume.personal_information.name = header[0].strip()

        contact = self.contact_extractor.extract(header)

        resume.personal_information.email = contact.get("email", "")
        resume.personal_information.phone = contact.get("phone", "")
        resume.personal_information.linkedin = contact.get("linkedin", "")
        resume.personal_information.github = contact.get("github", "")
        resume.personal_information.address = contact.get("location", "")

        # =====================================================
        # SUMMARY
        # =====================================================

        resume.summary = " ".join(
            sections.get("summary", [])
        ).strip()

        # =====================================================
        # SKILLS
        # =====================================================

        resume.skills = self.skills_extractor.extract(
            sections.get("skills", [])
        )

        # =====================================================
        # EXPERIENCE
        # =====================================================

        resume.experience = self.experience_extractor.extract(
            sections.get("experience", [])
        )

        # =====================================================
        # EDUCATION
        # =====================================================

        resume.education = self.education_extractor.extract(
            sections.get("education", [])
        )

        # =====================================================
        # CERTIFICATIONS
        # =====================================================

        resume.certifications = self.certification_extractor.extract(
            sections.get("certifications", [])
        )

        # =====================================================
        # PROJECTS
        # =====================================================

        resume.projects = self.project_extractor.extract(
            sections.get("projects", [])
        )

        # =====================================================
        # AWARDS
        # =====================================================

        resume.awards = self.award_extractor.extract(
            sections.get("awards", [])
        )

        # =====================================================
        # LANGUAGES
        # =====================================================

        resume.languages = self.language_extractor.extract(
            sections.get("languages", [])
        )

        return resume