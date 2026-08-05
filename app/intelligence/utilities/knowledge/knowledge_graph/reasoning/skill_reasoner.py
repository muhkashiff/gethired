"""
Enterprise Skill Reasoner

Enterprise V6

Responsible for enterprise skill intelligence.

Pipeline

Knowledge Graph

↓

Extract Skill Nodes

↓

Cluster Builder

↓

Technical Depth

↓

Business Breadth

↓

Future Readiness

↓

Recommendation Engine

↓

Statistics

↓

GraphReasoningResult.skills

Author
------
GETHIRED Enterprise AI
"""

from collections import Counter

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    SkillReasoningResult,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.skill_cluster_builder import (
    SkillClusterBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.technical_depth import (
    TechnicalDepthAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.business_breadth import (
    BusinessBreadthAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.future_readiness import (
    FutureReadinessAnalyzer,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.recommendation_engine import (
    RecommendationEngine,
)


class SkillReasoner:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.cluster_builder = SkillClusterBuilder()

        self.depth_analyzer = TechnicalDepthAnalyzer()

        self.breadth_analyzer = BusinessBreadthAnalyzer()

        self.future_analyzer = FutureReadinessAnalyzer()

        self.recommendation_engine = RecommendationEngine()

    ####################################################################
    # PUBLIC API
    ####################################################################

    def analyze(

        self,

        graph,

        reasoning,

    ):

        """
        Enterprise Skill Reasoning
        """

        result = SkillReasoningResult()

        ###############################################################
        # STEP 1
        # Extract Skill Nodes
        ###############################################################

        result.skill_nodes = self._extract_skill_nodes(graph)

        ###############################################################
        # STEP 2
        # Build Skill Clusters
        ###############################################################

        result.skill_clusters = (

            self.cluster_builder.build(

                result.skill_nodes

            )

        )

        ###############################################################
        # STEP 3
        # Technical Depth
        ###############################################################

        result.technical_depth = (

            self.depth_analyzer.analyze(

                result.skill_clusters

            )

        )

        ###############################################################
        # STEP 4
        # Business Breadth
        ###############################################################

        result.business_breadth = (

            self.breadth_analyzer.analyze(

                result.skill_clusters

            )

        )

        ###############################################################
        # STEP 5
        # Future Readiness
        ###############################################################

        result.future_readiness = (

            self.future_analyzer.analyze(

                result.skill_clusters

            )

        )

        ###############################################################
        # STEP 6
        # Recommendations
        ###############################################################

        result.recommendations = (

            self.recommendation_engine.generate(

                result.technical_depth,

                result.business_breadth,

                result.future_readiness,

                result.skill_clusters,

            )

        )

        ###############################################################
        # STEP 7
        # Statistics
        ###############################################################

        result.category_distribution = (

            self._build_category_distribution(

                result.skill_nodes

            )

        )

        result.domain_distribution = (

            self._build_domain_distribution(

                result.skill_nodes

            )

        )

        result.derived_skills = (

            self._build_derived_skills(

                result.skill_clusters

            )

        )

        result.overall_score = (

            self._calculate_overall_score(

                result

            )

        )

        result.confidence = (

            self._calculate_confidence(

                result.skill_nodes

            )

        )

        ###############################################################
        # STEP 8
        # Save into Global Reasoning Object
        ###############################################################

        reasoning.skills = self._finalize_result(result)

        reasoning.reasoning_steps.append(

            "Skill Reasoning"

        )

        return reasoning
        ####################################################################
    # SKILL EXTRACTION
    ####################################################################

    def _extract_skill_nodes(

        self,

        graph,

    ):

        """
        Extract skill entities from knowledge graph.

        The graph already contains normalized
        ontology objects.

        This layer only collects them.
        """

        return [

            node

            for node in graph.get_nodes()

            if getattr(

                node,

                "entity_type",

                "",

            ) == "skill"

        ]


    ####################################################################
    # CATEGORY DISTRIBUTION
    ####################################################################

    def _build_category_distribution(

        self,

        skills,

    ):

        """
        Builds skill category intelligence.

        Example:

        Programming       5

        Food Safety       8

        Quality           4

        """

        return dict(

            Counter(

                getattr(

                    skill,

                    "category",

                    "",

                )

                for skill in skills

                if getattr(

                    skill,

                    "category",

                    "",

                )

            )

        )


    ####################################################################
    # DOMAIN DISTRIBUTION
    ####################################################################

    def _build_domain_distribution(

        self,

        skills,

    ):

        """
        Builds business/domain coverage.
        """

        return dict(

            Counter(

                getattr(

                    skill,

                    "business_area",

                    "",

                )

                for skill in skills

                if getattr(

                    skill,

                    "business_area",

                    "",

                )

            )

        )


    ####################################################################
    # DERIVED SKILLS
    ####################################################################

    def _build_derived_skills(

        self,

        clusters,

    ):

        """
        Converts capability clusters into
        derived enterprise skills.

        Example:

        Python
        Pandas
        NumPy

        becomes

        Machine Learning
        """

        return [

            cluster.name

            for cluster in clusters

        ]


    ####################################################################
    # OVERALL SKILL SCORE
    ####################################################################

    def _calculate_overall_score(

        self,

        result,

    ):

        """
        Calculates combined skill intelligence score.

        Components:

        Technical Depth

        Business Breadth

        Future Readiness
        """

        scores = [

            getattr(

                result.technical_depth,

                "overall",

                0,

            ),

            getattr(

                result.business_breadth,

                "overall",

                0,

            ),

            getattr(

                result.future_readiness,

                "overall",

                0,

            ),

        ]


        valid_scores = [

            score

            for score in scores

            if score is not None

        ]


        if not valid_scores:

            return 0.0


        return round(

            sum(valid_scores)

            /

            len(valid_scores),

            2,

        )


    ####################################################################
    # CONFIDENCE CALCULATION
    ####################################################################

    def _calculate_confidence(

        self,

        skills,

    ):

        """
        Calculates reasoning confidence.

        Based on confidence of extracted
        skill nodes.
        """

        if not skills:

            return 0.0


        confidence_values = [

            getattr(

                skill,

                "confidence",

                1.0,

            )

            for skill in skills

        ]


        return round(

            sum(confidence_values)

            /

            len(confidence_values),

            2,

        )
        ####################################################################
    # REASONING METADATA
    ####################################################################

    def _build_metadata(

        self,

        result,

    ):

        """
        Builds diagnostic metadata.

        Used for explainability,
        debugging and analytics.
        """

        return {

            "skill_count": len(

                result.skill_nodes

            ),

            "cluster_count": len(

                result.skill_clusters

            ),

            "derived_skill_count": len(

                result.derived_skills

            ),

            "recommendation_count": len(

                result.recommendations

            ),

            "technical_depth_score":

                getattr(

                    result.technical_depth,

                    "overall",

                    0,

                ),

            "business_breadth_score":

                getattr(

                    result.business_breadth,

                    "overall",

                    0,

                ),

            "future_readiness_score":

                getattr(

                    result.future_readiness,

                    "overall",

                    0,

                ),

        }


    ####################################################################
    # VALIDATION
    ####################################################################

    def _validate_result(

        self,

        result,

    ):

        """
        Ensures reasoning output
        is complete.

        Enterprise safety layer.
        """

        warnings = []


        if not result.skill_nodes:

            warnings.append(

                "No skill nodes detected"

            )


        if not result.skill_clusters:

            warnings.append(

                "No capability clusters generated"

            )


        if result.confidence < 0.5:

            warnings.append(

                "Low skill reasoning confidence"

            )


        return warnings


    ####################################################################
    # FINALIZE RESULT
    ####################################################################

    def _finalize_result(

        self,

        result,

    ):

        """
        Final preparation before
        attaching to global reasoning state.
        """

        result.metadata = (

            self._build_metadata(

                result

            )

        )


        result.warnings = (

            self._validate_result(

                result

            )

        )


        return result