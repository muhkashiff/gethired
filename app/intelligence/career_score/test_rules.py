import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from career_score_rules import CareerScoreRules
from career_score_scorer import CareerScoreScorer

rules = CareerScoreRules()

scorer = CareerScoreScorer(rules)

detector_output = {

    "leadership_score": 92,

    "promotion_score": 55,

    "stability_score": 55,

    "trajectory_score": 98,

    "executive_score": 82.7

}

result = scorer.score(detector_output)

print(result)