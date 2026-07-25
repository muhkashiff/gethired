from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Education:

    degree: str = ""

    major: str = ""

    institution: str = ""

    location: str = ""

    graduation_year: int = 0

    level: str = ""

    keywords: List[str] = field(default_factory=list)