from dataclasses import dataclass


@dataclass
class DomainEvidence:

    food_safety: float = 0.0

    manufacturing: float = 0.0

    quality: float = 0.0

    laboratory: float = 0.0

    supply_chain: float = 0.0

    retail: float = 0.0

    operations: float = 0.0

    compliance: float = 0.0

    business_operations: float = 0.0

    customer_service: float = 0.0

    total_score: float = 0.0