from app.parser import ResumeParser, ResumeBuilder

from app.jd_parser.jd_parser import JDParser
from app.jd_parser.jd_builder import JDBuilder

from app.matcher.ats_matcher import ATSMatcher


# -----------------------------
# Resume
# -----------------------------

resume_parser = ResumeParser(
    "uploads/project_2/resume_original.docx"
)

sections = resume_parser.sections()

resume = ResumeBuilder().build(sections)

# -----------------------------
# Job Description
# -----------------------------

with open("sample_jd.txt", encoding="utf-8") as f:
    jd_text = f.read()

job = JDBuilder().build(jd_text)

# Temporary: use extracted keywords as required skills
job.required_skills = job.keywords

# -----------------------------
# Match
# -----------------------------

result = ATSMatcher().match(
    resume,
    job
)

print("=" * 60)
print("ATS RESULT")
print("=" * 60)

print("Overall Score :", result.overall_score)

print()

print("Skill Score :", result.skill_score)

print()

print("Matched Skills")

for s in result.matched_skills:
    print("✓", s)

print()

print("Missing Skills")

for s in result.missing_skills:
    print("✗", s)

print()

print("Recommendations")

for r in result.recommendations:
    print("-", r)