from app.intelligence.leadership_pattern_detector import LeadershipPatternDetector

from app.intelligence.leadership_weight_engine import LeadershipWeightEngine

from app.intelligence.leadership_dimension_scorer import LeadershipDimensionScorer


detector = LeadershipPatternDetector()

weight_engine = LeadershipWeightEngine()

dimension_engine = LeadershipDimensionScorer()


sentence = (

    "Led cross functional teams "

    "implemented FSSC 22000 "

    "achieving 99% product yield."

)

patterns = detector.detect(sentence)

weighted = []

for p in patterns:

    weighted.append(

        weight_engine.calculate(

            p,

            seniority_level=7,

            years_experience=15

        )

    )

profile = dimension_engine.score(weighted)

print()

print("=" * 70)

print("DIMENSION SCORES")

print("=" * 70)

for k, v in profile["scores"].items():

    print(f"{k:35} {round(v,2)}")

print()

print("=" * 70)

print("CONFIDENCE")

print("=" * 70)

print(profile["confidence"])