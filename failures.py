
"""

The failures you have seen prove this:

ResumeKnowledgePipeline.process_sentence() was missing → integration was using the wrong version.
DomainEvidence.scores missing → old WeightedScoreEngine expected an old evidence-model contract.
SummaryProfile.__init__() rejected domain_score → old ProfileBuilder was constructing an obsolete SummaryProfile.
MatchResult objects reached semantic resolver = 0 → the enterprise pipeline was consuming the KnowledgeFact output instead of carrying the actual V5 MatchResult[] forward.
Most importantly, your graph already contains much richer information than the old profile builder consumes.
KnowledgeEntity.impact_weight = 1.0 is part of the base entity model, so impact must be carried all the way from entity → semantic entity → graph node → profile scoring.
ATS is also an entity-level scoring dimension and should not be reconstructed from the old CapabilityEvidence pipeline.

So I would stop patching the old ProfileBuilder.


Resume
   │
   ▼
SectionDetector
   │
   ▼
KnowledgeDocumentBuilder
   │
   ▼
KnowledgeDocument
   │
   ▼
EnterpriseResumeKnowledgePipeline
   │
   ├── KnowledgeFact[]
   └── MatchResult[]
          │
          ▼
     SemanticResolver
          │
          ├── SemanticEntity[]
          ├── SemanticDependency[]
          ├── BusinessStatement[]
          ├── Cluster[]
          └── SemanticMetadata
                  │
                  ▼
          KnowledgeGraphBuilder
                  │
                  ▼
             KnowledgeGraph
                  │
                  ▼
        EnterpriseKnowledgeProfileBuilder
                  │
                  ├── entity evidence
                  ├── impact scoring
                  ├── ATS scoring
                  ├── domain scoring
                  ├── leadership
                  ├── technical
                  ├── executive
                  ├── business value
                  ├── achievements
                  ├── metrics
                  ├── seniority
                  └── career
                  │
                  ▼
             KnowledgeProfile


             Resume
 │
 ▼
ResumeReader
 │
 ▼
ResumeParser
 │
 ▼
ResumeSection[]
 │
 ▼
KnowledgeDocumentBuilder
 │
 ▼
KnowledgeDocument
 │
 ▼
EnterpriseResumeKnowledgePipeline
 │
 ├── KnowledgeFact[]
 └── MatchResult[]
          │
          ▼
   SemanticResolver
          │
          ├── SemanticEntity[]
          ├── SemanticDependency[]
          ├── BusinessStatement[]
          ├── Cluster[]
          └── SemanticMetadata
          │
          ▼
   KnowledgeGraphBuilder
          │
          ▼
      KnowledgeGraph
          │
          ▼
EnterpriseKnowledgeProfileBuilder
          │
          ├── AchievementProfile
          ├── LeadershipProfile
          ├── SeniorityProfile
          ├── MetricProfile
          ├── DomainProfile
          ├── ModifierProfile
          └── SummaryProfile
          │
          ▼
   KnowledgeProfile


   | Priority | Component                                   | Action                                                                                               |
| -------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1        | `ExtractionCoordinator`                     | Preserve `MatchResult[]`                                                                             |
| 2        | `ExtractionCoordinator`                     | Add technologies, methodologies, BKPI and other tested ontologies                                    |
| 3        | `SemanticEntity / BusinessStatementBuilder` | Normalize `technologie`/`methodologie` without destroying repository identity                        |
| 4        | `EnterpriseResumePipeline`                  | Pass actual `MatchResult[]` → `SemanticResolver` → Graph                                             |
| 5        | `ProfileBuilder`                            | Replace old evidence/score-engine orchestration with graph-aware `EnterpriseKnowledgeProfileBuilder` |

"""