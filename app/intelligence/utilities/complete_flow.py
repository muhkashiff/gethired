"""
                    GETHIRED INTELLIGENCE ENGINE
                              │
                              ▼
                     ┌─────────────────┐
                     │  RESUME / TEXT  │
                     └────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ KNOWLEDGE PARSER │
                    └────────┬─────────┘
                             │
                             ▼
                     KnowledgeDocument
                             │
                             ▼
                  ┌──────────────────────┐
                  │ SEMANTIC REASONING   │
                  │                      │
                  │ SemanticResolver     │
                  │ DependencyResolver   │
                  │ BusinessStatement    │
                  │ ClusterBuilder       │
                  │ Classifier           │
                  │ Metadata             │
                  └──────────┬───────────┘
                             │
                             ▼
                    SemanticResolution
                             │
                             ▼
                    Business Statements
                             │
                             ▼
                 ┌────────────────────────┐
                 │ KnowledgeGraphBuilder  │
                 └───────────┬────────────┘
                             │
                             ▼
                      KnowledgeGraph
                             │
             ┌───────────────┴───────────────┐
             │                               │
             ▼                               ▼
      KnowledgeProfile                ReasoningPipeline
                                             │
                                             ▼
                                   ReasoningContext
                                             │
                              ┌──────────────┼──────────────┐
                              ▼              ▼              ▼
                          Ontology        Domain          Skill
                          Reasoner       Reasoner       Reasoner
                              │              │              │
                              └──────────────┼──────────────┘
                                             ▼
                                      Achievement
                                       Reasoner
                                             │
                                             ▼
                                      Leadership
                                       Reasoner
                                             │
                                             ▼
                                      Executive
                                       Reasoner
                                             │
                                             ▼
                                    Recommendation
                                       Reasoner
                                             │
                                             ▼
                                    Career Reasoner
                                             │
                                             ▼
                                    Resume Reasoner
                                             │
                                             ▼
                                   Interview Reasoner

                                   
                                                       RAW RESUME / SENTENCE
                           │
                           ▼
                  ┌─────────────────┐
                  │  PARSING LAYER  │
                  └─────────────────┘
                           │
                           ▼
                 KnowledgeDocument
                           │
                           ▼
                  Parser Knowledge
                    Entities/Facts
                           │
                           ▼
                  ┌─────────────────┐
                  │ SEMANTIC LAYER  │
                  └─────────────────┘
                           │
                           ▼
                  SemanticEntity
                           │
                           ▼
                SemanticDependency
                           │
                           ▼
              BusinessStatementBuilder
                           │
                           ▼
                  BusinessStatement
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Statement Entities    Statement Relations
                │                     │
                └──────────┬──────────┘
                           ▼
                KnowledgeGraphBuilder
                           │
                           ▼
                    KnowledgeGraph
                           │
                           ▼
              ┌──────────────────────┐
              │ REASONING ENGINE     │
              └──────────────────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
         Ontology       Domain         Skill
         Reasoner       Reasoner       Reasoner
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                     Achievement
                       Reasoner
                           │
                           ▼
                    Leadership
                       Reasoner
                           │
                           ▼
                    Executive
                       Reasoner
                           │
                           ▼
                  Recommendation
                       Reasoner
                           │
                           ▼
                     Career
                       Reasoner
                           │
                           ▼
                     Resume
                       Reasoner
                           │
                           ▼
                   Interview
                       Reasoner
                           │
                           ▼
                 ReasoningContext
                           │
                           ▼
             PipelineExecutionReport


             RAW RESUME / BUSINESS TEXT
        │
        ▼
┌─────────────────────────┐
│ Knowledge Pipeline      │
│                         │
│ ClauseParser            │
│ ClauseRebuilder         │
│ ClauseNormalizer        │
│ ActionSegmenter         │
│ SentenceParser          │
└────────────┬────────────┘
             │
             ▼
      KnowledgeDocument
             │
             ▼
┌─────────────────────────┐
│ Semantic Resolution     │
│                         │
│ Parser Entities         │
│        ↓                │
│ SemanticEntity          │
│        ↓                │
│ DependencyResolver      │
│        ↓                │
│ BusinessStatementBuilder│
│        ↓                │
│ StatementRelation       │
│        ↓                │
│ ClusterBuilder          │
│ ClusterClassifier       │
│ MetadataBuilder         │
└────────────┬────────────┘
             │
             ▼
     SemanticResolution
             │
             ▼
┌─────────────────────────┐
│ KnowledgeGraphBuilder   │
│                         │
│ BusinessStatement       │
│      ↓                  │
│ GraphNode               │
│ GraphEdge               │
└────────────┬────────────┘
             │
             ▼
       KnowledgeGraph
             │
             ▼
┌─────────────────────────┐
│ Reasoning Pipeline      │
│                         │
│ OntologyReasoner        │
│        ↓                │
│ DomainReasoner          │
│        ↓                │
│ SkillReasoner           │
│        ↓                │
│ AchievementReasoner     │
│        ↓                │
│ LeadershipReasoner      │
│        ↓                │
│ ExecutiveReasoner       │
│        ↓                │
│ RecommendationReasoner  │
│        ↓                │
│ CareerReasoner          │
│        ↓                │
│ ResumeReasoner          │
│        ↓                │
│ InterviewReasoner       │
└────────────┬────────────┘
             │
             ▼
     ReasoningContext
             │
             ▼
      Intelligence Layer
             │
             ▼
      Resume / Interview /
      Career Recommendations



                           DOCUMENT
                   /          \
              RESUME           JD
                 \              /
                  \            /
                   SAME PIPELINE
                         │
                         ▼
                    EXTRACTORS
                         │
                         ▼
                 KnowledgeEntity
                         │
                         ▼
                 SemanticEntity
                  + statement_id
                         │
                         ▼
                 SEMANTIC REASONERS
                         │
                         ▼
               SemanticDependency
                         │
                         ▼
             BUSINESS STATEMENT BUILDER
                         │
                         ▼
                 BusinessStatement
                  ├── entities
                  ├── relations
                  └── metadata
                         │
                         ▼
              KNOWLEDGE GRAPH BUILDER
                         │
                         ▼
                   KnowledgeGraph
                  ├── GraphNodes
                  └── GraphEdges
                         │
                         ▼
                KNOWLEDGE PROFILE
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        RESUME PROFILE          JD PROFILE
             │                       │
             └───────────┬───────────┘
                         ▼
                  JD COMPARATOR
                         │
                         ▼
                   GAP ANALYSIS
                         │
                         ▼
                  ATS OPTIMIZER
                         │
                         ▼
                  UPDATED RESUME



                                      INPUT TEXT
                        │
                        ▼
              ┌───────────────────┐
              │ ExtractionRequest │
              │                   │
              │ text              │
              │ statement_id      │
              │ source_type       │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ KnowledgePipeline │
              │ Matcher / Ontology│
              └─────────┬─────────┘
                        │
             MatchResult objects
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
   ActionExtractor  MetricExtractor  SkillExtractor
        │               │                │
        └───────────────┼────────────────┘
                        ▼
              SemanticEntity objects
                        │
                        │
                        ▼
              ┌────────────────────┐
              │ DependencyResolver │
              │ / Reasoners        │
              └─────────┬──────────┘
                        │
                        ▼
             SemanticDependency objects
                        │
                        ▼
          ┌──────────────────────────┐
          │ BusinessStatementBuilder │
          └────────────┬─────────────┘
                       │
                       ▼
             BusinessStatement
             ├── statement_id
             ├── entities
             ├── relations
             ├── metadata
             └── confidence
                       │
                       ▼
          ┌──────────────────────────┐
          │   KnowledgeGraphBuilder  │
          └────────────┬─────────────┘
                       │
                       ▼
                KnowledgeGraph
                       │
                       ▼
               KnowledgeProfile
                       │
                       ▼
             Resume / JD Comparison
                       │
                       ▼
             Gap / Match Analysis
                       │
                       ▼
             Resume Optimization


                          RESUME
                │
                ▼
        Shared Knowledge Pipeline
                │
                ▼
          Resume Graph
                │
                ▼
        Resume KnowledgeProfile
                │
                │
                │
                │
JD ─────────────┤
                │
                ▼
        Shared Knowledge Pipeline
                │
                ▼
            JD Graph
                │
                ▼
          JD KnowledgeProfile
                │
                ▼
       ┌─────────────────────┐
       │ Knowledge Comparator│
       └──────────┬──────────┘
                  ▼
            Gap Analysis



            ========================================================
                 INPUT / DOCUMENT LAYER
========================================================

Resume
JD
Other Business Text

                │
                ▼

========================================================
               EXTRACTION LAYER
========================================================

ExtractionRequest
        ↓
KnowledgePipeline
        ↓
MatchResult
        ↓
BaseExtractor
        ↓
Domain Extractors

ActionExtractor
Object/TargetExtractor
MetricExtractor
MeasurementExtractor
SkillExtractor
StandardExtractor
MethodologyExtractor
DomainExtractor
KPIExtractor
AchievementExtractor
...

                │
                ▼

========================================================
              SEMANTIC ENTITY LAYER
========================================================

SemanticEntity

    entity_id
    statement_id
    entity_type
    canonical
    normalized
    confidence
    ontology_name
    business_area
    domain
    metadata
    position
    ...

                │
                ▼

========================================================
                REASONING LAYER
========================================================

DependencyResolver
Semantic Reasoners

        ↓

SemanticDependency

    source_entity
    target_entity
    relation
    confidence
    metadata

                │
                ▼

========================================================
             STATEMENT LAYER
========================================================

BusinessStatementBuilder

        ↓

BusinessStatement

    statement_id
    label
    confidence
    semantic_type
    primary_domain
    business_area
    achievement

    entities[]
    relations[]

                │
                ▼

========================================================
                 GRAPH LAYER
========================================================

KnowledgeGraphBuilder

        ↓

KnowledgeGraph

    GraphNode[]
    GraphEdge[]

                │
                ▼

========================================================
                PROFILE LAYER
========================================================

KnowledgeProfileBuilder

        ↓

KnowledgeProfile

                │
                ├──────── Resume Profile
                │
                └──────── JD Profile

                ▼

========================================================
             COMPARISON LAYER
========================================================

KnowledgeComparator

        ↓

Match
Gap
Missing Skill
Missing Standard
Missing Methodology
Missing KPI
Missing Achievement
Missing Domain
Missing Evidence

                │
                ▼

========================================================
             OPTIMIZATION LAYER
========================================================

ResumeOptimizationPlanner

        ↓

Recommended Changes

        ↓

ResumeCustomizer

        ↓

Optimized Resume
"""