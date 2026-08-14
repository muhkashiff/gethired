"""

                         RESUME INGESTION
                              │
                              ▼
                         ResumeBuilder
                              │
                              ▼
                            Resume
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
       RAW RESUME OBJECT             INTELLIGENCE LAYER
                                             │
                    ┌────────────────────────┼────────────────────┐
                    │                        │                    │
                    ▼                        ▼                    ▼
             SeniorityDetector      EducationEnricher     IndustryDetector
                    │                        │                    │
                    └────────────────────────┼────────────────────┘
                                             │
                                             ▼
                                  ExperienceEnricher
                                             │
                                             ▼
                                  ResumeIntelligence
                                             │
                                             ▼
                              ┌─────────────────────────┐
                              │ Existing Ontology V5    │
                              │ Domains                 │
                              │ Actions                 │
                              │ Targets                 │
                              │ Metrics                 │
                              │ Methodologies           │
                              │ Technologies            │
                              └────────────┬────────────┘
                                           │
                                           ▼
                                   JD Intelligence
                                           │
                                           ▼
                                  JD ↔ Resume Matcher
                                           │
                                           ▼
                                  Explainable Score

ResumeBuilder
     │
     ▼
Resume
     │
     ▼
ResumeEnrichmentPipeline
     │
     ├── ExperienceEnricher
     │      ├── seniority
     │      ├── domains
     │      ├── functional areas
     │      ├── leadership
     │      ├── achievements
     │      ├── quantified impact
     │      └── experience gaps
     │
     ├── SeniorityDetector
     │
     ├── EducationEnricher
     │
     └── IndustryDetector
             │
             ▼
      ResumeEnrichment
             │
             ▼
        JD Matching
                                  """