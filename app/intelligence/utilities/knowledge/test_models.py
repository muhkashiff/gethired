"""
STAGE 1 DEBUG
Checks ActionExtractor independently
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from knowledge_pipeline_v5.tokenizer.tokenizer import Tokenizer

t = Tokenizer()

sentence = (
    "Implemented ISO 9001 and FSSC22000 requirements "
    "using HACCP, GMP and BRCGS standards."
)

tokens = t.tokenize(sentence)

print(tokens)

assert tokens == [
    "Implemented",
    "ISO",
    "9001",
    "and",
    "FSSC22000",
    "requirements",
    "using",
    "HACCP",
    "GMP",
    "and",
    "BRCGS",
    "standards",
]

print("Tokenizer PASS")