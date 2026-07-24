from app.parser import ResumeParser, ResumeBuilder
from app.ats import ATSEngine

parser = ResumeParser("uploads/project_2/resume_original.docx")
sections = parser.sections()

builder = ResumeBuilder()
resume = builder.build(sections)

engine = ATSEngine()

results = engine.analyze(resume)

print("=" * 60)
print("ATS ANALYSIS")
print("=" * 60)

for key, value in results.items():
    print(f"\n{key.upper()}")
    print(value)