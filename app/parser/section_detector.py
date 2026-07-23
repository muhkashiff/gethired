"""
Section Detector

Detects common resume sections and organizes
content into structured categories.
"""

import re

import re

def detect(self, paragraphs):

    sections = {}

    current_section = "header"

    sections[current_section] = []

    for paragraph in paragraphs:

        text = paragraph.strip()

        # Normalize heading
        normalized = re.sub(
            r"[^a-z0-9 ]",
            "",
            text.lower()
        ).strip()

        found = False

        for section, names in self.HEADINGS.items():

            if normalized in names:

                current_section = section

                if current_section not in sections:
                    sections[current_section] = []

                found = True

                break

        if not found:

            sections[current_section].append(text)

    return sections


class SectionDetector:
    """
    Detect resume sections.
    """

    HEADINGS = {

    "summary": [
        "summary",
        "professional summary",
        "career summary",
        "profile",
        "objective"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical expertise",
        "core competencies",
        "core leadership competencies",
        "key skills",
        "technical proficiencies",
        "technology",
        "software",
        "tools"
    ],

    "experience": [
        "experience",
        "professional experience",
        "work experience",
        "employment history",
        "career history",
        "employment"
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ],

    "certifications": [
        "certifications",
        "professional certifications",
        "professional certifications accreditations",
        "licenses",
        "training",
        "accreditations"
    ],

    "projects": [
        "projects",
        "key projects"
    ],

    "languages": [
        "languages"
    ]
}

    def detect(self, paragraphs):

        sections = {}

        current_section = "header"

        sections[current_section] = []

        for paragraph in paragraphs:

            text = paragraph.strip()

            lower = text.lower()

            found = False

            for section, names in self.HEADINGS.items():

                if lower in names:

                    current_section = section

                    sections[current_section] = []

                    found = True

                    break

            if not found:

                sections[current_section].append(text)

        return sections