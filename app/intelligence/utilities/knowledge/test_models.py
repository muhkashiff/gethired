"""
Stage 1 Knowledge Parser Test

Pipeline

KnowledgeParser
        ↓
DocumentParser
        ↓
ClauseSegmenter
        ↓
SentenceParser
        ↓
KnowledgeDocument

STOP HERE

No Semantic Resolver
No Business Statements
No Knowledge Graph
No Scoring
"""

import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_parser.knowledge_parser import (
    KnowledgeParser,
)


# ============================================================
# Pretty Print Fact
# ============================================================

def print_fact(fact):

    print("\nFACT")
    print("-" * 60)

    print("Text:")
    print(fact.text)

    interp = fact.interpretation

    print("\nInterpretation")

    print(f"Action       : {getattr(interp.action,'canonical','')}")
    print(f"Target       : {getattr(interp.object,'canonical','')}")
    print(f"Domain       : {getattr(interp.domain,'domain','')}")
    print(f"Metric       : {getattr(interp.metric,'canonical','')}")
    print(f"Measurement  : {getattr(interp.measurement,'value','')}")
    print(f"Practice     : {getattr(interp.practice,'canonical','')}")

    print(f"\nAchievement  : {interp.achievement}")
    print(f"Quantified   : {interp.quantified}")
    print(f"Confidence   : {interp.confidence:.2f}")

    print("\nEntities")

    if interp.entities:

        for entity in interp.entities:

            print(
                f"{entity.entity_type:18}"
                f"{entity.canonical:35}"
                f"{entity.confidence:.2f}"
            )

    else:

        print("No ontology entities detected.")

    print("\nDependencies")

    if getattr(interp, "dependencies", None):

        for dep in interp.dependencies:

            print(
                f"{dep.source_entity} --{dep.relation}--> {dep.target_entity}"
            )

    else:

        print("No dependencies")


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 80)
    print("STAGE 1 KNOWLEDGE PARSER TEST")
    print("=" * 80)

    text = (
        "Implemented FSSC22000 requirements and increased "
        "Production Yield to 99% using Root Cause Analysis."
    )

    parser = KnowledgeParser()

    document = parser.parse(text)

    print("\nDOCUMENT")
    print("-" * 80)

    print("Raw Text\n")
    print(document.raw_text)

    print("\nStatistics")
    pprint(document.statistics)

    print(f"\nConfidence : {document.confidence:.2f}")

    print(f"Sentences  : {len(document.sentences)}")
    print(f"Facts      : {len(document.facts)}")

    print("\n" + "=" * 80)

    for i, sentence in enumerate(document.sentences, start=1):

        print(f"\nSENTENCE {i}")
        print("-" * 80)

        print(sentence.original_text)

        print(f"\nFacts : {len(sentence.facts)}")

        for fact in sentence.facts:

            print_fact(fact)

    print("\n" + "=" * 80)
    print("DOCUMENT SUMMARY")
    print("=" * 80)

    total_entities = 0
    total_dependencies = 0

    for fact in document.facts:

        total_entities += len(
            fact.interpretation.entities
        )

        total_dependencies += len(
            getattr(
                fact.interpretation,
                "dependencies",
                [],
            )
        )

    print(f"Total Sentences     : {len(document.sentences)}")
    print(f"Total Facts         : {len(document.facts)}")
    print(f"Total Entities      : {total_entities}")
    print(f"Total Dependencies  : {total_dependencies}")

    print("\nSUCCESS")
    print("=" * 80)


# ============================================================

if __name__ == "__main__":
    main()