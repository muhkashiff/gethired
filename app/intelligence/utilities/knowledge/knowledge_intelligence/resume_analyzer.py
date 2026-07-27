"""
Resume Intelligence Engine
"""

from statistics import mean

from app.intelligence.utilities.knowledge.knowledge_intelligence.intelligence_models import (
    ResumeIntelligence,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.leadership_analyzer import (
    LeadershipAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.quality_analyzer import (
    QualityAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_intelligence.operations_analyzer import (
    OperationsAnalyzer,
)

# Import these only if they already exist
# from app.intelligence.utilities.knowledge.knowledge_intelligence.manufacturing_analyzer import (
#     ManufacturingAnalyzer,
# )
#
# from app.intelligence.utilities.knowledge.knowledge_intelligence.food_safety_analyzer import (
#     FoodSafetyAnalyzer,
# )
#
# from app.intelligence.utilities.knowledge.knowledge_intelligence.supply_chain_analyzer import (
#     SupplyChainAnalyzer,
# )


class ResumeIntelligenceEngine:

    def __init__(self):

        self.leadership = LeadershipAnalyzer()

        self.quality = QualityAnalyzer()

        self.operations = OperationsAnalyzer()

        # Enable later when these analyzers are created

        # self.manufacturing = ManufacturingAnalyzer()

        # self.food_safety = FoodSafetyAnalyzer()

        # self.supply_chain = SupplyChainAnalyzer()

    # -----------------------------------------------------

    def analyze(self, document):

        intelligence = ResumeIntelligence()

        intelligence.leadership = self.leadership.analyze(document)

        intelligence.quality = self.quality.analyze(document)

        intelligence.operations = self.operations.analyze(document)

        # Uncomment when implemented

        # intelligence.manufacturing = self.manufacturing.analyze(document)

        # intelligence.food_safety = self.food_safety.analyze(document)

        # intelligence.supply_chain = self.supply_chain.analyze(document)

        scores = []

        if intelligence.leadership:
            scores.append(intelligence.leadership.score)

        if intelligence.quality:
            scores.append(intelligence.quality.score)

        if intelligence.operations:
            scores.append(intelligence.operations.score)

        intelligence.overall_score = round(mean(scores), 1) if scores else 0.0

        return intelligence