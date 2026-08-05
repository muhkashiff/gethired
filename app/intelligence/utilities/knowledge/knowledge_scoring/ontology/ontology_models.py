"""
Enterprise Ontology Models

Enterprise V12

Universal knowledge object used across
all scoring engines.
"""

from dataclasses import dataclass, field


# ==========================================================
# Capability Weight
# ==========================================================

@dataclass
class CapabilityWeight:

    capability: str

    weight: float = 1.0


# ==========================================================
# Ontology Item
# ==========================================================

@dataclass
class OntologyItem:

    # ---------------------------------------
    # Identity
    # ---------------------------------------

    canonical: str = ""

    category: str = ""

    aliases: list[str] = field(default_factory=list)

    description: str = ""

    # ---------------------------------------
    # Capability Mapping
    # ---------------------------------------

    capabilities: list[CapabilityWeight] = field(default_factory=list)

    # ---------------------------------------
    # Metadata
    # ---------------------------------------

    metadata: dict = field(default_factory=dict)