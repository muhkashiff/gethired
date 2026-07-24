import re


class SkillExtractor:

    def __init__(self):

        self.skill_database = {

            # -----------------------
            # Quality
            # -----------------------
            "haccp",
            "iso 9001",
            "iso22000",
            "fssc 22000",
            "brcgs",
            "gmp",
            "cgmp",
            "ssop",
            "ccp",
            "oprp",
            "prp",
            "food safety",
            "quality assurance",
            "quality management",
            "quality management system",
            "food safety management system",

            # -----------------------
            # Data
            # -----------------------
            "python",
            "sql",
            "power bi",
            "tableau",
            "excel",
            "power query",
            "power pivot",
            "machine learning",
            "statistics",
            "data analytics",
            "data analysis",

            # -----------------------
            # Software
            # -----------------------
            "sap",
            "sap qm",
            "minitab",
            "word",
            "outlook",
            "office 365",

            # -----------------------
            # Business
            # -----------------------
            "leadership",
            "procurement",
            "inventory management",
            "supply chain",
            "root cause analysis",
            "continuous improvement",
            "internal audit",
            "team management",
            "problem solving",

            # -----------------------
            # Manufacturing
            # -----------------------
            "kpi",
            "lean",
            "six sigma",
            "spc",
            "cp",
            "cpk",
            "capa"

        }


    def extract(self, sections):

        text = ""

        for section in sections.values():

            text += "\n".join(section)

            text += "\n"

        text = text.lower()

        found = []

        for skill in self.skill_database:

            if skill in text:

                found.append(skill)

        return sorted(list(set(found)))