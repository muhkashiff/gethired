"""
Enterprise Base Reasoner

Enterprise V7

Purpose
-------
Provides a unified execution pipeline for every
Knowledge Graph Reasoner.

Every specialized reasoner inherits from this class.

Examples

SkillReasoner

AchievementReasoner

LeadershipReasoner

ExecutiveReasoner

CareerReasoner

InterviewReasoner

ResumeReasoner

RecommendationReasoner

GraphReasoner
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from time import perf_counter

from typing import Any


class BaseReasoner(ABC):

    ####################################################################
    # CLASS METADATA
    ####################################################################

    name = "BaseReasoner"

    output_name = None

    priority = 100

    enabled = True

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self):

        self.enabled = True

        self.output_name = None

        self.enable_validation = True

        self.enable_diagnostics = True

        self.enable_timing = True

    ####################################################################
    # PUBLIC ENTRY
    ####################################################################

    def run(

        self,

        *args,

        **kwargs,

    ) -> Any:

        """
        Standard enterprise execution pipeline.

        Every reasoner follows this lifecycle.

        validate

        preprocess

        analyze

        postprocess

        diagnostics
        """

        self._before_run()

        start = perf_counter()

        if self.enable_validation:

            self.validate(

                *args,

                **kwargs,

            )

        context = self.preprocess(

            *args,

            **kwargs,

        )

        result = self.analyze(

            context,

        )

        result = self.postprocess(

            result,

        )

        if self.enable_timing:

            elapsed = (

                perf_counter()

                - start

            )

            self._record_time(

                result,

                elapsed,

            )

        if self.enable_diagnostics:

            self._diagnostics(

                result,

            )

        self._after_run()

        return result

    ####################################################################
    # VALIDATION
    ####################################################################

    def validate(

        self,

        *args,

        **kwargs,

    ):

        """
        Override when needed.
        """

        return

    ####################################################################
    # PREPROCESS
    ####################################################################

    def preprocess(

        self,

        *args,

        **kwargs,

    ):

        """
        Default behavior.

        Child classes may override.
        """

        return {

            "args": args,

            "kwargs": kwargs,

        }

    ####################################################################
    # CORE ANALYSIS
    ####################################################################

    @abstractmethod
    def analyze(

        self,

        context,

    ):

        """
        Child class implements reasoning.
        """

        raise NotImplementedError()

    ####################################################################
    # POSTPROCESS
    ####################################################################

    def postprocess(

        self,

        result,

    ):

        """
        Override if needed.
        """

        return result

    ####################################################################
    # BEFORE / AFTER
    ####################################################################

    def _before_run(self):

        return

    def _after_run(self):

        return

    ####################################################################
    # TIMING
    ####################################################################

    def _record_time(

        self,

        result,

        elapsed,

    ):

        if hasattr(

            result,

            "metadata",

        ):

            result.metadata[

                "execution_time"

            ] = round(

                elapsed,

                6,

            )

    ####################################################################
    # DIAGNOSTICS
    ####################################################################

    def _diagnostics(

        self,

        result,

    ):

        if hasattr(

            result,

            "metadata",

        ):

            result.metadata[

                "reasoner"

            ] = self.name