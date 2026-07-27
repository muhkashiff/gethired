from dataclasses import dataclass, field


@dataclass
class OntologyEntity:

    id: str = ""

    canonical: str = ""

    aliases: list = field(default_factory=list)

    category: str = ""

    business_area: str = ""

    description: str = ""

    metadata: dict = field(default_factory=dict)