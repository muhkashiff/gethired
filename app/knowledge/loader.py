import json
from pathlib import Path


class KnowledgeLoader:

    def __init__(self):

        self.base = Path(__file__).parent / "data"

    def load(self, filename):

        with open(self.base / filename, encoding="utf-8") as f:
            return json.load(f)

    def skills(self):
        return self.load("skills.json")

    def technologies(self):
        return self.load("technologies.json")

    def certifications(self):
        return self.load("certifications.json")

    def degrees(self):
        return self.load("degrees.json")

    def industries(self):
        return self.load("industries.json")

    def job_titles(self):
        return self.load("job_titles.json")

    def soft_skills(self):
        return self.load("soft_skills.json")