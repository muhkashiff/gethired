import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from app.intelligence.promotion.promotion_engine import PromotionEngine
from app.parser.parsed_models.experience import Experience

engine = PromotionEngine()

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

print(profile)