from app.parser import ResumeParser, ResumeBuilder

resume_file = r"uploads/project_2/resume_original.docx"

# Create parser
parser = ResumeParser()

# Parse resume into sections
sections = parser.parse(resume_file)

# Create builder
builder = ResumeBuilder()

# Build resume object
resume = builder.build(sections)

print("=" * 70)
print("CERTIFICATIONS")
print("=" * 70)

for cert in resume.certifications:
    print(cert)