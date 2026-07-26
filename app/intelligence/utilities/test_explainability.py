"""
Test Explainability Engine
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(ROOT))

from app.intelligence.utilities.explainability_engine import ExplainabilityEngine
from app.intelligence.career_score.cs_models.career_score_profile import CareerScoreProfile

# --------------------------------------------------------

profile = CareerScoreProfile()

profile.leadership_index = 89.2

profile.career_health_index = 70.0

profile.market_readiness_index = 90.1

profile.overall_score = 82.8

profile.confidence = 0.95

profile.strengths = [

    "Leadership",

    "Market Readiness",

    "Executive Potential"

]

profile.development_areas = [

    "Promotion Readiness",

    "Career Stability"

]

profile.evidence = [

    "Led cross-functional teams.",

    "Implemented FSSC 22000.",

    "Achieved 99% production yield.",

    "Average tenure 5.3 years.",

    "Executive progression."

]

# --------------------------------------------------------

engine = ExplainabilityEngine()

result = engine.explain_career(profile)

# --------------------------------------------------------

print("=" * 70)

print(result.title)

print("=" * 70)

print()

print("SUMMARY")

print("-" * 70)

print(result.summary)

print()

print("STRENGTHS")

print("-" * 70)

for item in result.strengths:

    print("•", item)

print()

print("DEVELOPMENT AREAS")

print("-" * 70)

for item in result.weaknesses:

    print("•", item)

print()

print("RECOMMENDATIONS")

print("-" * 70)

for item in result.recommendations:

    print("•", item)

print()

print("EVIDENCE")

print("-" * 70)

for item in result.evidence:

    print("•", item)

print()

print("CONFIDENCE")

print("-" * 70)

print(f"{result.confidence:.0%}")