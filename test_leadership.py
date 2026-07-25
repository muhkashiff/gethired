from app.intelligence.leadership_engine import LeadershipEngine

from app.parser.parsed_models.experience import Experience


job = Experience(

    title="QA Manager",

    responsibilities=[

        "Led cross functional teams.",

        "Managed food safety system.",

        "Implemented FSSC 22000.",

        "Directed production operations.",

        "Managed supplier quality.",

        "Performed strategic planning.",

        "Implemented Lean Manufacturing."

    ],

    achievements=[

        "Reduced waste by 35%.",

        "Improved productivity.",

        "Led quality improvement initiatives."

    ]

)

engine = LeadershipEngine()

leadership = engine.analyze([job])

print()

print("=" * 70)

print("LEADERSHIP PROFILE")

print("=" * 70)

print()

print(leadership)

print()

print("=" * 70)

print("OVERALL")

print("=" * 70)

print()

print("Overall Score :", leadership.overall_score)

print("Strengths :", leadership.strengths)

print("Continuous Improvement :", leadership.continuous_improvement)

print()

print("=" * 70)

print("EVIDENCE")

print("=" * 70)

for e in leadership.evidence:

    print("-", e)