import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))


from pprint import pprint



from app.intelligence.utilities.knowledge.knowledge_linker.entity_linker import EntityLinker

linker = EntityLinker()

tests = [
    "customer complaints",
    "yield",
    "FSSC 22000",
    "ISO 9001",
    "waste",
]

for item in tests:
    print("=" * 80)
    print(item)
    pprint(linker.link(item))