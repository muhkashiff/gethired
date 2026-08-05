"""
Enterprise Base Reasoning Result

Enterprise V7

Purpose
-------
Every Reasoner returns an object that inherits from
BaseReasoningResult.

Examples

OntologyReasoningResult

DependencyReasoningResult

SkillReasoningResult

AchievementReasoningResult

LeadershipReasoningResult

ExecutiveReasoningResult

RecommendationReasoningResult

CareerReasoningResult

InterviewReasoningResult

ResumeReasoningResult
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from .execution_status import ExecutionStatus

@dataclass
class BaseReasoningResult:

    ####################################################################
    # EXECUTION
    ####################################################################

    confidence: float = 0.0

    execution_time: float = 0.0

    status: ExecutionStatus = ExecutionStatus.NOT_EXECUTED

    ####################################################################
    # PIPELINE
    ####################################################################

    reasoner_name: str = ""

    version: str = "V7"

    ####################################################################
    # QUALITY
    ####################################################################

    warnings: List[str] = field(
        default_factory=list
    )

    diagnostics: Dict = field(
        default_factory=dict
    )

    ####################################################################
    # METADATA
    ####################################################################

    metadata: Dict = field(
        default_factory=dict
    )

    ####################################################################
    # TRACEABILITY
    ####################################################################

    timestamp: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    ####################################################################
    # VALIDATION
    ####################################################################

    validation_errors: List[str] = field(
        default_factory=list
    )

    ####################################################################
    # HELPER METHODS
    ####################################################################

    def add_warning(self, message):

        self.warnings.append(message)

        if self.status == ExecutionStatus.NOT_EXECUTED:

            self.status = ExecutionStatus.WARNING

    # ---------------------------------------------------------

    def add_validation_error(self, message):

        self.validation_errors.append(message)

        self.status = ExecutionStatus.FAILED

    # ---------------------------------------------------------

    def add_diagnostic(
        self,
        key,
        value,
    ):

        self.diagnostics[key] = value

    # ---------------------------------------------------------

    def add_metadata(
        self,
        key,
        value,
    ):

        self.metadata[key] = value


    def mark_success(self):

        self.status = ExecutionStatus.SUCCESS

    def mark_partial_success(self):

        self.status = ExecutionStatus.PARTIAL_SUCCESS

    def mark_skipped(self):

        self.status = ExecutionStatus.SKIPPED

    def mark_disabled(self):

        self.status = ExecutionStatus.DISABLED

    