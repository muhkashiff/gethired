import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

"""
Semantic Knowledge Engine Integration Test

Pipeline

Sentence
    ↓
Knowledge Pipeline
    ↓
Ontology Enricher
    ↓
Resume Intelligence
    ↓
Achievement Intelligence
"""

from app.intelligence.utilities.knowledge.knowledge_pipeline import KnowledgePipeline

from app.intelligence.utilities.knowledge.knowledge_knowledge.ontology_enricher import (
    OntologyEnricher,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.resume_analyzer import (
    ResumeIntelligenceEngine,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.achievement_analyzer import (
    AchievementAnalyzer,
)

# ----------------------------------------------------------------------

TEST_SENTENCES = [

    "Successfully implemented FSSC 22000 requirements and reduced customer complaints by 60%.",

    "Implemented ISO 9001 quality management system.",

    "Improved production yield from 70% to 99%.",

    "Reduced downtime by 40 hours per month.",

    "Managed supplier quality and trained staff.",

    "Optimized productivity by 25%.",

    "Reduced waste by 35%.",

]

# ----------------------------------------------------------------------

pipeline = KnowledgePipeline()

enricher = OntologyEnricher()

resume_analyzer = ResumeIntelligenceEngine()

achievement_analyzer = AchievementAnalyzer()

# ----------------------------------------------------------------------

print("=" * 100)
print("SEMANTIC KNOWLEDGE ENGINE")
print("=" * 100)

for sentence in TEST_SENTENCES:

    print()
    print("=" * 100)
    print(sentence)
    print("=" * 100)

    # -------------------------------------------------
    # Pipeline
    # -------------------------------------------------

    document = pipeline.process(sentence)

    document = enricher.enrich(document)

    # -------------------------------------------------
    # Facts
    # -------------------------------------------------

    for i, fact in enumerate(document.facts, start=1):

        print()
        print(f"FACT {i}")
        print("-" * 80)

        interp = fact.interpretation

        print("\nAction")
        pprint(interp.action)

        print("\nObject")
        pprint(interp.object)

        print("\nDomain")
        pprint(interp.domain)

        print("\nMetric")
        pprint(interp.metric)

        print("\nMeasurement")
        pprint(interp.measurement)

        # ---------------------------------------------
        # Ontology
        # ---------------------------------------------

        if interp.object.found:

            print("\nObject Ontology")

            print("Entity ID     :", getattr(interp.object, "entity_id", ""))

            print("Business Area :", getattr(interp.object, "business_area", ""))

            print("Source        :", getattr(interp.object, "source", ""))

            print("Metadata      :", getattr(interp.object, "metadata", {}))

        if interp.metric.found:

            print("\nMetric Ontology")

            print("Entity ID     :", getattr(interp.metric, "entity_id", ""))

            print("Business Area :", getattr(interp.metric, "business_area", ""))

            print("Source        :", getattr(interp.metric, "source", ""))

            print("Metadata      :", getattr(interp.metric, "metadata", {}))

    # -------------------------------------------------
    # Resume Intelligence
    # -------------------------------------------------

    print()
    print("-" * 80)
    print("RESUME INTELLIGENCE")
    print("-" * 80)

    profile = resume_analyzer.analyze(document)

    pprint(profile)

    # -------------------------------------------------
    # Achievement Intelligence
    # -------------------------------------------------

    print()
    print("-" * 80)
    print("ACHIEVEMENT INTELLIGENCE")
    print("-" * 80)

    achievements = achievement_analyzer.analyze(document)

    pprint(achievements)

print()
print("=" * 100)
print("SEMANTIC ENGINE TEST COMPLETED")
print("=" * 100)