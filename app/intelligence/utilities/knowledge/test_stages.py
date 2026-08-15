"""
STAGE 1 — DOCX
PASS

STAGE 2 — ResumeReader
PASS
78 blocks

STAGE 3 — SectionDetector
PASS
dict
7 sections

STAGE 4 — ResumeParser
PASS

STAGE 5 — ResumeBuilder
PASS
Resume

STAGE 6 — Resume extraction contents
PASS
experience=3
education=3
...

STAGE 7 — Resume → Knowledge traversal
PASS
N resume text units generated

STAGE 8 — ExtractionCoordinator
PASS
N ontology entities extracted

STAGE 9 — KnowledgeV5Pipeline
PASS
tokenization
matching
confidence
overlap
ranking

STAGE 10 — KnowledgeEntity conversion
PASS

STAGE 11 — Knowledge facts
PASS

"""