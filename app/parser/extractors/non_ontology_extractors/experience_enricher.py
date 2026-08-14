"""
GetHired
Experience Enricher

Adds

• Skills
• Technologies
• Keywords
• Industry
• Seniority

to each Experience object.
"""

import re

from app.knowledge.skill_loader import SkillKnowledge


class ExperienceEnricher:

    def __init__(self):

        self.skill_db = SkillKnowledge()

    # ==========================================================
    # Main
    # ==========================================================

    def enrich(self, experience):

        text = " ".join(

            experience.responsibilities
            + experience.achievements

        )

        experience.skills = self.extract_skills(text)

        experience.technologies = self.extract_technologies(text)

        experience.keywords = self.extract_keywords(text)

        experience.industry = self.detect_industry(text)

        experience.seniority = self.detect_seniority(
            experience.title,
            text
        )

        return experience

    # ==========================================================
    # Skills
    # ==========================================================

    def extract_skills(self, text):

        matches = self.skill_db.lookup_all(text)

        skills = []

        seen = set()

        for record in matches:

            name = record.get("canonical_name")

            if not name:
                continue

            key = name.lower()

            if key in seen:
                continue

            seen.add(key)

            skills.append(name)

        return skills

    # ==========================================================
    # Technologies
    # ==========================================================

    def extract_technologies(self, text):

        technologies = []

        known = [

            "SAP",
            "SAP QM",
            "Power BI",
            "Excel",
            "Word",
            "Outlook",
            "Python",
            "SQL",
            "Tableau",
            "Minitab",
            "Power Query",
            "Power Pivot",
            "HACCP",
            "FSSC 22000",
            "ISO 9001",
            "BRCGS",
            "PCQI"

        ]

        lower = text.lower()

        for tech in known:

            if tech.lower() in lower:

                technologies.append(tech)

        return sorted(set(technologies))

    # ==========================================================
    # Keywords
    # ==========================================================

    def extract_keywords(self, text):

        words = re.findall(

            r"[A-Za-z][A-Za-z0-9&+\- ]{3,}",

            text

        )

        stop = {

            "with",
            "from",
            "that",
            "this",
            "their",
            "into",
            "using",
            "were",
            "have",
            "been",
            "through",
            "across"

        }

        keywords = []

        seen = set()

        for w in words:

            word = w.strip()

            if word.lower() in stop:
                continue

            if word.lower() in seen:
                continue

            seen.add(word.lower())

            keywords.append(word)

        return keywords[:40]

    # ==========================================================
    # Industry
    # ==========================================================

    def detect_industry(self, text):

        lower = text.lower()

        if any(

            x in lower for x in [

                "food",
                "juice",
                "beverage",
                "haccp",
                "fssc",
                "quality",
                "manufacturing"

            ]

        ):

            return "Food & Beverage"

        if any(

            x in lower for x in [

                "retail",
                "customer",
                "cash",
                "store"

            ]

        ):

            return "Retail"

        if any(

            x in lower for x in [

                "python",
                "sql",
                "analytics",
                "machine learning"

            ]

        ):

            return "Data Analytics"

        return ""

    # ==========================================================
    # Seniority
    # ==========================================================

    def detect_seniority(self, title, text):

        value = (title + " " + text).lower()

        if any(

            x in value for x in [

                "director",
                "head",
                "chief",
                "vp"

            ]

        ):

            return "Executive"

        if any(

            x in value for x in [

                "manager",
                "lead",
                "supervisor"

            ]

        ):

            return "Management"

        if any(

            x in value for x in [

                "senior",
                "principal"

            ]

        ):

            return "Senior"

        return "Professional"