from app.parser import ResumeParser, ResumeBuilder

parser = ResumeParser(
    "uploads/project_2/resume_original.docx"
)

sections = parser.sections()

builder = ResumeBuilder()

resume = builder.build(sections)

print("=" * 60)
print("SKILLS")
print("=" * 60)

for skill in resume.skills:

    print("Name       :", skill.name)
    print("Category   :", skill.category)
    print("Importance :", skill.importance)
    print("Aliases    :", skill.aliases)
    print("-" * 40)