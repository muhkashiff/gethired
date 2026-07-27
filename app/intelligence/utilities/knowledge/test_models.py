import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))
"""
Test Domain Reasoner

Tests

Action Extraction
Object Extraction
Domain Reasoning

Run

python test_domain_reasoner.py
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import (
    ActionExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.object_extractor import (
    ObjectExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_reasoners.domain_reasoner import (
    DomainReasoner,
)


action_extractor = ActionExtractor()

object_extractor = ObjectExtractor()

reasoner = DomainReasoner()


sentences = [

    "Trained staff",

    "Managed supplier quality",

    "Implemented ISO 9001",

    "Successfully implemented FSSC 22000",

    "Reduced customer complaints",

    "Improved production yield",

    "Optimized productivity",

    "Reduced downtime by 40 hours",

]


print("=" * 90)
print("DOMAIN REASONER TEST")
print("=" * 90)

for sentence in sentences:

    action = action_extractor.extract(sentence)

    obj = object_extractor.extract(sentence)

    domain = reasoner.reason(
        action,
        obj,
    )

    print()

    print(sentence)

    print("-" * 60)

    print("Action")
    print(action)

    print()

    print("Object")
    print(obj)

    print()

    print("Domain")
    print(domain)

    print("-" * 60)