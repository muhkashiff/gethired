"""
GetHired
Resume Builder

Converts detected resume sections into a Resume object.
"""

from .resume_model import Resume
from .contact_extractor import ContactExtractor


class ResumeBuilder:

    def __init__(self):
        self.contact_extractor = ContactExtractor()

    def build(self, sections):

        resume = Resume()

        # =====================================================
        # HEADER / PERSONAL INFORMATION
        # =====================================================

        header = sections.get("header", [])

        # Name (first line of header)
        if header:
            resume.personal_information.name = header[0].strip()

        # Extract Contact Information
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

        parsed_skills = []

        for line in sections.get("skills", []):

            for skill in line.split(","):

                skill = skill.strip()

                if skill and skill not in parsed_skills:
                    parsed_skills.append(skill)

        resume.skills = parsed_skills

        # =====================================================
        # EXPERIENCE
        # =====================================================

        resume.experience = sections.get(
            "experience",
            []
        )

        # =====================================================
        # EDUCATION
        # =====================================================

        resume.education = sections.get(
            "education",
            []
        )

        # =====================================================
        # CERTIFICATIONS
        # =====================================================

        resume.certifications = sections.get(
            "certifications",
            []
        )

        # =====================================================
        # PROJECTS
        # =====================================================

        resume.projects = sections.get(
            "projects",
            []
        )

        # =====================================================
        # LANGUAGES
        # =====================================================

        resume.languages = sections.get(
            "languages",
            []
        )

        return resume