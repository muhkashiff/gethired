"""
Existing analyzed Project
        │
        ├── Resume Profile
        ├── JD Requirement Profile
        ├── KnowledgeMatchProfile
        ├── ATS Analysis Result
        ├── Recommendation Result
        └── original Resume + JD text
                │
                ▼
       CoverLetterService
                │
                ▼
       Evidence / Keyword Selection
                │
                ▼
       Truth-Safe Generation Context
                │
                ▼
       AI / ML Language Model
                │
                ▼
       CoverLetterFixer
                │
                ▼
       Final Cover Letter
                │
                ▼
       DOCX Builder
                │
                ▼
       cover_letter.docx
                │
                ▼
       Browser Download

       

       Candidate evidence
├── Experience
│   ├── Store Manager
│   ├── Managing Director
│   ├── Food production / operations experience
│   └── leadership evidence
│
├── Education
│   └── M.Sc / equivalent education level
│
├── Skills
│   ├── Leadership
│   ├── Process Improvement
│   └── ...
│
├── Technologies
│   ├── Python
│   ├── Azure
│   └── ...
│
├── Methodologies
│   ├── Agile
│   ├── Six Sigma
│   └── ...
│
├── Certifications
│   ├── PMP
│   └── ...
│
├── Business KPIs
│   └── NPS / quantified achievements where actually present
│
└── Evidence
    ├── matched requirements
    ├── partially matched requirements
    └── strong resume evidence


    JD evidence
├── Job title
├── responsibilities
├── required requirements
├── preferred requirements
├── contextual requirements
├── domain
├── important skills
├── important experience
└── relevant terminology


CoverLetterService
    │
    ├── AnalysisContextBuilder
    │
    ├── CoverLetterEvidenceSelector
    │
    ├── CoverLetterGenerator
    │
    ├── CoverLetterFixer
    │
    ├── CoverLetterValidator
    │
    └── CoverLetterDocxBuilder


    1. CoverLetterModels
        ↓
2. CoverLetterContextBuilder
        ↓
3. CoverLetterEvidenceSelector
        ↓
4. CoverLetterGenerator
        ↓
5. CoverLetterFixer
        ↓
6. CoverLetterValidator
        ↓
7. CoverLetterDocxBuilder
        ↓
8. CoverLetterService
        ↓
9. Flask route
        ↓
10. Existing Generate Cover Letter button
        ↓
11. Integration test

                    EXISTING ANALYSIS
                           │
             ┌─────────────┴─────────────┐
             │                           │
          RESUME                        JD
             │                           │
             └─────────────┬─────────────┘
                           │
                  Evidence Selector
                           │
                  Truth-Safe Context
                           │
                    AI Language Model
                           │
                         Draft
                           │
                   CoverLetterFixer
                           │
                  CoverLetterValidator
                           │
                    Final Letter
                           │
                  CoverLetterDocxBuilder
                           │
                    cover_letter.docx
                           │
                 Generate Cover Letter
                       Download
       """