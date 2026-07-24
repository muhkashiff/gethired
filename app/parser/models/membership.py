from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Membership:

    organization: str = ""

    role: str = ""

    start_year: Optional[int] = None

    end_year: Optional[int] = None

    status: str = ""

    keywords: List[str] = field(default_factory=list)