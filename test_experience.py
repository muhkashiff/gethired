from app.parser.readers.resume_reader import ResumeReader
from app.parser.section_detector import SectionDetector
from app.parser.experience.job_splitter import JobSplitter


reader = ResumeReader()

lines = reader.read(
    r"D:\Self Projects\gethired\gethired\uploads\project_2\resume_original.docx"
)

detector = SectionDetector()

sections = detector.detect(lines)

experience = sections.get("experience", [])

print("=" * 70)
print("EXPERIENCE SECTION")
print("=" * 70)

for line in experience:
    print(line)

print()

splitter = JobSplitter()

jobs = splitter.split(experience)

print("=" * 70)
print("TOTAL JOBS:", len(jobs))
print("=" * 70)

for i, job in enumerate(jobs, 1):

    print()

    print(f"JOB #{i}")

    print("-" * 50)

    for line in job:

        print(line)