from pprint import pprint

from app.parser import ResumeParser

resume = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"

parser = ResumeParser()

sections = parser.parse(resume)

print("=" * 80)
print("SECTION KEYS")
print("=" * 80)

pprint(sections.keys())

print()
print("=" * 80)
print("CERTIFICATION SECTION")
print("=" * 80)

pprint(sections.get("certifications"))