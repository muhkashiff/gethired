import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))


from app.intelligence.executive.executive_engine import ExecutiveEngine

from types import SimpleNamespace

# -------------------------------------------------------
# Mock Leadership Profile
# -------------------------------------------------------

leadership = SimpleNamespace(

    overall_score=92,

    strongest_dimensions=[
        "people_management",
        "strategic_leadership"
    ],

    summary="Strong leadership.",

    evidence=[
        "Led cross-functional teams."
    ]

)

# -------------------------------------------------------
# Mock Promotion Profile
# -------------------------------------------------------

promotion = SimpleNamespace(

    promotion_quality=55,

    promotion_count=2,

    highest_level="Executive"

)

# -------------------------------------------------------
# Mock Stability Profile
# -------------------------------------------------------

stability = SimpleNamespace(

    stability_score=55,

    stability_rating="Moderate",

    evidence=[
        "Average tenure 5.3 years."
    ]

)

# -------------------------------------------------------
# Mock Trajectory Profile
# -------------------------------------------------------

trajectory = SimpleNamespace(

    trajectory_score=98,

    career_stage="Executive",

    career_trend="Rapid Growth",

    executive_path=True,

    evidence=[
        "Executive progression."
    ]

)

# -------------------------------------------------------

engine = ExecutiveEngine()

profile = engine.evaluate(

    leadership,

    promotion,

    stability,

    trajectory

)

print("\n")
print("=" * 70)
print("EXECUTIVE PROFILE")
print("=" * 70)

print(profile)

print("\n")
print("=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"Executive Score      : {profile.executive_score}")

print(f"Executive Rating     : {profile.executive_rating}")

print(f"Executive Readiness  : {profile.executive_readiness}")

print(f"Next Role            : {profile.next_role}")

print(f"Future Roles         : {profile.future_roles}")

print(f"Strengths            : {profile.strengths}")

print(f"Development Areas    : {profile.development_areas}")

print("\n")
print("=" * 70)
print("SCORE BREAKDOWN")
print("=" * 70)

for k, v in profile.score_breakdown.items():

    print(f"{k:25} {v}")

print("\n")
print("=" * 70)
print("EVIDENCE")
print("=" * 70)

for e in profile.evidence:

    print("-", e)