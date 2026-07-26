import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from app.intelligence.stability.stability_engine import StabilityEngine
from app.parser.parsed_models.experience import Experience

engine = StabilityEngine()

exp1 = Experience(
    title="QA Chemist",
    duration=6
)

exp2 = Experience(
    title="Retail Store Manager",
    duration=8
)

exp3 = Experience(
    title="Managing Director",
    duration=2
)

profile = engine.evaluate([exp1, exp2, exp3])

print(profile)