# Resume Knowledge Traversal — Enterprise V5


"""
Enterprise V5
Resume Knowledge Traversal

Responsibility
--------------
Connect the completed ResumeBuilder output to the existing
Enterprise V5 ontology extraction pipeline.

Architecture:

    Resume
        |
        v
    ResumeKnowledgeTraversal
        |
        v
    Resume text units
        |
        v
    ExtractionCoordinator
        |
        v
    KnowledgeV5Pipeline
        |
        +--> Tokenizer
        +--> Matcher
        +--> Confidence
        +--> OverlapResolver
        +--> Ranker
        |
        v
    ExtractionResult
        |
        v
    KnowledgeEntity
        |
        v
    KnowledgeFact

IMPORTANT
---------
This class does NOT create a new extractor.

It does NOT perform:
    - tokenization
    - ontology matching
    - confidence calculation
    - overlap resolution
    - ranking
    - reasoning
    - knowledge graph construction
    - JD matching
    - ATS scoring

Those responsibilities already belong to existing Enterprise V5
components.

The traversal layer only connects the Resume object to them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional, Tuple

from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
    ExtractionCoordinator,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)


# =====================================================================
# TRAVERSAL RESULT
# =====================================================================

@dataclass
class ResumeKnowledgeTraversalResult:
    """
    Object returned by ResumeKnowledgeTraversal.

    This object represents the result of traversing the already-built
    Resume object through the existing ontology extraction layer.

    The object intentionally preserves the original Resume object.

    Nothing downstream needs to reconstruct the Resume.
    """

    resume: Any = None

    facts: List[KnowledgeFact] = field(
        default_factory=list
    )

    entities: List[KnowledgeEntity] = field(
        default_factory=list
    )

    sentences: List[str] = field(
        default_factory=list
    )

    processed_sentences: int = 0

    matched_sentences: int = 0

    entity_count: int = 0

    confidence: float = 0.0

    success: bool = False

    errors: List[str] = field(
        default_factory=list
    )

    # ---------------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------------

    @property
    def fact_count(self) -> int:
        return len(self.facts)

    @property
    def has_entities(self) -> bool:
        return bool(self.entities)


# =====================================================================
# RESUME KNOWLEDGE TRAVERSAL
# =====================================================================

class ResumeKnowledgeTraversal:
    """
    Connects ResumeBuilder output to Enterprise V5 knowledge extraction.

    Input:

        Resume

    Output:

        ResumeKnowledgeTraversalResult

    The traversal does not implement ontology extraction itself.

    Instead:

        Resume
            ↓
        text units
            ↓
        ExtractionCoordinator
            ↓
        KnowledgeV5Pipeline
            ↓
        ExtractedEntity
            ↓
        KnowledgeEntity
            ↓
        KnowledgeFact
    """

    # =================================================================
    # INITIALIZATION
    # =================================================================

    def __init__(
        self,
        knowledge_pipeline: Optional[
            KnowledgeV5Pipeline
        ] = None,
        coordinator: Optional[
            ExtractionCoordinator
        ] = None,
    ) -> None:

        # -------------------------------------------------------------
        # IMPORTANT
        #
        # We explicitly construct/use KnowledgeV5Pipeline here.
        #
        # ExtractionCoordinator is still responsible for running the
        # pipeline against all configured ontology collections.
        # -------------------------------------------------------------

        self.knowledge_pipeline = (
            knowledge_pipeline
            or KnowledgeV5Pipeline()
        )

        # -------------------------------------------------------------
        # Inject the SAME KnowledgeV5Pipeline into the coordinator.
        #
        # Therefore there is no second matching implementation.
        # -------------------------------------------------------------

        self.coordinator = (
            coordinator
            or ExtractionCoordinator(
                knowledge_pipeline=
                    self.knowledge_pipeline
            )
        )

    # =================================================================
    # PUBLIC API
    # =================================================================

    def run(
        self,
        resume: Any,
    ) -> ResumeKnowledgeTraversalResult:
        """
        Traverse a completed Resume object.

        Parameters
        ----------
        resume:
            Resume object produced by ResumeBuilder.

        Returns
        -------
        ResumeKnowledgeTraversalResult
        """

        result = ResumeKnowledgeTraversalResult(
            resume=resume
        )

        # -------------------------------------------------------------
        # Validate input
        # -------------------------------------------------------------

        if resume is None:

            result.errors.append(
                "Resume object is None."
            )

            return result

        # -------------------------------------------------------------
        # Extract textual units from Resume
        # -------------------------------------------------------------

        units = list(
            self._traverse_resume(
                resume
            )
        )

        # -------------------------------------------------------------
        # Preserve unique textual units
        # -------------------------------------------------------------

        seen = set()

        for unit in units:

            text = self._clean_text(
                unit[0]
            )

            if not text:
                continue

            normalized = text.casefold()

            if normalized in seen:
                continue

            seen.add(
                normalized
            )

            result.sentences.append(
                text
            )

        # -------------------------------------------------------------
        # Process each text unit through existing extraction layer
        # -------------------------------------------------------------

        for sentence in result.sentences:

            result.processed_sentences += 1

            try:

                fact = self._process_sentence(
                    sentence
                )

                result.facts.append(
                    fact
                )

                entities = (
                    fact.interpretation.entities
                )

                if entities:

                    result.matched_sentences += 1

                    result.entities.extend(
                        entities
                    )

            except Exception as exc:

                result.errors.append(
                    (
                        "Failed processing "
                        f"sentence={sentence!r}: "
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    )
                )

        # -------------------------------------------------------------
        # Deduplicate entities
        # -------------------------------------------------------------

        result.entities = (
            self._deduplicate_entities(
                result.entities
            )
        )

        result.entity_count = len(
            result.entities
        )

        # -------------------------------------------------------------
        # Calculate overall confidence
        # -------------------------------------------------------------

        result.confidence = self._calculate_confidence(
            result.entities
        )

        # -------------------------------------------------------------
        # Success
        #
        # Successful traversal does NOT require ontology matches.
        #
        # A Resume can legitimately contain no ontology entities.
        # -------------------------------------------------------------

        result.success = (
            result.processed_sentences > 0
            and not result.errors
        )

        return result

    # =================================================================
    # PROCESS ONE SENTENCE
    # =================================================================

    def process_sentence(
        self,
        sentence: str,
    ) -> KnowledgeFact:
        """
        Process one textual Resume unit.

        This is useful for testing individual Resume sentences.
        """

        sentence = self._clean_text(
            sentence
        )

        if not sentence:

            interpretation = (
                KnowledgeInterpretation()
            )

            interpretation.entities = []

            interpretation.confidence = 0.0

            return KnowledgeFact(
                text="",
                interpretation=interpretation,
                source="resume",
                confidence=0.0,
            )

        return self._process_sentence(
            sentence
        )

    # =================================================================
    # INTERNAL SENTENCE PROCESSING
    # =================================================================

    def _process_sentence(
        self,
        sentence: str,
    ) -> KnowledgeFact:
        """
        Run one Resume sentence through the existing
        ExtractionCoordinator.

        The coordinator internally invokes:

            KnowledgeV5Pipeline
                ↓
            Tokenizer
            Matcher
            Confidence
            OverlapResolver
            Ranker
        """

        extraction = (
            self.coordinator.run(
                sentence
            )
        )

        interpretation = (
            KnowledgeInterpretation()
        )

        entities = []

        # -------------------------------------------------------------
        # Convert ExtractedEntity -> KnowledgeEntity
        # -------------------------------------------------------------

        for extracted in (
            extraction.all_entities
        ):

            entity = (
                self._convert_entity(
                    extracted
                )
            )

            entities.append(
                entity
            )

        interpretation.entities = (
            entities
        )

        interpretation.confidence = (
            max(
                (
                    entity.confidence
                    for entity in entities
                ),
                default=0.0,
            )
        )

        # -------------------------------------------------------------
        # Build KnowledgeFact
        # -------------------------------------------------------------

        return KnowledgeFact(

            text=sentence,

            interpretation=
                interpretation,

            source="resume",

            confidence=
                interpretation.confidence,

        )

    # =================================================================
    # EXTRACTED ENTITY -> KNOWLEDGE ENTITY
    # =================================================================

    @staticmethod
    def _convert_entity(
        extracted: Any,
    ) -> KnowledgeEntity:
        """
        Convert the existing ExtractedEntity produced by
        ExtractionCoordinator into the common KnowledgeEntity model.

        No ontology logic is performed here.
        """

        entity = KnowledgeEntity(

            # ---------------------------------------------------------
            # Detection
            # ---------------------------------------------------------

            found=True,

            confidence=float(
                getattr(
                    extracted,
                    "confidence",
                    0.0,
                )
                or 0.0
            ),

            # ---------------------------------------------------------
            # Linguistic
            # ---------------------------------------------------------

            original=str(
                getattr(
                    extracted,
                    "phrase",
                    "",
                )
                or ""
            ),

            canonical=str(
                getattr(
                    extracted,
                    "canonical",
                    "",
                )
                or ""
            ),

            normalized=str(
                getattr(
                    extracted,
                    "canonical",
                    "",
                )
                or ""
            ).casefold(),

            # ---------------------------------------------------------
            # Classification
            # ---------------------------------------------------------

            category=str(
                getattr(
                    extracted,
                    "category",
                    "",
                )
                or ""
            ),

            entity_id=str(
                getattr(
                    extracted,
                    "entity_id",
                    "",
                )
                or ""
            ),

            entity_type=str(
                getattr(
                    extracted,
                    "entity_type",
                    "",
                )
                or ""
            ),

            ontology_name=str(
                getattr(
                    extracted,
                    "ontology",
                    "",
                )
                or ""
            ),

            business_area=str(
                getattr(
                    extracted,
                    "business_area",
                    "",
                )
                or ""
            ),

            domain=str(
                getattr(
                    extracted,
                    "domain",
                    "",
                )
                or ""
            ),

            # ---------------------------------------------------------
            # Repository / semantic information
            # ---------------------------------------------------------

            impact_weight=float(
                getattr(
                    extracted,
                    "impact_weight",
                    1.0,
                )
                or 1.0
            ),

            # ---------------------------------------------------------
            # Match
            # ---------------------------------------------------------

            matched_phrase=str(
                getattr(
                    extracted,
                    "phrase",
                    "",
                )
                or ""
            ),

            matched_alias=bool(
                getattr(
                    extracted,
                    "is_alias",
                    False,
                )
            ),

            # ---------------------------------------------------------
            # Position
            # ---------------------------------------------------------

            start_char=int(
                getattr(
                    extracted,
                    "start_char",
                    -1,
                )
                or -1
            ),

            end_char=int(
                getattr(
                    extracted,
                    "end_char",
                    -1,
                )
                or -1
            ),

            token_index=int(
                getattr(
                    extracted,
                    "token_index",
                    -1,
                )
                or -1
            ),

            token_count=int(
                getattr(
                    extracted,
                    "token_count",
                    0,
                )
                or 0
            ),

            sentence_index=int(
                getattr(
                    extracted,
                    "sentence_index",
                    0,
                )
                or 0
            ),

            # ---------------------------------------------------------
            # Repository
            # ---------------------------------------------------------

            source="resume",

            metadata=dict(
                getattr(
                    extracted,
                    "metadata",
                    {},
                )
                or {}
            ),

        )

        return entity

    # =================================================================
    # RESUME TRAVERSAL
    # =================================================================

    def _traverse_resume(
        self,
        resume: Any,
    ) -> Iterable[
        Tuple[str, str]
    ]:
        """
        Traverse the already-built Resume object.

        Returns:

            (text, source_path)

        The source path is retained so future KnowledgeFact
        enrichment can trace an entity back to its Resume location.

        Example:

            (
                "Led site-wide HACCP governance...",
                "experience[0].responsibilities[6]"
            )
        """

        # =============================================================
        # SUMMARY
        # =============================================================

        summary = getattr(
            resume,
            "summary",
            "",
        )

        if summary:

            yield (
                str(summary),
                "summary",
            )

        # =============================================================
        # EXPERIENCE
        # =============================================================

        experiences = getattr(
            resume,
            "experience",
            [],
        )

        if isinstance(
            experiences,
            (list, tuple),
        ):

            for exp_index, experience in enumerate(
                experiences
            ):

                # -----------------------------------------------------
                # Job title
                # -----------------------------------------------------

                title = getattr(
                    experience,
                    "title",
                    "",
                )

                if title:

                    yield (
                        str(title),
                        (
                            f"experience[{exp_index}]"
                            ".title"
                        ),
                    )

                # -----------------------------------------------------
                # Company
                # -----------------------------------------------------

                company = getattr(
                    experience,
                    "company",
                    "",
                )

                if company:

                    yield (
                        str(company),
                        (
                            f"experience[{exp_index}]"
                            ".company"
                        ),
                    )

                # -----------------------------------------------------
                # Location
                # -----------------------------------------------------

                location = getattr(
                    experience,
                    "location",
                    "",
                )

                if location:

                    yield (
                        str(location),
                        (
                            f"experience[{exp_index}]"
                            ".location"
                        ),
                    )

                # -----------------------------------------------------
                # Responsibilities
                # -----------------------------------------------------

                responsibilities = getattr(
                    experience,
                    "responsibilities",
                    [],
                )

                if isinstance(
                    responsibilities,
                    (list, tuple),
                ):

                    for line_index, line in enumerate(
                        responsibilities
                    ):

                        if line:

                            yield (
                                str(line),
                                (
                                    f"experience[{exp_index}]"
                                    f".responsibilities[{line_index}]"
                                ),
                            )

                # -----------------------------------------------------
                # Achievements
                # -----------------------------------------------------

                achievements = getattr(
                    experience,
                    "achievements",
                    [],
                )

                if isinstance(
                    achievements,
                    (list, tuple),
                ):

                    for line_index, line in enumerate(
                        achievements
                    ):

                        if line:

                            yield (
                                str(line),
                                (
                                    f"experience[{exp_index}]"
                                    f".achievements[{line_index}]"
                                ),
                            )

                # -----------------------------------------------------
                # Existing extracted skills
                # -----------------------------------------------------

                skills = getattr(
                    experience,
                    "skills",
                    [],
                )

                if isinstance(
                    skills,
                    (list, tuple),
                ):

                    for line_index, skill in enumerate(
                        skills
                    ):

                        if skill:

                            yield (
                                str(skill),
                                (
                                    f"experience[{exp_index}]"
                                    f".skills[{line_index}]"
                                ),
                            )

                # -----------------------------------------------------
                # Existing technologies
                # -----------------------------------------------------

                technologies = getattr(
                    experience,
                    "technologies",
                    [],
                )

                if isinstance(
                    technologies,
                    (list, tuple),
                ):

                    for line_index, technology in enumerate(
                        technologies
                    ):

                        if technology:

                            yield (
                                str(technology),
                                (
                                    f"experience[{exp_index}]"
                                    f".technologies[{line_index}]"
                                ),
                            )

        # =============================================================
        # EDUCATION
        # =============================================================

        education = getattr(
            resume,
            "education",
            [],
        )

        if isinstance(
            education,
            (list, tuple),
        ):

            for edu_index, item in enumerate(
                education
            ):

                degree = getattr(
                    item,
                    "degree",
                    "",
                )

                if degree:

                    yield (
                        str(degree),
                        (
                            f"education[{edu_index}]"
                            ".degree"
                        ),
                    )

                major = getattr(
                    item,
                    "major",
                    "",
                )

                if major:

                    yield (
                        str(major),
                        (
                            f"education[{edu_index}]"
                            ".major"
                        ),
                    )

                institution = getattr(
                    item,
                    "institution",
                    "",
                )

                if institution:

                    yield (
                        str(institution),
                        (
                            f"education[{edu_index}]"
                            ".institution"
                        ),
                    )

                description = getattr(
                    item,
                    "description",
                    "",
                )

                if description:

                    yield (
                        str(description),
                        (
                            f"education[{edu_index}]"
                            ".description"
                        ),
                    )

        # =============================================================
        # CERTIFICATIONS
        # =============================================================

        certifications = getattr(
            resume,
            "certifications",
            [],
        )

        if isinstance(
            certifications,
            (list, tuple),
        ):

            for cert_index, certification in enumerate(
                certifications
            ):

                # Certification can be an object or plain string.
                if isinstance(
                    certification,
                    str,
                ):

                    yield (
                        certification,
                        (
                            f"certifications[{cert_index}]"
                        ),
                    )

                    continue

                name = getattr(
                    certification,
                    "name",
                    "",
                )

                if name:

                    yield (
                        str(name),
                        (
                            f"certifications[{cert_index}]"
                            ".name"
                        ),
                    )

                description = getattr(
                    certification,
                    "description",
                    "",
                )

                if description:

                    yield (
                        str(description),
                        (
                            f"certifications[{cert_index}]"
                            ".description"
                        ),
                    )

        # =============================================================
        # SKILLS
        # =============================================================

        skills = getattr(
            resume,
            "skills",
            [],
        )

        if isinstance(
            skills,
            (list, tuple),
        ):

            for index, skill in enumerate(
                skills
            ):

                if skill:

                    yield (
                        str(skill),
                        f"skills[{index}]",
                    )

        # =============================================================
        # PROJECTS
        # =============================================================

        projects = getattr(
            resume,
            "projects",
            [],
        )

        if isinstance(
            projects,
            (list, tuple),
        ):

            for project_index, project in enumerate(
                projects
            ):

                if isinstance(
                    project,
                    str,
                ):

                    yield (
                        project,
                        f"projects[{project_index}]",
                    )

                    continue

                name = getattr(
                    project,
                    "name",
                    "",
                )

                if name:

                    yield (
                        str(name),
                        (
                            f"projects[{project_index}]"
                            ".name"
                        ),
                    )

                description = getattr(
                    project,
                    "description",
                    "",
                )

                if description:

                    yield (
                        str(description),
                        (
                            f"projects[{project_index}]"
                            ".description"
                        ),
                    )

        # =============================================================
        # LANGUAGES
        # =============================================================

        languages = getattr(
            resume,
            "languages",
            [],
        )

        if isinstance(
            languages,
            (list, tuple),
        ):

            for index, language in enumerate(
                languages
            ):

                if isinstance(
                    language,
                    str,
                ):

                    yield (
                        language,
                        f"languages[{index}]",
                    )

                    continue

                name = language.get(
                    "language",
                    "",
                ) if isinstance(
                    language,
                    dict,
                ) else getattr(
                    language,
                    "language",
                    "",
                )

                proficiency = language.get(
                    "proficiency",
                    "",
                ) if isinstance(
                    language,
                    dict,
                ) else getattr(
                    language,
                    "proficiency",
                    "",
                )

                text = " ".join(
                    value
                    for value in (
                        str(name).strip()
                        if name else "",
                        str(proficiency).strip()
                        if proficiency else "",
                    )
                    if value
                )

                if text:

                    yield (
                        text,
                        f"languages[{index}]",
                    )

    # =================================================================
    # CLEAN TEXT
    # =================================================================

    @staticmethod
    def _clean_text(
        value: Any,
    ) -> str:
        """
        Normalize a Resume text unit without changing its meaning.
        """

        if value is None:

            return ""

        text = str(
            value
        )

        # -------------------------------------------------------------
        # Normalize whitespace
        # -------------------------------------------------------------

        text = text.replace(
            "\r",
            " ",
        )

        text = text.replace(
            "\n",
            " ",
        )

        text = "\t".join(
            part
            for part in text.split("\t")
            if part
        )

        text = " ".join(
            text.split()
        )

        return text.strip()

    # =================================================================
    # DEDUPLICATION
    # =================================================================

    @staticmethod
    def _deduplicate_entities(
        entities: List[KnowledgeEntity],
    ) -> List[KnowledgeEntity]:
        """
        Deduplicate extracted KnowledgeEntity objects.

        Entity identity is based primarily on entity_id.

        If the same entity appears multiple times, retain the
        strongest-confidence occurrence.
        """

        entity_map = {}

        for entity in entities:

            entity_id = (
                entity.entity_id
                or entity.normalized
                or entity.canonical
            )

            if not entity_id:
                continue

            existing = entity_map.get(
                entity_id
            )

            if existing is None:

                entity_map[
                    entity_id
                ] = entity

                continue

            if (
                entity.confidence
                >
                existing.confidence
            ):

                entity_map[
                    entity_id
                ] = entity

        return sorted(
            entity_map.values(),
            key=lambda item: (
                -item.confidence,
                item.entity_id,
            ),
        )

    # =================================================================
    # CONFIDENCE
    # =================================================================

    @staticmethod
    def _calculate_confidence(
        entities: List[KnowledgeEntity],
    ) -> float:
        """
        Calculate aggregate confidence from the strongest
        extracted entities.

        This is an integration-level confidence only.

        It does NOT replace KnowledgeV5Pipeline confidence.
        """

        if not entities:

            return 0.0

        values = [
            max(
                0.0,
                min(
                    1.0,
                    float(
                        entity.confidence
                    ),
                ),
            )
            for entity in entities
        ]

        return sum(values) / len(
            values
        )

    # =================================================================
    # DEBUG / TRACE
    # =================================================================

    def trace(
        self,
        resume: Any,
    ) -> dict:
        """
        Return a lightweight traversal trace.

        Useful for Enterprise V5 pipeline tests.
        """

        units = list(
            self._traverse_resume(
                resume
            )
        )

        return {

            "resume_type":
                type(resume).__name__,

            "text_units":
                len(units),

            "units": [

                {
                    "text": text,
                    "source": source,
                }

                for text, source in units
            ],
        }

