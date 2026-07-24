from dataclasses import dataclass
from typing import Optional


@dataclass
class Reference:

    name: str = ""

    designation: str = ""

    company: str = ""

    relationship: str = ""

    email: str = ""

    phone: str = ""

    linkedin: str = ""

    address: str = ""

    years_known: Optional[float] = None

    available_on_request: bool = False

    notes: str = ""