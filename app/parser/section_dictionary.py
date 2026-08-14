"""
GetHired
Section Dictionary

Enterprise V5

Canonical resume section names and their supported aliases.

The SectionDetector uses this dictionary only to identify
resume section boundaries.

It does NOT interpret the content of a section.
"""

SECTION_HEADERS = {

    # =========================================================
    # SUMMARY
    # =========================================================

    "summary": [

        "SUMMARY",
        "PROFILE",
        "PROFESSIONAL SUMMARY",
        "CAREER SUMMARY",
        "PROFILE SUMMARY",
        "EXECUTIVE SUMMARY",
        "PROFESSIONAL PROFILE",
        "ABOUT ME",
        "OBJECTIVE",
        "CAREER OBJECTIVE",
    ],

    # =========================================================
    # SKILLS
    # =========================================================

    "skills": [

        "SKILLS",
        "TECHNICAL SKILLS",
        "CORE SKILLS",
        "KEY SKILLS",
        "CORE COMPETENCIES",
        "COMPETENCIES",
        "AREAS OF EXPERTISE",
        "TECHNICAL EXPERTISE",

        "CORE LEADERSHIP COMPETENCIES",
        "LEADERSHIP COMPETENCIES",

        "TECHNOLOGY",
        "TECHNOLOGIES",

        "TECHNICAL PROFICIENCIES",
        "TOOLS",
        "SOFTWARE",
        "SOFTWARE SKILLS",
        "COMPUTER SKILLS",
    ],

    # =========================================================
    # EXPERIENCE
    # =========================================================

    "experience": [

        "EXPERIENCE",
        "WORK EXPERIENCE",
        "PROFESSIONAL EXPERIENCE",
        "EMPLOYMENT",
        "EMPLOYMENT HISTORY",
        "CAREER HISTORY",
        "WORK HISTORY",
    ],

    # =========================================================
    # EDUCATION
    # =========================================================

    "education": [

        "EDUCATION",
        "ACADEMIC BACKGROUND",
        "ACADEMIC QUALIFICATIONS",
        "EDUCATIONAL QUALIFICATIONS",
    ],

    # =========================================================
    # CERTIFICATIONS / TRAINING
    # =========================================================

    "certifications": [

        "CERTIFICATIONS",
        "CERTIFICATES",
        "PROFESSIONAL CERTIFICATIONS",
        "PROFESSIONAL CERTIFICATES",

        "LICENSES",
        "LICENSES & CERTIFICATIONS",

        "ACCREDITATIONS",

        "PROFESSIONAL CERTIFICATIONS ACCREDITATIONS",
        "PROFESSIONAL CERTIFICATIONS & ACCREDITATIONS",

        "TRAINING",
        "TRAININGS",
        "TRAINING & CERTIFICATIONS",

        "COURSES",
    ],

    # =========================================================
    # PROJECTS
    # =========================================================

    "projects": [

        "PROJECTS",
        "KEY PROJECTS",
        "PROJECT EXPERIENCE",
    ],

    # =========================================================
    # AWARDS / RECOGNITION
    # =========================================================

    "awards": [

        "AWARDS",
        "HONOURS",
        "HONORS",
        "ACHIEVEMENTS",
        "RECOGNITION",
    ],

    # =========================================================
    # PUBLICATIONS / RESEARCH
    # =========================================================

    "publications": [

        "PUBLICATIONS",
        "RESEARCH",
        "PAPERS",
    ],

    # =========================================================
    # LANGUAGES
    # =========================================================

    "languages": [

        "LANGUAGES",
        "LANGUAGE",
    ],

    # =========================================================
    # REFERENCES
    # =========================================================

    "references": [

        "REFERENCES",
        "REFEREES",
    ],
}