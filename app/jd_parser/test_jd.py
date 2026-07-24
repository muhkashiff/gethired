from app.jd_parser.jd_parser import JDParser
from app.jd_parser.jd_builder import JDBuilder

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

parser = JDParser(jd_text)

builder = JDBuilder()

job = builder.build(parser.get_text())

print("=" * 60)
print("JOB DESCRIPTION")
print("=" * 60)

print(job.summary[:500])

print()

print("=" * 60)
print("KEYWORDS")
print("=" * 60)

for word in job.keywords[:50]:
    print(word)