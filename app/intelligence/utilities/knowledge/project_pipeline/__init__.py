"""
Project Pipeline Package
========================

Public orchestration boundary for the application pipeline.

Exports
-------
ProjectPipeline
    Main project orchestration pipeline.

ProjectPipelineResult
    Complete result object containing every pipeline checkpoint.

project_pipeline
    Convenience function for processing one document.
"""

from .project_pipeline import (
    ProjectPipeline,
    project_pipeline,
)

from .project_pipeline_result import (
    ProjectPipelineResult,
)
from app.intelligence.utilities.knowledge.matching.match_enricher import (
    KnowledgeMatchEnricher,
)


__all__ = [
    "ProjectPipeline",
    "ProjectPipelineResult",
    "project_pipeline",
    "KnowledgeMatchEnricher",
]