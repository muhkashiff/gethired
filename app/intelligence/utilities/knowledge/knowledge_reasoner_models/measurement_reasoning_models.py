"""
Measurement Reasoning Model
"""

from dataclasses import dataclass


@dataclass
class MeasurementReasoning:

    found: bool = False

    direction: str = ""

    effect: str = ""

    reasoning: str = ""

    confidence: float = 0.0