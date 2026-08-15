""""
                         uploaded resume.docx
                                │
                                ▼
                        ┌───────────────┐
                        │ ResumeReader  │
                        │ DOCX only     │
                        └───────┬───────┘
                                │
                         ResumeBlock[]
                                │
                                ▼
                       ┌────────────────┐
                       │ SectionDetector│
                       └───────┬────────┘
                               │
                       ResumeSection[]
                               │
                               ▼
                       ┌────────────────┐
                       │  ResumeParser  │
                       └───────┬────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        NON-ONTOLOGY                       ONTOLOGY
        extraction                         extraction
                │                             │
    ┌───────────┼────────────┐       ┌────────┼─────────┐
    │           │            │       │        │         │
 Contact    Experience   Education  Skills Certifications Standards
 Language   Projects     Awards     etc.       etc.       etc.
 Reference
                │                             │
                └──────────────┬──────────────┘
                               │
                               ▼
                         ResumeBuilder
                               │
                               ▼
                         Resume object
                               │
                               ▼
                    Resume Intelligence Layer
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
             Resume Analysis              JD Analysis
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                       JD ↔ Resume Matching
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
             ATS Score     Missing Skills   Recommendations


                              RESUME INGESTION
                       │
                       ▼
                 ResumeReader
                       │
                ResumeBlock[]
                       │
                       ▼
                SectionDetector
                       │
              ResumeSection[]
                       │
                       ▼
                 ResumeParser
                       │
                       ▼
                  Resume
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
 Non-Ontology Extraction       Raw Resume
          │
          │
          ├── Contact
          ├── Experience
          ├── Education
          ├── Projects
          ├── Awards
          ├── Languages
          └── References
          │
          ▼
     Structured Resume
          │
          ▼
     Ontology Knowledge
          │
          ├── Skills
          ├── Standards
          ├── Metrics
          ├── Methodologies
          ├── Technologies
          ├── Actions
          ├── Targets
          └── Domains
          │
          ▼
    KnowledgeDocument
          │
          ▼
    Resume Intelligence
          │
          ├── Seniority
          ├── Career progression
          ├── Leadership
          ├── Industry
          ├── Achievements
          ├── Competency evidence
          └── Candidate profile
          │
          ▼
        JD MATCHING
          │
          ├── ATS score
          ├── Required skills
          ├── Missing skills
          ├── Matching evidence
          ├── Experience fit
          ├── Education fit
          ├── Certification fit
          ├── Seniority fit
          └── Recommendations



          DOCX
 ↓
ResumeReader
 ↓
SectionDetector
 ↓
ResumeSection objects        ← parser layer
 ↓
ResumeParser
 ↓
ResumeBuilder
 ↓
Resume object
 ↓
KnowledgeParser               ← knowledge layer
 ↓
KnowledgeDocument


                         DOCX RESUME
                              │
                              ▼
                       ┌─────────────┐
                       │ ResumeReader│
                       └──────┬──────┘
                              │
                        ResumeBlock[]
                              │
                              ▼
                     ┌────────────────┐
                     │SectionDetector │
                     └───────┬────────┘
                             │
                     ResumeSection{}
                             │
                             ▼
                       ResumeParser
                             │
                             ▼
                       ResumeBuilder
                             │
                             ▼
                          Resume
                             │
             ┌───────────────┴────────────────┐
             │                                │
             ▼                                ▼
   Non-Ontology Extractors             Ontology Extraction
             │                                │
             │                    ┌───────────┴───────────┐
             │                    │                       │
             │                EntityExtractor       Ontology Repository
             │                    │
             └────────────┬───────┘
                          ▼
                  KnowledgeDocument
                          │
                          ▼
                Resume Intelligence
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
     Career Analysis   Leadership       JD Matching
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                 ATS / Recommendation




                 DOCX
 │
 ▼
ResumeReader
 │
 │ list[ResumeBlock]
 ▼
SectionDetector
 │
 │ dict[str, ResumeSection]
 ▼
ResumeParser
 │
 │ dict[str, ResumeSection]
 ▼
ResumeBuilder
 │
 │ converts ResumeBlock → text ONLY where legacy
 │ extractors require strings
 ▼
Resume
 │
 ├── Personal Information
 ├── Summary
 ├── Experience
 ├── Education
 ├── Projects
 ├── Awards
 ├── Languages
 └── References
 │
 ▼
Ontology / Knowledge Layer
 │
 ├── entities
 ├── standards
 ├── methodologies
 ├── technologies
 ├── metrics
 ├── actions
 └── domains
 │
 ▼
Resume Intelligence
 │
 ├── seniority
 ├── leadership
 ├── career progression
 ├── education enrichment
 ├── industry
 ├── achievements
 ├── ATS
 └── JD matching
 

                     RESUME INGESTION
                          │
                          ▼
                   ResumeBuilder
                          │
                          ▼
                 ┌─────────────────┐
                 │ Resume          │
                 │                 │
                 │ structural     │
                 │ extraction     │
                 └────────┬────────┘
                          │
                          ▼
              ResumeKnowledgeAdapter
                          │
                          ▼
              ResumeEntityCandidates
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Skill       Cert        Standard
          Extractor   Extractor   Extractor
              │           │           │
              ▼           ▼           ▼
          Knowledge    Knowledge    Knowledge
           Entity       Entity       Entity
              │           │           │
              └───────────┼───────────┘
                          ▼
                 Knowledge Extractor
                       Layer
                          │
                          ▼
                    Reasoner Layer
                          │
                          ▼
                   Knowledge Graph
                          │
                          ▼
                     Traversal
                          │
                          ▼
                    Knowledge Profile
                          │
                          ▼
                    JD Intelligence
                          │
                          ▼
                    JD Matching
                          │
                          ▼
                       ATS
                  """