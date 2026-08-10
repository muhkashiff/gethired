""""
Resume Sentence
       │
       ▼
Metric Extractor
       │
       ▼
MetricKnowledge
       │
       │ higher_is_better
       ▼
MeasurementParser
       │
       ├── RangeDetector
       ├── DeltaDetector
       └── AbsoluteDetector
       │
       ▼
MeasurementExtractor
       │
       ├── change_value
       ├── direction
       └── improvement
       │
       ▼
MeasurementKnowledge


                 RESUME SENTENCE
                        │
                        ▼
              ┌─────────────────┐
              │ Metric Extractor │
              └────────┬────────┘
                       │
                       ▼
                MetricKnowledge
                       │
                       ▼
              ┌─────────────────┐
              │MeasurementParser│
              └────────┬────────┘
                       │
                       ▼
             MeasurementKnowledge
                       │
                       ▼
              ┌─────────────────┐
              │ Domain Extractor │
              └─────────────────┘
                       │
                       ▼
                 DomainKnowledge
                       │
                       ▼
              ┌─────────────────┐
              │ KPI Extractor   │
              └─────────────────┘
                       │
                       ▼
                 KPIKnowledge
                       │
                       ▼
              Relationship Layer
                       │
                       ▼
             Business Interpretation
"""