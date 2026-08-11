
"""
repository_v5/

    knowledge_entity.py

    loader.py

    repository.py

    cache.py

    matcher.py

    phrase_matcher.py

    fuzzy_matcher.py

    tokenizer.py

    normalizer.py

    paths.py

    

                        RESUME
                      │
                      ▼
              Sentence/Section
                      │
                      ▼
             Knowledge Pipeline
                      │
                      ▼
              Extractor Hub
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
 Technology        Actions         Skills
 Extractor        Extractor       Extractor
       │              │              │
       └──────────────┼──────────────┘
                      ▼
              Unified Knowledge
                   Result
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Resume Profile          Job Matching
          │                       │
          └───────────┬───────────┘
                      ▼
                 ATS Analysis


                                          repository_v5
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
       ontology            ontology            ontology
          │                   │                   │
   business_kpis.json     actions.json       relations.json
          │                   │                   │
          └──────────────┬────┴───────────────────┘
                         │
                 RepositoryLoader
                         │
                         ▼
                RepositoryEntity
                         │
                         ▼
                    Repository
                         │
              ┌──────────┴──────────┐
              │                     │
        Entity indexes        Relation indexes
              │                     │
              │              ┌──────┼───────┐
              │              │      │       │
              │           source  target   type
              │              │      │       │
              └──────────────┴──────┴───────┘
                             │
                             ▼
                    Entity Extractors
                             │
                 ┌───────────┴───────────┐
                 │                       │
          ActionExtractor          TargetExtractor
                 │                       │
                 └───────────┬───────────┘
                             │
                     RepositoryEntity
                             │
                             ▼
                     RelationExtractor
                             │
                             ▼
                    RelationKnowledge
                             │
                             ▼
                       Semantic Graph
    """