from .base_extractor import BaseExtractor
import re


class SkillsExtractor(BaseExtractor):

    def extract(self, lines):

        skills = []

        text = "\n".join(lines)

        # split on commas, semicolons, newlines or bullets
        chunks = re.split(r"[,;\n•]+", text)

        for chunk in chunks:

            skill = chunk.strip()

            if skill:

                skills.append(skill)

        return skills