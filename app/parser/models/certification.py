from dataclasses import dataclass


@dataclass
class Certification:

    name: str = ""

    issuing_body: str = ""

    year: int = 0

    credential_id: str = ""

    expiration_year: int = 0

    category: str = ""

    international: bool = False