from app.parser.resume_normalizer import normalize_heading
from app.parser.section_dictionary import SECTION_HEADERS

heading = "PROFESSIONAL CERTIFICATIONS & ACCREDITATIONS"

print("Normalized heading:")
print(normalize_heading(heading))
print()

print("Certification headings:")

for h in SECTION_HEADERS["certifications"]:
    print(normalize_heading(h))