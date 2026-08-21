"""

                    ┌──────────────────────┐
                    │   DOCUMENT UPLOAD    │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   DOCUMENT ROUTER    │
                    └──────────┬───────────┘
                               ↓
                ┌──────────────────────────────┐
                │ SAME KNOWLEDGE PIPELINE      │
                └──────────────┬───────────────┘
                               ↓
                 ┌─────────────┴─────────────┐
                 ↓                           ↓
          ResumeProfile                 JDProfile
                 │                           │
                 └─────────────┬─────────────┘
                               ↓
                       KnowledgeMatcher
                               ↓
                     KnowledgeMatchProfile
                               ↓
                         GapAnalyzer
                               ↓
                        ATS Calculator
                               ↓
                    Comparative Summary
                               ↓
                  Resume Recommendations
                               ↓
                  Truth-Safe Cover Letter
                               ↓
                         Frontend


                         PHASE 1
DocumentType support
Resume/JD pipeline reuse

PHASE 2
JD-specific interpretation metadata
Requirement classification

PHASE 3
KnowledgeMatcher

PHASE 4
KnowledgeMatchProfile

PHASE 5
GapAnalyzer

PHASE 6
ATS calculation

PHASE 7
Comparative descriptive summary

PHASE 8
Resume improvement recommendations

PHASE 9
Truth-safe CoverLetterGenerator

PHASE 10
Frontend integration

                         """