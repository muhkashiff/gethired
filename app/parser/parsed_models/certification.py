"""
GetHired
Certification Model

Represents a professional certification extracted
from a resume.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Certification:

    # ---------------------------------------------------------
    # Certification Name
    # Example:
    # Lead Auditor ISO 9001
    # PCQI Human Food
    # Six Sigma Green Belt
    # ---------------------------------------------------------

    name: str

    # ---------------------------------------------------------
    # Organization issuing the certificate
    # Examples:
    # CQI/IRCA
    # Highfield
    # FSPCA
    # Microsoft
    # AWS
    # ---------------------------------------------------------

    issuer: str = ""

    # ---------------------------------------------------------
    # Certification Category
    # Food Safety
    # Quality
    # Analytics
    # Project Management
    # IT
    # Lean Six Sigma
    # Leadership
    # ---------------------------------------------------------

    category: str = ""

    # ---------------------------------------------------------
    # Certification Level
    # Examples:
    # Lead Auditor
    # Level 4
    # Green Belt
    # Black Belt
    # Associate
    # Professional
    # Expert
    # ---------------------------------------------------------

    level: str = ""

    # ---------------------------------------------------------
    # Year Earned
    # ---------------------------------------------------------

    year: Optional[int] = None

    # ---------------------------------------------------------
    # Expiration Year (if applicable)
    # ---------------------------------------------------------

    expiry: Optional[int] = None

    # ---------------------------------------------------------
    # Credential Number / License ID
    # ---------------------------------------------------------

    credential_id: str = ""

    # ---------------------------------------------------------
    # URL to verify certification
    # ---------------------------------------------------------

    verification_url: str = ""

    # ---------------------------------------------------------
    # ATS Confidence Score
    # 0.0 – 1.0
    # ---------------------------------------------------------

    confidence: float = 1.0

    # ---------------------------------------------------------
    # Used later by ATS Matcher
    # ---------------------------------------------------------

    matched: bool = False

    # ---------------------------------------------------------
    # Matching Score
    # Used by ATS engine
    # ---------------------------------------------------------

    score: float = 0.0

    # ---------------------------------------------------------
    # Original Resume Text
    # Keeps original formatting for regeneration
    # ---------------------------------------------------------

    raw_text: str = ""

    # ---------------------------------------------------------
    # Normalized name used by Knowledge Base
    # Example:
    # "Lead Auditor ISO9001"
    # ->
    # "lead auditor iso 9001"
    # ---------------------------------------------------------

    normalized_name: Optional[str] = None