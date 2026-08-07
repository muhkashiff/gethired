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
Enterprise Confidence Test

Stage 4

Pipeline

Sentence
    ↓
Tokenizer
    ↓
Repository
    ↓
Matcher
    ↓
Confidence Calculator
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.tokenizer.tokenizer import Tokenizer
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.matcher.matcher import Matcher
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.confidence.confidence_calculator import ConfidenceCalculator


sentence = (
    "Implemented ISO 9001 and FSSC22000 requirements "
    "using HACCP GMP and BRCGS standards."
)

tokenizer = Tokenizer()

matcher = Matcher(

    repository=repository,

    tokenizer=tokenizer,

)

calculator = ConfidenceCalculator(

    repository=repository,

)

############################################################

matches = matcher.match(

    ontology="standards",

    sentence=sentence,

)

print()

print("=" * 80)

print("MATCHES BEFORE CONFIDENCE")

print("=" * 80)

print()

for m in matches:

    print(

        f"{m.entity.entity_id:20}"

        f"{m.phrase:15}"

        f"{m.confidence:.3f}"

    )

############################################################

matches = calculator.score_all(matches)

############################################################

print()

print("=" * 80)

print("MATCHES AFTER CONFIDENCE")

print("=" * 80)

print()

for m in matches:

    print("-" * 60)

    print()

    print("Entity ID      :", m.entity.entity_id)

    print("Canonical      :", m.entity.canonical)

    print("Phrase         :", m.phrase)

    print("Confidence     :", m.confidence)

    print("Business Area  :", m.entity.business_area)

    print("Category       :", m.entity.category)

    print("Impact Weight  :", m.entity.impact_weight)

    print("Characters     :", m.start_char, "-", m.end_char)

############################################################

print()

print("=" * 80)

print("OBJECT CHECK")

print("=" * 80)

print()

print(type(matches[0]))

print()

print(matches[0])

print()

print("Confidence PASS")