from app.parser.extractors.seniority_detector import SeniorityDetector

detector = SeniorityDetector()

jobs = [

    {
        "title": "QA Chemist",
        "responsibilities": [],
        "achievements": []
    },

    {
        "title": "Retail Store Manager",
        "responsibilities": [],
        "achievements": []
    },

    {
        "title": "Managing Director",
        "responsibilities": [],
        "achievements": []
    },

    {
        "title": "Lead QA Engineer",
        "responsibilities": [],
        "achievements": []
    },

    {
        "title": "Production Supervisor",
        "responsibilities": [],
        "achievements": []
    },

    {
        "title": "Quality Intern",
        "responsibilities": [],
        "achievements": []
    }

]

print("=" * 70)
print("SENIORITY DETECTOR TEST")
print("=" * 70)

for job in jobs:

    seniority = detector.detect(
        title=job["title"],
        responsibilities=job["responsibilities"],
        achievements=job["achievements"]
    )

    print("\nTitle:", job["title"])
    print("Detected Seniority :", seniority.name)
    print("Level              :", seniority.level)
    print("Confidence         :", seniority.confidence)
    print("Evidence           :", seniority.evidence)