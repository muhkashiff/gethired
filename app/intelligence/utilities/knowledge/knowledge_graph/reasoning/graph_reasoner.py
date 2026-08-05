"""
Enterprise Graph Reasoner

Master Orchestrator

This class is the ONLY public reasoning entry point.

Every engine should call GraphReasoner instead of
calling individual reasoners.

Enterprise V5
"""

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.graph_reasoning_result import (
    GraphReasoningResult,
)

# ---------------------------------------------------------
# Individual Reasoners
# ---------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.dependency_reasoner import (
    DependencyReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.ontology_reasoner import (
    OntologyReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.skill_reasoner import (
    SkillReasoner,
)

# Future

# from achievement_reasoner import AchievementReasoner
# from leadership_reasoner import LeadershipReasoner
# from seniority_reasoner import SeniorityReasoner
# from executive_reasoner import ExecutiveReasoner


class GraphReasoner:
    """
    Enterprise Knowledge Graph Orchestrator.

    Executes all reasoning modules in the correct order.

    Dependency

        ↓

    Ontology

        ↓

    Skills

        ↓

    Achievement

        ↓

    Leadership

        ↓

    Seniority

        ↓

    Executive

    """

    ###############################################################

    def __init__(self):

        self.dependency_reasoner = DependencyReasoner()

        self.ontology_reasoner = OntologyReasoner()

        self.skill_reasoner = SkillReasoner()

        # Future

        self.achievement_reasoner = None

        self.leadership_reasoner = None

        self.seniority_reasoner = None

        self.executive_reasoner = None

    ###############################################################

    def analyze(self, graph):

        """
        Execute enterprise reasoning pipeline.
        """

        result = GraphReasoningResult()

        ###########################################################
        # Dependency Reasoning
        ###########################################################

        result.dependencies = (

            self.dependency_reasoner.analyze(graph)

        )

        ###########################################################
        # Ontology Reasoning
        ###########################################################

        result.ontology = (

            self.ontology_reasoner.analyze(graph)

        )

        ###########################################################
        # Skill Reasoning
        ###########################################################

        result.skills = (

            self.skill_reasoner.analyze(graph)

        )

        ###########################################################
        # Future Modules
        ###########################################################

        if self.achievement_reasoner:

            result.achievement = (

                self.achievement_reasoner.analyze(

                    graph,

                    result,

                )

            )

        if self.leadership_reasoner:

            result.leadership = (

                self.leadership_reasoner.analyze(

                    graph,

                    result,

                )

            )

        if self.seniority_reasoner:

            result.seniority = (

                self.seniority_reasoner.analyze(

                    graph,

                    result,

                )

            )

        if self.executive_reasoner:

            result.executive = (

                self.executive_reasoner.analyze(

                    graph,

                    result,

                )

            )

        ###########################################################

        return result
    