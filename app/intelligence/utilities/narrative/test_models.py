import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(ROOT))


from narrative_templates import NarrativeTemplates

engine = NarrativeTemplates()

print()

for i in range(5):

    print(

        engine.intro("leadership"),

        "...",

        engine.ending("leadership")

    )