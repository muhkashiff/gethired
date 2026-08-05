"""
Enterprise Evidence Builder Base

Enterprise V12

All evidence builders inherit from this class.

Input

    Capability Evidence

Output

    Domain Specific Evidence
"""

from abc import ABC
from abc import abstractmethod


class EvidenceBuilderBase(ABC):

    def __init__(self):

        pass

    # -------------------------------------------------

    @abstractmethod

    def build(

        self,

        capability_evidence,

    ):

        """
        Converts capability evidence

        into domain evidence.
        """

        raise NotImplementedError