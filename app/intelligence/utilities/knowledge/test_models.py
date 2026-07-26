import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_extractors.modifier_extractor import (
    ModifierExtractor,
)

extractor = ModifierExtractor()

examples = [

    "Successfully implemented FSSC 22000.",

    "Strategically led cross-functional teams.",

    "Globally managed supplier quality.",

    "Consistently improved production yield.",

    "Rapidly reduced customer complaints.",

    "Independently conducted ISO audits.",

    "Successfully and strategically led cross-functional teams globally.",

]

for sentence in examples:

    print("\n" + "=" * 80)

    print(sentence)

    print("-" * 80)

    modifiers = extractor.extract(sentence)

    if not modifiers:

        print("No modifiers found.")

    else:

        for modifier in modifiers:

            print(modifier)