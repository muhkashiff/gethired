from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Publication:

    title: str = ""

    publisher: str = ""

    year: Optional[int] = None

    link: str = ""

    authors: List[str] = field(default_factory=list)

    keywords: List[str] = field(default_factory=list)

    publication_type: str = ""