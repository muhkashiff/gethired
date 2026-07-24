from app.parser import ResumeParser
from app.parser.extractors import ExperienceExtractor

parser = ResumeParser(
    "uploads/project_2/resume_original.docx"
)

sections = parser.sections()

extractor = ExperienceExtractor()

jobs = extractor.extract(
    sections["experience"]
)

for job in jobs:

    print("=" * 60)

    print(job.job_title)

    print(job.company)

    print(job.start_year)

    print(job.end_year)

    print()

    print("Responsibilities")

    for r in job.responsibilities:
        print("-", r)

    print()

    print("Achievements")

    for a in job.achievements:
        print("-", a)