"""
Enterprise Ranker Test

Stage 6
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.tokenizer.tokenizer import Tokenizer
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.matcher import Matcher
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.confidence.confidence_calculator import ConfidenceCalculator
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.overlap.overlap_resolver import OverlapResolver
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.ranker.ranker import Ranker


sentence = (
    "Implemented ISO 9001 and FSSC22000 requirements "
    "using HACCP GMP and BRCGS standards."
)

tokenizer = Tokenizer()

matcher = Matcher(

    repository,

    tokenizer,

)

confidence = ConfidenceCalculator(

    repository,

)

resolver = OverlapResolver()

ranker = Ranker()

############################################################

matches = matcher.match(

    "standards",

    sentence,

)

matches = confidence.score_all(matches)

matches = resolver.resolve(matches)

matches = ranker.rank(matches)

############################################################

print()

print("=" * 80)

print("RANKED RESULTS")

print("=" * 80)

print()

for index, match in enumerate(matches, start=1):

    print(f"#{index}")

    print("Entity       :", match.entity.entity_id)

    print("Canonical    :", match.entity.canonical)

    print("Phrase       :", match.phrase)

    print("Confidence   :", match.confidence)

    print("Tokens       :", match.token_count)

    print()

############################################################

best = ranker.best(matches)

print("=" * 80)

print("BEST MATCH")

print("=" * 80)

print()

print(best)

print()

print("Ranker PASS")