"""
Enterprise Knowledge Extraction Models

Enterprise V12

These models bridge Resume Parsing and Semantic Resolution.

Pipeline

Resume Sections
        ↓
Knowledge Parser
        ↓
Knowledge Facts
"""

from dataclasses import dataclass, field
from typing import List


# ==========================================================
# EXTRACTED SENTENCE
# ==========================================================

@dataclass
class ExtractedSentence:

    sentence_id: str = ""

    section: str = ""

    text: str = ""

    position: int = 0

    metadata: dict = field(default_factory=dict)


# ==========================================================
# ENTITY MATCH
# ==========================================================

@dataclass
class EntityMatch:

    entity_id: str = ""

    entity_type: str = ""

    canonical: str = ""

    matched_text: str = ""

    confidence: float = 1.0

    ontology_source: str = ""

    metadata: dict = field(default_factory=dict)


# ==========================================================
# EXTRACTION RESULT
# ==========================================================

@dataclass
class ExtractionResult:

    sentence: ExtractedSentence | None = None

    entities: List[EntityMatch] = field(default_factory=list)

    confidence: float = 0.0

    metadata: dict = field(default_factory=dict)