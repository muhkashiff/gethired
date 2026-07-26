import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))


from app.intelligence.trajectory.trajectory_engine import TrajectoryEngine

from app.parser.parsed_models.experience import Experience


engine = TrajectoryEngine()

exp1 = Experience(

    title="QA Chemist",

    industry="Food",

    seniority="Professional",

    seniority_level=3

)

exp2 = Experience(

    title="Retail Store Manager",

    industry="Retail",

    seniority="Manager",

    seniority_level=7

)

exp3 = Experience(

    title="Managing Director",

    industry="Food",

    seniority="Executive",

    seniority_level=10

)

profile = engine.evaluate(

    [

        exp1,

        exp2,

        exp3

    ]

)

print(profile)