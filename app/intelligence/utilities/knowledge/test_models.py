import sys
from pathlib import Path
from pprint import pprint

ROOT = Path(__file__).resolve().parents[4]
sys.path.append(str(ROOT))

from app.intelligence.utilities.knowledge.knowledge_pipeline import (
    KnowledgePipeline,
)

from app.intelligence.utilities.knowledge.knowledge_knowledge.ontology_enricher import (
    OntologyEnricher,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.resume_analyzer import (
    ResumeIntelligenceEngine,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.achievement_analyzer import (
    AchievementAnalyzer,
)

# ---------------------------------------------------------
# Resume Sample
# ---------------------------------------------------------

RESUME_TEXT = """
Lead the facility by implementing FSSC 22000 requirements and achieved certification.

Increased production yield from 70% to 99%.

Reduced customer complaints by 60%.

Managed supplier quality.

Optimized productivity by 25%.

Reduced production waste by 35%.

Trained 120 production staff.

Implemented ISO 9001 Quality Management System.

Conducted GMP inspections.

Reduced downtime by 40 hours per month.

Improved efficiency by 18%.

Managed cross-functional teams.
"""

# ---------------------------------------------------------

pipeline = KnowledgePipeline()

enricher = OntologyEnricher()

resume_analyzer = ResumeIntelligenceEngine()

achievement_analyzer = AchievementAnalyzer()

# ---------------------------------------------------------

print("=" * 120)
print("END TO END RESUME TEST")
print("=" * 120)

document = None

for sentence in RESUME_TEXT.split("\n"):

    sentence = sentence.strip()

    if not sentence:
        continue

    parsed = pipeline.process(sentence)

    parsed = enricher.enrich(parsed)

    if document is None:

        document = parsed

    else:

        document.sentences.extend(parsed.sentences)

        document.facts.extend(parsed.facts)

# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

print()
print("=" * 120)
print("DOCUMENT STATISTICS")
print("=" * 120)

print("Sentences :", len(document.sentences))
print("Facts     :", len(document.facts))

# ---------------------------------------------------------
# Facts
# ---------------------------------------------------------

print()
print("=" * 120)
print("FACTS")
print("=" * 120)

for i, fact in enumerate(document.facts, start=1):

    interp = fact.interpretation

    print()
    print(f"FACT {i}")
    print("-" * 100)

    print("TEXT :", fact.text)

    if interp.action.found:
        print("ACTION :", interp.action.base)

    if interp.object.found:
        print("OBJECT :", interp.object.canonical)

        print("OBJECT ENTITY :", interp.object.entity_id)

        print("BUSINESS AREA :", interp.object.business_area)

    if interp.metric.found:
        print("METRIC :", interp.metric.canonical)

        print("METRIC ENTITY :", interp.metric.entity_id)

        print("BUSINESS AREA :", interp.metric.business_area)

        print("IMPACT WEIGHT :", getattr(interp.metric, "impact_weight", ""))

    if interp.measurement.found:
        print("VALUE :", interp.measurement.numeric_value)

        print("UNIT :", interp.measurement.unit)

        print("DIRECTION :", interp.measurement.direction)

    if interp.domain.found:
        print("DOMAIN :", interp.domain.domain)

# ---------------------------------------------------------
# Resume Intelligence
# ---------------------------------------------------------

print()
print("=" * 120)
print("RESUME INTELLIGENCE")
print("=" * 120)

profile = resume_analyzer.analyze(document)

pprint(profile)

# ---------------------------------------------------------
# Achievement Intelligence
# ---------------------------------------------------------

print()
print("=" * 120)
print("ACHIEVEMENTS")
print("=" * 120)

achievements = achievement_analyzer.analyze(document)

for achievement in achievements:

    pprint(achievement)

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print()
print("=" * 120)
print("SUMMARY")
print("=" * 120)

leadership = 0
quality = 0
food = 0
manufacturing = 0
operations = 0

for fact in document.facts:

    if fact.interpretation.domain.found:

        d = fact.interpretation.domain.domain

        if "lead" in d:
            leadership += 1

        elif "quality" in d:
            quality += 1

        elif "food" in d:
            food += 1

        elif "manufacturing" in d:
            manufacturing += 1

        elif "operation" in d:
            operations += 1

print(f"Leadership Facts     : {leadership}")
print(f"Quality Facts        : {quality}")
print(f"Food Safety Facts    : {food}")
print(f"Manufacturing Facts  : {manufacturing}")
print(f"Operations Facts     : {operations}")

print()
print("=" * 120)
print("TEST COMPLETED")
print("=" * 120)