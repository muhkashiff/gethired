import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))
from pprint import pprint

from app.intelligence.utilities.knowledge.knowledge_pipeline.semantic_pipeline import (
    SemanticPipeline,
)

pipeline = SemanticPipeline()

text = """
Implemented ISO 9001, trained staff and improved productivity by 25%.
"""

document = pipeline.process(text)

print("=" * 80)

print("SEMANTIC DOCUMENT")

print("=" * 80)

print()

print(document.statistics)

print()

for sentence in document.sentences:

    print(sentence.original_text)

    print()

    for clause in sentence.clauses:

        print("-" * 60)

        print(clause.text)

        print()

        print("Action")

        pprint(clause.action)

        print()

        print("Object")

        pprint(clause.object)

        print()

        print("Domain")

        pprint(clause.domain)

        print()

        print("Metric")

        pprint(clause.metric)

        print()

        print("Measurement")

        pprint(clause.measurement)

        print()

        print("Achievement")

        print(clause.achievement)

        print()

        print("Business Area")

        print(clause.business_area)

        print()

        print("Confidence")

        print(clause.confidence)

        print()