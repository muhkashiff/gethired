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
Enterprise Matcher Test
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.tokenizer.tokenizer import Tokenizer
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.matcher import Matcher


sentence = (
    "Implemented ISO 9001 and FSSC22000 requirements "
    "using HACCP GMP and BRCGS standards."
)

tokenizer = Tokenizer()

matcher = Matcher(
    repository=repository,
    tokenizer=tokenizer,
)

matches = matcher.match(
    ontology="standards",
    sentence=sentence,
)

print()
print("=" * 80)
print("MATCHER TEST")
print("=" * 80)

print()
print(f"Matches Found : {len(matches)}")
print()

for i, match in enumerate(matches):

    print("-" * 60)

    print(f"Match #{i+1}")

    print()

    print("Phrase         :", match.phrase)

    print("Matched Alias  :", match.matched_alias)

    print("Canonical      :", match.entity.canonical)

    print("Entity ID      :", match.entity.entity_id)

    print("Category       :", match.entity.category)

    print("Business Area  :", match.entity.business_area)

    print("Token Index    :", match.token_index)

    print("Token Count    :", match.token_count)

    print("Characters     :", match.start_char, "-", match.end_char)

    print("Alias Match    :", match.is_alias)

print()

print("=" * 80)
print("RAW OBJECTS")
print("=" * 80)

for match in matches:

    print(match)

print()

print("Matcher PASS")