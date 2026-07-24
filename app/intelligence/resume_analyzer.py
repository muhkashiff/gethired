from .experience_analyzer import ExperienceAnalyzer
from .skills_analyzer import SkillsAnalyzer
from .education_analyzer import EducationAnalyzer
from .certification_analyzer import CertificationAnalyzer
from .metrics_analyzer import MetricsAnalyzer


class ResumeAnalyzer:

    def analyze(self, resume):

        return {

            "experience":
                ExperienceAnalyzer().analyze(
                    resume.experience
                ),

            "skills":
                SkillsAnalyzer().analyze(
                    resume.skills
                ),

            "education":
                EducationAnalyzer().analyze(
                    resume.education
                ),

            "certifications":
                CertificationAnalyzer().analyze(
                    resume.certifications
                ),

            "metrics":
                MetricsAnalyzer().analyze(
                    resume.experience
                )
        }