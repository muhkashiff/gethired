import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_parser.sentence_parser import SentenceParser

parser = SentenceParser()

sentence = parser.parse(

    "Implemented FSSC22000 Quality Management System using Lean Manufacturing."

)

print("=" * 80)

print(sentence.original_text)

print("=" * 80)

fact = sentence.facts[0]

interp = fact.interpretation

print()

print("ACTION")

print(interp.action)

print()

print("OBJECT")

print(interp.object)

print()

print("DOMAIN")

print(interp.domain)

print()

print("METRIC")

print(interp.metric)

print()

print("MEASUREMENT")

print(interp.measurement)

print()

print("PRACTICE")

print(interp.practice)

print()

print("ENTITIES")

for entity in interp.entities:

    print(

        entity.entity_type,

        entity.entity_id,

        entity.canonical,

    )

print()

print("DEPENDENCIES")

for dep in interp.dependencies:

    print(dep)

print()

print("ACHIEVEMENT :", interp.achievement)

print("CONFIDENCE  :", interp.confidence)

print("IMPACT      :", interp.overall_impact_weight)

print("EXPLANATION :", interp.explanation)