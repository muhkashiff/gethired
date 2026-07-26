"""
Narrative Models

Shared by every AI engine.

Leadership
Promotion
Stability
Trajectory
Executive
Resume
JD
Matching
Cover Letter
Interview Coach
"""

from dataclasses import dataclass, field
from typing import List, Dict


# ==========================================================
# Narrative Paragraph
# ==========================================================

@dataclass
class NarrativeParagraph:

    heading: str = ""

    body: str = ""

    confidence: float = 1.0


# ==========================================================
# Recommendation
# ==========================================================

@dataclass
class Recommendation:

    priority: str = ""

    title: str = ""

    description: str = ""

    impact: str = ""


# ==========================================================
# Complete Narrative
# ==========================================================

@dataclass
class NarrativeReport:

    title: str = ""

    executive_summary: str = ""

    overall_assessment: str = ""

    strengths: List[str] = field(default_factory=list)

    development_areas: List[str] = field(default_factory=list)

    recommendations: List[Recommendation] = field(default_factory=list)

    paragraphs: List[NarrativeParagraph] = field(default_factory=list)

    evidence: List[str] = field(default_factory=list)

    confidence: float = 0.0

    metadata: Dict = field(default_factory=dict)