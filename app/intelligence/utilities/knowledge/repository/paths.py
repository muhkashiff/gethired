"""
Knowledge Paths

Single source of truth for every JSON location.
"""

from pathlib import Path

# repository/
CURRENT = Path(__file__).resolve().parent

# knowledge/
KNOWLEDGE_ROOT = CURRENT.parent

# knowledge/knowledge_knowledge/
DATA_ROOT = KNOWLEDGE_ROOT / "knowledge_knowledge"

CONFIG = DATA_ROOT / "config"

ONTOLOGY = DATA_ROOT / "ontology"

SEMANTICS = DATA_ROOT / "semantics"