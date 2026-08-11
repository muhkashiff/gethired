from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


"""
Enterprise V5
Real Pipeline -> Extraction Engine Integration Test

Flow:

Sentence
    ↓
KnowledgeV5Pipeline
    ↓
Tokenizer
    ↓
Matcher
    ↓
Confidence
    ↓
Overlap Resolver
    ↓
Ranker
    ↓
ExtractionEngine
    ↓
Structured entities
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.registry import (
    KnowledgeRegistry,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_engine import (
    ExtractionEngine,
)


####################################################################
# INITIALIZE REGISTRY
####################################################################

print()
print("=" * 70)
print("INITIALIZING KNOWLEDGE REGISTRY")
print("=" * 70)

registry = KnowledgeRegistry(
    repository=repository
)

print()
print(
    f"Entity count : {registry.entity_count}"
)

print(
    f"Alias count  : {registry.alias_count}"
)


####################################################################
# INITIALIZE V5 PIPELINE
####################################################################

print()
print("=" * 70)
print("INITIALIZING KNOWLEDGE V5 PIPELINE")
print("=" * 70)

pipeline = KnowledgeV5Pipeline(
    repository_instance=repository
)

print()
print("Pipeline initialized successfully.")


####################################################################
# INITIALIZE EXTRACTION ENGINE
####################################################################

print()
print("=" * 70)
print("INITIALIZING EXTRACTION ENGINE")
print("=" * 70)

engine = ExtractionEngine(
    registry=registry
)

print()
print("Extraction engine initialized successfully.")


####################################################################
# TEST SENTENCE
####################################################################

sentence = (
    "Implemented FSSC 22000 and HACCP requirements, "
    "improved quality assurance processes, "
    "reduced waste, and increased production yield."
)


####################################################################
# RUN V5 PIPELINE
####################################################################

print()
print("=" * 70)
print("RUNNING KNOWLEDGE V5 PIPELINE")
print("=" * 70)

print()
print("Sentence:")
print(sentence)

print()

ontology_names = [
    "skills",
    "actions",
    "targets",
    "domains",
    "metrics",
    "standards",
]

all_matches = []

for ontology in ontology_names:

    print()
    print("=" * 70)
    print(f"ONTOLOGY: {ontology.upper()}")
    print("=" * 70)

    matches = pipeline.run(
        ontology,
        sentence,
    )

    for match in matches:

        print(
            f"{match.entity_id} -> "
            f"{match.canonical} | "
            f"confidence={match.confidence:.3f}"
        )

    all_matches.extend(matches)

    print()
    print("=" * 70)
    print("TOTAL MATCHES")
    print("=" * 70)

    for match in all_matches:

        print(
            f"{match.entity_id} -> "
            f"{match.canonical} | "
            f"{match.confidence:.3f}"
        )


####################################################################
# DISPLAY RAW MATCHES
####################################################################

print("=" * 70)
print("V5 PIPELINE MATCHES")
print("=" * 70)

print()

if not matches:

    print("NO MATCHES FOUND")

else:

    for index, match in enumerate(
        matches,
        start=1,
    ):

        print(
            f"[{index}] {match}"
        )


####################################################################
# EXTRACTION ENGINE
####################################################################

print()
print("=" * 70)
print("RUNNING EXTRACTION ENGINE")
print("=" * 70)

result = engine.extract(
    matches
)


####################################################################
# DISPLAY SKILLS
####################################################################

print()
print("SKILLS")
print("-" * 70)

for item in result["skills"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# DISPLAY ACTIONS
####################################################################

print()
print("ACTIONS")
print("-" * 70)

for item in result["actions"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# DISPLAY TARGETS
####################################################################

print()
print("TARGETS")
print("-" * 70)

for item in result["targets"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# DISPLAY DOMAINS
####################################################################

print()
print("DOMAINS")
print("-" * 70)

for item in result["domains"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# DISPLAY METRICS
####################################################################

print()
print("METRICS")
print("-" * 70)

for item in result["metrics"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# DISPLAY STANDARDS
####################################################################

print()
print("STANDARDS")
print("-" * 70)

for item in result["standards"]:

    print(
        f"{item['entity_id']} "
        f"-> {item['canonical']} "
        f"| confidence={item['confidence']}"
    )


####################################################################
# COUNTS
####################################################################

print()
print("=" * 70)
print("EXTRACTION COUNTS")
print("=" * 70)

print()

for key, value in result["counts"].items():

    print(
        f"{key:15} : {value}"
    )


####################################################################
# ALL ENTITIES
####################################################################

print()
print("=" * 70)
print("ALL EXTRACTED ENTITIES")
print("=" * 70)

print()

for item in result["all_entities"]:

    print(
        f"{item['entity_id']:35} "
        f"-> {item['canonical']}"
    )


####################################################################
# COMPLETE
####################################################################

print()
print("=" * 70)
print("REAL PIPELINE EXTRACTION TEST COMPLETE")
print("=" * 70)