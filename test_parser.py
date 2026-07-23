from app.parser import ResumeParser
from app.parser import ResumeBuilder

parser = ResumeParser(
    "uploads/project_2/resume_original.docx"
)

sections = parser.sections()

print("=" * 70)
print("SECTIONS DETECTED")
print("=" * 70)

for key, value in sections.items():

    print(f"\n[{key.upper()}]")

    print("-" * 40)

    for line in value:
        print(line)

builder = ResumeBuilder()

resume = builder.build(sections)

print("\n")
print("=" * 70)
print("PERSONAL INFORMATION")
print("=" * 70)

print(f"Name      : {resume.personal_information.name}")
print(f"Email     : {resume.personal_information.email}")
print(f"Phone     : {resume.personal_information.phone}")
print(f"LinkedIn  : {resume.personal_information.linkedin}")
print(f"GitHub    : {resume.personal_information.github}")
print(f"Location  : {resume.personal_information.address}")

print("\n")
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(resume.summary)

print("\n")
print("=" * 70)
print("SKILLS")
print("=" * 70)

for skill in resume.skills:
    print(f"• {skill}")

print("\n")
print("=" * 70)
print("EXPERIENCE")
print("=" * 70)

for exp in resume.experience:
    print(f"• {exp}")

print("\n")
print("=" * 70)
print("EDUCATION")
print("=" * 70)

for edu in resume.education:
    print(f"• {edu}")

print("\n")
print("=" * 70)
print("CERTIFICATIONS")
print("=" * 70)

for cert in resume.certifications:
    print(f"• {cert}")

print("\n")
print("=" * 70)
print("PROJECTS")
print("=" * 70)

for project in resume.projects:
    print(f"• {project}")

print("\n")
print("=" * 70)
print("LANGUAGES")
print("=" * 70)

for language in resume.languages:
    print(f"• {language}")