from app.parser.readers.resume_reader import ResumeReader
from app.parser.section_detector import SectionDetector
from app.parser.resume_builder import ResumeBuilder

# ----------------------------------------------------
# Resume Path
# ----------------------------------------------------

resume_path = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"
# Replace the filename above with the exact filename if different.

# ----------------------------------------------------
# Read Resume
# ----------------------------------------------------

reader = ResumeReader()
lines = reader.read(resume_path)

# ----------------------------------------------------
# Detect Sections
# ----------------------------------------------------

detector = SectionDetector()
sections = detector.detect(lines)

# ----------------------------------------------------
# Build Resume Object
# ----------------------------------------------------

builder = ResumeBuilder()
resume = builder.build(sections)

# ----------------------------------------------------
# Print Certifications
# ----------------------------------------------------

print("=" * 70)
print("TOTAL CERTIFICATIONS:", len(resume.certifications))
print("=" * 70)

for i, cert in enumerate(resume.certifications, start=1):

    print(f"\nCertification #{i}")
    print("-" * 50)
    print("Name            :", cert.name)
    print("Issuer          :", cert.issuer)
    print("Category        :", cert.category)
    print("Level           :", cert.level)
    print("Year            :", cert.year)
    print("Expiry          :", cert.expiry)
    print("Credential ID   :", cert.credential_id)
    print("Verification URL:", cert.verification_url)
    print("Confidence      :", cert.confidence)
    print("Matched         :", cert.matched)
    print("Score           :", cert.score)
    print("Normalized Name :", cert.normalized_name)
    print("Raw Text        :", cert.raw_text)