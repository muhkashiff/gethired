from .jd_model import JobDescription

from app.ats.skill_extractor import ATSKnowledgeBase

from app.ats.experience_analyzer import ExperienceAnalyzer

from app.ats.certification_analyzer import CertificationAnalyzer

class JDBuilder:

    def build(self, jd_text):

        jd = JobDescription()

        kb = ATSKnowledgeBase()

        jd.skills = kb.extract_skills(jd_text)

        jd.certifications = CertificationAnalyzer().extract(jd_text)

        jd.experience_required = ExperienceAnalyzer().extract_required_years(jd_text)

        return jd