"""
Stage 1
Enterprise Tokenizer Test

Pipeline

Sentence
    ↓
Tokenizer
    ↓
Token Objects
    ↓
NGram Objects
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

"""
Enterprise Knowledge Pipeline Test
Enterprise V5

Tests complete pipeline:

Sentence
    ↓
Tokenizer
    ↓
Repository
    ↓
Matcher
    ↓
Confidence
    ↓
Overlap
    ↓
Ranker
"""

import os
import sys

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../../../..",
    )
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.match_result import (
    MatchResult,
)


pipeline = KnowledgeV5Pipeline()

sentence = (
    "Implemented ISO 9001 and "
    "FSSC22000 requirements using "
    "HACCP GMP and BRCGS standards."
)

print("=" * 80)
print("PIPELINE TEST")
print("=" * 80)

matches = pipeline.run(

    ontology="standards",

    sentence=sentence,

)

print()

print(f"Matches Found : {len(matches)}")

print()

assert isinstance(matches, list)

assert len(matches) >= 5

for i, match in enumerate(matches, start=1):

    print("-" * 60)

    print(f"Match #{i}")

    print()

    print("Entity ID      :", match.entity.entity_id)

    print("Canonical      :", match.entity.canonical)

    print("Phrase         :", match.phrase)

    print("Confidence     :", round(match.confidence, 3))

    print("Token Index    :", match.token_index)

    print("Token Count    :", match.token_count)

    print("Characters     :", match.start_char, "-", match.end_char)

    print("Alias Match    :", match.is_alias)

    print()

    assert isinstance(match, MatchResult)

print("=" * 80)
print("BEST MATCH")
print("=" * 80)

best = pipeline.best(

    ontology="standards",

    sentence=sentence,

)

print()

print(best)

assert isinstance(best, MatchResult)

assert best.entity.entity_id == "STD_ISO_9001"

print()

print("KnowledgeV5Pipeline PASS")