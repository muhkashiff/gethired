"""
Document Types
==============

Defines the supported document types for the Resume Customizer
knowledge architecture.

This module contains only domain-level document type definitions.
"""

from enum import Enum


class DocumentType(str, Enum):
    """
    Supported document types entering the Enterprise Knowledge Pipeline.
    """

    RESUME = "resume"
    JD = "jd"

    @classmethod
    def from_string(cls, value: str) -> "DocumentType":
        """
        Convert a string into a DocumentType.

        Parameters
        ----------
        value:
            Document type string.

        Returns
        -------
        DocumentType

        Raises
        ------
        ValueError
            If the supplied value is not supported.
        """

        if not isinstance(value, str):
            raise TypeError(
                "document_type must be a string."
            )

        normalized = value.strip().casefold()

        aliases = {
            "resume": cls.RESUME,
            "cv": cls.RESUME,
            "curriculum vitae": cls.RESUME,
            "jd": cls.JD,
            "job description": cls.JD,
            "job_description": cls.JD,
            "jobdescription": cls.JD,
        }

        document_type = aliases.get(normalized)

        if document_type is None:
            raise ValueError(
                f"Unsupported document type: {value!r}. "
                f"Supported types are: resume, jd."
            )

        return document_type