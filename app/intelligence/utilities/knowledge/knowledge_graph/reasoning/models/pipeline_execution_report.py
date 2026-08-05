"""
Enterprise Pipeline Execution Report

Enterprise V7

Purpose
-------
Captures execution details for the entire reasoning pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from .execution_status import ExecutionStatus


@dataclass
class ReasonerExecution:

    name: str = ""

    priority: int = 0

    output_name: str = ""

    status: ExecutionStatus = ExecutionStatus.NOT_EXECUTED

    execution_time: float = 0.0

    confidence: float = 0.0

    warnings: List[str] = field(
        default_factory=list
    )

    validation_errors: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )


@dataclass
class PipelineExecutionReport:

    ##########################################################
    # Pipeline Metadata
    ##########################################################

    pipeline_name: str = "Enterprise Knowledge Reasoning"

    version: str = "V7"

    started_at: str = field(
        default_factory=lambda:
        datetime.utcnow().isoformat()
    )

    finished_at: str = ""

    total_execution_time: float = 0.0

    ##########################################################
    # Overall Status
    ##########################################################

    status: ExecutionStatus = ExecutionStatus.NOT_EXECUTED

    ##########################################################
    # Individual Reasoners
    ##########################################################

    executions: List[ReasonerExecution] = field(
        default_factory=list
    )

    ##########################################################
    # Summary
    ##########################################################

    successful: int = 0

    warnings: int = 0

    partial_success: int = 0

    failed: int = 0

    skipped: int = 0

    disabled: int = 0

    ##########################################################
    # Diagnostics
    ##########################################################

    metadata: Dict = field(
        default_factory=dict
    )

    diagnostics: Dict = field(
        default_factory=dict
    )

    ##########################################################
    # Helper
    ##########################################################

    def add_execution(
        self,
        execution: ReasonerExecution,
    ):

        self.executions.append(execution)

        if execution.status == ExecutionStatus.SUCCESS:
            self.successful += 1

        elif execution.status == ExecutionStatus.WARNING:
            self.warnings += 1

        elif execution.status == ExecutionStatus.PARTIAL_SUCCESS:
            self.partial_success += 1

        elif execution.status == ExecutionStatus.FAILED:
            self.failed += 1

        elif execution.status == ExecutionStatus.SKIPPED:
            self.skipped += 1

        elif execution.status == ExecutionStatus.DISABLED:
            self.disabled += 1