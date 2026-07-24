from .match_result import MatchResult
from .skills_matcher import SkillsMatcher
from .recommendation_engine import RecommendationEngine


class ATSMatcher:

    def match(self, resume, job):

        result = MatchResult()

        skills = SkillsMatcher().match(
            resume.skills,
            job.required_skills
        )

        result.skill_score = skills["score"]
        result.matched_skills = skills["matched"]
        result.missing_skills = skills["missing"]

        # Placeholder scores until dedicated matchers are implemented
        result.experience_score = 100
        result.education_score = 100
        result.certification_score = 100
        result.technology_score = 100
        result.industry_score = 100

        weights = {
            "skills": 0.35,
            "experience": 0.25,
            "education": 0.10,
            "certification": 0.10,
            "technology": 0.10,
            "industry": 0.10,
        }

        result.overall_score = round(
            result.skill_score * weights["skills"] +
            result.experience_score * weights["experience"] +
            result.education_score * weights["education"] +
            result.certification_score * weights["certification"] +
            result.technology_score * weights["technology"] +
            result.industry_score * weights["industry"],
            2
        )

        result.recommendations = RecommendationEngine().generate(result)

        return result