import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from pprint import pprint

from app.intelligence.utilities.knowledge.knowledge_parser.sentence_parser import SentenceParser

parser = SentenceParser()

sentence = parser.parse(
    "Implemented FSSC 22000 requirements and increased Production Yield from 70% to 99% by leading cross-functional teams."
)

pprint(sentence)