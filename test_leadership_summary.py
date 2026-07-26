from app.intelligence.leadership_pattern_detector import LeadershipPatternDetector
from app.intelligence.leadership_weight_engine import LeadershipWeightEngine
from app.intelligence.leadership_dimension_scorer import LeadershipDimensionScorer
from app.intelligence.leadership_summary_builder import LeadershipSummaryBuilder

sentence = (
    "Led cross functional teams, "
    "implemented FSSC 22000, "
    "achieved 99% product yield."
)

detector = LeadershipPatternDetector()
weight_engine = LeadershipWeightEngine()
dimension_engine = LeadershipDimensionScorer()
summary_builder = LeadershipSummaryBuilder()

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

summary = summary_builder.build(profile)

print("=" * 70)
print("LEADERSHIP SUMMARY")
print("=" * 70)

print(summary)

print("\nTop Strengths")
print(summary.strongest_dimensions)

print("\nWeak Areas")
print(summary.weakest_dimensions)

print("\nNarrative")
print(summary.summary)