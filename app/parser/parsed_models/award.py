from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Award:

    title: str = ""

    issuer: str = ""

    year: Optional[int] = None

    description: str = ""

    category: str = ""

    keywords: List[str] = field(default_factory=list)