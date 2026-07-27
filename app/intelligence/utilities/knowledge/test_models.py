import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline.knowledge_pipeline import KnowledgePipeline

pipeline = KnowledgePipeline()

doc = pipeline.process(

    "Implemented ISO 9001, trained staff and improved productivity by 25%."

)

print()

print("DOCUMENT")

print(doc.statistics)

print()

for sentence in doc.sentences:

    print(sentence.original_text)

    print(sentence.confidence)

    print()

for fact in doc.facts:

    print(fact.interpretation.action.base)

    print(fact.interpretation.object.canonical)

    print(fact.interpretation.metric.canonical)

    print(fact.interpretation.measurement.value)

    print("-" * 60)