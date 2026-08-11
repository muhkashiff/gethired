"""

knowledge_pipeline_v5/
│
├── tokenizer/
│   ├── tokenizer.py
│   ├── tokenizer_rules.py
│   ├── normalizer.py
│   ├── ngrams.py
│   ├── cache.py
│   └── __init__.py
│
├── matcher/
│   ├── matcher.py
│   ├── fuzzy.py
│   ├── overlap.py
│   ├── ranker.py
│   └── __init__.py
│
├── extractors/
│   ├── base_extractor.py
│   ├── generic_ontology_extractor.py
│   └── standard_extractor.py
│
└── tests/
    ├── test_tokenizer.py
    ├── test_normalizer.py
    ├── test_ngrams.py
    ├── test_repository.py
    ├── test_matcher.py
    ├── test_overlap.py
    ├── test_ranker.py
    └── test_standard_extractor.py

    Sentence
      │
      ▼
Tokenizer
      │
      ▼
Repository
      │
      ▼
Matcher
      │
      ▼
Confidence
      │
      ▼
Overlap Resolver
      │
      ▼
Ranker
      │
      ▼
KnowledgeV5Pipeline
      │
      ▼
List[MatchResult]


PHASE 1
Ontology
    ↓
Repository
    ↓
Registry

PHASE 2
Knowledge V5 Pipeline
    ↓
Matching + confidence + overlap + ranking

PHASE 3  ← WE ARE HERE
Extraction Engine
    ↓
Skills / Actions / Targets / Domains / KPIs / Standards

PHASE 4
Reasoners
    ↓
Action → Target
Skill → Domain
Skill → KPI
Skill → Standard
Experience → Skill
Experience → Domain
Career progression
Cross-domain inference
AI reasoning

PHASE 5
Scoring / Job Matching / Resume Intelligence
"""