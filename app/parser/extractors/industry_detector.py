"""
GetHired
Industry Detector
"""

from app.knowledge.industry_loader import IndustryKnowledge


class IndustryDetector:

    def __init__(self):

        self.knowledge = IndustryKnowledge()

    # ==========================================================
    # Detect Industry
    # ==========================================================

    def detect(
        self,
        title="",
        company="",
        responsibilities=None,
        achievements=None,
        technologies=None,
        skills=None
    ):

        responsibilities = responsibilities or []
        achievements = achievements or []
        technologies = technologies or []
        skills = skills or []

        text = []

        text.append(title)
        text.append(company)

        text.extend(responsibilities)
        text.extend(achievements)

        # Technology objects or strings
        for tech in technologies:
            text.append(
                getattr(tech, "name", str(tech))
            )

        # Skill objects or strings
        for skill in skills:
            text.append(
                getattr(skill, "name", str(skill))
            )

        combined = " ".join(text)

        return self.knowledge.detect(combined)