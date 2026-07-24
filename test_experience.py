from app.parser import ResumeParser
from app.parser import ResumeBuilder

from app.ats.analyzers.experience_analyzer import ExperienceAnalyzer


# Parse resume
parser = ResumeParser(
    "uploads/project_2/resume_original.docx"
)

sections = parser.sections()


# Build Resume object
builder = ResumeBuilder()

resume = builder.build(sections)


# Analyze experience
analyzer = ExperienceAnalyzer()

result = analyzer.analyze(resume)

print("=" * 60)
print("EXPERIENCE ANALYSIS")
print("=" * 60)

print(result)