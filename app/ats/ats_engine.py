from .skill_matcher import SkillMatcher
from .technology_detector import TechnologyDetector
from .certification_detector import CertificationDetector
from .job_title_detector import JobTitleDetector
from .company_detector import CompanyDetector
from .experience_counter import ExperienceCounter
from .industry_detector import IndustryDetector
from .seniority_detector import SeniorityDetector
from .keyword_ranker import KeywordRanker


class ATSEngine:

    def __init__(self):

        self.skill_matcher = SkillMatcher()

        self.technology_detector = TechnologyDetector()

        self.certification_detector = CertificationDetector()

        self.job_detector = JobTitleDetector()

        self.company_detector = CompanyDetector()

        self.experience_counter = ExperienceCounter()

        self.industry_detector = IndustryDetector()

        self.seniority_detector = SeniorityDetector()

        self.keyword_ranker = KeywordRanker()

    def analyze(self, resume):

        result = {}

        result["skills"] = self.skill_matcher.find(resume)

        result["technologies"] = self.technology_detector.find(resume)

        result["certifications"] = self.certification_detector.find(resume)

        result["job_titles"] = self.job_detector.find(resume)

        result["companies"] = self.company_detector.find(resume)

        result["experience"] = self.experience_counter.calculate(resume)

        result["industry"] = self.industry_detector.find(resume)

        result["seniority"] = self.seniority_detector.find(resume)

        result["keywords"] = self.keyword_ranker.rank(resume)

        return result