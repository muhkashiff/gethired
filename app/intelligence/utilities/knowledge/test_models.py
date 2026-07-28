import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)

# --------------------------------------------------------
# Test Sentence
# --------------------------------------------------------

text = (
    "Implemented FSSC 22000 requirements and increased "
    "Production Yield from 70% to 99% by leading cross-functional teams."
)

pipeline = KnowledgePipeline()

result = pipeline.process(text)

document = result["knowledge_document"]

graph_document = result["graph_document"]

profile = result["knowledge_profile"]

# ======================================================
print("\n" + "=" * 80)
print("DOCUMENT STATISTICS")
print("=" * 80)

pprint(document.statistics)

# ======================================================
print("\n" + "=" * 80)
print("GRAPH SUMMARY")
print("=" * 80)

pprint(graph_document.graph.summary())

# ======================================================
print("\n" + "=" * 80)
print("MEASUREMENT")
print("=" * 80)

print("\nALL FACTS\n")

for i, fact in enumerate(document.facts, start=1):

    print(f"\nFACT {i}")
    print("-" * 50)

    print(fact.text)

    pprint(fact.interpretation.measurement.summary())

# ======================================================
print("\n" + "=" * 80)
print("KNOWLEDGE PROFILE")
print("=" * 80)

pprint(profile)

# ======================================================
print("\n" + "=" * 80)
print("ACHIEVEMENT")
print("=" * 80)

pprint(profile["achievement"])

# ======================================================
print("\n" + "=" * 80)
print("IMPACT")
print("=" * 80)

pprint(

    profile["achievement"]["details"]["impact"]

)

# ======================================================
print("\n" + "=" * 80)
print("MAGNITUDE")
print("=" * 80)

pprint(

    profile["achievement"]["details"]["magnitude"]

)