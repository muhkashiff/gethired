""""

                    ┌─────────────────────┐
                    │    RESUME DOCX      │
                    └──────────┬──────────┘
                               │
                               ▼
                    Resume Ingestion Layer
                               │
                               ▼
                    Resume Structural Parser
                               │
                               ▼
                    Resume Parser Extractors
                               │
                               ▼
                    Resume Ontology Parser
                               │
                               ▼
                    Resume Evidence Model
                               │
                               ▼
                    Resume Intelligence
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
        Leadership       Career Progression   Capability
        Analysis              Analysis         Analysis
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                     CANDIDATE PROFILE
                               │
                               │
                               │
                    ┌──────────▼──────────┐
                    │    JOB DESCRIPTION  │
                    └──────────┬──────────┘
                               │
                               ▼
                       JD Ingestion Layer
                               │
                               ▼
                         JD Parser
                               │
                               ▼
                       JD Extractors
                               │
                               ▼
                       JD Ontology Parser
                               │
                               ▼
                         JD Evidence Model
                               │
                               ▼
                         JOB INTELLIGENCE
                               │
             ┌─────────────────┼──────────────────┐
             │                 │                  │
             ▼                 ▼                  ▼
        Required Skills    Responsibilities    Requirements
        Technologies       Actions             Certifications
        Domains            Targets             Experience
        Metrics            Methodologies        Education
                               │
                               ▼
                    ┌─────────────────────┐
                    │   MATCHING ENGINE   │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
          ▼                    ▼                    ▼
     Skill Match         Experience Match     Ontology Match
          │                    │                    │
          ▼                    ▼                    ▼
     Missing Skills      Missing Evidence     Domain Match
          │                    │                    │
          └────────────────────┼────────────────────┘
                               ▼
                       CANDIDATE-JD SCORE
                               │
                               ▼
                       ATS ANALYSIS
                               │
                               ▼
                    GAP / RISK ANALYSIS
                               │
                               ▼
                    RECOMMENDATION ENGINE
                               │
                ┌──────────────┼───────────────┐
                │              │               │
                ▼              ▼               ▼
          Resume Changes   Skill Gaps     Positioning
                │              │               │
                └──────────────┼───────────────┘
                               ▼
                       RESUME CUSTOMIZER
                               │
                               ▼
                         UPDATED DOCX

                         CANDIDATE-JD ANALYSIS
══════════════════════════════════

Overall Match:             84%
ATS Compatibility:         92%
Evidence Strength:         88%

STRONG MATCHES
──────────────────────────────
✓ HACCP
✓ FSSC 22000
✓ BRCGS
✓ Six Sigma
✓ Quality Management
✓ Food Safety
✓ Operations
✓ Team Leadership

PARTIAL MATCHES
──────────────────────────────
△ Data Analytics
△ Continuous Improvement
△ Production Optimization

MISSING / WEAK
──────────────────────────────
✗ Power BI
✗ SAP
✗ ISO 45001

EXPERIENCE GAP
──────────────────────────────
JD asks: 7+ years Quality Management
Resume evidence: strong related experience

RECOMMENDATIONS
──────────────────────────────
1. Bring FSSC 22000 certification achievement into
   the top third of the resume.

2. Add measurable quality/operations achievements.

3. Surface Six Sigma earlier.

4. Highlight leadership evidence rather than listing
   "Leadership" as a skill.

5. Add Power BI only if genuinely possessed.

6. Do not add unsupported keywords merely for ATS.


LAYER 1 — INGESTION
────────────────────────
DOCX Resume Reader
JD Reader
Document preservation
Source locations


LAYER 2 — STRUCTURAL PARSING
────────────────────────
ResumeParser
SectionDetector
JDParser
Section detection
Experience records
Education records
etc.


LAYER 3 — EXTRACTION
────────────────────────
Parser Models
Ontology Parser Extractors
Non-Ontology Parser Extractors

Domains
Actions
Targets
Metrics
Methodologies
Technologies
Dates
Leadership evidence
Career evidence
etc.


LAYER 4 — INTELLIGENCE
────────────────────────
Resume Intelligence
JD Intelligence
Evidence Graph
Capability Analysis
Career Progression
Leadership Analysis
Requirement Analysis


LAYER 5 — DECISION / OUTPUT
────────────────────────
Resume ↔ JD Matching
ATS Analysis
Gap Analysis
Candidate Score
Recommendations
Resume Customization
Updated DOCX
"""