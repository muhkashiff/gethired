"""
Enterprise Execution Status

Enterprise V7

Standard execution state used across every
Reasoner and Pipeline.
"""

from enum import Enum


class ExecutionStatus(str, Enum):

    SUCCESS = "SUCCESS"

    WARNING = "WARNING"

    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

    FAILED = "FAILED"

    SKIPPED = "SKIPPED"

    DISABLED = "DISABLED"

    NOT_EXECUTED = "NOT_EXECUTED"