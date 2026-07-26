from app.intelligence.career_progression_engine import CareerProgressionEngine
from app.parser.parsed_models.experience import Experience

engine = CareerProgressionEngine()

exp1 = Experience(
    title="QA Chemist",
    seniority="Professional",
    duration=6
)

exp2 = Experience(
    title="Retail Store Manager",
    seniority="Manager",
    duration=8
)

exp3 = Experience(
    title="Managing Director",
    seniority="Executive",
    duration=2
)

profile = engine.evaluate([exp1, exp2, exp3])

print("=" * 70)

print(profile)