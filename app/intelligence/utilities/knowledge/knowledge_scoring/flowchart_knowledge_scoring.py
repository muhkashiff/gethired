"""""
knowledge_scoring/

│
├── ontology/
│
├── mappings/
│   domain_mapping.py
│   technical_mapping.py
│   leadership_mapping.py
│   executive_mapping.py
│   business_value_mapping.py
│   ats_mapping.py
│
├── reasoners/
│   capability_reasoner.py
│
├── evidence/
│   evidence_models.py
│   generic_evidence_builder.py
│
├── scoring/
│   generic_score_engine.py
│
├── predictors/
│   seniority_predictor.py
│   career_predictor.py
│   executive_predictor.py
│
└── profile/

Knowledge Graph
        │
        ▼
CapabilityReasoner
        │
        ▼
CapabilityEvidence
        │
        ▼
GenericEvidenceBuilder
        │
        ▼
Evidence Objects
        │
        ▼
Score Engines
        │
        ▼
Predictors
        │
        ▼
KnowledgeProfile

"""