"""
Enterprise Reasoning Pipeline

Enterprise V7

Purpose
-------
Central orchestration engine for all enterprise
knowledge graph reasoners.

Pipeline

Knowledge Graph
        │
        ▼
Reasoner Registry
        │
        ▼
Ontology
        │
        ▼
Dependency
        │
        ▼
Skill
        │
        ▼
Achievement
        │
        ▼
Leadership
        │
        ▼
Executive
        │
        ▼
Recommendation
        │
        ▼
Career
        │
        ▼
Resume
        │
        ▼
Interview

Output

ReasoningContext
PipelineExecutionReport
"""

from time import perf_counter

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.reasoning_context import (
    ReasoningContext,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.reasoner_registry import (
    ReasonerRegistry,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.execution_status import (
    ExecutionStatus,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.pipeline_execution_report import (
    PipelineExecutionReport,
    ReasonerExecution,
)

# ----------------------------------------------------------
# Built-in Reasoners
# ----------------------------------------------------------

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.ontology_reasoner import (
    OntologyReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.dependency_reasoner import (
    DependencyReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.skill_reasoner import (
    SkillReasoner,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.achievement_reasoner import (
    AchievementReasoner,
)

# Future Registration

# from leadership_reasoner import LeadershipReasoner
# from executive_reasoner import ExecutiveReasoner
# from recommendation_reasoner import RecommendationReasoner
# from career_reasoner import CareerReasoner
# from resume_reasoner import ResumeReasoner
# from interview_reasoner import InterviewReasoner


class ReasoningPipeline:

    """
    Enterprise orchestration engine.

    Every reasoner receives exactly one object:

        ReasoningContext

    Every reasoner returns exactly one object:

        BaseReasoningResult
    """

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.registry = ReasonerRegistry()

        self._register_default_reasoners()

    ####################################################################
    # DEFAULT REGISTRATION
    ####################################################################

    def _register_default_reasoners(self):

        """
        Register enterprise built-in reasoners.
        """

        self.registry.register_many(

            [

                OntologyReasoner(),

                DependencyReasoner(),

                SkillReasoner(),

                AchievementReasoner(),

                # Future

                # LeadershipReasoner(),

                # ExecutiveReasoner(),

                # RecommendationReasoner(),

                # CareerReasoner(),

                # ResumeReasoner(),

                # InterviewReasoner(),

            ]

        )

    ####################################################################
    # PUBLIC API
    ####################################################################

    def register_reasoner(

        self,

        reasoner,

    ):

        """
        Register external plugin reasoner.
        """

        self.registry.register(

            reasoner

        )

    ####################################################################
    # REMOVE
    ####################################################################

    def unregister_reasoner(

        self,

        reasoner,

    ):

        self.registry.unregister(

            reasoner

        )

    ####################################################################
    # ENABLE
    ####################################################################

    def enable_reasoner(

        self,

        reasoner_name,

    ):

        self.registry.enable(

            reasoner_name

        )

    ####################################################################
    # DISABLE
    ####################################################################

    def disable_reasoner(

        self,

        reasoner_name,

    ):

        self.registry.disable(

            reasoner_name

        )

    ####################################################################
    # MAIN EXECUTION
    ####################################################################

    def run(

        self,

        graph,

        parsed_resume=None,

    ):

        """
        Execute the complete enterprise reasoning pipeline.

        Returns

            (
                ReasoningContext,
                PipelineExecutionReport,
            )
        """

        ###############################################################
        # Pipeline Timer
        ###############################################################

        pipeline_start = perf_counter()

        ###############################################################
        # Context
        ###############################################################

        context = ReasoningContext()

        context.graph = graph

        context.parsed_resume = parsed_resume

        ###############################################################
        # Execution Report
        ###############################################################

        report = PipelineExecutionReport()

        report.status = ExecutionStatus.SUCCESS

        ###############################################################
        # Execute Every Registered Reasoner
        ###############################################################

        for reasoner in self.registry.get_reasoners():

            execution = ReasonerExecution()

            execution.name = reasoner.name

            execution.priority = getattr(

                reasoner,

                "priority",

                999,

            )

            execution.output_name = getattr(

                reasoner,

                "output_name",

                "",

            )

            ###########################################################
            # Dependency Validation
            ###########################################################

            dependency_error = self._validate_dependencies(

                context,

                reasoner,

            )

            if dependency_error:

                execution.status = ExecutionStatus.SKIPPED

                execution.validation_errors.append(

                    dependency_error

                )

                report.add_execution(

                    execution

                )

                continue

            ###########################################################
            # Execute Reasoner
            ###########################################################

            start = perf_counter()

            try:

                result = reasoner.run(

                    context

                )

                elapsed = (

                    perf_counter()

                    - start

                )

                #######################################################
                # Populate Result
                #######################################################

                result.execution_time = round(

                    elapsed,

                    4,

                )

                result.reasoner_name = (

                    reasoner.name

                )

                #######################################################
                # Store inside Context
                #######################################################

                setattr(

                    context,

                    reasoner.output_name,

                    result,

                )

                #######################################################
                # Execution Report
                #######################################################

                execution.execution_time = (

                    result.execution_time

                )

                execution.status = (

                    result.status

                )

                execution.confidence = (

                    result.confidence

                )

                execution.warnings = list(

                    result.warnings

                )

                execution.validation_errors = list(

                    result.validation_errors

                )

                execution.metadata = dict(

                    result.metadata

                )

            except Exception as ex:

                execution.status = (

                    ExecutionStatus.FAILED

                )

                execution.validation_errors.append(

                    str(ex)

                )

                report.status = (

                    ExecutionStatus.FAILED

                )

            ###########################################################
            # Save Execution
            ###########################################################

            report.add_execution(

                execution

            )

            ###############################################################
        # Pipeline Completion
        ###############################################################

        pipeline_elapsed = (

            perf_counter()

            - pipeline_start

        )

        report.total_execution_time = round(

            pipeline_elapsed,

            4,

        )

        from datetime import datetime

        report.finished_at = datetime.utcnow().isoformat()

        ###############################################################
        # Pipeline Metadata
        ###############################################################

        report.metadata["reasoner_count"] = len(

            self.registry

        )

        report.metadata["graph_loaded"] = (

            context.graph is not None

        )

        report.metadata["pipeline_version"] = (

            "Enterprise V7"

        )

        ###############################################################
        # Context Metadata
        ###############################################################

        context.metadata["pipeline_completed"] = True

        context.metadata["pipeline_execution_time"] = (

            report.total_execution_time

        )

        context.metadata["pipeline_status"] = (

            report.status.value

        )

        ###############################################################
        # Diagnostics
        ###############################################################

        report.diagnostics[

            "successful_reasoners"

        ] = report.successful

        report.diagnostics[

            "warning_reasoners"

        ] = report.warnings

        report.diagnostics[

            "failed_reasoners"

        ] = report.failed

        report.diagnostics[

            "skipped_reasoners"

        ] = report.skipped

        ###############################################################
        # Return
        ###############################################################

        return (

            context,

            report,

        )

    ####################################################################
    # DEPENDENCY VALIDATION
    ####################################################################

    def _validate_dependencies(

        self,

        context,

        reasoner,

    ):

        """
        Validate whether a reasoner's dependencies
        are available inside the ReasoningContext.

        Every reasoner may define

            dependencies = [
                "ontology_reasoning",
                "dependency_reasoning",
            ]
        """

        dependencies = getattr(

            reasoner,

            "dependencies",

            [],

        )

        for dependency in dependencies:

            if getattr(

                context,

                dependency,

                None,

            ) is None:

                return (

                    f"Missing dependency: {dependency}"

                )

        return None

    ####################################################################
    # PIPELINE SUMMARY
    ####################################################################

    def summary(

        self,

        report,

    ):

        """
        Produce simple pipeline summary.
        """

        return {

            "status": report.status.value,

            "successful": report.successful,

            "warnings": report.warnings,

            "partial_success": report.partial_success,

            "failed": report.failed,

            "skipped": report.skipped,

            "disabled": report.disabled,

            "execution_time": report.total_execution_time,

        }

    ####################################################################
    # RESET
    ####################################################################

    def clear_registry(self):

        """
        Remove all registered reasoners.
        """

        self.registry.clear()