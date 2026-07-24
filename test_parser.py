from app.parser import ResumeParser, ResumeBuilder

# Path to your resume
resume_path = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"

# Parse Resume
parser = ResumeParser()
sections = parser.parse(resume_path)

# Build Resume Object
builder = ResumeBuilder()
resume = builder.build(sections)

print("=" * 60)
print("PERSONAL INFORMATION")
print("=" * 60)

print("Name :", resume.personal_information.name)
print("Email:", resume.personal_information.email)
print("Phone:", resume.personal_information.phone)

print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

print(resume.summary)

print()

print("=" * 60)
print("SKILLS")
print("=" * 60)

for skill in resume.skills:
    print(skill)

print()

print("=" * 60)
print("EXPERIENCE")
print("=" * 60)

for exp in resume.experience:
    print(exp)

print()

print("=" * 60)
print("EDUCATION")
print("=" * 60)

for edu in resume.education:
    print(edu)

print()

print("=" * 60)
print("CERTIFICATIONS")
print("=" * 60)

for cert in resume.certifications:
    print(cert)