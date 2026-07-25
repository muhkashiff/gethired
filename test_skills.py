from app.parser.readers.resume_reader import ResumeReader
from app.parser.section_detector import SectionDetector
from app.parser.extractors.skills_extractor import SkillsExtractor

RESUME = r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"

reader = ResumeReader()
lines = reader.read(RESUME)

detector = SectionDetector()
sections = detector.detect(lines)

print("=" * 70)
print("SKILLS SECTION")
print("=" * 70)

print(sections.get("skills", []))

extractor = SkillsExtractor()

skills = extractor.extract(
    sections.get("skills", [])
)

print("\n")
print("=" * 70)
print("TOTAL SKILLS:", len(skills))
print("=" * 70)

for i, skill in enumerate(skills, 1):

    print(f"\nSkill #{i}")
    print("-" * 40)

    print("Name           :", skill.name)
    print("Category       :", skill.category)
    print("Level          :", skill.level)
    print("Years          :", skill.years)
    print("Confidence     :", skill.confidence)
    print("Matched        :", skill.matched)
    print("Score          :", skill.score)
    print("Normalized     :", skill.normalized_name)
    print("Raw Text       :", skill.raw_text)